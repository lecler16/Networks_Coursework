# This code is built upon code from a github repository
# Richeal, P. (2024). katmfoo/python-client-server. [online] GitHub. Available at: https://github.com/katmfoo/python-client-server/tree/master [Accessed 1 Jan. 2024].

import socket
import threading
import sys
import os


# Wait for incoming data from server
# If cannnot receive data then output disconnect message
def receive(socket, signal):
    # add variable to determine whether or not to print message received or to put into file
    downloading = 0
    while signal:
        try:
            # receive data from server
            data = socket.recv(1024)
            decoded_data = str(data.decode("UTF-8"))
            if downloading == 0:
                # this means that 
                print(decoded_data)
            elif downloading == 1:
                # The server has sent a message indicating that the next data that is sent is for a .txt file
                # Create a text file in a folder named by the client's username
                file_path = os.path.join(client_username, decoded_data[22:])
                # write the incoming data to the file
                with open(file_path, 'w') as f:
                    f.write(decoded_data)
                    f.close()
                downloading = 0
        except:
            # if cannot recieve data then assume disconnected from server
            print("You have been disconnected from the server")
            signal = False
            break
        
        # check if the next message will need to be stored in a file.
        if decoded_data[:22] == 'Attempting to download':
            # make folder named by username of client to store downloaded files, if it does not already exist.
            if not os.path.exists(client_username):
                os.makedirs(client_username)
            # tell the program that the next data that is received from the server is intended for a .txt file
            downloading = 1

#Get host and port
server_address = (sys.argv[2], int(sys.argv[3]))

#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

# Get client username and send it to the server
client_username = sys.argv[1]
print('--Your client username is {}.'.format(client_username))
sock.sendall(client_username.encode('UTF-8'))



#Create new thread to wait for data
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()

# Print helpful commands for client 
print("--Type to broadcast a message")
print("--Begin your message with /[name] to unicast a message to a user with that name.")
print("--To view a list of the files available to be downloaded type /downloads")
print("--To download a text file, type '/[filename].txt'")
print("--To disconnect from the server, type '/exit'")

#Send message data to server
while True:
    message = client_username + ': ' + input()
    # check if client is attempting to disconnect 
    # There is no need to send data to server in this case - it will sense the signal is lost and infer that the client has disconnected
    if message.lower() != str(client_username + ': ' + '/exit'):
        sock.sendall(str.encode(message))
    else:
        sock.close()
        break