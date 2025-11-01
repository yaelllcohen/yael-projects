import rsa
import os


class RsaKeys:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(2048)
        self.FORMAT = "utf-8"



    def generate_keys(self):
        os.makedirs("keys", exist_ok=True)  # יוצר את התיקייה אם לא קיימת


        with open("keys/public_key.pem", "wb") as f:
            f.write(self.public_key.save_pkcs1('PEM'))

        with open("keys/private_key.pem", "wb") as f:
            f.write(self.private_key.save_pkcs1('PEM'))



    def load_keys(self):

        with open("keys/public_key.pem", "rb") as f:
            self.public_key = rsa.PublicKey.load_pkcs1(f.read())

        with open("keys/private_key.pem", "rb") as f:
            self.private_key = rsa.PrivateKey.load_pkcs1(f.read())

        return self.public_key, self.private_key



    def encrypt(self, msg, key):
        return rsa.encrypt(msg.encode(self.FORMAT), key)


    def decrypt(self, cipher_text, key):
        try:
            return rsa.decrypt(cipher_text, key).decode(self.FORMAT)
        except:
            return False








    def sign_sha256(self, msg, key):
        return rsa.sign(msg.encode(self.FORMAT), key, 'SHA-256')


    def verify_shal(self, msg, signature, key):
        try:
            return rsa.verify(msg.encode(self.FORMAT),signature, key) == 'SHA-256'
        except:
            return False


if __name__ == "__main__":
    keys = RsaKeys()

    keys.generate_keys()
    keys.public_key, keys.private_key = keys.load_keys()

    message = input("enter a message: ")
    cipher_text = keys.encrypt(message,keys.public_key)

    signature = keys.sign_sha256(message, keys.private_key)

    plain_text = keys.decrypt(cipher_text, keys.private_key)

    print(f"cipher text: {cipher_text}")
    print(f"signature: {signature}")

    if plain_text:
        print(f"plain text: {plain_text}")
    else:
        print("couldn't decrypt the message")

    if keys.verify_shal(plain_text, signature,keys.public_key):
        print("signature verified")
    else:
        print('could not verify the message signature')


