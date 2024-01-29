

# 56 LOAD_CONST               8 (b'%PDF-1.4\n%\xd3\xeb\xe9\xe1\n1')
# 58 STORE_NAME              10 (PDF_PREFIX_)

from Cryptodome.Cipher import AES
key = b"Pyc7h3Unr4vel1ng"

canvas_header = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x75\xc0\x61\x61\x61\x61'
pdf_prefix = b'%PDF-1.4\n%\xd3\xeb\xe9\xe1\n1'

decrypted_header = AES.new(key, AES.MODE_ECB).decrypt(canvas_header)
iv = bytes([decrypted_header[i] ^ pdf_prefix[i] for i in range(16)])

print(iv)