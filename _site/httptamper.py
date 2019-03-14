import requests

verbs = ["GET", "PUT", "HEAD", "OPTIONS", "POST", "TRACE", "DELETE", "CONNECT"]
url = "http://challenge01.root-me.org/realiste/ch3/admin/"

for verb in verbs:
    print "-----------------------"
    print "Testing for " + verb
    resp = requests.request(verb, url=url)
    print resp
    print resp.content
    print "-----------------------"



