import socket
import argparse
import struct
import csv
from datetime import datetime
import time
from collections import OrderedDict

def create_request_packet(file_name):
    udp_header = struct.pack('!cII', bytes('R', 'utf-8'), socket.htonl(0), socket.htonl(0))
    payload = bytes(file_name, 'utf-8')
    packet = udp_header + payload
    return packet

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=True, help='Port number, required')
    parser.add_argument('-o', '--file', type=str, required=True, help='The name of the file being requested')

    args = parser.parse_args()
    file_name = args.file

    HOST_IP = (socket.gethostbyname(socket.gethostname()))
    PORT = args.port

    send_ip = socket.gethostbyname('snares-09')
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
        if row[0] == file_name:
            # found the file in the table, populate the dict with info
            id_dict[row[1]] = {
                "host": row[2],
                "port": row[3],
                "data_size": int(row[4][:-1]), # remove the B at the end
                "start_time": None,
                "end_time": None,
            }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST_IP, PORT))

    for id in id_dict:
        send_ip = socket.gethostbyname(id_dict[id]["host"])
        send_port = int(id_dict[id]["port"])
        # 1) send a request packet
        running_total = 0
        num_packets = 0
        req_packet = create_request_packet(file_name)
        sock.sendto(req_packet, (send_ip, send_port))
        
        # 2) wait for data response'
        start_time = time.perf_counter()

        while True:
            data, addr = sock.recvfrom(1024)

            sender_ip = addr[0]
            sender_port = addr[1]

            if data[0] == ord('D'):
                #if start_time == None:
                    # first data packet received
                    #start_time = datetime.now()
                num_packets += 1
                content = ''
                # data packet
                packet_type, seq_num, payload_length = struct.unpack('!cII', data[:9])
                seq_num = socket.ntohl(seq_num)  # convert back from network byte order
                payload_length = socket.ntohl(payload_length)
                payload = data[9:]  # the rest of the packet is the payload

                # convert payload to string
                payload_str = payload.decode('utf-8')
                content += payload_str

                # get curr time
                current_time = datetime.now()
                formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                first_4_bytes = payload[:4] if len(payload) >= 4 else payload

                running_total += len(payload)
                print('DATA packet')
                print(f'send time: {formatted_time}')
                print(f'sender address: {sender_ip}:{sender_port}')
                print(f'packet sequence number: {seq_num}')
                print(f"payload length (in bytes): {len(payload)}")
                print(f'percentage received: {running_total/id_dict[id]["data_size"] * 100:.2f}%')
                print(f'first 4 bytes: {first_4_bytes.decode("utf-8")}\n')

                with open(file_name, 'a') as f:
                    f.write(content)
            elif data[0] == ord('E'):
                # received end packet
                end_time = time.perf_counter()
                # num_packets += 1

                duration = (end_time - start_time) * 1000 # calculated in ms
                packet_type, seq_num, payload_length = struct.unpack('!cII', data[:9])
                seq_num = socket.ntohl(seq_num)  # Convert back from network byte order
                payload_length = socket.ntohl(payload_length)
                payload = data[9:]  # The rest of the packet is the payload

                # get curr time
                current_time = datetime.now()
                formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                first_4_bytes = payload[:4] if len(payload) >= 4 else payload

                print("END Packet")
                print(f'send time: {formatted_time}')
                print(f'sender address: {sender_ip}:{sender_port}')
                print(f'sequence number: {seq_num}')
                print(f'payload length (in bytes): {len(payload)}')
                print(f'first 4 bytes: {first_4_bytes.decode("utf-8")}\n')

                print(f'Summary:')
                print(f'sender address: {sender_ip}:{sender_port}')
                print(f'total data packets received: {num_packets}')
                print(f'total data bytes received: {running_total}')
                print(f'avg packets/second: {num_packets / (duration / 1000)} ')
                print(f'duration of the test: {duration} ms')
                print('---------------------------------')

                # last packet received from this host, so continue to the next request if needed
                break
    # done looping thru all ids, exit
    exit(0)
