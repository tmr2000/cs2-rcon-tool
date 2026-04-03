# https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
import socket
import struct
import os
from dotenv import load_dotenv
load_dotenv()  # loads variables from .env

class CS2RCON:

    def __init__(self):
        self.request_id_counter = 0
        self.password = os.getenv("CS2_PASSWORD")
        self.port = int(os.getenv("CS2_PORT"))
        self.server = os.getenv("CS2_SERVER")
        self.DEBUG = False

    def next_request_id(self): # incraments request_id_counter - each packet should be unqique per RCON session
        self.request_id_counter += 1
        if self.DEBUG:
            print (f"[DEBUG] Request ID: {self.request_id_counter}")
        return self.request_id_counter

    def build_login_packet(self, request_id): # build login RCON packet
        payload_bytes = self.password.encode('utf-8') + b'\x00\x00' # payload + 2 null bytes
        packet_size = 4 + 4 + len(payload_bytes) # request_id length (ALWAYS 4 BYTES) + type length (ALWAYS 4 BYTES) + payload length (VARIABLE DUE TO PASSWORD LENGTH)
        packet = struct.pack('<iii', packet_size, request_id, 3) + payload_bytes # 3 is type ID for login - SERVERDATA_AUTH
        if self.DEBUG:
            print (f"[DEBUG] Login Packet: {packet}")
        return packet

    def build_command_packet(self, request_id, command):
        payload_bytes = command.encode('utf-8') + b'\x00\x00'  # command + 2 null bytes
        packet_size = 4 + 4 + len(payload_bytes)  # 4 bytes for request_id, 4 for type, rest for payload
        packet = struct.pack('<iii', packet_size, request_id, 2) + payload_bytes  # type 2 = command
        if self.DEBUG:
            print(f"[DEBUG] Command Packet: {packet}")
        return packet

    def receive_all(self, n): # recieves n bytes from the socket
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Connection closed before receiving full data")
            data += chunk
        if self.DEBUG:
            print(f"[DEBUG] Received {len(data)} bytes")
        return data

    def read_rcon_packet(self): # read full RCON packet
        size_data = self.receive_all(4) # get first 4 bytes
        packet_size = struct.unpack('<i', size_data)[0] # get length of rest of packet
        packet_data = self.receive_all(packet_size) # read rest of packet
        response_id, response_type = struct.unpack('<ii', packet_data[:8]) # get request ID and and request type (int)
        payload = packet_data[8:-2].decode('utf-8') # get payload (minus end 2 bytes) (str)
        if self.DEBUG:
            print(f"[DEBUG] Packet received - ID: {response_id}, Type: {response_type}, Payload length: {len(payload)}")
        return response_id, response_type, payload

    def connect_and_login(self): # initial connect and login to server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        self.sock.connect((self.server, self.port))
        print(f"Connected to server: {self.server}:{self.port}")
        self.sock.sendall(self.build_login_packet(self.next_request_id())) #
        response_id, response_type, payload = self.read_rcon_packet()
        if response_id == -1:
            if self.DEBUG:
                print (f"[DEBUG] Login Response ID: {response_id}")
            print("Login failed \n")
            self.sock.close()
            return False
        else:
            if self.DEBUG:
                print (f"[DEBUG] Login Response ID: {response_id}")
            print("Login successful \n")
            return True

    def send_rcon_command (self, command): # send rcon command to server, and return with full response
        command_id = self.next_request_id()
        self.sock.sendall(self.build_command_packet(command_id, command)) # send command
        end_id = self.next_request_id()
        self.sock.sendall(self.build_command_packet(end_id, "")) # send blank packet, to capture any overflow from command response - detailed on wiki
        full_response = ""
        while True: # loop reading packets forever until empty packet recieved (end of message)
            response_id, response_type, response = self.read_rcon_packet()
            if self.DEBUG:
                print(f"[DEBUG] ID: {response_id}, Type: {response_type}, Response:\n{response.strip()}")
            if response_id == end_id:
                break
            if response_id not in (command_id, end_id):
                continue
            if response_id == command_id:
                full_response += response
        return full_response.strip()
