from socket import socket, AF_INET, SOCK_DGRAM

class Server(object):
    def __init__(self, host, port, buffer=1000):
        self.host = host
        self.port = port
        self.buffer = buffer
        self.udp_server_socket = socket(AF_INET, SOCK_DGRAM)
        self.last_msg = ""

    def start(self):
        print("Starting Server")
        self.udp_server_socket.bind((self.host, self.port))
        while self.last_msg != "stop":
            self.last_msg, client = self.udp_server_socket.recvfrom(self.buffer)
            print("(Client IP, Client PORT) = {0}\n message = {1}".format(client, self.last_msg.decode()))
            self.response(client)
        self.udp_server_socket.close()
        print("Server stopped")

    def response(self, client_dest):
        self.udp_server_socket.sendto("ACK".encode(), client_dest)
        print("Sent ACK")

def main():
    serv = Server("", 5000)
    serv.start()

if __name__ == "__main__":
    main()
