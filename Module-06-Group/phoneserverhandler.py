"""
File: phoneserverhandler.py
Project 10.10
Client handler for chatroom. Receives ThreadSafeTranscript object from
the server, handles requests from client.
"""
from codecs import decode
from threading import Thread
import re

BUFSIZE = 1024
CODE = "ascii"


class PhoneServerHandler(Thread):

    """Handles phone server requests from a client."""
    def __init__(self, client):
        """Save references to the client socket and shared transcript."""
        Thread.__init__(self)
        self.client = client

    def run(self):
        """Obtains name from the client, then enters
        an interative loop to take and respond to
        requests."""
        # Establish the client's name.
        self.name = decode(self.client.recv(BUFSIZE), CODE)
        if not self.name:
            print("Client disconnected")
            self.client.close()
        else:
            print(self.name, "is connected")
            # respond to client with menu options
            options = " 1. Print Phone Numbers \n 2. Add a Phone Number \n " \
                      "3. Remove a Phone Number \n " \
                      "4. Lookup a Phone Number \n " \
                      "5. Quit \n" \
                      "Type in a number (1-5): "
            self.client.send(bytes(str(options), CODE))

            # load phone book in initially
            phoneBook = {}
            with open("phoneBooks.txt", 'r') as f:
                for line in f:
                    items = line.split()
                    key, values = items[0], items[1:]
                    phoneBook[key] = values
            print(phoneBook)

            while True:
                menu_choice = int(decode(self.client.recv(BUFSIZE), CODE))
                # menu handling for phone book
                if menu_choice == 1:
                    # update phone book
                    phoneBook = {}
                    with open("phoneBooks.txt", 'r') as f:
                        for line in f:
                            items = line.split()
                            key, values = items[0], items[1:]
                            phoneBook[key] = values
                    print(phoneBook)
                    self.client.send(bytes(str(phoneBook), CODE))
                elif menu_choice == 2:
                    self.client.send(bytes(str("Input Name:"), CODE))
                    key = decode(self.client.recv(BUFSIZE), CODE)
                    self.client.send(bytes(str("Input Number:"), CODE))
                    values = decode(self.client.recv(BUFSIZE), CODE)
                    with open("phoneBooks.txt", 'a') as f:
                        f.write('\n'), f.write(key.strip('\n')), f.write(' '), f.write(values.strip('\n')), f.close()
                    self.client.send(bytes(str("Name Added."), CODE))
                elif menu_choice == 3:
                    self.client.send(bytes(str("Enter name to be deleted below "), CODE))
                    name = str(decode(self.client.recv(BUFSIZE), CODE))
                    if name.strip('\n') in phoneBook:
                        phoneBook.pop(name.strip('\n'))
                        print(phoneBook)
                        with open("phoneBooks.txt", 'w') as f:
                            for key in phoneBook:
                                f.write(key), f.write(" "), f.write(str(re.sub('[^A-Za-z0-9]+', '', str(values))).strip('*')), f.write('\n')
                        self.client.send(bytes(str("Entry Deleted."), CODE))
                    else:
                        self.client.send(bytes(str("Name not found."), CODE))
                elif menu_choice == 4:
                    self.client.send(bytes(str("Enter desired name below. "), CODE))
                    name = str(decode(self.client.recv(BUFSIZE), CODE))
                    searchfile = open("phoneBooks.txt", "r")
                    find = False
                    found = ''
                    for line in searchfile:
                        if name.strip('\n') in line:
                            found = str(line)
                            find = True
                    if find is True:
                        self.client.send(bytes(str(found), CODE))
                    else:
                        self.client.send(bytes(str("Name not found."), CODE))
                    searchfile.close()
                elif menu_choice != 5:
                    self.client.close()


