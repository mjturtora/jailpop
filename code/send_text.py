__author__ = 'notme'

#from twilio.rest import TwilioRestClient
from twilio import rest

"""
input account_sid
auth_token
to_numbers (as string)
from_number (as string)
"""

# Your Account Sid and Auth Token from twilio.com/user/account

client = rest.TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body="Jo please?! I love you <3",
    to=to_number,    # Replace with your phone number
    from_=from_number) # Replace with your Twilio number
print message.sid
