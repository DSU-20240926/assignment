import socket
import threading
import os
import time
import logUtils as log

#Server class to manage connections and messaging
class MessengerServer:
    def __init__(self, host='0.0.0.0', port=6697, pid=None, rootPasswd=""):
        self.host = host
        self.port = port
        self.pid = pid
        self.rootPasswd = rootPasswd
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        log.info(f"Server Listen on TCP {self.host}:{self.port} | OS = {'Windows' if os.name == 'nt' else 'UNIX'}")

    def fdc(self):
        """
        files(서버에서 파일저장), downloads(클라에서 파일저장) 폴더 생성
        """
        if not os.path.exists(f"files"): os.mkdir(f"files") # 파일 폴더생성
        if not os.path.exists(f"downloads"): os.mkdir(f"downloads") # 다운로드 폴더생성

    def userCheck(self, nick, passwd):
        if nick == "root" and self.rootPasswd == passwd: return "ok"
        elif nick == "root" and self.rootPasswd != passwd: return "af"
        elif nick in self.clients.values(): return "dupl"
        else: return "ok"

    def broadcast(self, message, logType="chat", sender_socket=None, userDM=None, serverDM=False, alert=False):     
        if logType == "msg": #logType이 msg 즉 전체 채팅 한정 logchat.txt 에 로깅함
            with open("logchat.txt", "a") as f: f.write(f"[{int(time.time())}] - {self.clients[sender_socket]}: {message}\n")
        sender = self.clients[sender_socket] if not alert else "Server"
        if sender_socket and userDM: sli = [(cs, sender) for cs, nick in self.clients.items() if nick == userDM] #sender --> userDM
        elif sender_socket and serverDM: sli = [(sender_socket, "Server")] #Server --> sender
        elif sender_socket and alert: sli = [(cs, sender) for cs in self.clients.keys()] #sender --> normal chat (내가 적은것도 다시 출력함)
        else: sli = [(cs, sender) for cs in self.clients.keys() if cs != sender_socket] #normal chat (내가 적은건 출력안함)
        for client_socket, nickname in sli:
            try: client_socket.send(f"{logType}|{nickname}|{message}".encode()) #전체채팅, user의 DM, server의 DM 등등 조건에 맞게 클라에게 메세지를 보냄 
            except Exception as e:
                log.error(f"Error sending message: {e}")
                del self.clients[client_socket]

    def handle_client(self, client_socket, client_address):
        log.info(f"New connection: {client_address}")
        try:
            while True: #클라에게 받은 닉네임 존재 여부 확인후 클라에게 ok, dupl, af 중 하나를 전송
                nick, passwd = client_socket.recv(1024).decode().split("|")
                uc = self.userCheck(nick, passwd)
                client_socket.send(uc.encode())
                if uc == "ok": break
            self.clients[client_socket] = nick
            log.info(f"Nickname set for {client_address}: {nick}")
            self.broadcast(f"{nick} has joined the chat!", logType="info", sender_socket=client_socket, alert=True)

            while True:
                data = client_socket.recv(1024).decode()
                sender_nick = self.clients[client_socket]
                if not data: break
                elif data == '/exit': self.broadcast(f"byebye", logType="exit", sender_socket=client_socket, serverDM=True); break #유저가 /exit 명령어 입력시 연결은 끊음
                elif data == '/list': self.broadcast(f"You: {sender_nick} | Users List: {list(self.clients.values())}", logType="info", sender_socket=client_socket, serverDM=True)
                elif data.startswith('/dm '): #접속중인 유저에게 DM을 보냄
                    try:
                        _, user, message = data.split(" ", 2)
                        if user == sender_nick: self.broadcast("DM can't send Yourself!", logType="warning", sender_socket=client_socket, serverDM=True)
                        elif user in self.clients.values(): self.broadcast(message, logType="dm", sender_socket=client_socket, userDM=user) #DM 전송
                        else: self.broadcast(f"{user} is not Connecting!", logType="warning", sender_socket=client_socket, serverDM=True)
                    except: self.broadcast("Use /dm {nickname} {message}", logType="warning", sender_socket=client_socket, serverDM=True)

                #파일 처리
                elif data.startswith('/fileup|'): #client --> Server 업로드
                    try:
                        self.fdc(); _, filename, filesize = data.split("|", 2); filesize = int(filesize)
                        if os.path.exists(f"files/{filename}"): self.broadcast(f"{filename} is Exist! Server Replace to Your File!", logType="warning", sender_socket=client_socket, serverDM=True)
                        with open(f"files/{filename}", "wb") as f: f.write(client_socket.recv(filesize))
                        log.info(f"File received From {nick}: {filename}")
                        self.broadcast(f"{nick} sent a file: {filename}", logType="info", sender_socket=client_socket, alert=True)
                    except Exception as e: self.broadcast(e, logType="error", sender_socket=client_socket, serverDM=True)
                elif data.startswith('/filedown|'): #Sever --> client 다운로드
                    try:
                        self.fdc(); filename = data.split("|")[1]
                        self.broadcast(f"/filedown|{filename}|{os.path.getsize(f'files/{filename}')}", logType="ServerData", sender_socket=client_socket, serverDM=True)
                        with open(f"files/{filename}", "rb") as f: client_socket.send(f.read()) #클라로 파일 전속함
                        log.info(f"File sent To {nick}: {filename}")
                        self.broadcast(f"{nick} download a file: {filename}", logType="info", sender_socket=client_socket, alert=True)
                    except Exception as e: self.broadcast(e, logType="error", sender_socket=client_socket, serverDM=True)
                elif data.startswith('/filedel|'): #서버의 파일 삭제
                    try:
                        self.fdc(); filename = data.split("|")[1]
                        os.remove(f"files/{filename}")
                        log.info(f"File deleted by {nick}: {filename}")
                        self.broadcast(f"{nick} deleted a file: {filename}", logType="info", sender_socket=client_socket, alert=True)
                    except Exception as e: self.broadcast(e, logType="error", sender_socket=client_socket, serverDM=True)
                #files 폴더속 파일명 조회후 클라에게 전송
                elif data == '/filelist': self.fdc(); self.broadcast(f'/filelist|{os.listdir("files")}', logType="ServerData", sender_socket=client_socket, serverDM=True)

                elif data.startswith('/kick '): #사용자 또는 서버를 추방(종료)
                    target = data.split(" ")[1]
                    if target not in self.clients.values() and target.lower() != "server": self.broadcast(f"{target} is not Connecting!", logType="warning", sender_socket=client_socket, serverDM=True)
                    elif sender_nick != "root" and sender_nick != target: self.broadcast("You Don't Have Permission!", logType="warning", sender_socket=client_socket, serverDM=True)
                    elif target.lower() == "server" and sender_nick == "root":
                        killmsg = f"Server Killed by {sender_nick}!\nbyebye"
                        self.broadcast(killmsg, logType="info", sender_socket=client_socket, alert=True)
                        log.warning(killmsg); os.system(f"taskkill /f /pid {self.pid}")
                    elif target in self.clients.values() and sender_nick == "root" or sender_nick == target:
                        for cs, nick in self.clients.items():
                            if nick == target:
                                self.broadcast(f"You Kicked by {sender_nick}", logType="exit", sender_socket=cs, serverDM=True)
                                self.broadcast(f"{target} Kicked by {sender_nick}", logType="warning", sender_socket=cs, alert=True)
                                log.warning(f"{target} Kicked by {sender_nick}")
                elif data.startswith('/su|'): #리눅스 명령어 su 를 참고함
                    _, nick, passwd = data.split("|", 2)
                    uc = self.userCheck(nick, passwd)
                    if uc == "ok":
                        self.clients[client_socket] = nick; log.info(f"User changed! | {sender_nick} --> {nick}")
                        self.broadcast(f'{sender_nick} has changed nickname to {nick}', logType="info", sender_socket=client_socket, alert=True)
                    self.broadcast(f"/su|{nick}|{uc}", logType="ServerData", sender_socket=client_socket, serverDM=True)
                elif data.startswith('/ping|'): st_ser = time.time(); self.broadcast(f"/ping|{data.split('|')[1]}|{st_ser}", logType="ServerData", sender_socket=client_socket, serverDM=True) #ping
                elif data == '/help' or data == '/h': #명령어 목록
                    msg = "\n\n\nCommands : /help(h), /exit, /list, /dm {nickname} {message}, /file(f) {up|down|del|list} {|filename(down)|filename(del)|}, \n/kick {username|server}, /su {username}, /ping\n"
                    self.broadcast(msg, logType="help", sender_socket=client_socket, serverDM=True)
                else: log.chat(f"Message from {sender_nick}: {data}"); self.broadcast(data, logType="msg", sender_socket=client_socket) #전체 채팅
        except Exception as e: log.error(f"Connection error: {e}")
        finally:
            sender_nick = self.clients[client_socket]
            log.info(f"Connection closed: {client_address}: {sender_nick}")
            self.broadcast(f"{sender_nick} has left the chat.", logType="info", sender_socket=client_socket, alert=True)
            try: del self.clients[client_socket]; client_socket.close()
            except Exception as e: log.error(e)

    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()