from expar_analex import lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado: ", simb)

def rec_term(expected):
    global prox_simb
    if prox_simb.type == expected:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)

def rec_Factor():
    global prox_simb
    if prox_simb.type == 'NUM':
        value = int(prox_simb.value)
        prox_simb = lexer.token()
        return value
    elif prox_simb.type == 'LPAREN':
        prox_simb = lexer.token()
        value = rec_Exp()
        if prox_simb.type == 'RPAREN':
            prox_simb = lexer.token()
            return value
    else:
        parserError(prox_simb)
        return None

def rec_TermR(left):
    global prox_simb
    if prox_simb is None or prox_simb.type not in ['TIMES', 'DIVIDE']:
        return left
    
    if prox_simb.type == 'TIMES':
        rec_term('TIMES')
        right = rec_Factor()
        return rec_TermR(left * right)
    elif prox_simb.type == 'DIVIDE':
        rec_term('DIVIDE')
        right = rec_Factor()
        return rec_TermR(left / right)

def rec_Term():
    global prox_simb
    left = rec_Factor()
    return rec_TermR(left)

def rec_ExpR(left):
    global prox_simb
    if prox_simb is None or prox_simb.type not in ['PLUS', 'MINUS']:
        return left
    
    if prox_simb.type == 'PLUS':
        rec_term('PLUS')
        right = rec_Term()
        return rec_ExpR(left + right)
    elif prox_simb.type == 'MINUS':
        rec_term('MINUS')
        right = rec_Term()
        return rec_ExpR(left - right)

def rec_Exp():
    global prox_simb
    left = rec_Term()
    return rec_ExpR(left)

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    result = rec_Exp()
    return result