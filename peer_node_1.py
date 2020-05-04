from peer import Server
from peer import Client
import time

while True:
    try:
        server_obj = Server("0.0.0.0",5001)
        server_obj.recieve_data()
    except Exception as e:
        print("Trying to be a client...")

    time.sleep(10)
    try:
        client_obj = Client("0.0.0.0", 5005)
        client_obj.send_data("temp_test.txt")
    except Exception as e:
        print("Trying to be server..")
