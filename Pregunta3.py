import socket
import threading
import sys

# Dirección y puerto del servidor
HOST = '127.0.0.1'
PORT = 55555

# Crear un socket TCP/IP
sockCli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace del socket al host y puerto
try:
    sockCli.bind((HOST, PORT))
except socket.error:
    print("Servidor no puede iniciarse.")
    exit()
except Exception as e:
    print("Servidor no puede iniciarse.")
    exit()

# Escuchar conexiones entrantes
sockCli.listen()

# Lista para almacenar las conexiones de los clientes
clients = []

# Función para enviar mensajes de difusión a todos los clientes
def broadcast(message, sender_socket=None):
    encoded_message = message.encode('utf-8')  # Codificar el mensaje a bytes
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(encoded_message)
            except socket.error:
                clients.remove(client_socket)

# Función para manejar la conexión con cada cliente
def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            mensajeDecode = message.decode('utf-8').lower()
            if "adios" in mensajeDecode:
                message2 = mensajeDecode.split(':')
                # Enviar mensaje de despedida a los demás clientes
                broadcast(f"{client_address} - {message2[0]} se ha desconectado.", client_socket)
                print(f"{client_address} - {message2[0]} se ha desconectado.")
        except Exception as e:
            print(f"Error en la conexión con {client_address}: {e}")
            break

        # Aquí puedes agregar más lógica para manejar otros tipos de mensajes

        # Si un cliente se desconecta, lo eliminamos de la lista de conexiones
        if client_socket not in clients:
            clients.remove(client_socket)

# Función para aceptar conexiones entrantes
def accept_connections():
    while True:
        client_socket, client_address = sockCli.accept()
        clients.append(client_socket)
        print(f"Nueva conexión de {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Iniciar el servidor
print(f"Servidor escuchando en {HOST}:{PORT}")
accept_connections()
