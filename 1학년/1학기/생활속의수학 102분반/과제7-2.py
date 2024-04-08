upper = [0, 4, 8, 12]
lower = [1, 2, 3, 4]
result = []

""" for ui, u in enumerate(upper):
    for li, l in enumerate(lower):
        print((u, l), (ui, li))
        result.append([u + l] ) """

for w in range(4):
    A, B, C, D = (w) % 4, (w + 1) % 4, (w + 2) % 4, (w + 3) % 4
    for h in range(4):
        #A = w, B = w + 1, C = w + 2
        a, b, c, d = (h) % 4, (h + 1) % 4, (h + 2) % 4, (h + 3) % 4
        #print("w", w, A, B, C, D)
        #print("h", h, a, b, c, d)
        """ print("upper", upper[A], upper[B], upper[C], upper[D])
        print("lower", lower[a], lower[b], lower[c], lower[d])
        print() """
        """ result.append([[upper[A] + lower[a], upper[B] + lower[b], upper[C] + lower[2], upper[3] + lower[3]], 
                [upper[3] + lower[2], upper[C] + lower[3], upper[B] + lower[a], upper[A] + lower[b]],
                [upper[B] + lower[3], upper[A] + lower[2], upper[3] + lower[b], upper[C] + lower[a]],
                [upper[C] + lower[b], upper[3] + lower[a], upper[A] + lower[3], upper[B] + lower[2]]
            ]) """
        
        """ result.append([["{uA}" + "{la}", upper[B] + lower[b], upper[C] + lower[2], upper[3] + lower[3]], 
                [upper[3] + lower[2], upper[C] + lower[3], upper[B] + lower[a], upper[A] + lower[b]],
                [upper[B] + lower[3], upper[A] + lower[2], upper[3] + lower[b], upper[C] + lower[a]],
                [upper[C] + lower[b], upper[3] + lower[a], upper[A] + lower[3], upper[B] + lower[2]]
            ]) """
        """ print(f"{upper[A] + lower[a]} {upper[B] + lower[b]} {upper[C] + lower[c]} {upper[D] + lower[d]}")
        print(f"{upper[D] + lower[c]} {upper[C] + lower[D]} {upper[B] + lower[a]} {upper[A] + lower[b]}")
        print(f"{upper[B] + lower[d]} {upper[A] + lower[c]} {upper[D] + lower[b]} {upper[C] + lower[a]}")
        print(f"{upper[C] + lower[b]} {upper[D] + lower[a]} {upper[A] + lower[d]} {upper[B] + lower[c]}")
        print("\n\n") """
        """ print(f"{upper[A] + lower[a]} {upper[B] + lower[b]} {upper[C] + lower[c]} {upper[D] + lower[d]}")
        print(f"{upper[D] + lower[c]} {upper[C] + lower[D]} {upper[B] + lower[a]} {upper[A] + lower[b]}")
        print(f"{upper[B] + lower[d]} {upper[A] + lower[c]} {upper[D] + lower[b]} {upper[C] + lower[a]}")
        print(f"{upper[C] + lower[b]} {upper[D] + lower[a]} {upper[A] + lower[d]} {upper[B] + lower[c]}")
        print("\n\n") """

        if (upper[A] + lower[a] + upper[B] + lower[b] +
            upper[C] + lower[c] + upper[D] + lower[d] == 34 and
            upper[D] + lower[c] + upper[C] + lower[D] +
            upper[B] + lower[a] + upper[A] + lower[b] == 34 and
            upper[B] + lower[d] + upper[A] + lower[c] +
            upper[D] + lower[b] + upper[C] + lower[a] == 34 and
            upper[C] + lower[b] + upper[D] + lower[a] +
            upper[A] + lower[d] + upper[B] + lower[c] == 34):
            ap = True
        else:
            ap = False

        if ap:
            result.append([
                [upper[A] + lower[a], upper[B] + lower[b], upper[C] + lower[c], upper[D] + lower[d]],
                [upper[D] + lower[c], upper[C] + lower[D], upper[B] + lower[a], upper[A] + lower[b]],
                [upper[B] + lower[d], upper[A] + lower[c], upper[D] + lower[b], upper[C] + lower[a]],
                [upper[C] + lower[b], upper[D] + lower[a], upper[A] + lower[d], upper[B] + lower[c]]
                ])

for num, i in enumerate(result):
    print(num + 1)
    print(f"{i[0]}\n{i[1]}\n{i[2]}\n{i[3]}")
    print()
input("\nX 눌러서 종료 또는 ENTER 키 입력")