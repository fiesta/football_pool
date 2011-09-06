import settings

import json, urllib, urllib2

api_server = 'https://api.fiesta.cc'
#api_server = 'http://localhost:5586'

def create_group(access_token):
    creator = {"address": "dan@corp.fiesta.cc",
               "name": "Daniel Gottlieb"}
    members = [creator, {"address": "gofiestacc@gmail.com", "name": "Mike Dirolf"}]
    create_group_inputs = json.dumps({"creator": creator,
                                      "name": settings.list_name,
                                      "members": members})

    create_group_request = urllib2.Request('%s/group' % (api_server))
    create_group_request.add_header('Authorization', 'Bearer %s' % (access_token))
    create_group_request.add_header("Content-Type", "application/json")
    create_group_request.add_data(create_group_inputs)
    try:
        response = urllib2.urlopen(create_group_request)
    except Exception as inst:
        response = inst

    return response


token_uri = '%s/token' % (api_server)
password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, token_uri,
                              settings.client_id, settings.client_secret)
urllib2.install_opener(
    urllib2.build_opener(
        urllib2.HTTPBasicAuthHandler(password_manager)))

def get_client_token():
    request = urllib2.Request(token_uri)
    response = urllib2.urlopen(request, data=urllib.urlencode({'grant_type': 'client_credentials'}))

    access_token = json.loads(response.read())['access_token']
    return access_token


def get_user_token(user_code):
    request = urllib2.Request(token_uri)
    response = urllib2.urlopen(request, data=urllib.urlencode({'grant_type': 'authorization_code', 'code': user_code}))

    access_token = json.loads(response.read())['access_token']
    return access_token


def add_member(email):
    pass


if __name__ == '__main__':
    create_group()
