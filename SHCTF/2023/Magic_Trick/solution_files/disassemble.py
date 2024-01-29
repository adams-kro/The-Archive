import dis
import marshal

# Path to the .pyc file
pyc_path = "magic_extracted/magic.pyc"

# Open the .pyc file in binary read mode
with open(pyc_path, "rb") as f:
    # Skip the first 16 bytes (magic number and timestamp)
    f.read(16)
    # Read the rest of the file, which contains the marshalled code object
    code_obj = marshal.load(f)

# Disassemble the code object
dis.dis(code_obj)

