# import zipfile

# zip_obj=zipfile.ZipFile('unzip_me_for_instructions.zip','r')
# zip_obj.extractall("extracted_content")

import os
import re

path="C:\\Users\\Alex\\Documents\\Projects\\Complete-Python-3-Bootcamp-master\\12-Advanced Python Modules\\08-Advanced-Python-Module-Exercise\\extracted_content"

result=os.listdir(path)
print(result)

for folder , sub_folders , files in os.walk(path):  
    for f in files:
        if f=="Instructions.txt":
            continue
        file = open(folder + '\\' + f,'r')
        text=file.read()
        result=re.search(r'\d{3}-\d{3}-\d{4}',text)
        if result:
            print(f'Found number: {result.group()} in file: {f}')
