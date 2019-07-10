from socket import socket, AF_INET, SOCK_DGRAM, timeout
from struct import pack
import sys 
import time
import random

MODES = ['netascii', 'octet', 'mail']
class Client(object):
    def __init__(self, host="127.0.0.1", port=5000, buffer=1024, timeout=20):
        self.dest = (host, port)
        self.udp_client_socket = socket(AF_INET, SOCK_DGRAM)
        self.last_msg = ""
        self.buffer = buffer
        self.timeout = timeout

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
        rrq = pack(fmt, opcode, filename.encode('ascii'), 0, mode.encode('ascii'), 0)
        self.udp_client_socket.sendto(rrq, self.dest)
        self.udp_client_socket.settimeout(self.timeout)
        try:
            recv_data = self.udp_client_socket.recv(self.buffer)
            #print("Recebi")
            self.parse_packet(recv_data)
        except timeout:
            print("Timeout")

    def send_ack(self, block_number):
        """
               ACK packet
          2 bytes     2 bytes
         ---------------------
        | Opcode |   Block #  |
         ---------------------
        """
        opcode = 4
        fmt = '!HH'
        ack = pack(fmt, opcode, block_number)
        self.udp_client_socket.sendto(ack, self.dest)
        print("ACK enviado, B#={0}".format(block_number))

    def parse_packet(self, packet):
        """
           opcode  operation
            1     Read request (RRQ)
            2     Write request (WRQ)
            3     Data (DATA)
            4     Acknowledgment (ACK)
            5     Error (ERROR)
        """
        opcode = packet[0:2]
        if opcode == b'\x00\x03':
            self.handle_data(packet)
        elif opcode == b'\x00\x04':
            self.handle_ack(packet)
        elif opcode == b'\x00\x05':
            self.handle_error(packet)
        else:
            sys.exit("Opcode não tratado")

    def handle_data(self, packet):
        """
                        DATA packet
            2 bytes     2 bytes      n bytes
            ----------------------------------
           | Opcode |   Block #  |   Data     |
            ----------------------------------
        """
        block_number_start = 1
        receiving = True
        dado_perdido = False
        with open('recebido/received.txt', 'wb') as file_2_receive:
            while receiving:
                print("\nEsperando dados")
                if random.uniform(0,1) > 0.3:
                    print("Dado perdido")
                    self.udp_client_socket.sendto("error".encode(), self.dest)
                    data = packet[4:]
                    dado_perdido = True
                else:
                    dado_perdido = False
                    block_number = int.from_bytes(packet[2:4], 'big')
                    data = packet[4:]
                    print("Dados recebidos")
                    print("Tamanho dos dados: {0} bytes.\nDados:".format(len(data)))
                    print(data)
                    file_2_receive.write(data)
                    self.send_ack(block_number)
                
                time.sleep(1)
                packet = self.udp_client_socket.recv(self.buffer)
                if not dado_perdido:
                    if len(data) < 1000:
                        receiving = False
            print("Finish")

    def handle_error(self, packet):
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
        error_code = packet[2:4]
        error_msg_end = packet.find(b'\0', 4)
        error_msg = packet[4:error_msg_end].decode('ascii')
        sys.exit("Pacote de erro recebido.")
        #print(error_code)
        #print(error_msg)
        pass

def main():
    client = Client()
    client.establish_connection("send.txt")

if __name__ == "__main__":
    main()
