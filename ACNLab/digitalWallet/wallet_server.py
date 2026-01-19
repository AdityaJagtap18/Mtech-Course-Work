import socket
import struct

# Server Configuration
HOST = '10.85.206.149'
PORT = 5555
MAX_BALANCE = 65535

def handle_instruction(instruction, amount, balance):
    """
    Process wallet instruction and return response code and value.
    
    Args:
        instruction: 2-byte instruction ('CR' or 'DB')
        amount: Amount to credit or debit
        balance: Current wallet balance
    
    Returns:
        tuple: (response_code, value)
    """
    if instruction == b'CR':
        # Credit instruction
        if balance + amount > MAX_BALANCE:
            return b'ER', 0
        else:
            new_balance = balance + amount
            return b'BA', new_balance
    
    elif instruction == b'DB':
        # Debit instruction
        if balance >= amount:
            new_balance = balance - amount
            return b'BA', new_balance
        else:
            return b'ER', 0
    
    else:
        # Invalid instruction
        return b'ER', 0

def start_server():
    """Start the digital wallet server."""
    balance = 0  # Initial wallet balance
    
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind to address and port
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Digital Wallet Server started on {HOST}:{PORT}")
        print(f"Initial Balance: {balance}")
        print("Waiting for client connections...\n")
        
        while True:
            # Accept client connection
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}")
            
            try:
                # Receive 4-byte instruction message
                data = client_socket.recv(4)
                
                if len(data) == 4:
                    # Unpack: 2-byte CHAR instruction + 2-byte unsigned short amount
                    instruction = data[:2]
                    amount = struct.unpack('!H', data[2:4])[0]
                    
                    print(f"Received: Instruction={instruction.decode()}, Amount={amount}")
                    
                    # Process instruction
                    response_code, value = handle_instruction(instruction, amount, balance)
                    
                    # Update balance if operation was successful
                    if response_code == b'BA':
                        balance = value
                        print(f"Success: New Balance={balance}")
                    else:
                        print(f"Error: Operation failed, Balance={balance}")
                    
                    # Pack and send response: 2-byte response code + 2-byte unsigned short value
                    response = response_code + struct.pack('!H', value)
                    client_socket.sendall(response)
                    print(f"Sent: Response={response_code.decode()}, Value={value}\n")
                
            except Exception as e:
                print(f"Error handling client request: {e}\n")
            
            finally:
                client_socket.close()
    
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    
    finally:
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    start_server()
