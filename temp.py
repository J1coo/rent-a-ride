
import os
from twilio.rest import Client
def OTPverification():
    account_sid = "AC0b484c1ca305d3820ac6ceb619e3f5b9"
    auth_token = "55b373b918b3e09933f94af8fe5cf34e"
    verify_sid = "VA7ed221e2e0bfc457c064459cd5efc2e9"
    verified_number = "+918287288456"

    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to=verified_number, channel="sms")
    print(verification.status)

    otp_code = input("Please enter the OTP:")

    verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to=verified_number, code=otp_code)
    print(verification_check.status)


OTPverification()