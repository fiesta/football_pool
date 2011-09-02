import settings

import json, urllib, urllib2

def create_group():
    token_uri = 'https://api.fiesta.cc/token'
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, token_uri,
                                  settings.client_id, settings.client_secret)
    urllib2.install_opener(
        urllib2.build_opener(
            urllib2.HTTPBasicAuthHandler(password_manager)))

    request = urllib2.Request(token_uri)
    response = urllib2.urlopen(request, data=urllib.urlencode({'grant_type': 'client_credentials'}))

    access_token = json.loads(response.read())['access_token']

    creator = {"address": "dan@corp.fiesta.cc",
               "name": "Daniel Gottlieb"}
    members = [creator, {"address": "mike@corp.fiesta.cc", "name": "Mike Dirolf"}]
    """
    create_group_inputs = json.dumps({"creator": creator,
                                      "name": settings.list_name,
                                      "members": members})
                                      """
    create_group_inputs = json.dumps({"name": settings.list_name,
                                      "members": members})

    create_group_request = urllib2.Request('https://api.fiesta.cc/group')
    create_group_request.add_header('Authorization', 'Bearer %s' % (access_token))
    create_group_request.add_data(create_group_inputs)
    return create_group_request
    response = urllib2.urlopen(create_group_request)
    return response

    data = response.read()
    print data

if __name__ == '__main__':
    q = create_group()
