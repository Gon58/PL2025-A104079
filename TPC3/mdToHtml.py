import sys
import re

def process_line(line):
    # Cabeçalhos
    header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
    if header_match:
        level = len(header_match.group(1))
        return f"<h{level}>{header_match.group(2)}</h{level}>"

    # Bold
    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
    
    # Itálico
    line = re.sub(r'\*(.+?)\*', r'<i>\1</i>', line)

    # Lista numerada
    ol_match = re.match(r'^\d+\.\s+(.+)$', line)
    if ol_match:
        return f"<li>{ol_match.group(1)}</li>"

    # Lista não ordenada
    ul_match = re.match(r'^\s*[\-\*]\s+(.+)$', line)
    if ul_match:
        return f"<li>{ul_match.group(1)}</li>"

    # Links
    line = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', line)

    # Imagens
    line = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1"/>', line)

    # Parágrafos
    if line.strip():
        return f"<p>{line}</p>"
    
    return ""

def md_to_html(input_text):
    html_lines = []
    in_list = False
    
    lines = input_text.split('\n')
    
    for line in lines:
        processed = process_line(line.strip())
        
        if processed.startswith('<li>'):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
        elif in_list:
            html_lines.append('</ul>')
            in_list = False
            
        if processed:
            html_lines.append(processed)
    
    if in_list:
        html_lines.append('</ul>')
        
    return '\n'.join(html_lines)

def main():
    if len(sys.argv) != 2:
        print("Número de argumentos inválido")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as file:
            content = file.read()
            
        html_content = md_to_html(content)
        
        output_file = sys.argv[1].rsplit('.', 1)[0] + '.html'
        with open(output_file, 'w') as file:
            file.write(html_content)
            
        print(f"Conversão concluída. Ficheiro guardado: {output_file}")
        
    except FileNotFoundError:
        print(f"Erro: Não foi possível encontrar o ficheiro '{sys.argv[1]}'")
        sys.exit(1)

if __name__ == "__main__":
    main()