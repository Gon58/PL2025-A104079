import sys

def soma_inteiros(l):
    res = 0
    i = 0
    on = True
    while i < len(l):
        valor = 0
        sinal = 1
        if l[i] == '-':
            sinal = -1
            i = i + 1
        elif l[i] in "0123456789":
            while l[i] in "0123456789":
                valor = valor * 10 + int(l[i])
                i = i + 1
            valor = valor * sinal
            if on:
                res += valor
        elif l[i] == '=':
            print(res)
            i = i + 1
        elif l[i] == 'O':
            i = i + 1
            if l[i] == 'n':
                on = True
                i = i + 1
            elif l[i] == 'f':
                i = i + 1
                if l[i] == 'f':
                    on = False
                    i = i + 1
        else:
            i = i + 1
    return res

for linha in sys.stdin:
    inteiros = soma_inteiros(linha)