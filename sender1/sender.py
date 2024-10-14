import socket
import argparse
import struct
import os
import time
from datetime import datetime

def create_data_packet(seq_num, length, payload):
    udp_header = struct.pack('!cII', bytes('D', 'utf-8'), socket.htonl(seq_num), socket.htonl(length))
    packet = udp_header + payload
    return packet

def create_end_packet(seq_num):
    udp_header = struct.pack('!cII', bytes('E', 'utf-8'), socket.htonl(seq_num), socket.htonl(0))
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

    pps = 1 / rate

    PORT = port
    HOST_IP = socket.gethostbyname(socket.gethostname())

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST_IP, PORT))

    print(f"Listening for requests on {HOST_IP}:{PORT}")

    while True:
        # wait for packet
        data, addr = sock.recvfrom(1024)
        req_ip = addr[0]

        # check if it's a request packet
        if data[0] == ord('R'):
            # process the filename from payload
            file_name = data[9:].decode('utf-8')
            try:
                file_size = os.path.getsize(file_name) # get size of file in bytes
            except OSError as e:
                print(f"OSError: File {file_name} does not exist or is inaccessible")
                err_end_packet = create_end_packet(seq_no)
                sock.sendto(err_end_packet, addr)
                raise
            except Exception as e:
                print(f"Unexpected Exception: {e}")
                err_end_packet = create_end_packet(seq_no)
                sock.sendto(err_end_packet, addr)
                raise

            # file successfully found, continue
            file_size = os.path.getsize(file_name) # get size of file in bytes
            print(f'{file_name} size: {file_size}')

            with open(file_name,'rb') as f: # read file contents as bytes
                pointer = 0
                next_packet_time = time.time() # time that we expect the next packet to be sent
                while pointer < file_size:
                    chunk = f.read(length)
                    data_packet = create_data_packet(seq_no, len(chunk), chunk)
                    first_4_bytes = data_packet[9:13]

                    sock.sendto(data_packet, addr)
                    current_time = datetime.now()

                    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                    print('DATA packet')
                    print(f'send time: {formatted_time}')
                    print(f'requester address: {req_ip}')
                    print(f'sequence number: {seq_no}')
                    print(f'first 4 bytes: {first_4_bytes}\n')
                                        
                    # calculate the time for the next packet
                    next_packet_time += pps

                    sleep_time = max(next_packet_time - time.time(), 0)

                    time.sleep(sleep_time) # distribute sending intervals

                    pointer += len(chunk)
                    seq_no += len(chunk) 

            # done sending data, send the end packet
            end_packet = create_end_packet(seq_no)
            sock.sendto(end_packet, addr)
            exit(0)