import socket
import base64
import random
import string

# Constants
MAX_CHUNK_SIZE = 32  # Maximum chunk size
DOMAIN_SUFFIX = ".example.com"  # Suffix for the domain name

def process_dns_query(query_data):
    parts = query_data.split(b'.')
    data_b64 = parts[0]
    index = int(parts[1])
    data_chunk = base64.b64decode(data_b64)
    return index, data_chunk

def save_to_file(data_chunks):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    filename = f"received_{random_string}.txt"
    with open(filename, 'ab') as file:
        for index, data_chunk in sorted(data_chunks.items()):
            file.write(data_chunk)

def main():
    server_ip = '0.0.0.0'  # Listen on all interfaces
    server_port = 53

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_ip, server_port))

    print("Server listening...")

    data_chunks = {}
    expected_index = 0
    total_packets = 0

    while True:
        data, addr = sock.recvfrom(1024)
        total_packets += 1
        index, data_chunk = process_dns_query(data)
        print(f"Received packet {index + 1}")
        print("Data received:", data_chunk.decode())  # Print the received data chunk

        if index == expected_index:
            data_chunks[index] = data_chunk
            expected_index += len(data_chunk)
        else:
            print(f"Missing chunk: {expected_index}")
            continue

        # Check if there are any missing chunks
        while expected_index in data_chunks:
            expected_index += len(data_chunks[expected_index])

        if len(data_chunk) < MAX_CHUNK_SIZE:
            break

    save_to_file(data_chunks)
    print("File received and saved.")
    print(f"Total number of packets received: {total_packets}")

    sock.close()

if __name__ == "__main__":
    main()
