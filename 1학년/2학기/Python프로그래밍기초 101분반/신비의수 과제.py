#https://github.com/DSU-20240926/assignment/tree/main/1학년/2학기/Python프로그래밍기초%20101분반/신비의수%20과제.py

class MysteriousNumber:
    def __init__(self, sn: int=100, en: int=333) -> None:
        """
        초기화: 탐색 범위를 설정
        """
        print("\n? ~ 241211 Python프로그래밍기초 101분반 신비의 수 과제 \n컴퓨터공학과 20240926 전강현\n")
        self.sn = sn
        self.en = en
        self.MyNum = []

    def find(self) -> list:
        """
        신비의 수를 찾고 저장 및 반환
        """
        for n in range(self.sn, self.en + 1):
            ck = f"{n}{n * 2}{n * 3}"
            if len(ck) == 9 and set(ck) == set("123456789"): self.MyNum.append(n)
        return self.MyNum

finder = MysteriousNumber()
result = finder.find()

for i, d in enumerate(result): print(f"{i + 1}. | {d} | {d} --> {d * 2} --> {d * 3}")