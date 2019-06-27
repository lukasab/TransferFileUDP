from socket import socket, AF_INET, SOCK_DGRAM

class Client(object):
    def __init__(self, host="127.0.0.1", port=5000, buffer=1000):
        self.dest = (host, port)
        self.udp_client_socket = socket(AF_INET, SOCK_DGRAM)
        self.last_msg = ""
        self.buffer = buffer

    def send_msg(self):
        print("To exit type 'stop'")
        while self.last_msg != "stop":
            self.last_msg = input("Send something\n")
            self.udp_client_socket.sendto(self.last_msg.encode(), self.dest)
            recv_data = self.udp_client_socket.recv(self.buffer)
            print(recv_data)
        self.udp_client_socket.close()
        print("Client and Server stopped")

def main():
    client = Client()
    client.send_msg()

if __name__ == "__main__":
    main()
