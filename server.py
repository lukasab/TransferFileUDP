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
            self.parse_packet(self.last_msg, client)
            #print("(Client IP, Client PORT) = {0}\n message = {1}".format(client, self.last_msg.decode()))
            self.response(client)
        self.udp_server_socket.close()
        print("Server stopped")

    def parse_packet(self, packet, client):
        """
           opcode  operation
            1     Read request (RRQ)
            2     Write request (WRQ)
            3     Data (DATA)
            4     Acknowledgment (ACK)
            5     Error (ERROR)
        """
        opcode = packet[0:2]
        #manda pra método do operação correta

    def handle_rrq(self):
        nameEnd = packet.find(b'\0', 2)
        filename = packet[2:nameEnd].decode('ascii')
        modeEnd = p.find(b'\0', start=nameEnd+1)
        mode = p[nameEnd+1:modeEnd].decode('ASCII')
        pass
    
    def handle_wrq(self):
        pass
    
    def handle_ack(self):
        pass
    
    def handle_error(self):
        pass

    def response(self, client_dest):
        self.udp_server_socket.sendto("ACK".encode(), client_dest)
        print("Sent ACK")

def main():
    serv = Server("", 5000)
    serv.start()

if __name__ == "__main__":
    main()
