import time
import requests
import sys
try:
    # For Python 3.0 and later
    import urllib.parse as urlparse
except ImportError:
    # Fall back to Python 2's urlparse
    import urlparse

CLIENT_ID = "enterpriseapi-sb-0iSeXHHzheNu1AzI7DJbzea7"
CLIENT_SECRET = "0be2610f200b69fdd1699084822cae2a96183d45"
REDIRECT_URL = "http://localhost:8000/giftr/login_only"
cardNumber = 8729
rewardsAccountReferenceId = None


global auth_token
global prev_time
global rewards


def getCodeFromUrl(url):
	parsed = urlparse.parse_qs(urlparse.urlparse(url).query)
	print(parsed)
	if 'code' in parsed:
		return parsed['code'][0]
	return None

def getAccessToken(code):
	global auth_token
	global prev_time



	headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
	}

	data = 'code='+code+'&client_id='+CLIENT_ID+'&client_secret='+CLIENT_SECRET+'&grant_type=authorization_code&redirect_uri='+REDIRECT_URL

	response = requests.post('https://api-sandbox.capitalone.com/oauth/oauth20/token', headers=headers, data=data)
	print(response.ok)
	print(response.text)
	auth_token = response.json()
	prev_time = time.time()			
	return response.json()


def refreshAccessToken():
	global auth_token
	global prev_time
	refresh_token = auth_token['refresh_token']

	headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
	}

	data = 'client_id='+CLIENT_ID+'&client_secret='+CLIENT_SECRET+'&grant_type=refresh_token&refresh_token='+refresh_token

	response = requests.post('https://api-sandbox.capitalone.com/oauth/oauth20/token', headers=headers, data=data)
	auth_token = response.json()	
	prev_time = time.time()


	return response.json()


def refresh():
	if time.time() + 10 > prev_time + auth_token['expires_in']:
		refreshAccessToken()



def getRewardsAccounts():
	global rewardsAccountReferenceId

	refresh()
	headers = {
    'Accept': 'application/json;v=1',
    'Authorization': 'Bearer '+ auth_token['access_token']
	}

	url = 'https://api-sandbox.capitalone.com/rewards/accounts?creditCardLastFour='+str(cardNumber)

	response = requests.get(url, headers=headers)

	if response.ok and "rewardsAccounts" in response.json():
		rewardsAccountReferenceId = urlparse.quote_plus(response.json()['rewardsAccounts'][0]['rewardsAccountReferenceId'])



def getRewardsAccountsDetails():
	getRewardsAccounts()
	print(rewardsAccountReferenceId)

	headers = {
    'Accept': 'application/json;v=1',
    'Authorization': 'Bearer '+ auth_token['access_token']
	}

	response = requests.get('https://api-sandbox.capitalone.com/rewards/accounts/'+rewardsAccountReferenceId, headers=headers)
	print(response.ok)
	print(response.json())
	return response.json()

def authenticate(url):
# # 	#go to authenticate website
	# grab url
	#url = ""
	getAccessToken(url)

	while True:
		#check if token needs to be refreshed 
		
		if (time.time() + 10) > (prev_time + auth_token['expires_in']):
			print ("refreshing token")
			refreshAccessToken()


def redeemMoney():
	rewardsDetails = getRewardsAccountsDetails()
	if rewardsDetails['canRedeem'] and rewardsDetails['rewardsCurrency'] == "Cash":
		#super lazy for now
		print("You can save up to " + str(rewardsDetails['rewardsBalance']))
		return rewardsDetails['rewardsBalance']



# # paste your url here: e.g. https://www.google.com/?code=idFKpQH1T8RcHVOzFbo-qOlVaDi67_IWd0FpGg
# url = "https://www.google.com/?code=sfZ_TYEVGTkBoxHf0S0IuVbhWc5MbzYIbz0Vmw"
# getAccessToken(url)
# print(auth_token)
# while True:
# 	refresh()


# paste your url here: e.g. https://www.google.com/?code=idFKpQH1T8RcHVOzFbo-qOlVaDi67_IWd0FpGg
# url = "https://www.google.com/?code=KZVwGfrUFTGv0B2DUyaO3wF9b43WvWe3aT4A4A"
# getAccessToken(url)
# getRewardsAccounts()
# getRewardsAccountsDetails()


def main():
	url = sys.argv[1]
	code = getCodeFromUrl(url)
	if code is not None:
		getAccessToken(code)
		return redeemMoney()
	return 0


url = sys.argv[1]
code = getCodeFromUrl(url)
if code is not None:
	getAccessToken(code)
	rewards = redeemMoney()
rewards = 0









