# This code is built upon code from a github repository
# Richeal, P. (2024). katmfoo/python-client-server. [online] GitHub. Available at: https://github.com/katmfoo/python-client-server/tree/master [Accessed 1 Jan. 2024].

import socket
import sys
import threading
import logging
import os
# this may need to be downloaded if the code does not run.
from PIL import Image

# Set up logging
log_file = 'server.log'
if os.path.exists(log_file):
    os.remove(log_file)
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create downloads folder if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Create a text file in the downloads folder
text_file_path = os.path.join('downloads', 'demofile.txt')
with open(text_file_path, 'w') as f:
    f.write('This is a sample text file.')
    f.close()

# Create a simple image file in the downloads folder
image_size = (10, 10)
image = Image.new('1' , image_size, color=255)
image.save(os.path.join('downloads', 'example_image.png'))

# Variables for holding information about connections
connections = []
total_connections = 0

#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    def run(self):
        while self.signal:
            try:
                # Attempt to receive data from client.
                data = self.socket.recv(1024)
                decoded_data = data.decode('UTF-8')
            except:
                # If unable to, then assume client has disconnected and remove them from server data.
                logging.info('%s has disconnected', self.name)
                # send a message to all other clients notifying them that this client has disconnected.
                dc_message = str(self.name + " has disconnected.")
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(dc_message.encode('UTF-8'))
                self.signal = False
                connections.remove(self)
                break
            
            if data != "":
                unicasting = 0
                # If data received check for comands
                files = os.listdir('downloads')
                for file in files:
                    # allows client to request specific files to download
                    if decoded_data[(len(self.name)+2):((len(self.name)+3+len(file)))] == ('/'+file):
                        unicasting += 1
                        
                        # unfortunately could only get text files (.txt) to be sent using sockets
                        if file[-3:] == 'txt':
                            # sends indication that the following data sent is to be written to a .txt file.
                            check_message = 'Attempting to download '+ file
                            self.socket.sendall(check_message.encode('UTF-8'))
                            logging.info('%s requested to download %s"', self.name, file)
                            # read data from file and send it to the client.
                            file_path = os.path.join('downloads', file)
                            with open(file_path, 'r') as f:
                                file_data = f.read()
                                self.socket.sendall(file_data.encode("UTF-8"))
                                f.close()
                        else:
                            # if a file that isn't a txt file is requested for download, an error message is displayed.
                            apology_message = 'Apologies, but only .txt files can be downloaded at this time'
                            self.socket.sendall(apology_message.encode("UTF-8"))
                            logging.info('%s was unable to download %s"', self.name, file)

                # sends list of files in downloads folder to client
                if decoded_data[(len(self.name)+2):(len(self.name)+12)] == ('/downloads'):
                    for file in files:
                        self.socket.sendall(file.encode('UTF-8'))
                    logging.info('%s requested a list of files in the download folder"', self.name)
                    
                else:
                    # check for unicasting command
                    if unicasting == 0:
                        for client in connections:
                            if decoded_data[(len(self.name)+2):(len(self.name)+len(client.name)+3)] == ('/' + client.name):
                                # if unicasting command, send message only to intended recipient.
                                unicasting += 1
                                client.socket.sendall(data)
                                logging.info('%s unicast a message to %s: "%s"', self.name, client.name, decoded_data)
                    # If no command, broadcast message to everyone other than the sender.
                    if unicasting == 0:
                        for client in connections:
                            if client.id != self.id:
                                client.socket.sendall(data)
                        logging.info('%s broadcast a message to everyone: "%s"', self.name, decoded_data)


# Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        try:
            # Receive the username from the client
            client_username = sock.recv(1024).decode('UTF-8')
        except ValueError:
            logging.error('Client did not send a valid username')
            print('Client did not send a valid username')
            return    
        # adding client to list of clients
        connections.append(Client(sock, address, total_connections, client_username, True))
        connections[len(connections) - 1].start()

        # on the server console, print where the connection is coming from.
        print("New connection from", address)
        logging.info('New connection, %s, from %s', client_username, address)

        # send welcome message to client
        welcome_message = str('Welcome, ' + client_username + '.')
        connections[-1].socket.sendall(welcome_message.encode('UTF-8'))

        # send joining message to all other clients
        joining_message = str(client_username + " has joined!")
        for i in range(len(connections)-1):
            connections[i].socket.sendall(joining_message.encode('UTF-8'))
        total_connections += 1

def main():
    # reading server address
    server_address = ('127.0.0.1', int(sys.argv[1]))
    print('starting up on {} port {}'.format(*server_address))
    logging.info('Starting up on %s port %s', *server_address)
    print ('Awaiting first connection')

    # Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((server_address))
    sock.listen()

    # Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()

main()