# guessing-game
This Python script implements a simple guessing game server using sockets and threading. It allows multiple clients to connect and compete to guess a randomly chosen word.

Features:
Server listens for client connections.
Clients send their names upon connection.
Server assigns a score to each connected client.
Server broadcasts the current word (with some letters hidden) to all clients.
Clients send guesses to the server.
Server checks guesses and updates scores accordingly.
Server broadcasts messages when a client guesses the word or requests a change.
Server gracefully handles client disconnections.

Requirements:
Python 3.x
socket library
threading library

How to Run:
1- Open a terminal window and navigate to the directory where you saved the script.
Run the server using the command:
python server.py

2- On a separate machine or terminal window on the same machine, run the client using the command:
python client.py

3- Enter your name when prompted by the client.



