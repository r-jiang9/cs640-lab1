import socket
import argparse
import struct

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
        # sock.sendto(data, addr)  # Echo back the received message

