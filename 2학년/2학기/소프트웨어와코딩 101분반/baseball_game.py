import random, string

class BaseBallGame:
    def __init__(self, origin: str="") -> None:
        print("================20240926 전강현==========\n================Game Start===============")
        self.tcnt = 0 #TotalCount
        self.origin = "".join(random.sample(string.digits[1:], k=3)) if not origin else origin #인스턴스로 불러올 시 디버깅 용으로 랜덤값 대신 지정값 사용 가능하게 만듦
        print(self.origin)

    def input(self):
        while True:
            self.userInput = input("숫자 3자리를 입력하세요 : ")
            if self.userInput.isdigit(): break

tcnt = 0 #TotalCount
origin = "".join(random.sample(string.digits[1:], k=3))
print(origin)
bbg = BaseBallGame()
while True:
    cS = cB = 0 #Strike, Ball Count
    while True:
        userInput = input("숫자 3자리를 입력하세요 : ")
        if userInput.isdigit(): break
    cnt += 1

    if origin[0] == userInput[0]: cS += 1
    if origin[1] == userInput[1]: cS += 1
    if origin[2] == userInput[2]: cS += 1

    if userInput[0] in origin[0]: cB += 1
    if userInput[1] in origin[1]: cB += 1
    if userInput[2] in origin[2]: cB += 1

    cB = cB = cS
    print(f"결과 : [ {cS} ] Strike | [ {cB} ] Ball")
    if origin == userInput: print(f"=========================================\n{tcnt} 번 만에 정답을 맟추셨습니다.\n================Game over================")