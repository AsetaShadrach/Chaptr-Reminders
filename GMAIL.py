from CreateService import CreateService
from email.mime.text import MIMEText 
import base64



class ChaptrGmail():
    SCOPES = [  'https://www.googleapis.com/auth/gmail.compose', 'openid', 
                'https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/gmail.send',
                'https://www.googleapis.com/auth/gmail.insert',
                'https://www.googleapis.com/auth/gmail.modify']


    def __init__(self, params):
        self.sender_email = params['sender_email']
        self.assignment_name = params['assignment_name']
        self.link_to_assignment = params['link_to_assignment']


    def create_message(self, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = self.sender_email
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
        return { 'raw': raw_message.decode("utf-8")  }
        
    
    def send_message(self, message):
        try:
            message = (self.service.users().messages().send(userId=self.sender_email, body=message)
                    .execute())
            return message
        except Exception as exception: 
            if type(exception).__name__ == 'HttpError':
                print ('HttpError  occurred\n'+ str(exception))
            else:
                print(type(exception).__name__)
        
        

    def send_reminder_email(self,row):
        # Text to be displayed on the email
        salutations = "\nHi, "+ row[0]+"\n"
        body =  "\nYou are yet to submit "+self.assignment_name + " assignment."
        link_to = "\n\nHere is the link to the assignment  : " + self.link_to_assignment
        more_text = '''
        \nIf you had submitted your project, you could be receiving this email because :
        - You submitted with a title different from the one specified.
        - You used an email for submission that is different from the one you registered on Chaptr.        
        \nDo resubmit, but make sure to follow the guidelines and use the specific email you registered with.'''
                    
        # ----------

        email_string = salutations + body + link_to + more_text
        email_to_send = self.create_message(row[1],
                                            'UNSUBMITTED ASSIGNMENT REMINDER',
                                            email_string
                                            )
        self.send_message(email_to_send)
            
        return 1


    def gmail_main(self, df):
        service = CreateService('ChaptrGmailSecret.json',
                                'chaptr_gmail_token.json',
                                'gmail', 
                                'v1', 
                                self.SCOPES)
        self.service = service.CreateApiService()
        
        df.apply(self.send_reminder_email,axis=1)
    

