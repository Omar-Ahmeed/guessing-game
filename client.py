import socket
import threading
import tkinter as tk
from tkinter import messagebox


HOST = "127.0.0.1"  # Server IP address
PORT = 55555        # Server port

def send_guess():
    guess = entry_guess.get().strip()
    if guess:
        client_socket.send(guess.encode())
        entry_guess.delete(0, tk.END)

def change_word():
    client_socket.send("Change Word".encode())

def update_word(word):
    label_word.config(text=word)
    print("Word updated to:", word)

def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            print("Received data:", data)
            if data:
                if data.startswith("Type your name: "):
                    name = entry_guess.get().strip()
                    client_socket.send(name.encode())
                elif len(data) > 10:
                    # create message Box to show the the message 
                    messagebox.showinfo("Message", data)
                elif data.startswith("Score :"):
                    label_Score.config(text=data)
                else:
                    update_word(data)

        except ConnectionAbortedError:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

root = tk.Tk()
root.title("Word Guessing Game")
root.geometry("400x400")
root.resizable(False, False)

# window color hex code
root.configure(bg="#E6FF94")

label_word = tk.Label(root, text="ENTER YOUR NAME", font=("Bahnschrift", 20), bg="#006769", fg="#FFD662")
label_word.pack(pady=20)

entry_guess = tk.Entry(root, font=("Arial", 16))
entry_guess.pack(pady=10)

btn_send = tk.Button(root, text="Send", font=("Arial", 16), command=send_guess)
btn_send.pack(pady=10)

root.bind("<Return>", lambda event: send_guess())


btn_change_word = tk.Button(root, text="Change Word", font=("Arial", 16), command=change_word)
btn_change_word.pack(pady=10)

label_Score = tk.Label(root, text="Score: 0", font=("Bahnschrift", 20), bg="#006769", fg="#FFD662")
label_Score.pack(pady=20)

# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# end session when the window is closed
def on_closing():
    client_socket.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()
