from peer import Client
from peer import Server
import time

while True:
    try:
        client_obj = Client("0.0.0.0", 5001)
        client_obj.send_data("test.txt")
    except Exception as e:
        print("Trying to be client failed, try to be server.")
    try:
        server_obj = Server("0.0.0.0",5005)
        server_obj.recieve_data()
    except Exception as e:
        print("Now trying to be client again")
    time.sleep(20)
