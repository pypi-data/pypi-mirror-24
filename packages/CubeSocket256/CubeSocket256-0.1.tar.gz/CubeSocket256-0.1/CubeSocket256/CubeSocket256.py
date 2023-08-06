from pycube256 import Cube
import socket
import os

# v0.1

class CubeSocket:
    def __init__(self, key, nonce_support=1, dc=0, mode=0):
        self.key = key
        self.session_key = ""
        self.nonce_support = nonce_support
        self.key_length = 16
        self.nonce_length = 16
        self.direct_connect = dc
        if mode == 0:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif mode == 1:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def wrap(self, sock):
        self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, buf, nonce=""):
        if self.nonce_support == 0:
            buf = Cube(self.key).encrypt(buf)
            self.sock.send(buf)
        elif self.nonce_support == 1:
            buf = Cube(self.key, nonce).encrypt(buf)
            self.sock.send(buf)

    def recv(self, buf_size, nonce=""):
        buf = self.sock.recv(buf_size)
        if self.nonce_support == 0:
            buf = Cube(self.key).decrypt(buf)
        elif self.nonce_support == 1:
            buf = Cube(self.key, nonce).decrypt(buf)
        return buf

    def close(self):
        self.sock.close()

    def listen(self, num_listeners):
        self.sock.listen(num_listeners)

    def bind(self, host, port):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

    def cli_keyexchange(self, sock):
        if self.nonce_support == 0:
	    session_key = self.gen_key(self.key_length)
    	    self.send(session_key)
	    self.key = session_key
        elif self.nonce_support == 1:
            nonce = self.gen_key(self.nonce_length)
            self.sock.send(nonce)
	    session_key = self.gen_key(self.key_length)
            key = Cube(self.key, nonce).encrypt(session_key)
    	    self.sock.send(key)
	    self.key = session_key

    def srv_keyexchange(self, client_sock):
        if self.nonce_support == 0:
	    session_key = client_sock.recv(self.key_length)
	    self.session_key = Cube(self.key).decrypt(session_key)
	    self.key = self.session_key
        elif self.nonce_support == 1:
            nonce = client_sock.recv(self.nonce_length)
            key = client_sock.recv(self.key_length)
            session_key = Cube(self.key, nonce).decrypt(key)
            self.key = session_key

    def accept(self):
        client, addr = self.sock.accept()
        if self.direct_connect == 0:
	    self.srv_keyexchange(client)
        return client, addr

    def gen_key(self, length):
        key = ""
        for x in range(0,length):
            char = os.urandom(1)
            key += char
        return key

    def cubeconnect(self, host, port):
        self.connect(host, port)
	self.cli_keyexchange(self.sock)

    def cubesend(self, buf):
        if self.nonce_support == 1:
            nonce = self.gen_key(self.nonce_length)
            self.sock.send(nonce)
            buf = Cube(self.key, nonce).encrypt(buf)
            self.sock.send(buf)
        elif self.nonce_support == 0:
            session_key = self.gen_key(self.key_length)
            key = Cube(self.key).encrypt(session_key)
            self.sock.send(key)
            buf = Cube(session_key).encrypt(buf)
            self.sock.send(buf)

    def cuberecv(self, buf_size):
        if self.nonce_support == 1:
            nonce = self.sock.recv(self.nonce_length)
            buf = self.sock.recv(buf_size)
            buf = Cube(self.key, nonce).decrypt(buf)
        elif self.nonce_support == 0:
            key = self.sock.recv(self.key_length)
            session_key = Cube(self.key).decrypt(key)
            buf = self.sock.recv(buf_size)
            buf = Cube(session_key).decrypt(buf)
        return buf

    def cubesendto(self, buf, ip, port):
        if self.nonce_support == 1:
            nonce = self.gen_key(self.nonce_length)
            buf = Cube(self.key, nonce).encrypt(buf)
            self.sock.sendto(nonce+buf, (ip, port))
        elif self.nonce_support == 0:
            session_key = self.gen_key(self.key_length)
            buf = Cube(session_key).encrypt(buf)
            session_key = Cube(self.key).encrypt(session_key)
            self.sock.sendto(session_key+buf, (ip, port))

    def cuberecvfrom(self, buf_size):
        if self.nonce_support == 1:
            buf, addr = self.sock.recvfrom(buf_size)
            nonce = buf[0:16]
            data = buf[16:]
            data = Cube(self.key, nonce).decrypt(data)
        elif self.nonce_support == 0:
            buf, addr = self.sock.recvfrom(buf_size)
            session_key = buf[0:16]
            session_key = Cube(self.key).decrypt(session_key)
            data = buf[16:]
            data = Cube(session_key).decrypt(data)
        return data

class CubeWrap:
    def __init__(self, sock, key, nonce_support=1):
        self.sock = CubeSocket(key)
        self.sock.wrap(sock)
        self.raw_sock = sock
        self.sock.nonce_support = nonce_support
