import hashlib
import base64
passw = "peter"

# Step 1: Hash 'peter' with MD5

encoded_passw = hashlib.md5(passw.encode()).hexdigest()  # Get hex stringprint(f"MD5 Hash (Hex): {encoded_passw}")# Step 2: Convert hex to raw bytes


encoded_passw_bytes = bytes.fromhex(encoded_passw)# Step 3: Base64 encode the raw bytes


base64_encoded = base64.b64encode(encoded_passw_bytes).decode()
print(f"Base64 Encoded (Raw Bytes): {base64_encoded}")



