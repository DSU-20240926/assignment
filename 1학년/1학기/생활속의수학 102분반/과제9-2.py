Alphabet = "abcdefghijklmnopqrstuvwxyz"
text = "It is true that you have a good reputation and be faithful in marriage."
key = [2, 5, 8, 10, 23]
hashed_text = ""

#띄어쓰기, . 을 제외하고 키를 적용함
for i, t in enumerate(text.replace(" ", "").replace(".", "")):
    ANum = key[i % 5] + Alphabet.find(t.lower())
    if ANum > 25: ANum = ANum % 26
    hashed_word = Alphabet[ANum]
    #print((t, key[i % 5], hashed_word))

    hashed_text += hashed_word
hashed_text += "." #마지막에 . 추가
print(hashed_text)



#GPT code
encrypted_chars = [char for char in hashed_text]
result = ''
for c in text:
    if c == ' ':
        result += ' '
    elif c == c.upper():
        result += encrypted_chars.pop(0).upper()
    else:
        result += encrypted_chars.pop(0)
print(result)
input("\nX 눌러서 종료 또는 ENTER 키 입력")