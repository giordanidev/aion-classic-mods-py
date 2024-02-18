## Writing files to zip
import zipfile, shutil, os

def main():

    dest_path = '.\\download\\aionfilter.zip'
    file_name = 'aionfilter.zip'
    dest_na_file = '.\\download\\aionfilterchat_load.dat'
    na_file = 'aionfilterchat_load.dat'
    dest_eu_file = '.\\download\\aionfilterline_load.dat'
    eu_file = 'aionfilterline_load.dat'

    shutil.copy2(dest_na_file, na_file)
    shutil.copy2(dest_eu_file, eu_file)
    shutil.copy2(dest_path, file_name)

    # opening the 'Zip' in reading mode to check
    with zipfile.ZipFile(file_name, 'r') as file:
        print('Arquivos antes!')
        print(file.namelist())

    # Opening the 'Zip' in writing mode
    with zipfile.ZipFile(file_name, 'w') as file:
        # write mode overrides all the existing files in the 'Zip.'
        # you have to create the file which you have to write to the 'Zip.'
        file.write(na_file)
        file.write(eu_file)
        print('Novo zip criado.')

    # opening the 'Zip' in reading mode to check
    with zipfile.ZipFile(file_name, 'r') as file:
        print('Arquivos depois.')
        print(file.namelist())
    
    shutil.copy2(file_name, dest_path)
    print('Novo arquivo zip copiado para a pasta "download".')

    os.remove(file_name)
    os.remove(na_file)
    os.remove(eu_file)
    print('Arquivos temporários removidos.')

if __name__ == '__main__': main()