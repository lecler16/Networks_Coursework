Set-up:

- Open a terminal, make sure you are in the correct folder and run 'py server.py [port]', with the port number desired (I personally used port 8800).

- The server will now be set up on localhost, and will create a 'downloads' folder cointaining an example text file and an example image. To create the image, a python imaging library is imported. A new server.log file will also be created.

- Next split the terminal and run 'py client.py [username] [hostname] [port]', with hostname 'localhost' or '127.0.0.1', and the same port that was entered when starting the server. Repeat this process for as many clients as desired, using a different username for each new client.

- Whenever a new client connects, the server console should print out where the connection is coming from, and the new client's console should print a simple welcome message (along with some useful commands). If there are other clients, their consoles should print that the new client has joined: '[username] has joined!'.

Functions:

- Once connected, the client can input a message to broadcast to all other clients (this is the default form of messaging). In order to unicast a message to another client, the client wanting to send the message must start it with '/[username]', where the username is the username of the intended recipient. Both of these can be done as many times as the client desires.

- A client can request a list of files available to download from the downloads folder by starting their message with '/downloads'.

- To download a file from the downloads folder, a client must start their message with '/[file]', where [file] is the full name of the file as it appears when the list is requested (e.g. '/demofile.txt' would download the demo text file provided). Unfortunately only text (.txt) files can be downloaded. If a client attempts to download an image or video, a helpful error message will be displayed.

- To disconnect from the server the client can type '/exit' or simply close their terminal. All other client's consoles will print that the client has left: '[username] has left.'.

Log File:

- A log file, server.log, will be produced containing information relating to the connection and messaging functions and activities.
- The log file will be reset each new time the server is run.
- Currently there is an example of what the log file could look like.

References:

Richeal, P. (2024). katmfoo/python-client-server. [online] GitHub. Available at: https://github.com/katmfoo/python-client-server/tree/master [Accessed 1 Jan. 2024].
codezup (2020). Socket Server with Multiple Clients | Multithreading | Python. [online] Codez Up. Available at: https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/.
