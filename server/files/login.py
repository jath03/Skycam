from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets as FFC
import httplib2
import json
import pathlib
import subprocess
import pickle
subprocess.run('sudo rm /home/jack/projects/server/files/flow.dat /home/jack/projects/server/files/params.dat', shell=True)
flow = FFC('/home/jack/.creds/client_secrets.json', scope=('https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'), redirect_uri='http://192.168.5.1.nip.io:6789')
with open('/home/jack/projects/server/files/flow.dat', 'wb') as f:
  pickle.dump(flow, f)


def main():
  auth_uri = flow.step1_get_authorize_url()
  print('''<!DOCTYPE html>
<html>
	<head>
		<script>window.location = "{}";</script>
	</head>
	<body>
		<h1>Hello</h1>
	</body>
</html>'''.format(auth_uri))
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    subprocess.run(['sudo rm /home/jack/.creds/credentials.dat'])

