# check if file exsits

import os

from get_elsys_team import Teams

DIR = "certificates"

def check_if_file_exists (file_name):
    if os.path.isfile(file_name):
        return True
    else:
        return False
    
def check_certificates ():
    db = Teams()
    
    for i in range(1, 63 + 1):
        team = db.get_team_emails(i)
        for member in team:
            if not check_if_file_exists(f"{DIR}/{member[1]}.png"):
                print(f"Certificate for ({i}) \"{member[1]}\" does not exist!")
                print(f"EXPECTED: {DIR}/{member[1]}.png")
                return False
        
    
    print("All certificates exist!")

check_certificates()