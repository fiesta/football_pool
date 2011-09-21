import base64

league_password = 'fiesta.cc'
list_name = 'football-pool'

client_id = "TmE01CtLAnL8AAAA"
client_secret = "fbRHbPWbkXDOyMTGBO_yLyu41k0BazCo9i8yKS36"

def get_basic_auth_header():
    return "Basic " + base64.b64encode("%s:%s" % (client_id, client_secret))
