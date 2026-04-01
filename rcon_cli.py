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
DEBUG = True

def next_request_id(): # incraments request_id_counter - each packet should be unqique per RCON session
    global request_id_counter #use global to change previously made variable outside of this function
    request_id_counter += 1
    if DEBUG:
        print (f"[DEBUG] Request ID: {request_id_counter}")
    return request_id_counter

def build_login_packet(request_id, password): # build login RCON packet
    payload_bytes = password.encode('utf-8') + b'\x00\x00' # payload + 2 null bytes
    packet_size = 4 + 4 + len(payload_bytes) # request_id length (ALWAYS 4 BYTES) + type length (ALWAYS 4 BYTES) + payload length (VARIABLE DUE TO PASSWORD LENGTH)
    packet = struct.pack('<iii', packet_size, request_id, 3) + payload_bytes # 3 is type ID for login - SERVERDATA_AUTH
    if DEBUG:
        print (f"[DEBUG] Login Packet: {packet}")
    return packet

def build_command_packet(request_id, command): # build command RCON packet
    payload_bytes = command.encode('utf-8') + b'\x00\x00' # payload + 2 null bytes
    packet_size = 4 + 4 + len(payload_bytes) # request_id length (ALWAYS 4 BYTES) + type length (ALWAYS 4 BYTES) + payload length (VARIABLE DUE TO PASSWORD LENGTH)
    packet = struct.pack('<iii', packet_size, request_id, 2) + payload_bytes # 2 is type ID for send command - SERVERDATA_EXECCOMMAND
    if DEBUG:
        print (f"[DEBUG] Command Packet: {packet}")
    return packet

def receive_all(sock, n): # recieves n bytes from the socket
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

def connect_and_login(): # initial connect and login to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((cs2_server, cs2_server_port))
    print("Connected to server", cs2_server)
    sock.sendall(build_login_packet(next_request_id(), cs2_server_password)) #
    response_id, response_type, payload = read_rcon_packet(sock)
    if response_id == -1:
        if DEBUG:
            print (f"[DEBUG] Login Response ID: {response_id}")
        print("Login failed \n")
        sock.close()
        return None
    else:
        if DEBUG:
            print (f"[DEBUG] Login Response ID: {response_id}")
        print("Login successful \n")
        return sock

def send_rcon_command (sock, command): # send rcon command to server, and return with full response
    
    command_id = next_request_id()
    sock.sendall(build_command_packet(command_id, command)) # send command

    end_id = next_request_id()
    sock.sendall(build_command_packet(end_id, "")) # send blank packet, to capture any overflow from command response - detailed on wiki
    
    full_response = ""

    while True: # loop reading packets forever until empty packet recieved (end of message)
        response_id, response_type, response = read_rcon_packet(sock)

        if DEBUG:
            print(f"[DEBUG] ID: {response_id}, Type: {response_type}, Response:\n{response.strip()}")

        if response_id == end_id:
            break

        if response_id not in (command_id, end_id):
            continue

        if response_id == command_id:
            full_response += response

    return full_response.strip()

sock = connect_and_login()
if not sock:
    quit()

while True: # running loop
    try:
        command = input("CS2 RCON> ").strip()

        if not command: # if empty command, don't send to server
            continue

        if command.lower() in ["exit", "quit"]: # exit shell command
            print("Closing connection")
            break

        response = send_rcon_command(sock, command)
        if not DEBUG:
            print (response)

    except (socket.timeout, ConnectionError, BrokenPipeError): #Handles timeout's / connection loss - attempts reconnect
        print("Connection lost. Reconnecting...")
        sock.close()
        sock = connect_and_login()
        if not sock:
            break

    except KeyboardInterrupt: # Press CTRL+C in Python
        print("\nClosing connection")
        break

sock.close()