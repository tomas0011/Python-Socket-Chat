import socket   
import threading

host = '127.0.0.1'
port = 33334

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Servidor de chat corriendo en {host}:{port}")


clients = []
usernames = []

def emisorDeMensajes(message, _client):
  for client in clients:
    if client != _client:
      client.send(message)

def receptorDeMensajes(client):
  while True:
    try:
      message = client.recv(1024)
      emisorDeMensajes(message, client)
    except:
      index = clients.index(client)
      username = usernames[index]
      emisorDeMensajes(f"ChatBot: {username} disconnected".encode('utf-8'), client)
      clients.remove(client)
      usernames.remove(username)
      client.close()
      break


def receptorDeConexiones():
  while True:
    client, address = server.accept()

    client.send("@username".encode("utf-8"))
    username = client.recv(1024).decode('utf-8')

    clients.append(client)
    usernames.append(username)

    print(f"{username} se conecto desde {str(address)}")

    message = f"{username} entro al chat!".encode("utf-8")
    emisorDeMensajes(message, client)
    client.send("Conectado al servidor de chat".encode("utf-8"))

    thread = threading.Thread(target=receptorDeMensajes, args=(client,))
    thread.start()

receptorDeConexiones()
