class Packet:
    def __init__(self, packet_type, seq_num, length, payload):
        # valid packet types: R, D, E
        if(packet_type != 'R' or 'D' or 'E'):
            raise Exception("Not a valid packet type")
        self.packet_type = packet_type
        self.seq_num = seq_num
        self.length = length
        self.payload = payload