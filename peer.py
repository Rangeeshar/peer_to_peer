import sys
import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
MAX_QUEUE = 5
DEFAULT_TIMEOUT = 10 # 10 seconds timeout for connection error


class Client:
	def __init__(self, host, port):
            self.s = None

            # the ip address or hostname of the server, the receiver
            self.host = host
    
            # the port, let's use 5001
            self.port = port

            # Creating socket object
            for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC,
                          socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
                print(f"[+] Connecting to {host}:{port}")
                af, socktype, proto, canonname, sa = res
                try:
                    self.s = socket.socket(af, socktype, proto)
                except OSError as msg:
                        self.s = None
                        continue

                # Trying to connect tp host and port
                try:
                    self.s.settimeout(DEFAULT_TIMEOUT)
                    self.s.connect(sa)
                except OSError as msg:
                    self.s.close()
                    self.s = None
                    continue
                break

            if self.s is None:
                print('could not open socket')
                sys.exit(1)
                print("[+] Connected.")

                    
	def send_data(self, file_name):
            # the name of file we want to send, make sure it exists
            self.filename = file_name

            # get the file size , checking current directory, #TODO accept multiple paths
            self.filesize = os.path.getsize(self.filename)

            self.s.send(f"{self.filename}{SEPARATOR}{self.filesize}".encode())
            # start sending the file
            progress = tqdm.tqdm(range(self.filesize), f"Sending {self.filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(self.filename, "rb") as f:
                for _ in progress:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break # file transmitting is done
                    # we use sendall to assure transimission in 
                    # busy networks
                    self.s.sendall(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
            # close the socket
            self.s.close()


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = None
        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC,
                          socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                self.s = socket.socket(af, socktype, proto)
            except OSError as msg:
                self.s = None
                self.s.close()
                sys.exit(1)
                continue
            try:
                self.s.bind(sa)
                self.s.listen(MAX_QUEUE)
                print(f"[*] Listening as {self.host}:{self.port}")
            except OSError as msg:
                self.s.close()
                self.s = None
                continue
            
            break

        if self.s is None:
            print('could not open socket')
            sys.exit(1)

        self.conn, self.addr = self.s.accept()
        print('Connected by', self.addr)
                
    def recieve_data(self):
            # receive using client socket, not server socket
            self.recieved = None
            try:
                self.received = self.conn.recv(BUFFER_SIZE).decode()
            except Exception as e:
                print("recieve_data Exception: ",e)
                self.conn.close()
                self.s.close()
                sys.exit(1)

            self.filename, self.filesize = self.received.split(SEPARATOR)

            # remove absolute path if there is
            self.filename = os.path.basename(self.filename)
            self.filename = "temp_{}".format(self.filename)
            
            # convert to integer #TODO use for restricting file size.
            self.filesize = int(self.filesize)

            # start receiving the file from the socket
            # and writing to the file stream
            progress = tqdm.tqdm(range(self.filesize), f"Receiving {self.filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(self.filename, "wb") as f:
                for _ in progress:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = self.conn.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))

            # close the client socket
            self.conn.close()
            # close the server socket
            self.s.close()


