# Importação de bibliotecas
import os
import shutil
from tqdm import tqdm

# Diretório de origem e destino
source_dir = 'Inserir caminho da pasta aqui'
dest_dir = 'Inserir caminho da pasta aqui'  

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
    'reporting':['.rdl','.pbix'],
    'others': []  # Para todos os outros tipos de arquivo
}

# Mapeamento de extensões para pastas
extension_to_folder = {ext: folder for folder, exts in folders.items() for ext in exts}

# Criação das pastas de destino se não existirem
for folder in folders.keys():
    os.makedirs(os.path.join(dest_dir, folder), exist_ok=True)

# Função para gerar um novo nome de arquivo se já existir
def get_unique_filename(dest_path):
    base, ext = os.path.splitext(dest_path)
    counter = 1
    new_dest_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_dest_path):
        counter += 1
        new_dest_path = f"{base}_{counter}{ext}"
    return new_dest_path

# Função para mover arquivos para as pastas correspondentes
def organize_files(source_dir, dest_dir):
    total_files = sum(len(files) for _, _, files in os.walk(source_dir))
    with tqdm(total=total_files, desc="Organizando arquivos") as pbar:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                folder = extension_to_folder.get(ext.lower(), 'others')
                dest_path = os.path.join(dest_dir, folder, file)
                
                if os.path.exists(dest_path):
                    dest_path = get_unique_filename(dest_path)
                
                shutil.move(file_path, dest_path)
                pbar.update(1)

# Organização dos arquivos
organize_files(source_dir, dest_dir)

print("Arquivos organizados com sucesso!")
