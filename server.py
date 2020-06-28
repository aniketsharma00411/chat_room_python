import socket
import _thread
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Correct usage: python3 script.py <local_ip_of_server> <port_number>")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
# Binding the server to the entered IP address and port number. The clients must know these parameters to connect
server.bind((IP_address, Port))
# Listens for maximum 10 active connections. This number can be changed accordingly.
server.listen(10)
list_of_clients = []


def clientthread(conn, addr):
    conn.send(b"Welcome to this chatroom!")
    while True:
        try:
            message = conn.recv(2048)
            if message:
                # To convert byte object to string
                message = message.decode(encoding='UTF-8')
                print("<" + addr[0] + "> " + message)
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                # To convert byte object to byte
                message = message.encode(encoding="UTF-8")
                clients.send(message)
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    _thread.start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
