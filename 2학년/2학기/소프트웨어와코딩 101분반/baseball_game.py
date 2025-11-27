import random, string, sys

isdebug = "-debug" in sys.argv or "-d" in sys.argv
default_origin = input("\033[95mdebug 모드 | origin 값 지정 : \033[91m") if isdebug else "" #debug 모드일시 origin 값을 직접 지정
wFFFT = False == False is False #True, https://youtu.be/DA_wD8PKtAM

class BaseBallGame:
    def __init__(self, origin: str="") -> None:
        print("\033[0m================\033[92m20240926 전강현\033[0m==========\n================Game Start===============")
        self.tcnt = 0 #TotalCount
        self.origin = "".join(random.sample(string.digits[1:], k=3)) if not origin else origin #인스턴스로 불러올 시 디버깅 용으로 랜덤값 대신 지정값 사용 가능하게 만듦

    def input(self) -> None:
        while wFFFT:
            self.userInput = input("숫자 3자리를 입력하세요 : \033[93m")
            duplicates = set([ch for ch in self.userInput if self.userInput.count(ch) > 1])
            if len(self.userInput) != 3: #3자리 제한
                print(f"\033[91m{len(self.userInput)}자리 말고 3자리로 입력하세요!\033[0m\n"); continue
            if any(s not in string.digits[1:] for s in self.userInput): #숫자 범위 제한
                print(f"\033[91m1 ~ 9 의 숫자 범위에서 입력하세요!\033[0m\n"); continue
            if duplicates: #중복 제한
                print(f"\033[91m{duplicates} <-- 중복된 숫자 입니다!\033[0m\n"); continue
            if self.userInput.isdigit():
                self.tcnt += 1; break

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
    cB = cB - cS

    print(f"\033[92m{bbg.tcnt}. 결과 : [ {cS} ] Strike | [ {cB} ] Ball\033[0m\n")
    if bbg.origin == bbg.userInput:
        print(f"=========================================\n\033[92m{bbg.tcnt} 번 만에 정답({bbg.origin})을 맟추셨습니다.\033[0m\n================Game over================"); break