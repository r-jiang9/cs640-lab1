import argparse
import socket

if __name__ == "__main__":
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
    
    port = args.port
    req_port = args.requester_port
    if not (2049 < port < 65536 and 2049 < req_port < 65536):
        raise Exception('ports should be in the range 2049 < port < 65536')

    print(port, req_port)

# Each sender will have a copy of the file parts that it is responsible for in the same folder as it is running from, so that it can access them directly. The sender should be invoked in the following way:

#  python3 sender.py -p <port> -g <requester port> -r <rate> -q <seq_no> -l <length>

# port is the port on which the sender waits for requests,
# requester port is the port on which the requester is waiting,
# rate is the number of packets to be sent per second,
# seq_no is the initial sequence of the packet exchange,
# length is the length of the payload (in bytes) in the packets.

# Moreover, in case a wrong input is entered (e.g., string instead of number) your program should print an error explaining the mistake and exit.