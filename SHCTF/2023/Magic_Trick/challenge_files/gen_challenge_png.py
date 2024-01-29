from Cryptodome.Cipher import AES


# This script generates the challenge png by encrypting the magic out.pdf we created

algo = AES.new(b'Pyc7h3Unr4vel1ng', AES.MODE_CBC, b'\x14mwJ\x90[\x8ar:\xe1\xccY\xbc\xb5\x8b\xa1')

with open("out.pdf", "rb") as f:
    d = f.read()

d = algo.encrypt(d)

with open("canvas.png", "wb") as f:
    f.write(d)