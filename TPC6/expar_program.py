from expar_anasin import rec_Parser

linha = input("Introduza uma expressão aritmética: ")
result = rec_Parser(linha)
print("Resultado: " + str(result))