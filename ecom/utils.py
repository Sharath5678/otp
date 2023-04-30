import os
from twilio.rest import Client

account_sid = 'AC877bc7976215da7dc6ef1df24ee8e91a'
auth_token = '7fa8797ea27fb28d6cf7521133902163'
client = Client(account_sid,auth_token)

def send_sms(user_code,phone_number):
    messages = client.messages.create(
        body = f' Hey lad, your Username and Verification is {user_code} ',
        from_ = '+17262007184',
        to=f'{phone_number}'
    )
    print(messages.sid)