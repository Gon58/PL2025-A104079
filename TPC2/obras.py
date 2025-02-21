import re

with open("obras.csv", "r", encoding="utf-8") as f:
    content = f.read()
    compositores = []
    contents = []
    quantidade_periodo = {}
    obras_periodo = {}
    first = True
    rows_content = re.split(r'\n(?=(?:[^"]*"[^"]*")*[^"]*$)', content) #divide o conteudo do csv pelas linhas, separando onde encontra o carácter '\n' fora de ""

    for linha in rows_content:
        if first:
            first = False
            continue
        campos = re.findall(r'(?:[^;"]|"(?:[^"]|"")*")+', linha) #divide as linhas csv, separando onde tem ';' fora de ""

        compositores.append(campos[4])

        periodo = campos[3]
        if periodo in quantidade_periodo:
            quantidade_periodo[periodo]+=1
        else:
            quantidade_periodo[periodo] = 1

        titulo = campos[0]
        if periodo in obras_periodo:
            obras_periodo[periodo].append(titulo)
        else:
            obras_periodo[periodo] = [titulo]

    compositores.sort()
    
    for periodo in obras_periodo:
        obras_periodo[periodo].sort()

    with open("Compositores", "w", encoding="utf-8") as ficheiro:
        ficheiro.write(str(compositores))

    with open("QuantidadeObrasPeriodo", "w", encoding="utf-8") as ficheiro:
        ficheiro.write(str(quantidade_periodo))

    with open("ObrasPeriodo", "w", encoding="utf-8") as ficheiro:
        ficheiro.write(str(obras_periodo))