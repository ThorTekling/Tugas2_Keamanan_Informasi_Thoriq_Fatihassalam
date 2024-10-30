import socket
from main import decrypt_block 

server_ip = '127.0.0.1'
server_port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f"Server is listening on {server_ip}:{server_port}...")

try:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} established.")

    encrypted_message = client_socket.recv(1024)
    if encrypted_message:
        print(f"Encrypted message received: {encrypted_message}")

        decrypted_message = decrypt_block(encrypted_message)
        print(f"Decrypted message: {decrypted_message}")

    else:
        print("No message received or the message is empty.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
    server_socket.close()
    print("Connection closed.")
