import uuid, hashlib, base64

# Generate a UUID.
uuid1 = uuid.uuid4()

# Convert the UUID to a string.
uuid_str1 = str(uuid1).upper()

# Create the code verifier.
code_verifier = uuid_str1 + "-" + uuid_str1

# Create the code challenge based on the code verifier.
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode('utf-8')

# Remove all padding from the code challenge.
code_challenge = code_challenge.replace('=', '')

# Print the code verifier and the code challenge.
# Use these in your calls to manually generate
# access tokens for OAuth U2M authentication.
print(f"code_verifier:  {code_verifier}")
print(f"code_challenge: {code_challenge}")