import random
import socket

def hex_to_bin(s):
    mp = {
        '0': "0000", '1': "0001", '2': "0010", '3': "0011", '4': "0100",
        '5': "0101", '6': "0110", '7': "0111", '8': "1000", '9': "1001",
        'A': "1010", 'B': "1011", 'C': "1100", 'D': "1101", 'E': "1110",
        'F': "1111"
    }
    return ''.join(mp[ch] for ch in s)

def bin_to_hex(s):
    mp = {
        "0000": '0', "0001": '1', "0010": '2', "0011": '3', "0100": '4',
        "0101": '5', "0110": '6', "0111": '7', "1000": '8', "1001": '9',
        "1010": 'A', "1011": 'B', "1100": 'C', "1101": 'D', "1110": 'E',
        "1111": 'F'
    }
    return ''.join(mp[s[i:i + 4]] for i in range(0, len(s), 4))

def bin_to_dec(binary):
    return int(binary, 2)

def dec_to_bin(num):
    return bin(num).replace("0b", "").zfill(64)

def permute(k, arr, n):
    return ''.join(k[i - 1] for i in arr)

def shift_left(k, nth_shifts):
    return k[nth_shifts:] + k[:nth_shifts]

def xor(a, b):
    return ''.join('1' if a[i] != b[i] else '0' for i in range(len(a)))

def generate_key():
    return ''.join(random.choice('01') for _ in range(64))

def generate_hex_key():
    random_key = generate_key()  
    hex_key = hex(int(random_key, 2))[2:].zfill(16).upper()  
    return hex_key


s_box = [
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
        ]

initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]
 
exp_box = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]
 
perm = [16,  7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2,  8, 24, 14,
       32, 27,  3,  9,
       19, 13, 30,  6,
       22, 11,  4, 25]
 


final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

def generate_key():
    return ''.join(random.choice('01') for _ in range(64))

def key_schedule(key):
    key = permute(key, [57, 49, 41, 33, 25, 17, 9,
                        1, 58, 50, 42, 34, 26, 18,
                        10, 2, 59, 51, 43, 35, 27,
                        19, 11, 3, 60, 52, 44, 36,
                        63, 55, 47, 39, 31, 23, 15,
                        7, 62, 54, 46, 38, 30, 22,
                        14, 6, 61, 53, 45, 37, 29,
                        21, 13, 5, 28, 20, 12, 4, 16])
    
    round_keys_bin = []
    left = key[:28]
    right = key[28:]
    shifts = [1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2]

    for shift in shifts:
        left = shift_left(left, shift)
        right = shift_left(right, shift)
        combined = left + right
        round_keys_bin.append(permute(combined, [14, 17, 11, 24, 1, 5, 3, 28,
                                                  15, 6, 21, 10, 23, 19, 12, 4,
                                                  26, 8, 16, 7, 27, 20, 13, 2,
                                                  41, 52, 31, 37, 47, 55, 30, 40,
                                                  51, 45, 33, 48, 44, 49, 39, 56,
                                                  34, 24, 42, 30, 5, 12, 3, 21,
                                                  10, 36, 15, 4, 18, 29, 19, 26]))
    
    return round_keys_bin

def f_function(R, K):
    expanded_R = permute(R, [32, 1, 2, 3, 4, 5, 4, 5,
                              6, 7, 8, 9, 8, 9, 10, 11,
                              12, 13, 12, 13, 14, 15, 16, 17,
                              16, 17, 18, 19, 20, 21, 20, 21,
                              22, 23, 24, 25, 24, 25, 26, 27,
                              28, 29, 28, 29, 30, 31, 32, 1])
    
    xor_result = xor(expanded_R, K)
    sbox_output = ''

    for i in range(8):
        row = int(xor_result[i * 6] + xor_result[i * 6 + 5], 2)
        col = int(xor_result[i * 6 + 1:i * 6 + 5], 2)
        sbox_output += dec_to_bin(s_box[i][row][col]).zfill(4)

    
    return permute(sbox_output, perm)

def encrypt_block(plain_text, keys):
    text = permute(plain_text, initial_perm)
    left, right = text[:32], text[32:]

    for i in range(16):
        left, right = right, xor(left, f_function(right, keys[i]))

    combined = right + left  
    return permute(combined, final_perm)

def decrypt_block(cipher_text, keys):
    text = permute(cipher_text, initial_perm)
    left, right = text[:32], text[32:]

    for i in range(15, -1, -1):
        left, right = right, xor(left, f_function(right, keys[i]))

    combined = right + left  
    return permute(combined, final_perm)

def start_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', port))
    s.listen(1)
    print(f"Server listening on port {port}...")
    conn, addr = s.accept()
    print(f"Connection from {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        key = data.decode()
        print(f"Received key: {key}")
        
        encrypted_key = encrypt_block(hex_to_bin(key), key_schedule(generate_key()))
        conn.send(bin_to_hex(encrypted_key).encode())

    conn.close()
    s.close()

def start_client(host, port, key):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("Connected to the server.")
    
    s.send(key.encode())
    encrypted_key = s.recv(1024)
    print(f"Received encrypted key: {encrypted_key.decode()}")

    s.close()

if __name__ == "__main__":
   
    port = 5000 
    start_server(port)

    hex_key = generate_hex_key()  

    start_client('localhost', port, hex_key)