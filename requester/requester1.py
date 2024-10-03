import argparse
import socket
import struct
import csv

def create_request_packet(packet_type, file_name):
    udp_header = struct.pack('!cII', bytes(packet_type, 'utf-8'), socket.htonl(0), 0)
    payload = bytes(file_name, 'utf-8')
    packet = udp_header + payload
    return packet

if __name__ == "__main__":
    #  python3 requester.py -p <port> -o <file option>
    # port is the port on which the requester waits for packets,
    # file option is the name of the file that is being requested.
    # The requester must print the following information for each packet that it receives, with each packet's information in a separate line:

    parser = argparse.ArgumentParser(
            description='sum the integers at the command line')
    parser.add_argument('-p', '--port', type=int, required=True, help='Port number, required')
    parser.add_argument('-o', '--file', type=str, required=True, help='The name of the file being requested')

    args = parser.parse_args()
    
    port = args.port
    file_name = args.file

    if not (2049 < port < 65536):
        raise Exception('port should be in the range 2049 < port < 65536')

    # read contents of tracker.txt
    tracker = []
    with open("tracker.txt") as file:
        reader = csv.reader(file, delimiter = ' ')
        for row in reader:
            tracker.append(row)
            print(row)
    
    # tracker_info = { }
    # for row in tracker:
    #     if row[0] == file_name:
    #         tracker_info[row[1]] = row # get relevant rows from tracker that have our file
    # print(tracker_info)

    # for key in tracker_info.keys():
    #     port = int(tracker_info[key][3])
    #     host = tracker_info[key][2]
    #     ip_address = socket.gethostbyname(host)
    #     # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     print(key, host, port, ip_address)
    #     # sock.bind((ip_address, port)) 
    #     # extract the port, host name, file name
    #     pass

    # translate host name to IP address format
    socket.gethostbyname('mumble-01')
    # construct a request packet, total 9 bytes
    # 1 byte: packet type (char)
    # 4 bytes: sequence num (uint)
    # 4 bytes: length (uint)

    udp_header = struct.pack('!cII', b'R', 0, 0)
    payload = bytes(file_name, 'utf-8') # cast filename to bytes
    payload_with_header = udp_header + payload
    UDP_IP = socket.gethostbyname("royal-06") # TODO: currently hardcoding. alt way?

    print(UDP_IP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port)) 

    # sender_port = 5005
    sender_addr = (UDP_IP, 7)
    sock.sendto(payload_with_header, sender_addr)
    sock.settimeout(5)  # Set a 5-second timeout
    try:
        data, addr = sock.recvfrom(1024)
        print(f"Received message: {data}")
    except socket.timeout:
        print("No response received, timed out.")

    UDP_IP = socket.gethostbyname("royal-06")  # Replace with the target hostname
    UDP_PORT = 7
    MESSAGE = b"Hello, Echo!"

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Set timeout to 5 seconds

    try:
        print(f"Sending message to {UDP_IP}:{UDP_PORT}")
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

        # Wait for echo reply
        data, addr = sock.recvfrom(1024)  # Buffer size 1024 bytes
        print(f"Received echo: {data}")
    except socket.timeout:
        print("No response, Echo service might not be available.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        sock.close()


# The requester is invoked in the following way.

#  python3 requester.py -p <port> -o <file option>

# port is the port on which the requester waits for packets,
# file option is the name of the file that is being requested.
# The requester must print the following information for each packet that it receives, with each packet's information in a separate line:
