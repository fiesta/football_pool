import db
import settings

import json, urllib, urllib2

api_server = 'https://api.fiesta.cc'
#api_server = 'http://localhost:5586'

token_uri = '%s/token' % (api_server)
password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, token_uri,
                              settings.client_id, settings.client_secret)
urllib2.install_opener(
    urllib2.build_opener(
        urllib2.HTTPBasicAuthHandler(password_manager)))

def get_user_token(user_code):
    request = urllib2.Request(token_uri)
    response = urllib2.urlopen(request, data=urllib.urlencode({'grant_type': 'authorization_code', 'code': user_code}))

    access_token = json.loads(response.read())['access_token']
    db.save_access_token(access_token)
    return access_token


def create_group(email_address, access_token):
    creator = {"address": email_address,
               "group_name": "football-pool",
               "welcome_message": {"subject": "Welcome to your Football Pool mailing list",
                                   "text": "The Football Pool application has created a mailing list to help manage communication for the league."}}
    create_group_inputs = json.dumps({"creator": creator})

    create_group_request = urllib2.Request('%s/group' % (api_server))
    create_group_request.add_header('Authorization', 'Bearer %s' % (access_token))
    create_group_request.add_header("Content-Type", "application/json")
    create_group_request.add_data(create_group_inputs)
    try:
        response = urllib2.urlopen(create_group_request)
    except Exception as inst:
        response = inst

    jres = json.loads(response.read())
    db.save_group_id(jres['data']['group_id'])
    return response


def add_member(email):
    access_token = db.get_access_token()
    membership = {"group_name": "football-pool",
                  "address": email,
                  "welcome_message": {"subject": "Welcome to the Football Pool!",
                                      "text": "Welcome to the Football Pool! This list is used to help manage communication between players in the pool."}}
    add_member_inputs = json.dumps(membership)

    add_member_request = urllib2.Request('%s/membership/%s' % (api_server, db.get_group_id()))
    add_member_request.add_header('Authorization', 'Bearer %s' % (db.get_access_token()))
    add_member_request.add_header('Content-Type', 'application/json')
    add_member_request.add_data(add_member_inputs)
    try:
        response = urllib2.urlopen(add_member_request)
    except Exception as inst:
        response = inst

    print response

    jres = json.loads(response.read())
    db.save_fiesta_id_for_user(email, jres['data']['user_id'])
    return response


if __name__ == '__main__':
    create_group()
