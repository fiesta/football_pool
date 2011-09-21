import db
import settings
import web

import base64, json, urllib, urllib2

api_server = 'https://api.fiesta.cc'
#api_server = 'http://localhost:5586'

def _create_and_send_request(uri, inputs):
    request = urllib2.Request(uri)
    request.add_header('Authorization', 'Bearer %s' % (db.get_access_token()))
    request.add_header("Content-Type", "application/json")
    request.add_data(json.dumps(inputs))
    return urllib2.urlopen(request)


def get_user_token(grant_code):
    request = urllib2.Request('%s/token' % (api_server))
    request.add_header('Authorization', settings.get_basic_auth_header())
    response = urllib2.urlopen(request, data=urllib.urlencode({'grant_type': 'authorization_code', 'code': grant_code}))

    jres = json.loads(response.read())
    access_token = str(jres['access_token'])
    refresh_token = str(jres['refresh_token'])

    db.save_access_token(access_token)
    db.save_refresh_token(refresh_token)

    return access_token, refresh_token


def refresh_user_token():
    request = urllib2.Request('%s/token' % (api_server))
    request.add_header('Authorization', settings.get_basic_auth_header())
    response = urllib2.urlopen(request, data=urllib.urlencode({'grant_type': 'refresh_token', 'refresh_token': db.get_refresh_token()}))

    jres = json.loads(response.read())
    access_token = str(jres['access_token'])
    refresh_token = str(jres['refresh_token'])

    db.save_access_token(access_token)
    db.save_refresh_token(refresh_token)

    return access_token, refresh_token

def create_group(email_address):
    creator = {"address": email_address,
               "group_name": "football-pool",
               "welcome_message": {"subject": "Welcome to your Football Pool mailing list",
                                   "text": "The Football Pool application has created a mailing list to help manage communication for the league."}}

    try:
        response = _create_and_send_request('%s/group' % (api_server),
                                            {"creator": creator})
    except Exception as inst:
        response = inst

    jres = json.loads(response.read())
    print jres

    db.save_group_id(jres['data']['group_id'])
    return response


def add_member(email):
    membership = {"group_name": "football-pool",
                  "address": email,
                  "welcome_message": {"subject": "Welcome to the Football Pool!",
                                      "text": "Welcome to the Football Pool! This list is used to help manage communication between players in the pool."}}

    try:
        response = _create_and_send_request('%s/membership/%s' % 
                                            (api_server, db.get_group_id()),
                                            membership)
    except Exception as inst:
        response = inst

    jres = json.loads(response.read())
    db.save_fiesta_id_for_user(email, jres['data']['user_id'])
    return response


def send_mail(subject, text):
    print refresh_user_token()

    group = db.get_group_id()
    uri = '%s/message/%s' % (api_server, group)
    try:
        response = _create_and_send_request('%s/message/%s' % (api_server, group),
                                            {"subject": subject, "message": text})
    except Exception as inst:
        response = inst

    jres = json.loads(response.read())
    return jres['success']

if __name__ == '__main__':
    request = urllib2.Request('https://api.fiesta.cc/hello/client')
    request.add_header("Authorization", settings.get_basic_auth_header())
    response = urllib2.urlopen(request)
    print response.read()

    #send_mail("test mail", "just testing the football mailing list")
    
