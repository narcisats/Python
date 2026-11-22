from deep_translator import GoogleTranslator
import re
from tqdm import tqdm

# Lista de nomes próprios a serem tratados como exceção
EXCLUDED_PROPER_NOUNS = {'Earn', 'Bow', 'Ratee',}  # Adicione mais nomes próprios conforme necessário

# Função para traduzir o texto mantendo a estrutura do arquivo SRT
def translate_text_srt(text, target_language='pt'):
    lines = text.splitlines()
    translated_lines = []
    buffer = []
    
    for line in tqdm(lines, desc='Traduzindo legendas', unit='linha'):
        if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            if buffer:
                translated_text = translate_text(' '.join(buffer), target_language)
                translated_text = replace_excluded_proper_nouns(translated_text)
                translated_lines.append(translated_text)
                buffer = []
            translated_lines.append(line)
        elif re.match(r'^\d+$', line):
            if buffer:
                translated_text = translate_text(' '.join(buffer), target_language)
                translated_text = replace_excluded_proper_nouns(translated_text)
                translated_lines.append(translated_text)
                buffer = []
            translated_lines.append(line)
        else:
            if line.strip():
                buffer.append(line.strip())
            else:
                if buffer:
                    translated_text = translate_text(' '.join(buffer), target_language)
                    translated_text = replace_excluded_proper_nouns(translated_text)
                    translated_lines.append(translated_text)
                    buffer = []
                translated_lines.append(line)
    
    if buffer:
        translated_text = translate_text(' '.join(buffer), target_language)
        translated_text = replace_excluded_proper_nouns(translated_text)
        translated_lines.append(translated_text)
    
    return '\n'.join(translated_lines)

# Função para traduzir o texto
def translate_text(text, target_language='pt'):
    try:
        # Traduz o texto completo
        translation = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translation if translation else text
    except Exception as e:
        print(f"Erro na tradução de '{text}': {e}")
        return text

# Função para substituir os nomes próprios na tradução
def replace_excluded_proper_nouns(text):
    # Verifica se cada nome próprio original ou sua forma traduzida está presente no texto e faz a substituição
    for noun in EXCLUDED_PROPER_NOUNS:
        # Primeiramente, substituir a tradução do nome próprio se estiver presente
        translated_noun = GoogleTranslator(source='auto', target='en').translate(noun)
        text = re.sub(r'\b' + re.escape(translated_noun) + r'\b', noun, text, flags=re.IGNORECASE)
        # Depois, substituir o nome próprio original se estiver presente
        text = re.sub(r'\b' + re.escape(noun) + r'\b', noun, text, flags=re.IGNORECASE)
    return text

# Função para ler e traduzir o conteúdo do arquivo SRT
def translate_file(input_file, output_file, target_language='pt'):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    translated_text = translate_text_srt(text, target_language)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(translated_text)

# Exemplos de uso
input_file = 'C:\\Users\\sogam\\OneDrive\\Desktop\\teste legenda\\tsou\\EP 08\\Legendas Oficiais\\en\\[Eng Sub] ใจซ่อนรัก The Secret Of Us EP.8 ตอนที่ 1 4 (ตอนจบ) 12-08-67 3Plus [English (United Kingdom)] [GetSubs.cc].srt'  # Nome do arquivo de entrada
output_file = 'C:\\Users\\sogam\\OneDrive\\Desktop\\teste legenda\\tsou\\EP 08\\ใจซ่อนรัก The Secret Of Us EP.8 ตอนที่ 1 4 (ตอนจบ) 12-08-67  3Plus.srt'  # Nome do arquivo de saída
translate_file(input_file, output_file, 'pt')

print(f'Texto traduzido salvo em {output_file}')