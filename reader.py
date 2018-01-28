import sys, os, shutil

def getWords(filename):
    """
    Checks txt for the last date and time checked.
    
    :returns: the date
    """ 
    try:
        with open("./Transcribe/"+filename, 'r') as trans_file:
            for tex in trans_file:
                result = tex.strip('[]').replace('\'', '').split(',')
                print(result)
            trans_file.close()
    except IOError as e:
        print ("I/O error({0}): {1}").format(e.errno, e.strerror)
    
    return result

def getFiles():
    """
    Checks txt for the last date and time checked.
    
    :returns: the date
    """ 
    files = []
    
    try:
        for filename in os.listdir("./Transcribe/"):
            files.append(filename)
    except IOError as e:
        print ("I/O error({0}): {1}").format(e.errno, e.strerror)
    
    return files
    
def removeTrans():
    #https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
    folder = "./Transcribe/"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    getWords()
    print(getFiles())