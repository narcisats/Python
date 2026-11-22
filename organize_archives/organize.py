import os
import hashlib
import shutil
from PIL import Image
import imagehash
from tqdm import tqdm
from docx import Document
import PyPDF2

def calculate_perceptual_hash(image_path):
    try:
        image = Image.open(image_path)
        return imagehash.average_hash(image)
    except Exception as e:
        print(f"Erro ao processar imagem {image_path}: {e}")
        return None

def calculate_file_hash(file_path, chunk_size=8192):
    hash_algo = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hash_algo.update(chunk)
        return hash_algo.hexdigest()
    except Exception as e:
        print(f"Erro ao processar arquivo {file_path}: {e}")
        return None

def find_duplicates(root_folder):
    hash_dict = {}
    duplicates = []

    total_files = sum(len(files) for _, _, files in os.walk(root_folder))

    with tqdm(total=total_files, desc="Calculando hashes", unit="arquivo") as pbar:
        for root, _, files in os.walk(root_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[-1].lower()

                if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
                    file_hash = calculate_perceptual_hash(file_path)
                else:
                    file_hash = calculate_file_hash(file_path)

                if file_hash is None:
                    pbar.update(1)
                    continue

                if file_hash in hash_dict:
                    duplicates.append(file_path)
                else:
                    hash_dict[file_hash] = file_path

                pbar.update(1)

    return duplicates

def move_file(file_path, destination_folder):
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, file_name)

    if os.path.exists(destination_path):
        base, extension = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(destination_path):
            destination_path = os.path.join(destination_folder, f"{base}_{counter}{extension}")
            counter += 1

    shutil.move(file_path, destination_path)
    return file_path, destination_path  # Adicionado para retornar a origem e o destino

def move_duplicates(duplicates, root_folder, duplicates_folder, movements):
    if not os.path.exists(duplicates_folder):
        os.makedirs(duplicates_folder)

    with tqdm(total=len(duplicates), desc="Movendo duplicatas", unit="arquivo") as pbar:
        for file_path in duplicates:
            relative_path = os.path.relpath(file_path, root_folder)
            destination_path = os.path.join(duplicates_folder, relative_path)

            destination_dir = os.path.dirname(destination_path)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            original_path, new_path = move_file(file_path, destination_dir)
            movements.append((original_path, new_path))
            print(f"Movido {original_path} para {new_path}")  # Imprime o movimento realizado
            pbar.update(1)

def organize_files(root_folder, destination_folder, movements):
    file_types = {
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

    for file_type, extensions in file_types.items():
        folder_path = os.path.join(destination_folder, file_type)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    total_files = sum(len(files) for _, _, files in os.walk(root_folder))

    with tqdm(total=total_files, desc="Organizando arquivos", unit="arquivo") as pbar:
        for root, _, files in os.walk(root_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[-1].lower()

                moved = False
                for file_type, extensions in file_types.items():
                    if file_ext in extensions:
                        folder_path = os.path.join(destination_folder, file_type)
                        original_path, new_path = move_file(file_path, folder_path)
                        movements.append((original_path, new_path))
                        print(f"Movido {original_path} para {new_path}")  # Imprime o movimento realizado
                        moved = True
                        break

                if not moved:
                    # Se o tipo de arquivo não for reconhecido, mova para a pasta 'others'
                    other_folder_path = os.path.join(destination_folder, 'others')
                    if not os.path.exists(other_folder_path):
                        os.makedirs(other_folder_path)
                    original_path, new_path = move_file(file_path, other_folder_path)
                    movements.append((original_path, new_path))
                    print(f"Movido {original_path} para {new_path}")  # Imprime o movimento realizado

                pbar.update(1)

def main():
    # Diretório de origem e destino
    source_dir = 'D:\\Nova pasta (3)\\CAIO\\CAIO.HONORATO\\Desktop'
    dest_dir = 'D:\\Arquivos'
    duplicates_dir = os.path.join(dest_dir, 'duplicates')

    movements = []  # Lista para armazenar movimentos de arquivos

    duplicates = find_duplicates(source_dir)
    move_duplicates(duplicates, source_dir, duplicates_dir, movements)
    organize_files(source_dir, dest_dir, movements)

    print("Os arquivos foram organizados e as duplicatas foram movidas para a pasta especificada.")
    print("\nMovimentos realizados:")
    for original, new in movements:
        print(f"Origem: {original} -> Destino: {new}")

if __name__ == "__main__":
    main()
