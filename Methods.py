import os

def subpath(folder_path,level=2):
    paths = os.listdir(folder_path)
    new_path=[]
    if level == 2:
        for path in paths:
            filename=os.path.join(folder_path,path)
            if not os.path.isdir(filename):
                if filename.endswith('.xlsm'): #or filename.endswith('.xlsx'):
                    if not filename.startswith('Exception'):
                        new_path.append(path)
            else:
                paths2 = os.listdir(filename)
                for path2 in paths2:
                    filename2 = os.path.join(filename, path2)
                    if filename2.endswith('.xlsm'):# or filename2.endswith('.xlsm'):
                        if not os.path.basename(filename2).startswith('Exception'):
                            new_path.append(os.path.join(path, path2))

    if level ==1:
        for path in paths:
            filename=os.path.join(folder_path,path)
            if not os.path.isdir(filename):
                if filename.endswith('.xlsm'):#or filename.endswith('.xlsm'):
                    new_path.append(path)
    return new_path

def link_msps(path,epath,efile_name,tail=2):
    # get file names
    filenames = os.listdir(path)
    if tail == 1:
        per='.msp'
    if tail ==2:
        per='.msp.msp'
    # create export file
    file = open(epath +'/' + efile_name, 'w+', encoding="utf-8")
    # export
    for file_name in filenames:
        file_path = path + '/'
        file_path = file_path + file_name
        if per in file_name and file_name != efile_name:
            for line in open(file_path,errors='ignore'):
                file.writelines(line)
            if line != '\n':
                file.write('\n')
    file.close()