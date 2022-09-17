import socket   
import threading

username = input("Ingresa tu nombre de usuario: ")

host = '8.tcp.ngrok.io'
port = 19768

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receptorDeMensajes():
  while True:
    try:
      message = client.recv(1024).decode('utf-8')

      if message == "@username":
        client.send(username.encode("utf-8"))
      else:
        print(message)
    except:
      print("Ocurrio un error")
      client.close
      break

def emisorDeMensajes():
    while True:
        message = f"{username}: {input('>> ')}"
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receptorDeMensajes)
receive_thread.start()

write_thread = threading.Thread(target=emisorDeMensajes)
write_thread.start()