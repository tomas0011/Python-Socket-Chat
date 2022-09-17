import socket   
import threading


host = '127.0.0.1'
port = 33334

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")


clients = []
usernames = []

def messageSender(message, _client):
  for client in clients:
    if client != _client:
      client.send(message)

def handle_messages(client):
  while True:
    try:
      message = client.recv(1024)
      messageSender(message, client)
    except:
      index = clients.index(client)
      username = usernames[index]
      messageSender(f"ChatBot: {username} disconnected".encode('utf-8'), client)
      clients.remove(client)
      usernames.remove(username)
      client.close()
      break


def receive_connections():
  while True:
    client, address = server.accept()

    client.send("@username".encode("utf-8"))
    username = client.recv(1024).decode('utf-8')

    clients.append(client)
    usernames.append(username)

    print(f"{username} se conecto desde {str(address)}")

    message = f"{username} entro al chat!".encode("utf-8")
    messageSender(message, client)
    client.send("Conectado al servidor de chat".encode("utf-8"))

    thread = threading.Thread(target=handle_messages, args=(client,))
    thread.start()

receive_connections()
