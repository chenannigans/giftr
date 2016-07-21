import time
import requests
import sys
import urlparse
import urllib

CLIENT_ID = "enterpriseapi-sb-0iSeXHHzheNu1AzI7DJbzea7"
CLIENT_SECRET = "0be2610f200b69fdd1699084822cae2a96183d45"
REDIRECT_URL = "http://localhost:8000/giftr/cap-one-connect"

cards = []
rewardsAccounts = []
auth_info = None
prev_time = None
selected_account = None


def get_code_from_url(url):
    print("getting code from url")
    parsed = urlparse.parse_qs(urlparse.urlparse(url).query)
    if 'code' in parsed:
        return parsed['code'][0]
    return None


def get_access_token(code):
    print("getting access code")
    global auth_info
    global prev_time

    if code is None:
        return None

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = 'code=' + code + '&client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + \
           '&grant_type=authorization_code&redirect_uri=' + REDIRECT_URL

    response = requests.post('https://api-sandbox.capitalone.com/oauth/oauth20/token', headers=headers, data=data)
    print("reached")
    print("retrieved access token: " + str(response.ok))
    if not response.ok:
        return None

    print(response.ok)
    print(response.text)
    auth_info = response.json()
    prev_time = time.time()
    return response.json()


def refresh_access_token():
    global auth_info
    global prev_time
    refresh_token = auth_info['refresh_token']

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = 'client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + \
           '&grant_type=refresh_token&refresh_token=' + refresh_token

    response = requests.post('https://api-sandbox.capitalone.com/oauth/oauth20/token', headers=headers, data=data)

    auth_token = response.json()
    prev_time = time.time()

    return response.json()


def refresh():
    if time.time() + 10 > prev_time + auth_info['expires_in']:
        refresh_access_token()


def get_rewards_accounts():
    global rewardsAccounts
    global cards
    global cashIndex

    if auth_info is None:
        return []

    headers = {
        'Accept': 'application/json;v=1',
        'Authorization': 'Bearer ' + auth_info['access_token']
    }

    url = 'https://api-sandbox.capitalone.com/rewards/accounts'

    response = requests.get(url, headers=headers)

    print("retrieved accounts: " + str(response.ok))
    
    if response.ok and "rewardsAccounts" in response.json():
        rewardsAccounts = response.json()['rewardsAccounts']
        for i in range(0, len(rewardsAccounts)):
            account = rewardsAccounts[i]
            rewardsAccounts[i]['rewardsAccountReferenceId'] = urllib.quote_plus(account['rewardsAccountReferenceId'])
            # if type = cash, save index
            if account["rewardsCurrency"] == "Cash":
                cashIndex = i
            cards.append(account["rewardsAccountReferenceId"])
    return rewardsAccounts

def get_account_details(referenceID):
    headers = {
        'Accept': 'application/json;v=1',
        'Authorization': 'Bearer ' + auth_info['access_token']
    }

    response = requests.get('https://api-sandbox.capitalone.com/rewards/accounts/' + referenceID,
                            headers=headers)
    print("Got account details: " + str(response.ok))
    print(response.json())
    return response.json()


def authenticate(url):
    # # 	#go to authenticate website
    # grab url
    # url = ""
    get_access_token(url)

    while True:
        # check if token needs to be refreshed

        if (time.time() + 10) > (prev_time + auth_info['expires_in']):
            print ("refreshing token")
            refresh_access_token()


def redeem_money():
    rewardsDetails = get_account_details()
    if rewardsDetails['canRedeem'] and rewardsDetails['rewardsCurrency'] == "Cash":
        # super lazy for now
        print("You can save up to " + str(rewardsDetails['rewardsBalance']))
        return int(rewardsDetails['rewardsBalance'].replace(",", ""))
    return 0


def get_cards(code):
    if code is not None:
        get_access_token(code)
        get_rewards_accounts()
        return cards
    return None


def get_card_information(i):
    global selected_account
    selected_account = i
    card = {}

    assert i < len(rewardsAccounts)

    account = get_account_details(rewardsAccounts[i]['rewardsAccountReferenceId'])

    card["name"] = account["accountDisplayName"]
    customer = account["primaryAccountHolder"]
    card["customer"] = customer["firstName"] + " " + customer["lastName"]
    card["rewards_balance"] = 0

    if account["canRedeem"] and account["rewardsCurrency"] == "Cash":
        card["rewards_balance"] = account["rewardsBalance"]

    return card

def get_cash_balance(code):
    global cashIndex
    cards = get_cards(code)
    print ("GET_CASH_BALANCE CASHINDEX: "), cashIndex
    card = get_card_information(cashIndex)
    print(card["rewards_balance"])
    return card["rewards_balance"]

def main():
    get_cards(sys.argv[1])
    print(cards)
    print(get_card_information(int(sys.argv[2])))


