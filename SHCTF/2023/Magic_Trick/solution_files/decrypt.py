from Cryptodome.Cipher import AES

algo = AES.new(b'Pyc7h3Unr4vel1ng', AES.MODE_CBC, b'\x14mwJ\x90[\x8ar:\xe1\xccY\xbc\xb5\x8b\xa1')

with open("canvas.png", "rb") as f:
    d = f.read()

d = algo.decrypt(d)

with open("dec-" + "target.pdf", "wb") as f:
    f.write(d)