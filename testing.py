import hashlib

def hash_user_code(code):
    # Ensure the user_id is in string format
    user_id_str = str(code)
    
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    
    # Encode the user ID to bytes and update the hash object
    hash_object.update(user_id_str.encode('utf-8'))
    
    # Get the hexadecimal representation of the hash
    hashed_user_code = hash_object.hexdigest()
    
    return hashed_user_code


# print(hash_user_code(12345))
# 5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5
# 5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5

import numpy as np
def create_verification_code():
    return np.random.randint(10000, 99999)
    

print(create_verification_code())