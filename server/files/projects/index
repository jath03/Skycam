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


def main():
  # Create a Storage object. This object holds the credentials that your
  # application needs to authorize access to the user's data. The name of the
  # credentials file is provided. If the file does not exist, it is
  # created. This object can only hold credentials for a single user, so
  # as-written, this script can only handle a single user.
  with open('/home/jack/projects/server/files/flow.dat', 'r+b') as f:
    flow = pickle.load(f)
  with open('/home/jack/projects/server/files/params.dat', 'r+b') as file:
    params = pickle.load(file)
  try:
    credentials = flow.step2_exchange(params['code'])
  # The get() function returns the credentials for the Storage object. If no
  # credentials were found, None is returned.
  # If no credentials are found or the credentials are invalid due to
  # expiration, new credentials need to be obtained from the authorization
  # server. The oauth2client.tools.run_flow() function attempts to open an
  # authorization server page in your default web browser. The server
  # asks the user to grant your application access to the user's data.
  # If the user grants access, the run_flow() function returns new credentials.
  # The new credentials are also stored in the supplied Storage object,
  # which updates the credentials.dat file.
  # Create an httplib2.Http object to handle our HTTP requests, and authorize it
  # using the credentials.authorize() function.
    http = httplib2.Http()
    http = credentials.authorize(http)

  # The apiclient.discovery.build() function returns an instance of an API service
  # object can be used to make API calls. The object is constructed with
  # methods specific to the calendar API. The arguments provided are:
  #   name of the API ('calendar')
  #   version of the API you are using ('v3')
  #   authorized httplib2.Http() object that can be used for API calls
    service = build('oauth2', 'v2', http=http)
    try:
      profile = service.userinfo().v2().me().get().execute()
      if profile['id'] != '101157566449352653116':
        print('''<!DOCTYPE html>
<html>
 	<head>
		<link type="text/css" rel="stylesheet" href="style.css">
		<title>Jack.com</title>
	</head>
	<body>
		<h2>Access Denied</h2>
		<p>
			You do not have permission to view this page.
			Please go back to the <a href"http://192.168.5.1:6789/login?redirect=projects">login page</a> or the <a href="http://192.168.5.1:6789/login">home page</a>.
			If this is a bug please <a href"http://192.168.5.1:6789/login?redirect=projects">reauthenticate</a>.
		</p>
	</body>
</html>'''.format(name=profile['name'], pic=profile['picture'], email=profile['email'], id=profile['id']))
      else:
        path = pathlib.Path('/home/jack/projects/')
        projects = list(path.glob('*'))
        pro = list()
        for p in projects:
          pro.append(p.parts[-1])
        print('''<!DOCTYPE html>

<html>
        <head>
                <link type="text/css" rel="stylesheet" href="style.css">
                <title>Jack.com</title>
        </head>
        <body>
                <div id="header">
                        <h1>Jack's Website</h1>
                </div>
                <div id="nav">
                        <h4>Hello, {name}</h4>
                        <ul>
				<li><a href="http://192.168.5.1:6789/login">Home</a></li>
                                <li><a href="sites.html">My favorite sites</a></li>
                                <li><a href="secret-fake.html">Secret site</a></li>
				<li><a href="http://192.168.5.1:6789/login?redirect=projects">My projects</a></li>
                        </ul>
                </div>
                <div id="section1">
                        <h3>Projects</h3>
			<p>Projects: {projects}</p> 
                </div>
        </body>
</html>'''.format(projects=', '.join(pro), name=profile['name']))
    except AccessTokenRefreshError:
      # The AccessTokenRefreshError exception is raised if the credentials
      # have been revoked by the user or they have expired.
      print ("The credentials have been revoked or expired, please re-run"
             "the application to re-authorize")
  except Exception as error:
    print("""<!DOCTYPE html>
<html>
	<head>
	</head>
	<body>
		<h2>Error: {error}</h2>
		<p>Redirecting...</p>
		<script>window.location = "http://192.168.5.1:6789/login?redirect=projects";</script>
	</body>
</html>""".format(error=error))
    
if __name__ == '__main__':
  main()
