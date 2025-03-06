import sys
import re

def tokenize(code):
    token_specification = [
        ('SELECT', r'select'),
        ('WHERE', r'where'),
        ('LIMIT', r'LIMIT'),
        ('VARIAVEL', r'\?[a-zA-Z]+'),
        ('ID', r'[_A-Za-z]\w*'),
        ('CA', r'\{'),
        ('CF', r'\}'),
        ('PONTO', r'\.'),
        ('STRING', r'"[^"]*"@\w{2}'),
        ('NUMBER', r"\d+"),
        ('COMMENT', r'#.*'), 
        ('DOISPONTOS', r':'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('ERRO', r'.'),
    ]

    tok_regex = '|'.join([f'(?P<{id}>{expreg})' for (id, expreg) in token_specification])

    reconhecidos = []
    linha = 1
    mo = re.finditer(tok_regex, code)
    result = []

    for m in mo:
        tipo = m.lastgroup
        valor = m.group(tipo)

        if tipo == 'NEWLINE':
            linha += 1
            continue
        elif tipo == 'SKIP':
            continue
        else:
            result.append((tipo, valor, linha, m.span()))
    
    return result

def main():
    if len(sys.argv) != 2:
        print("Número de argumentos inválido")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    result = tokenize(code)

    with open("result.txt", "w") as f:
        for r in result:
            f.write(f"{r[0]} - '{r[1]}' - Linha {r[2]} - Posição {r[3]}\n")

if __name__ == "__main__":
    main()