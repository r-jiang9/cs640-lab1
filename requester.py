import argparse
import socket

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='sum the integers at the command line')
    parser.add_argument('-p', '--port', type=int, required=True, help='Port number, required')
    parser.add_argument('-o', '--file', type=str, required=True, help='The name of the file being requested')

    args = parser.parse_args()
    print("Argument Values")
    for arg in vars(args):
        print(f'{arg}: {getattr(args, arg)}, {type(getattr(args, arg))}')
    port = args.port
    if not (2049 < port < 65536):
        raise Exception('port should be in the range 2049 < port < 65536')
    UDP_IP = '127.0.0.1'
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT)) 

    while True:
        data, addr = sock.recvfrom(1024) # pass buffer size
        print(f"received message: {data}")


# The requester is invoked in the following way.

#  python3 requester.py -p <port> -o <file option>

# port is the port on which the requester waits for packets,
# file option is the name of the file that is being requested.
# The requester must print the following information for each packet that it receives, with each packet's information in a separate line:

# The time at which the packet was received in millisecond granularity,
# Sender's IP address (in decimal-dot notation) and sender’s port number,
# The packet sequence number,
# The payload's length (in bytes)
# (DATA packets only) The percentage of the data received (round to two decimal places), and
# the first 4 bytes of the payload.
# After the END packet is received, it should print the following summary information about the test separately for "each" sender:

# Sender's IP address (in decimal-dot notation) and sender’s port number,
# Total data packets received,
# Total data bytes received (which should add up to the file part size),
# Average packets/second, and
# Duration of the test. This duration should start with the first data packet received from that sender and end with the END packet from it.
# The requester also should write the chunks that it receives to a file with the same file name as it requested. This new file will be compared with the actual file that was sent out.

# Moreover, in case a wrong input is entered (e.g., string instead of number) your program should print an error explaining the mistake and exit.