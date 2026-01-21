from cryptography.fernet import Fernet
import json
import os

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
PATH = os.path.dirname(THIS_PATH)


class passManager:
    def encrypt(self, text):
        return text

    def decrypt(self, text):
        return text
