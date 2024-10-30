import socket
from main import encrypt_block, generate_key  

server_ip = '127.0.0.1'
server_port = 5000

plaintext = "This is a test message that exceeds 8 characters."

key = '12345678'  
keys = generate_key(key)  

try:
    encrypted_message = encrypt_block(plaintext, keys)  
    
    if isinstance(encrypted_message, str):
        encrypted_message = encrypted_message.encode()  

except Exception as e:
    print(f"Encryption error: {e}")
    exit(1)

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    client_socket.send(encrypted_message)
    print(f"Encrypted message sent: {encrypted_message}")

except Exception as e:
    print(f"An error occurred while sending the message: {e}")

finally:
    client_socket.close()
