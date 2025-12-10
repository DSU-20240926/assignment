import random, string, sys, time, os, json
from typing import Union

agree = input(f"\033[93m커맨드 라인 인자(flags)가 존재함!\n\033[91m-d\033[0m 옵션은 \033[95m디버깅\n\033[91m-l\033[0m 옵션은 \033[92m.txt 파일로 저장 및 원격 서버로 전송 \033[91m(중요! 이 옵션 선택 시 제작자의 원격 서버로 IP 주소랑 함께 전송됩니다!)\n\033[92m현재 {sys.argv[1:]} 옵션으로 선택됨!\n\033[92magree\033[0m 입력시 게임 시작!\n")
exit() if not agree.lower() == "agree" else ""
isdebug = "-debug" in sys.argv or "-d" in sys.argv
islogging = "-logging" in sys.argv or "-l" in sys.argv
logFileName = f"{int(time.time())}.txt" if not isdebug else "debug.txt"

def printf(*args, **kwargs): #print 함수 파일로 로깅
    end_char = kwargs.get("end", "\n")
    t = " ".join(str(a) for a in args); print(t, **kwargs)
    if islogging:
        with open(logFileName, "a", encoding="utf-8") as f: f.write(f"{t}{end_char}")
def inputf(prompt=""): #input 함수 파일로 로깅
    if prompt: printf(prompt, end="")
    t = input()
    if islogging:
        with open(logFileName, "a", encoding="utf-8") as f: f.write(f"{t}\n")
    return t

class ANSI: #ANSI Escape Code | 과제에 중요한 코드가 아니기 때문에 인스턴스 선언 없이 @classmethod 를 사용하여 쓸 예정
    endc = f"\033[0m"  #reset

    @classmethod
    def error(self, msg: str, endc: bool = True, isprint: bool = True) -> Union[None, str]: #red 출력 or 리턴
        rt = f"\033[91m{msg}{self.endc if endc else ''}"; return printf(rt) if isprint else rt

    @classmethod
    def info(self, msg: str, endc: bool = True, isprint: bool = True) -> Union[None, str]: #green 출력 or 리턴
        rt = f"\033[92m{msg}{self.endc if endc else ''}"; return printf(rt) if isprint else rt
    
    @classmethod
    def warning(self, msg: str, endc: bool = True, isprint: bool = True) -> Union[None, str]: #yellow 출력 or 리턴
        rt = f"\033[93m{msg}{self.endc if endc else ''}"; return printf(rt) if isprint else rt
    
    @classmethod
    def chat(self, msg: str, endc: bool = True, isprint: bool = True) -> Union[None, str]: #blue 출력 or 리턴
        rt = f"\033[94m{msg}{self.endc if endc else ''}"; return printf(rt) if isprint else rt

    @classmethod
    def debug(self, msg: str, endc: bool = True, isprint: bool = True) -> Union[None, str]: #Magenta 출력 or 리턴
        rt = f"\033[95m{msg}{self.endc if endc else ''}"; return printf(rt) if isprint else rt

default_origin = inputf(f"{ANSI.debug('debug 모드 | origin 값 지정 : ', False, False)}{ANSI.chat('', False, False)}") if isdebug else "" #debug 모드일시 origin 값을 직접 지정
if isdebug and (not default_origin.isdigit() or any(s not in string.digits[1:] for s in default_origin) or len(default_origin) != 3 or set([ch for ch in default_origin if default_origin.count(ch) > 1])):
    ANSI.error("초기값은 1 ~ 9 의 숫자 범위에서 각각 한 번 씩만 사용하여 3자리를 입력 받습니다!\n다시 실행해 주세요!"); exit()
wFFFT = False == False is False #True, https://youtu.be/DA_wD8PKtAM

class BaseBallGame: #게임 메인 클래스
    def __init__(self, origin: str = "") -> None: #초기화
        printf(f"{ANSI.endc}================{ANSI.info('20240926 전강현', isprint=False)}==========\n================Game Start===============") #이름 출력
        self.st = time.time()
        self.__tcnt = 0 #TotalCount
        self.__origin = "".join(random.sample(string.digits[1:], k=3)) if not origin else origin #인스턴스로 불러올 시 디버깅 용으로 랜덤값 대신 지정값 사용 가능하게 만듦

    def input(self) -> None: #유저에게 입력 받고 값을 검증
        while wFFFT:
            self.userInput = inputf(f"숫자 3자리를 입력하세요 : {ANSI.warning('', endc=False, isprint=False)}")
            duplicates = set([ch for ch in self.userInput if self.userInput.count(ch) > 1])
            if len(self.userInput) != 3: #3자리 제한
                ANSI.error(f"{len(self.userInput)}자리 말고 3자리로 입력하세요!\n"); continue
            if any(s not in string.digits[1:] for s in self.userInput): #숫자 범위 제한
                ANSI.error(f"1 ~ 9 의 숫자 범위에서 입력하세요!\n"); continue
            if duplicates: #중복 제한
                ANSI.error(f"{duplicates} <-- 중복된 숫자 입니다!\n"); continue
            if self.userInput.isdigit():
                self.__tcnt += 1; break

    @property
    def origin(self) -> int: return self.__origin #__로 감싼 origin 직접 출력

bbg = BaseBallGame(origin=default_origin)
while wFFFT:
    bbg.input()

    cS = cB = 0 #Strike, Ball Count
    if bbg.origin[0] == bbg.userInput[0]: cS += 1
    if bbg.origin[1] == bbg.userInput[1]: cS += 1
    if bbg.origin[2] == bbg.userInput[2]: cS += 1
    if bbg.userInput[0] in bbg.origin: cB += 1
    if bbg.userInput[1] in bbg.origin: cB += 1
    if bbg.userInput[2] in bbg.origin: cB += 1
    cB -= cS

    ANSI.info(f"{bbg._BaseBallGame__tcnt}. 결과 : [ {cS} ] Strike | [ {cB} ] Ball{ANSI.debug(f' | ({bbg.origin})', isprint=False) if isdebug else ''}\n")
    if bbg.origin == bbg.userInput:
        printf(f"=========================================\n{ANSI.info(f'{bbg._BaseBallGame__tcnt} 번 만에 정답({bbg.origin})을 맟추셨습니다.', isprint=False)}\n================Game over================"); break

ANSI.chat(f"{round(time.time() - bbg.st, 2)} Sec")
if islogging:
    try:
        IP = json.loads(os.popen(f"curl -s --max-time 3 https://b.redstar.moe/ip").read())["ip"] #IP 주소 추출
        status = os.popen(f'curl -s -o NUL -w "%{{http_code}}" --max-time 10 --connect-timeout 3 -X POST -F "file=@{logFileName};filename={IP}-{logFileName}" https://flask.nanokvm.ch').read() #원격 서버로 파일 전송 | 솔직히 requests 라이브러리 쓰면 os.system 으로 curl 하는 괴상한 짓거리 안해도 되는데 의존성 줄이려고 선택함
        if int(status) == 200: ANSI.info(f"제작자의 서버로 {logFileName} 파일 전송 완료!")
        else: raise Exception(f"업로드 실패! HTTP STATUS: {status}")
    except Exception as e: ANSI.error(f"제작자의 서버로 {int(bbg.st)}-{logFileName} 파일 전송 실패!\n{ANSI.debug(f'원인 : {e}', isprint=False)}")
    if os.name == "nt": os.system(f'start notepad "{logFileName}"') #Windows 에서 로깅된 파일 메모장 으로 열기
    else: os.system(f'vi "{logFileName}"') #Linux 에서 로깅된 파일 vi 로 열기
ANSI.info("프로그램을 종료합니다.")