import socket
import argparse
import struct
import csv
from datetime import datetime
from collections import OrderedDict

def create_request_packet(file_name):
    udp_header = struct.pack('!cII', bytes('R', 'utf-8'), socket.htonl(0), socket.htonl(0))
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
    send_ip = socket.gethostbyname('royal-23')
    UDP_PORT = 5000
    start_time = None

    # get host name and port from tracker.txt
    tracker = []
    with open('tracker.txt', 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        for row in reader:
            tracker.append(row)

    # sort the tracker by ID number to make it easier when looping thru the id_dict
    tracker_sorted = sorted(tracker, key=lambda x: int(x[1]))

    id_dict = OrderedDict() # ensure that IDs are added in ascending order

    for row in tracker_sorted:
        print(tracker_sorted[0])
        if row[0] == file_name:
            # found it in the table, populate the dict with info
            id_dict[row[1]] = {
                "host": row[2],
                "port": row[3],
                "data_size": row[4],
                "start_time": None,
                "end_time": None,
                "end_packet_received": False,
                "accumulated_payload": None
            }
    print(id_dict)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, port))

    for id in id_dict:
        # 1) send a request packet
        # 2) wait for data response
        # 3) when receiving an END packet, break out of while loop
        print(id)


    # send a request packet
    req_packet = create_request_packet(file_name)
    sock.sendto(req_packet, (send_ip, UDP_PORT))
    content = ''

    # OK to loop thru each host manually
    print(f"Listening on {UDP_IP}:{port}")
    while True:
        # wait for response
        data, addr = sock.recvfrom(1024)

        sender_ip = addr[0]
        sender_port = addr[1]

        if data[0] == ord('D'):
            if start_time == None:
                start_time = datetime.now()
            # data packet
            packet_type, seq_num, payload_length = struct.unpack('!cII', data[:9])
            seq_num = socket.ntohl(seq_num)  # convert back from network byte order
            payload_length = socket.ntohl(payload_length)
            payload = data[9:]  # The rest of the packet is the payload

            # convert payload to string
            payload_str = payload.decode('utf-8')
            content += payload_str

            # get curr time
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            first_4_bytes = payload[:4] if len(payload) >= 4 else payload

            print('DATA packet')
            print(f'send time: {formatted_time}')
            print(f'percentage received: IDK')
            print(f'requester address: {sender_ip}:{sender_port}')
            print(f'first 4 bytes: {first_4_bytes}\n')
        elif data[0] == ord('E'):
            # received end packet
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() * 1000
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
            print(f'requester address: {sender_ip}:{sender_port}')
            print(f'first 4 bytes: {first_4_bytes}\n')

            print('---------------------------------')
            print('summary')
            print(f'total packets: ')
            print(f'total data bytes: ')
            print(f'avg packets/second: ')
            print(f'duration of the test: {duration} ms')

            # check tracker dict to see if all end packets have been received
            # if yes, write to output file
            with open('output.txt', 'w') as f:
                f.write(content)
            # last packet received from this host, so break out of the loop
            break


