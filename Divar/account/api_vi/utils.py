from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
import threading
import hashlib
import numpy as np



class customRefreshToken(RefreshToken):
    # lifetime = timedelta(minutes=5)
    @classmethod
    def for_user(cls, user, code):
        token = super().for_user(user)
        print('==================',hash_user_code(code))
        token['hash_code'] = hash_user_code(code)
        return token

# this part should move to utils.py
def get_tokens_for_user(user, code):
    refresh = customRefreshToken.for_user(user, code)
    access = refresh.access_token
    return str(refresh), str(access)


class EmailThreading(threading.Thread):
    def __init__(self, message):
        threading.Thread.__init__(self)
        self.message = message
        
    def run(self):
        self.message.send()


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



def create_verification_code():
    return np.random.randint(10000, 99999)