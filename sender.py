import argparse
import socket
import struct
import time

def create_data_packet(packet_type, seq_num, length):
    udp_header = struct.pack('!cII', bytes(packet_type, 'utf-8'), socket.htonl(seq_num), length)

    #payload = bytes(file_name, 'utf-8')
    #packet = udp_header + payload
    return packet

# The sender will chunk a requested file and send each file chunk via UDP packets to the requester. 
if __name__ == "__main__":
    # parse arguments
    # python3 sender.py -p <port> -g <requester port> -r <rate> -q <seq_no> -l <length>
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=True, help='the port where the sender waits for requests')
    parser.add_argument('-g', '--requester_port', type=int, required=True, help='requester port, port where the requester is waiting')
    parser.add_argument('-r', '--rate', type=int, required=True, help='number of packets to be sent per second')
    parser.add_argument('-q', '--seq_no', type=int, required=True, help='initial sequence of the packet exchange')
    parser.add_argument('-l', '--length', type=int, required=True, help='length of the payload (in bytes) in the packets')

    # sender and requester port should be in this range: 2049 < port < 65536
    args = parser.parse_args()
    print("Argument Values")
    for arg in vars(args):
        print(f'{arg}: {getattr(args, arg)}, {type(getattr(args, arg))}')
    
    # set all args
    port = args.port
    req_port = args.requester_port
    rate = args.rate
    seq_no = args.seq_no
    length = args.length

    if not (2049 < port < 65536 and 2049 < req_port < 65536):
        raise Exception('ports should be in the range 2049 < port < 65536')

    # socket for listening to requests
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_sock.bind(('127.0.0.1', port))

    # assemble the packet header, total 9 bytes
    # 1 byte: packet type (char)
    # 4 bytes: sequence num
    # 4 bytes: length
    udp_header = struct.pack("!cII", req_port, port, length)

    UDP_IP = '127.0.0.1' # TODO: hardcoding for now
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            # listen for request
            listen_sock.settimeout(1) 
            request_data, addr = listen_sock.recvfrom(1024) 
            print(f"Received request from {addr}: {request_data.decode('utf-8')}")

        except socket.timeout:
            # continue sending stuff
            pass
        # TODO: message will be bytes from the file
        MESSAGE = b'FILLER STUFF FOR NOW'
        sock.sendto(MESSAGE, ('127.0.0.1', req_port))
        # TODO: will have to sleep for some amount of time according to rate
# Each sender will have a copy of the file parts that it is responsible for in the same folder as it is running from, so that it can access them directly. The sender should be invoked in the following way:

