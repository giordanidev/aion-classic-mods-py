## Writing files to zip
import zipfile, shutil, os

def main():

    file_name = '.\\tests\\aionfilter.zip'
    dest_path = '.\\download\\aionfilter.zip'

    # Opening the 'Zip' in writing mode
    with zipfile.ZipFile('.\\tests\\aionfilterchat_load.zip', 'w') as file:
        # write mode overrides all the existing files in the 'Zip.'
        # you have to create the file which you have to write to the 'Zip.'
        file.write('.\\download\\aionfilterchat.dat')
        print('Novo arquivo "aionfilterchat_load.zip" criado.')

    # opening the 'Zip' in reading mode to check
    with zipfile.ZipFile('.\\tests\\aionfilterchat_load.zip', 'r') as file:
        print(file.namelist())
    
    os.rename('.\\tests\\aionfilterchat_load.zip', '.\\tests\\aionfilterchat_load.pak')
    print('Arquivo "aionfilterchat_load.pak" renomeado.')

        # Opening the 'Zip' in writing mode
    with zipfile.ZipFile('.\\tests\\aionfilterline_load.zip', 'w') as file:
        # write mode overrides all the existing files in the 'Zip.'
        # you have to create the file which you have to write to the 'Zip.'
        file.write('.\\download\\aionfilterline.dat')
        print('Novo arquivo "aionfilterline_load.zip" criado.')

    # opening the 'Zip' in reading mode to check
    with zipfile.ZipFile('.\\tests\\aionfilterline_load.zip', 'r') as file:
        print(file.namelist())

    os.rename('.\\tests\\aionfilterline_load.zip', '.\\tests\\aionfilterline_load.pak')
    print('Arquivo "aionfilterline_load.pak" renomeado.')

    # Opening the 'Zip' in writing mode
    with zipfile.ZipFile(file_name, 'w') as file:
        # write mode overrides all the existing files in the 'Zip.'
        # you have to create the file which you have to write to the 'Zip.'
        file.write('.\\tests\\aionfilterchat_load.pak')
        file.write('.\\tests\\aionfilterline_load.pak')
        file.write('.\\download\\aionfilterchat.dat')
        file.write('.\\download\\aionfilterline.dat')
        print('Novo zip criado.')

    # opening the 'Zip' in reading mode to check
    with zipfile.ZipFile(file_name, 'r') as file:
        print(file.namelist())
    
    shutil.copy2(file_name, dest_path)
    print('Arquivo temporário copiado para a pasta "download".')

    os.remove(file_name)
    os.remove('.\\tests\\aionfilterchat_load.pak')
    os.remove('.\\tests\\aionfilterline_load.pak')
    print('Arquivos temporários removidos.')

if __name__ == '__main__': main()