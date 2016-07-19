import time
import requests
import sys
import urlparse
import urllib

CLIENT_ID = "enterpriseapi-sb-0iSeXHHzheNu1AzI7DJbzea7"
CLIENT_SECRET = "0be2610f200b69fdd1699084822cae2a96183d45"
REDIRECT_URL = "http://localhost:8000/giftr/login_only"

#cardNumbers = []
#cardNumber = 8729
#rewardsAccountReferenceId = None
#accountRefIds = []

cards = []
rewardsAccounts = []
#auth_token
#prev_time
#selected_account



def get_access_token(code):
    global auth_token
    global prev_time

    if auth_token is None:
        return None

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = 'code=' + code + '&client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + \
           '&grant_type=authorization_code&redirect_uri=' + REDIRECT_URL

    response = requests.post('https://api-sandbox.capitalone.com/oauth/oauth20/token', headers=headers, data=data)

    if not response.ok:
        return None

    print(response.ok)
    print(response.text)
    auth_token = response.json()
    prev_time = time.time()
    return response.json()


def refresh_access_token():
    global auth_token
    global prev_time
    refresh_token = auth_token['refresh_token']

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
    if time.time() + 10 > prev_time + auth_token['expires_in']:
        refresh_access_token()


def get_rewards_accounts():
    global rewardsAccounts
    global cards

    headers = {
        'Accept': 'application/json;v=1',
        'Authorization': 'Bearer ' + auth_token['access_token']
    }

    url = 'https://api-sandbox.capitalone.com/rewards/accounts?creditCardLastFour=' + str(cardNumber)

    response = requests.get(url, headers=headers)

    if response.ok and "rewardsAccounts" in response.json():
        rewardsAccounts = response.json()['rewardsAccounts']
        for i in rewardsAccounts:
            account = rewardsAccounts[i]
            rewardsAccounts[i]['rewardsAccountReferenceId'] = urllib.quote_plus(account['rewardsAccountReferenceId'])
            cards[i] = account["accountDisplayName"]
    return rewardsAccounts


def get_account_details(referenceID):
    headers = {
        'Accept': 'application/json;v=1',
        'Authorization': 'Bearer ' + auth_token['access_token']
    }

    response = requests.get('https://api-sandbox.capitalone.com/rewards/accounts/' + referenceID,
                            headers=headers)
    print(response.ok)
    print(response.json())
    return response.json()


def authenticate(url):
    # # 	#go to authenticate website
    # grab url
    # url = ""
    get_access_token(url)

    while True:
        # check if token needs to be refreshed

        if (time.time() + 10) > (prev_time + auth_token['expires_in']):
            print ("refreshing token")
            refresh_access_token()


def redeem_money():
    rewardsDetails = get_account_details()
    if rewardsDetails['canRedeem'] and rewardsDetails['rewardsCurrency'] == "Cash":
        # super lazy for now
        print("You can save up to " + str(rewardsDetails['rewardsBalance']))
        return int(rewardsDetails['rewardsBalance'].replace(",", ""))
    return 0


def get_cards(auth_code):
    if auth_code is not None:
        get_access_token(auth_code)
        get_rewards_accounts()
        return cards
    return None


def get_card_information(i):
    global selected_account
    selected_account = i
    card = {}

    account = get_account_details(rewardsAccounts[i]['rewardsAccountReferenceId'])

    card["name"] = account["accountDisplayName"]
    customer = account["primaryAccountHolder"]
    card["customer"] = customer["firstName"] + " " + customer["lastName"]
    card["rewards_balance"] = 0

    if account["canRedeem"] and account["rewardsCurrency"] == "Cash":
        card["rewards_balance"] = int(account["rewardsBalance"].replace(",", ""))

    return card
