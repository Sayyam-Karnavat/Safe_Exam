from deploy_file import Blockchain
import json
import string
import random

def generate_password(length=6):
    #  Define the characters that can be used in the password
    characters = string.ascii_letters + string.punctuation
    # Randomly choose characters and join them to form a password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_users( users_names_list ):
    all_valid_user = {}
    for user in users_names_list:
        valid_user = {
            f"{user}":{
                "userID":user,
            "password" : generate_password()
            }
        }
        all_valid_user.update(valid_user)

    with open("valid_users.json" ,"w") as f:
        json.dump(obj=all_valid_user , fp=f)
        f.close()
    
    return all_valid_user

if  __name__ == "__main__":
    user_names_list = ["admin","sanyam","drashti"]
    generate_users(users_names_list=user_names_list)
