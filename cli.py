import socket
from cs2rcon import CS2RCON

rcon = CS2RCON()
if not rcon.connect_and_login():
    quit()
while True: # running loop
    try:
        command = input("CS2 RCON> ").strip()
        if not command: # if empty command, don't send to server
            continue
        if command.lower() in ["exit", "quit"]: # exit shell command
            print("Closing connection")
            break
        response = rcon.send_rcon_command(command)
        if not rcon.DEBUG:
            print (response)
    except (socket.timeout, ConnectionError, BrokenPipeError): #Handles timeout's / connection loss - attempts reconnect
        print("Connection lost. Reconnecting...")
        rcon.sock.close()
        if not rcon.connect_and_login():
            break
    except KeyboardInterrupt: # Press CTRL+C in Python
        print("\nClosing connection")
        break
rcon.sock.close()