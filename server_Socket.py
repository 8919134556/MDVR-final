import socket
import threading
import configparser
from concurrent.futures import ThreadPoolExecutor
from ClientHandler import MDVRClientHandler

class MDVRServer:
    def __init__(self):
        self.config = self.read_config()
        self.port = int(self.config.get('Server', 'Port'))
        self.server_socket = None
        self.thread_pool = ThreadPoolExecutor(max_workers=500)  # Adjust the number of workers as needed
        self.clients = []
        self.shutdown_event = threading.Event()

    def read_config(self):
        config = configparser.ConfigParser()
        config.read('mdvr_config.ini')  # Specify the path to your .ini file
        return config

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(500)  # Adjust the maximum number of queued connections

            print(f"MDVR Server is listening on port {self.port}")

            while not self.shutdown_event.is_set():
                try:
                    client_socket, addr = self.server_socket.accept()
                    print(f"Client Address: {addr}")
                    handler = MDVRClientHandler(client_socket, addr, self)
                    self.clients.append(handler)
                    self.thread_pool.submit(handler.run)
                except socket.error as e:
                    print(f"Socket error while accepting connection: {e}")
        except Exception as e:
            print(f"An exception occurred while creating the MDVR server socket: {e}")

    def stop_server(self):
        self.shutdown_event.set()
        for client in self.clients:
            client.stop()
        self.thread_pool.shutdown(wait=False)
        self.server_socket.close()

    def run(self):
        self.start_server()

if __name__ == "__main__":
    mdvr_server = MDVRServer()
    mdvr_server.run()
