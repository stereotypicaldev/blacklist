import subprocess
import sys 
import os 
import pathlib
import time
from pathlib import Path
from datetime import date
import urllib 
    
black_command = " ".join(
    [
        "sqlite3",
        '"/etc/pihole/gravity.db"',
        '"SELECT',
        'domain',
        "FROM",
        "domainlist",
        "WHERE",
        "enabled=1",
        "AND",
        'type=1;"',
    ])

def return_subDirs(subdirectory):
    return [f.name for f in os.scandir(subdirectory) if f.is_dir()]

def create_path(folder,subfolder):
    return Path(os.path.join(folder,subfolder))

# Search Files' Names for Today's Date and return matches  
def count(Date, Files):
    counter = 1
    for N in Files:
        if str(Date) in N:
            counter = counter + 1
    return counter
     
try:
    # Step 1 : Run the black command to Fetch Domains
    blacks = subprocess.check_output(
        black_command, shell=True, executable="/bin/bash", stderr=subprocess.STDOUT
    )
    
    if not blacks:
    
        print("Blacklist is Empty...")
        sys.exit()
    
    else:
        
        # Project Root Directory
        root_directory = dir_path = os.path.dirname(os.path.realpath(__file__))
        
        # Set Search onto Adlists > Sources
        subD = os.path.join(root_directory, "Blacklist", "Adlists","Sources")
        
        # Fetch all Subfolders inside Adlists > Sources
        subF = return_subDirs(subdirectory=subD)
        
        # Sort them so you add to the last One (Iterations)
        selected = sorted(subF)[-1]
        
        # Change Working Directory to Last Source
        last_iteration = create_path(subD,str(selected))
        os.chdir(Path(last_iteration))

        # Step 2 : Get all Txt Files in Current Directory
        TextFiles = [f for f in os.listdir(os.curdir) if f.endswith('.txt')]
        today = date.today().strftime("%d-%m-%Y")
        counter = count(Date=today,Files=TextFiles) 
    
        # Step 3 : Create the File based on BlackDomains (Backup)
    
        # Check if Bytes are Empty - So no domains

        # Create a New Text File (named [Number]. Date inside the folder
        with open('.'.join([str("{:02d}".format(counter)),str(today),'txt']), 'w') as f:
            lines = 0 
                
            for line in blacks.splitlines():
                # Fetch Data by line
                line = str(line.decode()).rstrip().strip()
                # Append to it line by line a formatted domain entry.
                f.write(line + '\n')
                lines  = lines + 1
            # Save the File
            f.close()
                
    # Step 4 - Delete Exact Blacklist 

    delete_command = " ".join([
        "sqlite3",
        '"/etc/pihole/gravity.db"',
        '"DELETE',
        "FROM",
        "domainlist",
        "WHERE",
        'type=1;"',
    ])
    
    # In case blacklist commands is processed...
    if int(lines) > 0:
        # Verify the exact blacklist is nuked.
        time.sleep(3)
        # Delete Exact Blacklist using PiHole Command
        print("Nuking Blacklist using Pi-Hole Interface Command...")
        subprocess.call(["pihole", "-b", "--nuke"]) 
        time.sleep(5)
        print("Nuking Blacklist using Database Command...")
        # Nuke the exact blacklist by using the delete_command (Directly from Database)
        subprocess.call(delete_command,shell=True, executable="/bin/bash")
       
        # Git Add
        
        # Git Commit

        # Git Push
        

        # Git Raw URLS Creator
        base_url = "https://raw.githubusercontent.com/gzachariadis/Pi-Hole/main/Blacklist/Adlists/Sources/"
        directory = urllib.parse.quote(selected)
        filename = str('.'.join([str("{:02d}".format(counter)),str(today),'txt']))
        
        whole_url = base_url + '/' + str(directory) + '/' + filename
        
        print(whole_url)
        
        ## Add the URL into the domain list
        
        add_command = " ".join(
        [
            "sqlite3",
            '"/etc/pihole/gravity.db"',
            '"INSERT',
            "INTO",
            "adlist",
            "(address,",
            "enabled,",
            "comment)",
            "VALUES",
            "('{whole_url}',",
            "1,"
            "'{filename}');",
            '"'
        ])
        
        # Execute the Command 
        subprocess.call(add_command,shell=True, executable="/bin/bash")
        print("Appended generated File into the ADlists Database...")
    else:
        print("The produced text file is empty or some error occurred.")
        sys.exit()
        
except subprocess.CalledProcessError as cpe:
    blacks = cpe.output
    print("Error when extracting blacklist...")
