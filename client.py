from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack

MODES = ['netascii', 'octet', 'mail']
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
    
    def establish_connection(self, filename, mode='netascii'):
        """
                             RRQ/WRQ packet
            2 bytes     string    1 byte     string   1 byte
            ------------------------------------------------
           | Opcode |  Filename  |   0  |    Mode    |   0  |
            ------------------------------------------------
        """
        if mode.lower() not in MODES:
            sys.exit('Modo não definido')
        if filename is None:
            sys.exit('Nome do arquivo não especificado')

        opcode = 1
        fmt = '!H'+str(len(filename))+'sb'+str(len(mode))+'sb'
        rrq = pack(fmt, opcode, filename.encode("ascii"), 0, mode.encode("ascii"), 0)
        self.udp_client_socket.sendto(rrq, self.dest)
        recv_data = self.udp_client_socket.recv(self.buffer)
        print(recv_data)


def main():
    client = Client()
    client.establish_connection("test.txt")

if __name__ == "__main__":
    main()
