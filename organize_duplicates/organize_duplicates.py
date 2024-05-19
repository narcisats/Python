# importacao de bibliotecas
import os
import hashlib
import shutil

# funcao de calculo de hash
def calculate_hash(file_path, chunk_size=8192):
    hash_algo = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

# funcao para encontrar arquivos duplicados
def find_duplicates(root_folder):
    hash_dict = {}
    duplicates = []

    for root, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)
            if file_hash in hash_dict:
                duplicates.append(file_path)
            else:
                hash_dict[file_hash] = file_path

    return duplicates

# funcao para mover arquivos duplicados
def move_duplicates(duplicates, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for file_path in duplicates:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_folder, file_name)
        
        if os.path.exists(destination_path):
            base, extension = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(destination_path):
                destination_path = os.path.join(destination_folder, f"{base}_{counter}{extension}")
                counter += 1
        
        shutil.move(file_path, destination_path)
        print(f"Movido {file_path} para {destination_path}")
# funcao de ponto de entrada
def main():
    root_folder = input("Digite o caminho para a pasta raiz: ")
    destination_folder = os.path.join(root_folder, "duplicatas")

    duplicates = find_duplicates(root_folder)
    move_duplicates(duplicates, destination_folder)
    print("Os arquivos duplicados foram movidos para a pasta 'duplicatas'.")

# execucao do script
if __name__ == "__main__":
    main()
