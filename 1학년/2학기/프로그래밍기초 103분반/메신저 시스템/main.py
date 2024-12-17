import os
import logUtils as log
from server import MessengerServer
from client import MessengerClient

if __name__ == "__main__":
    pid = os.getpid()
    if os.name != 'nt': log.warning("UNIX Detected!\nPlease RUN on Windows"); exit() #Windwos 가 아닌 다른 모든 OS 실행 감지시 코드종료
    host = input("Input Server address(127.0.0.1) : "); host = "127.0.0.1" if not host else host #클라가 사용할 host 주소를 입력받고, 공란시 localhost로 접속함
    port = input("Input Port(6697) : "); port = 6697 if not port else int(port) #서버, 클라가 사용할 port 번호를 입력받고, 공란시 IRC SSL 포트인 6697 포트 사용함
    choice = input("Start server or client? (s/c): ").strip().lower() #서버로 실행 or 클라로 실행 선택기
    if choice == 's':
        rPw = input("Input Server root password(root) : "); rPw = "root" if not rPw else rPw #root 비밀번호 설정
        MessengerServer(host='0.0.0.0', port=port, pid=pid, rootPasswd=rPw).run() #서버로 선택시 서버로 실행함
    elif choice == 'c': MessengerClient(host=host, port=port, pid=pid).run() #클라로 선택시 클라로 실행함
    else: log.warning("Invalid choice.")