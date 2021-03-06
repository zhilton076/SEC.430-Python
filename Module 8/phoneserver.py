"""
File: phoneserver.py
Created By: Zack Hilton, Austin Cloutier
Project 10.10
Server for providing phonebook access.
Uses client handlers to handle clients' requests.
"""
from socket import *
from phoneserverhandler import PhoneServerHandler

# Creates tcp/ip socket
server = socket(AF_INET, SOCK_STREAM)

# bind the address to the socket
HOST = "localhost"
PORT = 5000
ADDRESS = (HOST, PORT)
try:
    server.bind(ADDRESS)
except error:
    PORT += 1
    ADDRESS = (HOST, PORT)
    server.bind(ADDRESS)

# put socket into listen mode
server.listen(5)

while True:
    print("Waiting for connection . . .")
    client, address = server.accept()
    print("... connected from: ", address, PORT)
    handler = PhoneServerHandler(client)
    handler.start()





