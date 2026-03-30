# https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
import socket
import struct
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env
cs2_server = os.getenv("CS2_SERVER")
cs2_server_port = int(os.getenv("CS2_PORT"))
cs2_server_password = os.getenv("CS2_PASSWORD")
request_id_counter = 0

def next_request_id(): #incraments request_id_counter - each packet should be unqique per RCON session
    global request_id_counter #use global to change previously made variable outside of this function
    request_id_counter += 1
    return request_id_counter

def build_login_packet(request_id, password): # build login RCON packet
    payload_bytes = password.encode('utf-8') + b'\x00\x00' # payload + 2 null bytes
    packet_size = 4 + 4 + len(payload_bytes) # request_id length (ALWAYS 4 BYTES) + type length (ALWAYS 4 BYTES) + payload length (VARIABLE DUE TO PASSWORD LENGTH)
    packet = struct.pack('<iii', packet_size, request_id, 3) + payload_bytes # 3 is type ID for login - SERVERDATA_AUTH
    return packet

def build_command_packet(request_id, command): # build command RCON packet
    payload_bytes = command.encode('utf-8') + b'\x00\x00' # payload + 2 null bytes
    packet_size = 4 + 4 + len(payload_bytes) # request_id length (ALWAYS 4 BYTES) + type length (ALWAYS 4 BYTES) + payload length (VARIABLE DUE TO PASSWORD LENGTH)
    packet = struct.pack('<iii', packet_size, request_id, 2) + payload_bytes # 2 is type ID for send command - SERVERDATA_EXECCOMMAND
    return packet

def receive_all(sock, n): #recieves n bytes from the socket
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed before receiving full data")
        data += chunk
    return data

def read_rcon_packet(sock): # read full RCON packet
    size_data = receive_all(sock, 4) # get first 4 bytes
    packet_size = struct.unpack('<i', size_data)[0] # get length of rest of packet
    packet_data = receive_all(sock, packet_size) # read rest of packet
    response_id, response_type = struct.unpack('<ii', packet_data[:8]) # get request ID and and request type (int)
    payload = packet_data[8:-2].decode('utf-8') # get payload (minus end 2 bytes) (str)
    return response_id, response_type, payload

def connect_and_login(): #Initial connect and login to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((cs2_server, cs2_server_port))
    print("Connected to server", cs2_server)
    sock.sendall(build_login_packet(next_request_id(), cs2_server_password)) #
    response_id, response_type, payload = read_rcon_packet(sock)
    if response_id == -1:
        print("Login failed \n")
        sock.close()
        return None
    else:
        print("Login successful \n")
        return sock

sock = connect_and_login()
if not sock:
    quit()

while True:
    command = input("RCON> ")

    if command.lower() in ["exit", "quit"]:
        print("Closing connection.")
        break

    sock.sendall(build_command_packet(next_request_id(), command))
    response_id, response_type, payload = read_rcon_packet(sock)

    print(payload)

sock.close()


