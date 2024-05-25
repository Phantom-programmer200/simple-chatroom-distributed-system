import socket
import threading


class ChatClient:
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        self.client_socket.send(self.nickname.encode("utf-8"))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        self.send_messages()

    def send_messages(self):
        print("To send a private message, use '@nickname:message'")
        while True:
            message = input("Enter message: ")
            if message.startswith('@'):
                recipient, private_message = message.split(':', 1)
                self.client_socket.send(message.encode("utf-8"))
            else:
                self.client_socket.send(message.encode("utf-8"))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                print(message)
            except ConnectionAbortedError:
                break


if __name__ == "__main__":
    host = "127.0.0.1"  # Change to your server's IP address
    port = 55555        # Change to your server's port
    nickname = input("ENTER USERNAME: ")

    client = ChatClient(host, port, nickname)
