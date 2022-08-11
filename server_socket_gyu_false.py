from http import client
import multiprocessing
import socket
from _thread import *
from multiprocessing import Process, Queue
from threading import Thread

class socket_Transportation():
    def __init__(self, INNER_HOST, ROBOT_HOST, PORT):
        self.INNER_HOST = INNER_HOST
        self.ROBOT_HOST = ROBOT_HOST
        self.PORT = PORT

        self.client_sockets = list() # 서버에 접속한 클라이언트 목록


    def start_process(self):
        pc1 = Thread(target=self.socket_thread, args=(self.INNER_HOST, self.PORT))
        pc2 = Thread(target=self.socket_thread, args=(self.ROBOT_HOST, self.PORT))

        pc1.start()
        pc2.start()


    def socket_thread(self, HOST, PORT):
        # 서버 소켓 생성
        print(f'>> {HOST} Server Start')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        try:
            while True:
                print('>> Wait')

                # print(client_socket) == <socket.socket fd=440, ... , laddr=('192.168.2.2', 9999), raddr=('192.168.2.3', 45786)
                # print(addr) == ('192.168.2.3', 45788)
                client_socket, addr = server_socket.accept()
                self.client_sockets.append(client_socket)
                start_new_thread(self.threaded, (client_socket, addr))
                print(f"{HOST} 참가자 수 : ", len(self.client_sockets))
                    
        except Exception as e :
            print ('에러는? : ',e)

        finally:
            server_socket.close()



    # 쓰레드에서 실행되는 코드입니다.
    # 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
    def threaded(self, client_socket, addr):
        print('>> Connected by :', addr[0], ':', addr[1])

        # 클라이언트가 접속을 끊을 때 까지 반복합니다.
        while True:
            try:
                # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
                data = client_socket.recv(1024)

                if not data:
                    print('>> Disconnected by ' + addr[0], ':', addr[1])
                    break

                print('>> Received from ' + addr[0], ':', addr[1], data.decode())

                # 서버에 접속한 클라이언트들에게 채팅 보내기
                # 메세지를 보낸 본인을 제외한 서버에 접속한 클라이언트에게 메세지 보내기
                for client in self.client_sockets :
                    if client != client_socket :
                        client.send(data)

            except ConnectionResetError as e:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

        if client_socket in self.client_sockets :
            self.client_sockets.remove(client_socket)
            print('remove client list : ',len(self.client_sockets))

        client_socket.close()



if __name__ == '__main__':
    # 서버 IP 및 열어줄 포트
    INNER_HOST = '10.10.33.161' # 내부망
    ROBOT_HOST = '192.168.2.2' # 공유기
    PORT = 9999

    a = socket_Transportation(INNER_HOST, ROBOT_HOST, PORT)
    a.start_process()
