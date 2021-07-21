import requests
r = requests.get("http://app.objco.com:8099/?account=NTB37PKZUG&limit=4")
print(r.text)