## Writing files to zip
import zipfile, shutil, os

def main():

    dest_path = '.\\download\\aionfilter.zip'
    file_name = 'aionfilter.zip'

    dest_na_file = '.\\download\\aionfilterchat.dat'
    file_na = 'aionfilterchat.dat'
    dest_eu_file = '.\\download\\aionfilterline.dat'
    file_eu = 'aionfilterline.dat'

    zip = 'aionfilter_load.zip'
    pak = 'aionfilter_load.pak'

    shutil.copy2(dest_na_file, file_na)
    shutil.copy2(dest_eu_file, file_eu)
    shutil.copy2(dest_path, file_name)

    # ZIP > PAK
    with zipfile.ZipFile(zip, 'w') as file:
        file.write(file_na)
        file.write(file_eu)
    os.rename(zip, pak)

    # Opening the 'Zip' in writing mode
    with zipfile.ZipFile(file_name, 'w') as file:
        # write mode overrides all the existing files in the 'Zip.'
        # you have to create the file which you have to write to the 'Zip.'
        file.write(pak)
        print('Novo zip criado.')

    # opening the 'Zip' in reading mode to check
    with zipfile.ZipFile(file_name, 'r') as file:
        print('Arquivos depois.')
        print(file.namelist())
    
    shutil.copy2(file_name, dest_path)
    print('Novo arquivo zip copiado para a pasta "download".')

    os.remove(file_name)
    os.remove(file_na)
    os.remove(file_eu)
    os.remove(pak)
    print('Arquivos temporários removidos.')

if __name__ == '__main__': main()