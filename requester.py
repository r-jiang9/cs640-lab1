import socket
import argparse
import struct
import csv
from datetime import datetime

def create_request_packet(file_name):
    udp_header = struct.pack('!cII', bytes('R', 'utf-8'), socket.htonl(0), 0)
    payload = bytes(file_name, 'utf-8')
    packet = udp_header + payload
    return packet

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                description='sum the integers at the command line')
    parser.add_argument('-p', '--port', type=int, required=True, help='Port number, required')
    parser.add_argument('-o', '--file', type=str, required=True, help='The name of the file being requested')

    args = parser.parse_args()

    port = args.port
    file_name = args.file

    packet = create_request_packet(file_name)

    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    # read from tracker.txt
    tracker = []
    with open('tracker.txt', 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        for row in reader:
            tracker.append(row)
    print(tracker)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, port))

    # send a request packet
    req_packet = create_request_packet(file_name)
    sock.sendto(req_packet, (UDP_IP, UDP_PORT))

    print(f"Listening on {UDP_IP}:{port}")
    while True:
        # wait for response
        data, addr = sock.recvfrom(1024)
        print(f"Received data: {data} from {addr}")

        sender_ip = addr[0]
        sender_port = addr[1]

        if data[0] == ord('D'):
            # data packet
            packet_type, seq_num, payload_length = struct.unpack('!cII', data[:9])
            seq_num = socket.ntohl(seq_num)  # Convert back from network byte order
            payload_length = socket.ntohl(payload_length)
            payload = data[9:]  # The rest of the packet is the payload

            # get curr time
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            first_4_bytes = payload[:4] if len(payload) >= 4 else payload

            print('DATA packet')
            print(f'send time: {formatted_time}')
            print(f'percentage received: IDK')
            print(f'requester address: {sender_ip}')
            print(f'first 4 bytes: {first_4_bytes}\n')
        elif data[0] == ord('E'):
            # data packet
            packet_type, seq_num, payload_length = struct.unpack('!cII', data[:9])
            seq_num = socket.ntohl(seq_num)  # Convert back from network byte order
            payload_length = socket.ntohl(payload_length)
            payload = data[9:]  # The rest of the packet is the payload

            # get curr time
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            first_4_bytes = payload[:4] if len(payload) >= 4 else payload

            print('END packet')
            print(f'send time: {formatted_time}')
            print(f'percentage received: IDK')
            print(f'requester address: {sender_ip}')
            print(f'first 4 bytes: {first_4_bytes}\n')
        # sock.sendto(data, addr)  # Echo back the received message

