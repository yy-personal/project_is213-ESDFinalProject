import json
import os

import amqp_setup
from twilio.rest import Client

monitorBindingKey='*.error'

def receiveError():
    amqp_setup.check_setup()
    
    queue_name = "Error"  

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an error by " + __file__)
    processError(body)
    print(body)
    print() # print a new line feed

def processError(errorMsg):
    print("--DATA:", errorMsg)
    # Your Account SID from twilio.com/console
    account_sid = "AC5475d2fba086a2ea2998f3c196f95267"
    #Your Auth Token from twilio.com/console
    auth_token  = "0f97588a4baf6268c08a80caaebefde1"
    client = Client(account_sid, auth_token)
        
    message = client.messages.create(
        to="+65 9178 8772", 
        from_="+14235928583",
        body= errorMsg)
    print(message.sid)
    print()


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveError()
