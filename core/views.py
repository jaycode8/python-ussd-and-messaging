from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import africastalking
import os
from dotenv import load_dotenv
load_dotenv()

africastalking.initialize(
    username=os.getenv("username"),
    api_key=os.getenv("api_key")
)
sms = africastalking.SMS

def send_sms():
    recipients = ["+254748428348","+254778750215"]
    message = "Hey this is a message i automated with django using africas talking";
    # sender = "XXYYZZ"
    try:
        response = sms.send(message, recipients)
        print (response)
    except Exception as e:
        print (f'James, we have a problem: {e}')

@csrf_exempt
def ussd_callback(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""
        recipients = ["+254111482180","+254778750215"]

        if text == "":
            response = """
                CON What would you like to check
                1. Your Phone Number
                2. Check email
                3. Just Checking in
                4. Send an sms
            """

        elif text == "1":
            response = f'END Your Phone Number is {phone_number} \n'

        elif text == "2":
            response = """
                CON What email do you what to access
                1. Company email
                2. Your email
                3. Exit
            """

        elif text == "3":
            response = "END Thank you for checking in \n"

        elif text == "4":
            try:
                send_sms()
                response = "END Thank you for using jaytech ticketing \n"
            except:
                response = "END Thank you for using jaytech ticketing but an error has occured when delivering the sms \n"

        elif text == "2*1":
            response = "END infor@jay.com \n"

        elif text == "2*2":
            response = "END yours@email.com \n"

        elif text == "2*3":
            response = "END Thank you \n"


        return HttpResponse(response)