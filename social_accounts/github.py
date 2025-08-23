import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed



class Github:
    @staticmethod
    def exchange_code_for_token(code):  #User gets code from GitHub Auth Syst and gives our app. Our app exchanges the code with GitHub for an access token 
        param_payload={
            "client_id":settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code":code
        }
        res = requests.post("https://github.com/login/oauth/access_token", params=param_payload, headers={'Accept':'application/json'})
        payload=res.json()
        token=payload.get("access_token")
        return token

    @staticmethod
    def retrieve_github_user(access_token): # The access token allows you to make requests to the API on behalf of a user.
        try:
            headers={
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get("https://api.github.com/user", headers=headers)
            user_data=response.json()
            return user_data

        except Exception as e:
            raise AuthenticationFailed(detail="Token is invalid or has expired")




# res = requests.post("https://github.com/login/oauth/access_token", params=param_payload, headers={'Accept':'application/json'})
# Accept: application/json
# {
#   "access_token":"gho_16C7e42F292c6912E7710c838347Ae178B4a",
#   "scope":"repo,gist",
#   "token_type":"bearer"
# }

# Accept: application/xml
# <OAuth>
#   <token_type>bearer</token_type>
#   <scope>repo,gist</scope>
#   <access_token>gho_16C7e42F292c6912E7710c838347Ae178B4a</access_token>
# </OAuth>