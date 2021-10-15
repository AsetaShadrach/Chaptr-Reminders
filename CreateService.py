import os 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class CreateService():
    """
    client_secret - Path to the client secret file (MUST EXIST)
    token_file - Path to the token file (Will be created if doesn't exist)
    service_name - e.g gmail
    service_id - e,g v1

    """
    def __init__(self,client_secret , token_file, service_name, service_id, scopes ):
        self.client_secret = client_secret
        self.token_file = token_file
        self.SCOPES = scopes
        self.SERVICE_NAME = service_name
        self.SERVICE_ID = service_id

    def CreateApiService(self):
        creds = None
        
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret, self.SCOPES)
                flow.run_local_server()
                creds = flow.credentials
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
            
        service = build(self.SERVICE_NAME, self.SERVICE_ID, credentials = creds)

        return service