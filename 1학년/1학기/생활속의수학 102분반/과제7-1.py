result = []

def checkDigit(value):
    ck = str(value).split(".")
    return True if int(ck[1]) == 0 and int(ck[0]) != 0 else False

for a in range(-4, 5):
    if a != 0:
        for b in range(-4, 5):
            if b != 0:
                c = -(a + b) / 2
                d = (a - b) / 2
                if a != b and checkDigit(c) and checkDigit(d):
                    result.append([a, b, int(c), int(d)])

print("\na, b, c, d \n")
for i in result:
    print(i)


for i, data in enumerate(result):
    print(f"\n{i + 1}번째")
    print(f"{5 + data[2]} {5 + data[1]} {5 + data[3]}\n{5 + data[0]} 5 {5 - data[0]}\n{5 - data[3]} {5 - data[1]} {5 - data[2]}")
input("\nX 눌러서 종료 또는 ENTER 키 입력")