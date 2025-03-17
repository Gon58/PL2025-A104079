import sys
import json
from datetime import datetime
import ply.lex as lex

tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'SAIR',
    'SALDO',
    'VALOR',
    'COD',
    'COMMA',
    'PERIOD'
)

t_LISTAR = r'LISTAR'
t_SAIR = r'SAIR'
t_SALDO = r'SALDO'
t_MOEDA = r'MOEDA'
t_SELECIONAR = r'SELECIONAR'
t_COMMA = r','
t_PERIOD = r'\.'

def t_VALOR(t):
    r'\d+[ec]'
    return t

def t_COD(t):
    r'[A-Z]\d+'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def print_line():
    print("-" * 70)

def calcular_troco(saldo):
    troco_moedas = {}
    moedas_disponiveis = {
        "2e": 2.00, "1e": 1.00, "50c": 0.50, "20c": 0.20, "10c": 0.10, "5c": 0.05
    }
    
    for moeda, valor in moedas_disponiveis.items():
        quantidade = 0
        while saldo >= valor:
            saldo = round(saldo - valor, 2)
            quantidade += 1
        if quantidade > 0:
            troco_moedas[moeda] = quantidade
    
    troco_str = ", ".join([f"{qtd}x {moeda}" for moeda, qtd in troco_moedas.items()])

    return troco_str

def handleCommand(command, dados, saldo):
    lexer.input(command)
    tokens = list(lexer)
    
    if not tokens:
        print("maq: Comando inválido.")
        return saldo

    command_type = tokens[0].type

    if command_type == 'LISTAR':
        print("maq:")
        print_line()
        print(f"| {'Código':^6} | {'Nome':^30} | {'Quantidade':^10} | {'Preço':^12} |")
        print_line()
        for item in dados['produtos']:
            cod = item['cod']
            nome = item['nome']
            quant = item['quant']
            preco = float(item['preco'])
            print(f"| {cod:^6} | {nome:<30} | {quant:^10} | {preco:>11.2f}€ |")
        print_line()
        return saldo

    elif command_type == 'MOEDA':
        valor = 0
        valid_moedas = ["2e", "1e", "50c", "20c", "10c", "5c"]
        i = 1
        while i < len(tokens):
            if tokens[i].type == 'VALOR' and tokens[i].value in valid_moedas:
                moeda = tokens[i].value
                if moeda.endswith('e'):
                    valor += float(moeda[:-1])
                else:
                    valor += float(moeda[:-1])/100
                i += 1
                if i < len(tokens):
                    if tokens[i].type == 'COMMA':
                        i += 1 
                    elif tokens[i].type == 'PERIOD':
                        i += 1
                        break
                    else:
                        print("maq: Formato inválido. Use vírgulas entre moedas e termine com ponto.")
                        return saldo
            else:
                print("maq: Moeda inválida.")
                return saldo
        
        if i <= len(tokens) and tokens[i-1].type != 'PERIOD':
            print("maq: O comando deve terminar com ponto.")
            return saldo
            
        saldo += valor
        print(f"maq: Saldo = {saldo:.2f}€")
        return saldo

    elif command_type == 'SELECIONAR':
        if len(tokens) < 2 or tokens[1].type != 'COD':
            print("maq: Código de produto inválido.")
            return saldo
            
        cod = tokens[1].value
        for item in dados['produtos']:
            if item['cod'] == cod:
                preco = float(item['preco'])
                if item['quant'] <= 0:
                    print(f"maq: Produto {cod} esgotado.")
                    return saldo
                if saldo >= preco:
                    item['quant'] -= 1
                    saldo = saldo - preco
                    print(f"maq: Pode retirar o produto dispensado \"{item['nome']}\"")
                    print(f"maq: Saldo = {saldo:.2f}€")
                    with open('stock.json', 'w', encoding='utf-8') as f:
                        json.dump(dados, f, ensure_ascii=False, indent=4)
                    return saldo
                else:
                    print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
                    print(f"maq: Saldo = {saldo:.2f}€; Pedido = {preco:.2f}€")
                    return saldo
        print(f"maq: Produto {cod} não existe.")
        return saldo

    elif command_type == 'SALDO':
        print(f"maq: Saldo = {saldo:.2f}€")
        return saldo

    elif command_type == 'SAIR':
        if saldo > 0:
            print(f"maq: Pode retirar o troco: {calcular_troco(saldo)}.")
        print("maq: Até à próxima")
        sys.exit(0)

    else:
        print("maq: Comando inválido.")
        return saldo

def main():
    saldo = 0.0
    with open('stock.json', 'r', encoding='utf-8') as file:
        dados = json.load(file)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"maq: {current_date}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    
    while True:
        comando = input(">> ").upper()
        saldo = handleCommand(comando, dados, saldo)

if __name__ == "__main__":
    main()
