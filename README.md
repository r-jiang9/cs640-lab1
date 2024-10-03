
**Packet type**

Valid values for packet type are:

- 'R' (uppercase R), meaning Request packet
- 'D' (uppercase D), meaning DATA packet
- 'E' (uppercase E), meaning END packet

**Sequence number**

The sequence number is unsigned and must be converted to network byte order while being placed in the packet. Please see Socket DocumentationLinks to an external site.  to find information on using socket.htonl() and socket.ntohl() for conversion from network byte order to host byte order and vice versa.
For the sender, the sequence number can start at any arbitrary value, as specified by the user in the parameters. The sequence value should increment with the number of "payload" bytes sent during a test. It should not include the 9 bytes required for the header in the packet layout shown above.
For Request packets, the sequence field is set to 0.

**Length**

The length field is unsigned and specifies the number of bytes carried in the "payload" of the packet.
In case the packet type is a request, the packet length should be set to 0.

**Payload**

The payload data is chunks from the file that the requester has requested. The sender chunks the file part that it has to payloads of the size that is identified by the length field in its parameters (see below) and sends them to the requester. The last chunk can be of the size less than the length parameter based on how many bytes are left in the file.
There is no limit on the max size of the payload length.
The requester fills the payload field with the name of the file that it is requesting.

```
python3 sender.py -p 5000 -g 5001 -r 1 -q 100 -l 100

python3 requester.py -p 5001 -o split1.txt
```