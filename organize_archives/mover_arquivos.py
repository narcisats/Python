# Importação de bibliotecas
import os
import shutil
import hashlib
from tqdm import tqdm

# Diretórios de origem e destino
source_dir = 'origem'
dest_dir = 'destino'
duplicate_dir = os.path.join(dest_dir, 'duplicados')  # Nova pasta para duplicados
log_file_path = os.path.join(duplicate_dir, 'relatorio_duplicados.txt')

# Definição das pastas e extensões
folders = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'texts': ['.txt', '.md'],
    'pdfs': ['.pdf'],
    'docs': ['.doc', '.docx', '.odt'],
    'spreadsheets': ['.xls', '.xlsx', '.csv'],
    'presentations': ['.ppt', '.pptx'],
    'videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
    'audio': ['.mp3', '.wav', '.aac', '.flac', '.wma'],
    'archives': ['.zip', '.rar', '.tar', '.gz'],
    'scripts': ['.py', '.js', '.sh', '.bat'],
    'reporting': ['.rdl', '.pbix'],
    'subtitle': ['.srt'],
    'index': ['.idx'],
    'html': ['.html'],
    'jason file': ['.json'],
    'logs': ['.log'],
    'xml': ['.xml'],
    'php': ['.php'],
    'exe': ['.exe'],
    'dll': ['.dll'],
    'css': ['.css'],
    'others': []
}

# Mapeamento de extensões para pastas
extension_to_folder = {ext: folder for folder, exts in folders.items() for ext in exts}

# Criar todas as pastas de destino
for folder in list(folders.keys()) + ['duplicados']:
    os.makedirs(os.path.join(dest_dir, folder), exist_ok=True)

# Função para gerar hash SHA256 do conteúdo do arquivo
def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

# Função para gerar nome único se já existir
def get_unique_filename(dest_path):
    base, ext = os.path.splitext(dest_path)
    counter = 1
    new_dest_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_dest_path):
        counter += 1
        new_dest_path = f"{base}_{counter}{ext}"
    return new_dest_path

# Função para organizar arquivos com verificação de duplicatas e log
def organize_files(source_dir, dest_dir):
    hashes = {}
    total_files = sum(len(files) for _, _, files in os.walk(source_dir))
    duplicados_encontrados = []

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        with tqdm(total=total_files, desc="Organizando arquivos") as pbar:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_hash = get_file_hash(file_path)
                    _, ext = os.path.splitext(file)
                    folder = extension_to_folder.get(ext.lower(), 'others')

                    if file_hash in hashes:
                        # Arquivo duplicado
                        dup_folder = os.path.join(duplicate_dir, folder)
                        os.makedirs(dup_folder, exist_ok=True)
                        dest_path = os.path.join(dup_folder, file)
                        dest_path = get_unique_filename(dest_path)
                        shutil.move(file_path, dest_path)

                        log_file.write(f"[DUPLICADO] {file_path} => {dest_path}\n")
                        duplicados_encontrados.append(dest_path)
                    else:
                        # Arquivo novo
                        dest_path = os.path.join(dest_dir, folder, file)
                        if os.path.exists(dest_path):
                            dest_path = get_unique_filename(dest_path)
                        shutil.move(file_path, dest_path)
                        hashes[file_hash] = dest_path

                    pbar.update(1)

    print(f"\nOrganização finalizada! {len(duplicados_encontrados)} duplicado(s) movido(s) para: {duplicate_dir}")
    print(f"Relatório salvo em: {log_file_path}")

# Executa
organize_files(source_dir, dest_dir)