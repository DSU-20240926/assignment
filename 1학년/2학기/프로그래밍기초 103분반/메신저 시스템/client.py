import socket
import threading
import os
import tkinter as tk
from tkinter import filedialog
import time
import logUtils as log

#Client class to manage user interactions
class MessengerClient:
    def __init__(self, host, port, pid=None):
        self.host = host
        self.port = port
        self.pid = pid
        self.nickname = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: self.client_socket.connect((self.host, self.port))
        except socket.gaierror as e: log.error(f"연결 실패: 잘못된 호스트 이름 또는 주소입니다! 올바른 호스트 이름을 입력했는지 확인하세요! \nsocket.gaierror: {e}"); self.client_socket = None
        except OverflowError as e: log.error(f"연결 실패: 포트 범위는 0~65535 입니다! {self.port} 포트 대신 다른 포트 번호를 입력하세요! \nOverflowError: {e}"); self.client_socket = None
        except ConnectionRefusedError as e: log.error(f"연결 실패: 대상 컴퓨터에서 연결을 거부했습니다! 서버가 실행 중인지 확인하세요! \nConnectionRefusedError: {e}"); self.client_socket = None
        if not self.client_socket: os.system(f"taskkill /f /pid {self.pid}")
        log.info(f"Connected to server at TCP {self.host}:{self.port}")

    def send_message(self):
        while True:
            message = input(f"{self.host}:{self.port}/{self.nickname}$ ") #콘?솔 커?서 템플릿?
            if message.startswith("/file ") or message.startswith("/f "): #파일처리
                action = message.split(" ")[1]
                if action == "up": #client --> Server 업로드
                    filename = self.select_file()
                    if not filename: log.warning("Canceld"); continue
                    self.client_socket.send(f"/fileup|{os.path.basename(filename)}|{os.path.getsize(filename)}".encode())
                    with open(filename, "rb") as f: self.client_socket.send(f.read())
                elif action == "down": #Sever --> client 다운로드
                    try: self.client_socket.send(f"/filedown|{message.split(' ')[2]}".encode())
                    except: pass
                elif action == "del": #서버의 파일 삭제
                    try: self.client_socket.send(f"/filedel|{message.split(' ')[2]}".encode())
                    except: pass
                elif action == "list": self.client_socket.send("/filelist".encode()) #files 폴더속 파일명 조회후 클라에게 전송
            elif message.startswith("/dm "):
                try: #DM 한정 발신 logdm.txt 에 로깅함 (받는 사름이 정확하지 않을 수 있음)
                    with open("logdm.txt", "a") as f: f.write(f"[{int(time.time())}] - {self.nickname}(me) --> {message.split(' ')[1]}: {message.split(' ')[2]}\n")
                    self.client_socket.send(message.encode())
                except: pass
            elif message.startswith("/su"):
                if len(message.split(" ")) > 1: user = message.split(" ")[1]
                elif message == '/su' or message.split(" ")[1] == "root": user = "root"
                else: user = message.split(" ")[1]
                self.client_socket.send(f"/su|{user}|{input('Password: ') if user == 'root' else ''}".encode())
            elif message == "/ping": st_cli = time.time(); self.client_socket.send(f"/ping|{st_cli}".encode())
            elif message == "/exit": self.client_socket.send(message.encode()); break #유저가 /exit 명령어 입력시 연결은 끊음
            else: self.client_socket.send(message.encode()) #전체 채팅

    def receive_message(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode()
                logType, sender = msg.split("|")[0:2]
                msg = msg.replace(f"{logType}|{sender}|", "")

                if logType == "ServerData": #서버에서 클라에게 보내는 데이터 수신하는 곳
                    if msg.startswith("/filedown|"):
                        filename, filesize = msg.replace("/filedown|", "").split("|"); filesize = int(filesize)
                        if os.path.exists(f"downloads/{filename}"):
                            newFilename = filename.replace(f'.{filename.split(".")[-1]}', f' cp.{filename.split(".")[-1]}')
                            log.warning(f"downloads/{filename} 파일이 이미 존재하여 downloads/{newFilename} 로 변경하여 저장함")
                            filename = newFilename
                        with open(f"downloads/{filename}", "wb") as f: f.write(self.client_socket.recv(filesize))
                        os.system(f'start "" "downloads"') #다운로드 완료시 폴더 오픈
                    elif msg.startswith("/filelist|"): log.info(eval(msg.replace("/filelist|", "")))
                    elif msg.startswith("/su|"): #사용자 변경 작업
                        _, nick, res = msg.split("|", 2)
                        if res == "ok": self.nickname = nick
                        elif res == "dupl": log.warning(f"Nickname {nick} is Duplicated!")
                        elif res == "af": print("\nsu: Authentication failure")
                    elif msg.startswith("/ping|"):
                        et = time.time(); st_cli, st_ser = msg.replace("/ping|", "").split("|"); st_cli, st_ser = [float(st_cli), float(st_ser)]
                        log.info(f"You -----({st_ser - st_cli}ms)-----> Server -----({et - st_ser}ms)-----> You | {et - st_cli}ms")
                elif logType == "exit": log.warning(msg); os.system(f"taskkill /f /pid {self.pid}") #서버에서 연결 끊을시 하는 작업
                elif logType == "warning": log.warning(f"{sender}: {msg}")
                elif logType == "error": log.error(f"{sender}: {msg}")
                elif logType == "info": log.info(f"{sender}: {msg}")
                elif logType == "debug": log.debug(f"{sender}: {msg}")
                elif logType == "chat": log.chat(f"{sender}: {msg}")
                elif logType == "msg": print('\033[94m'+(" "*8 + f"Server - {sender}: {msg}")+'\033[0m') #log.chat() 색인 파란색 직접 출력
                elif logType == "dm":
                    print('\033[94m'+(" "*8 + f"DM - {sender}: {msg}")+'\033[0m') #log.chat() 색인 파란색 직접 출력
                    with open("logdm.txt", "a") as f: f.write(f"[{int(time.time())}] - {sender} --> {self.nickname}(me): {msg}\n") #DM 한정 수신 logdm.txt 에 로깅함
                else: print(f"{sender}: {msg}")
            except Exception as e: log.error(f"Connection error: {e}"); break

    def select_file(self):
        """
        탐색기 창을 열어 업로드 할 파일 선택
        """
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path

    def set_nickname(self):
        while True:
            nick = input("Set your nickname: ").strip()
            if not nick: continue
            passwd = input('Password: ') if nick == "root" else ""
            self.client_socket.send(f"{nick}|{passwd}".encode()) #서버로 닉네임 전송 (+root 면 비밀번호도 전송)
            res = self.client_socket.recv(1024).decode() #서버에거 ok, dupl, af 을 리턴받음
            if res == "ok": self.nickname = nick; break
            elif res == "dupl": log.warning(f"Nickname {nick} is Duplicated!")
            elif res == "af": print("\nsu: Authentication failure")

    def run(self):
        self.set_nickname()
        self.client_socket.send("/help".encode()) #서버 접속시 명령어 출력
        threading.Thread(target=self.send_message).start()
        threading.Thread(target=self.receive_message).start()