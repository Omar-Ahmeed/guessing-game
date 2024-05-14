import random
from tkinter import *
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 55555
server.bind((host, port))
server.listen(5)
print(f"Server is listening on {host}:{port}")



CURRENT_WORD = ""
to_guess_word = "" 
clients = []
clients_names = []
clients_score = {}

def choose_word():
    global CURRENT_WORD
    global to_guess_word
    words = ["apple", "banana", "cherry", "date", "fig", "grape",
              "honeydew", "kiwi", "lemon", "mango", "orange",
                "raspberry", "strawberry", "vanilla", "watermelon",
                  "xigua", "yellow", "blackberry", "blueberry", "pineapple"]
    CURRENT_WORD = words[random.randint(0, len(words) - 1)]
    print(CURRENT_WORD)
    to_guess_word = guess_word(CURRENT_WORD)

def guess_word(word):
    word = word.lower()
    word = list(word)
    word = [i for i in word]
    word = " ".join(word)
    word = word.split(" ")
    word = [i for i in word]
    # make random letters in word to "_"
    for i in range(len(word)):
        if random.randint(0, 1) == 1:
            word[i] = "_"
    word = "".join(word)
    print(word)
    return word

    

def handle_client(client_socket, address):
    # send the current word to all clients
    broadcast(to_guess_word)
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(f"Received {message} from {clients_names[clients.index(client_socket)]}")
            # check if the message is the same as the current word
            if message.lower() == CURRENT_WORD:
                index = clients.index(client_socket)
                name = clients_names[index]
                print(f"{name} has guessed the word!")
                clients_score[name] += 1
                score = clients_score[name]
                print(f"Score: {clients_score}")
                for client in clients:
                    if client == client_socket:
                        client.send(f"Score : {score} ".encode()) 
                    else:
                        client.send(f"{name} has guessed the word! \n he is SMART! \n the word was {CURRENT_WORD}".encode())
                choose_word()
                broadcast(to_guess_word)
            elif message.lower() == "change word":
                for client in clients:
                    if client == client_socket:
                        client.send("You have requested to change the word! \n you are STUPID!".encode())
                    else:
                        client.send(f"{clients_names[clients.index(client_socket)]} has requested to change the word! \n he is STUPID!".encode())
                # broadcast(f"{clients_names[clients.index(client_socket)]} has requested to change the word! \n he is STUPID!")
                choose_word()
                broadcast(to_guess_word)
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            name = clients_names[index]
            broadcast(f"{name} has left the game!")
            clients_names.remove(name)
            clients_score.pop(name)
            print(f"{name} has left the game!")
            break



def broadcast(message):
    for client in clients:
        client.send(message.encode())

def recieve():
    while True:
        client, address = server.accept()

        client.send("Type your name: ".encode())
        name = client.recv(1024).decode()
        print(f"Name: {name}")

        clients_names.append(name)
        clients.append(client)
        # add the client name as a key and the score as a value
        clients_score[name] = 0
        print(f"Name: {name} has connected to the server! with address {address} \n {clients} \n {clients_names} \n {clients_score}")
        choose_word()
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

recieve()