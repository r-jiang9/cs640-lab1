import socket
import argparse
import struct
import os
import math

def create_data_packet(seq_num, length, payload):
    udp_header = struct.pack('!cII', bytes('D', 'utf-8'), socket.htonl(seq_num), length)
    packet = udp_header + payload
    print(f'Created data packet: {packet}')
    return packet

def create_end_packet(seq_num):
    udp_header = struct.pack('!cII', bytes('E', 'utf-8'), socket.htonl(seq_num), 0)
    packet = udp_header
    return packet  

def create_send_data_packet(seq_num, length):
    udp_header = struct.pack('!cII', bytes('D', 'utf-8'), socket.htonl(seq_num), length)
    packet = udp_header
    return packet

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=True, help='the port where the sender waits for requests')
    parser.add_argument('-g', '--requester_port', type=int, required=True, help='requester port, port where the requester is waiting')
    parser.add_argument('-r', '--rate', type=int, required=True, help='number of packets to be sent per second')
    parser.add_argument('-q', '--seq_no', type=int, required=True, help='initial sequence of the packet exchange')
    parser.add_argument('-l', '--length', type=int, required=True, help='length of the payload (in bytes) in the packets')

    args = parser.parse_args()
    port = args.port
    req_port = args.requester_port
    rate = args.rate
    seq_no = args.seq_no
    length = args.length

    UDP_IP = "127.0.0.1"
    UDP_PORT = port
    packet = create_data_packet(seq_no, length, b'THIS IS A RANDOM MSG')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print(f"Listening for requests on {UDP_IP}:{UDP_PORT}")

    while True:
        # wait for packet
        data, addr = sock.recvfrom(1024)
        print(f"Received request: {data} from {addr}")

        # check if it's a request packet
        if data[0] == ord('R'):
            print("received request packet, sending data")
            # process the filename from payload
            file_name = data[9:].decode('utf-8')
            file_size = os.path.getsize(file_name) # get size of file in bytes
            print(f'{file_name} size: {file_size}')

            with open(file_name,'rb') as f: # read file contents as bytes
                pointer = 0
                while pointer < file_size:
                    chunk = f.read(length)
                    data_packet = create_data_packet(seq_no, len(chunk), chunk)
                    pointer += len(chunk)
                    seq_no += len(chunk)      
                    sock.sendto(data_packet, addr)  # Send a data packet back to the requester  
                    print(f"Sent data packet to {addr}")
            # done sending data, send the end packet
            end_packet = create_end_packet(seq_no)
            sock.sendto(end_packet, addr)
            # send data packets back
