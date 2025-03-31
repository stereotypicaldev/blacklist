import os
import mimetypes
import magic


f = magic.Magic(mime=True)

# Get current file working directory
parent = os.getcwd()
adlists = parent + '/Blacklist/Adlists/Sources'

# Change Directory to Adlists

os.chdir(adlists)

# Ensure current working directory
print("Current working directory: {0}".format(os.getcwd()))

# Gather all sufolder (iterations)
paths = [ f.path for f in os.scandir(os.getcwd()) if f.is_dir() ]
Filetype = {}
Encoding = {}

def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]

for x in paths:
    for filename in os.scandir(x):
        if filename.is_file():
            if mimetypes.guess_type(filename)[0] != 'text/plain':
                set_key(Filetype,x,filename.name)
            if f.from_file(filename) != 'text/plain':
                pass
                # set_key(Encoding,x,filename.name,[f.from_file(filename)])
    break


# By now, we have two types of files...
# Filetype - the file type is wrong and the script won't be able to process it.
# Encoding - the encoding is wrong and the script won't be able to process it.
print(Filetype)
print(Encoding)


# Fix Files?

# Processing


# Create List of Files


# Find ones already processed


# Process the other ones

