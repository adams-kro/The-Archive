from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import struct
from binascii import crc32

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_CHUNK_TYPE = b"aaaa"
BLOCK_SIZE = 16
PDF_PREFIX_ = b'%PDF-1.4\n%\xd3\xeb\xe9\xe1\n1' # 16 bytes

def derive_key() -> bytes:
    """Derive the AES key from a XOR-ed string."""
    xored_string = "[rh<c8^ey?}ng:el"
    return "".join(chr(ord(char) ^ 11) for char in xored_string).encode()

def read_file_content(file_path: str) -> bytes:
    """Read and pad the content of the file."""
    with open(file_path, "rb") as f:
        return pad(f.read(), BLOCK_SIZE)
    
def embed_and_extract(pdf_path: str, png_path: str):
    """
    This function embeds the contents of a PDF file into a PNG file and then extracts it back.

    It first reads and pads the contents of both the PDF and PNG files. Then, it derives an 
    initialization vector (IV) using the AES-ECB mode on the PNG header, XOR-ed with the PDF prefix. 
    Using this IV and a derived AES key, it encrypts the PDF content and appends it to the PNG content.

    Afterwards, it uses the same IV and key to decrypt the newly formed encrypted PDF content and 
    writes it to 'out.pdf'. This demonstrates a method of concealing data (PDF) within an image file (PNG).
    """
    key = derive_key()

    pdf_content = read_file_content(pdf_path)
    png_content = read_file_content(png_path)

    # Derive the IV from the PDF prefix and PNG header
    plain_pdf_prefix = pdf_content[:BLOCK_SIZE] # PDF prefix is 16 bytes
    png_header = PNG_SIGNATURE + struct.pack(">I", len(pdf_content) - BLOCK_SIZE) + PNG_CHUNK_TYPE
    decrypted_header = AES.new(key, AES.MODE_ECB).decrypt(png_header)
    iv = bytes([decrypted_header[i] ^ plain_pdf_prefix[i] for i in range(BLOCK_SIZE)])
    print(iv)

    # Encrypt the PDF content and append to PNG
    aes_encryption = AES.new(key, AES.MODE_CBC, iv)
    encrypted_pdf = aes_encryption.encrypt(pdf_content)
    encrypted_pdf += struct.pack(">I", crc32(encrypted_pdf[12:]) & 0xffffffff)
    encrypted_pdf += png_content[8:]

    # Decrypt the embedded PDF content
    aes_decryption = AES.new(key, AES.MODE_CBC, iv)
    with open("out.pdf", "wb") as f:
        f.write(aes_decryption.decrypt(pad(encrypted_pdf, BLOCK_SIZE)))

embed_and_extract("source.pdf", "target.png")
