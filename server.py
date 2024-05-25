import threading
import socket


def start_server():
    host = '127.0.0.1'
    port = 55555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []
    nicknames = []

    def broadcast(message, sender):
        for client in clients:
            client.send(f"{sender}: {message}".encode("utf-8"))

    def handle(client):
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message.startswith('@'):
                    recipient, private_message = message.split(':', 1)
                    recipient = recipient[1:].strip()
                    private_message = private_message.strip()
                    send_private_message(recipient, private_message, client)
                else:
                    broadcast(message, nicknames[clients.index(client)])
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f"{nickname} left the chat", "Server")
                nicknames.remove(nickname)
                break

    def send_private_message(recipient, private_message, sender_client):
        if recipient in nicknames:
            recipient_index = nicknames.index(recipient)
            recipient_client = clients[recipient_index]
            sender_nickname = nicknames[clients.index(sender_client)]
            recipient_client.send(
                f"{sender_nickname} (private): {private_message}".encode("utf-8"))
        else:
            sender_client.send(
                f"User '{recipient}' not found or not online.".encode("utf-8"))

    def receive():
        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            client.send("ENTER USERNAME: ".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")
            nicknames.append(nickname)
            clients.append(client)

            print(f"Username of the client is {nickname}")
            broadcast(f"{nickname} joined the chat", "Server")
            client.send("Connected to the server!".encode("utf-8"))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()


if __name__ == "__main__":
    start_server()
