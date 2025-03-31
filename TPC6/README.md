# TPC6 - Trabalho Prático 6 (26/03/2024)

- **Nome:** Gonçalo da Silva Alves
- **Nº:** A104079
- **Foto:** <br/> <img src="pic.jpeg" alt="Profile picture" width="188" height="250"/>

## Resumo
Este trabalho, realizado no âmbito da UC de Processamento de Linguagens, implementa um analisador léxico e sintático para processar expressões aritméticas. O programa é capaz de reconhecer e calcular expressões que incluem:
- Números inteiros
- Operadores: +, -, *, /
- Parênteses para controlar precedência
- Expressões aninhadas

## Componentes Implementados

### 1. Analisador Léxico (`expar_analex.py`)
- Define tokens para números, operadores e parênteses
- Processa a entrada e gera uma sequência de tokens

### 2. Analisador Sintático (`expar_anasin.py`)
- Implementa uma gramática que respeita a precedência dos operadores:
  ```
  Exp   -> Term ExpR
  ExpR  -> + Term ExpR | - Term ExpR | ε
  Term  -> Factor TermR
  TermR -> * Factor TermR | / Factor TermR | ε
  Factor-> NUM | ( Exp )
  ```
- Calcula o resultado das expressões recursivamente
- Respeita a precedência dos operadores (* e / antes de + e -)

### 3. Programa Principal (`expar_program.py`)
- Interface para o utilizador
- Permite calcular múltiplas expressões
- Apresenta os resultados de forma clara

## Lista de Resultados
- [expar_analex.py](expar_analex.py) - Analisador léxico
- [expar_anasin.py](expar_anasin.py) - Analisador sintático
- [expar_program.py](expar_program.py) - Programa principal

## Utilização
1. Executar o programa:
   ```sh
   python3 expar_program.py
   ```
2. Inserir uma expressão aritmética, por exemplo:
   ```
   (9-2)*(13-4)
   ```
