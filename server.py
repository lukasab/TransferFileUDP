"""
Server program for the TFTP protocol (https://tools.ietf.org/html/rfc1350).
It can transfer files with a UDP connection
"""
from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack
import sys
import os
import time 

class Server():
    """
    Server class with all methods defined in the protocol
    """
    def __init__(self, host, port, buffer=1000, timeout=5):
        self.host = host
        self.port = port
        self.buffer = buffer
        self.udp_server_socket = socket(AF_INET, SOCK_DGRAM)
        self.last_msg = ""
        self.timeout=timeout
        self.stop = False

    def start(self):
        """
        Start server, listening for any read or write request
        """
        print("Starting Server")
        self.udp_server_socket.bind((self.host, self.port))
        while not self.stop:
            self.last_msg, client = self.udp_server_socket.recvfrom(self.buffer)
            self.parse_packet(self.last_msg, client)
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
        if opcode == b'\x00\x01':
            self.handle_rrq(packet, client)
        elif opcode == b'\x00\x02':
            self.handle_wrq(packet, client)
        elif opcode == b'\x00\x03':
            self.handle_data(packet, client)
        elif opcode == b'\x00\x04':
            self.handle_ack(packet, client)
        elif opcode == b'\x00\x05':
            self.handle_error(packet, client)
        else:
            sys.exit("Opcode não identificado")

    def handle_rrq(self, packet, client):
        name_end = packet.find(b'\0', 2)
        filename = packet[2:name_end].decode('ascii')
        mode_end = packet.find(b'\0', name_end+1)
        mode = packet[name_end+1:mode_end].decode('ASCII')
        #FIX-ME depois de ter uma requisição de leitura o sevidor manda os dados e espera ack e vai mandando até acabar
        if(os.path.isfile(filename)):
            self.send_data(filename, client)
        else:
            self.send_error(1, client, "Arquivo nao existe")

    def handle_wrq(self, packet, client):
        pass

    def handle_data(self, packet, client):
        pass

    def handle_ack(self, packet, client):
        pass

    def handle_error(self):
        pass

    def send_data(self, filename, client):
        """
                        DATA packet
            2 bytes     2 bytes      n bytes
            ----------------------------------
           | Opcode |   Block #  |   Data     |
            ----------------------------------
        """
        opcode = 3
        block_number = 1
        with open(filename, 'rb') as file_2_send:
            end_of_file = False
            while not end_of_file:
                bytes_2_send = file_2_send.read(self.buffer)
                print(len(bytes_2_send))
                if len(bytes_2_send) < self.buffer:
                    end_of_file = True
                fmt = '!HH'+str(len(bytes_2_send))+'s'
                data = pack(fmt, opcode, block_number, bytes_2_send)
                print(data)
                self.udp_server_socket.sendto(data, client)
                block_number += 1
                time.sleep(1)
        pass

    def send_error(self, error_code, client, error_msg=""):
        """
                          ERROR packet
            2 bytes     2 bytes      string    1 byte
            -----------------------------------------
           | Opcode |  ErrorCode |   ErrMsg   |   0  |
            -----------------------------------------
            
                          Error Codes
            Value              Meaning

              0         Not defined, see error message (if any).
              1         File not found.
              2         Access violation.
              3         Disk full or allocation exceeded.
              4         Illegal TFTP operation.
              5         Unknown transfer ID.
              6         File already exists.
              7         No such user.
        """
        opcode = 5
        fmt = '!HH'+str(len(error_msg))+'sb'
        error = pack(fmt, opcode, error_code, error_msg.encode('ascii'), 0)
        self.udp_server_socket.sendto(error, client)
        self.stop = True

    def response(self, client_dest):
        self.udp_server_socket.sendto("ACK".encode(), client_dest)
        print("Sent ACK")

def main():
    """
    Control program flow
    """
    serv = Server("", 5000)
    serv.start()

if __name__ == "__main__":
    main()
