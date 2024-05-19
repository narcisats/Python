import os
import shutil

# defina o diretorio de origem e destino
source_dir = 'caminho/para/diretorio/origem.'
dest_dir = 'caminho/para/diretorio/destino.'

# cria pastas de destino se nao existirem
folders = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'texts': ['.txt', '.md'],
    'pdfs': ['.pdf'],
    'docs': ['.doc', '.docx', '.odt'],
    'spreadsheets': ['.xls', '.xlsx', '.csv'],
    'presentations': ['.ppt', '.pptx'],
    'videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
    'audio': ['.mp3', '.wav', '.aac', '.flac'],
    'archives': ['.zip', '.rar', '.tar', '.gz'],
    'scripts': ['.py', '.js', '.sh', '.bat'],
    'others': []  # Para todos os outros tipos de arquivo
}

for folder in folders.keys():
    os.makedirs(os.path.join(dest_dir, folder), exist_ok=True)

# mapeamento de extensoes para pastas
extension_to_folder = {}
for folder, extensions in folders.items():
    for extension in extensions:
        extension_to_folder[extension] = folder

# funcao para mover arquivos para as pastas correspondentes
def organize_files(source_dir, dest_dir):
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path):
            _, ext = os.path.splitext(item)
            ext = ext.lower()
            folder = extension_to_folder.get(ext, 'others')
            shutil.move(item_path, os.path.join(dest_dir, folder, item))
        elif os.path.isdir(item_path):
            organize_files(item_path, dest_dir)

# organizar os arquivos
organize_files(source_dir, dest_dir)

print("Arquivos organizados com sucesso!")