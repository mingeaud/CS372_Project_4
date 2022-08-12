###############################################################################
#
#   Author: David Mingeaud
#   Class: CS372 - Summer 2022
#   Project 4: Client-Server Chat
#   File: client.py is one side of the chat app. This is to be
#   run with server.py
#
###############################################################################

import socket
import threading


class Client:

    def __init__(self):

        self.header = 64
        self.port = 5050
        self.format = 'utf-8'

        self.server = "127.0.0.1"
        self.addr = (self.server, self.port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)

        # This variable is to disconnect when a user send /q
        self.connected = True

        self.prompt_message = '>'

        # When a user enters '/q' the chat will end
        self.disconnect_message = '/q'

    def receive_message(self):
        """
        The receive thread listens for a message from the server and displays
        it.
        """

        # while still connected, keep running this loop, listening for messages
        while self.connected:

            # wait for a message.
            msg = self.client.recv(2048).decode(self.format)

            # if the other person sent the quit message, change the connection
            # flag to False and end the thread
            if msg == self.disconnect_message:
                print('\nConnection has been closed by the other person')
                print('Press Enter to close application')
                self.connected = False
                return
            else:
                print(msg, '\n>', end="")

    def send_message(self):
        """
        The send message thread waits for input from the user and sends the
        message to the server
        """

        # While the connected flag is True, keep waiting for input from the
        # user.
        while self.connected:

            # prompt the user for a message to send
            msg = input(self.prompt_message)
            message = msg.encode(self.format)
            msg_length = len(message)

            # this checks the connection again in case the other person
            # disconnected while waiting for input above
            if self.connected:
                # This method of sending the length of the message first so the
                # server will know how to parse it properly is from:
                # https://www.techwithtim.net/
                send_length = str(msg_length).encode(self.format)
                send_length += b' ' * (self.header - len(send_length))
                self.client.send(send_length)
                self.client.send(message)

            # if the message received is '/q', then change the connection flag
            # to false and exit the while loop, which ends the thread
            if msg == self.disconnect_message:
                self.connected = False

    def start_client(self):
        """
        The main part of the client file. This function creates two threads.
        One to wait for user input to send to the server. The other thread
        waits for a message received from the server.
        """

        print("Client is connected to", self.server, 'on port', self.port)
        print('Type /q to quit')
        print('Enter message to send...')

        # The idea for creating different threads for sending and receiving is
        # from https://www.techwithtim.net/
        listen_thread = threading.Thread(target=self.receive_message, args=())
        listen_thread.start()

        send_thread = threading.Thread(target=self.send_message, args=())
        send_thread.start()


if __name__ == '__main__':
    main_object = Client()
    main_object.start_client()
