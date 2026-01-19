import socket
import struct
import sys

# Server Configuration
HOST = '127.0.0.1'
PORT = 5555

def send_instruction(instruction, amount):
    """
    Send instruction to wallet server and receive response.
    
    Args:
        instruction: 'CR' for credit or 'DB' for debit
        amount: Amount to credit or debit (0-65535)
    """
    # Validate instruction
    if instruction not in ['CR', 'DB']:
        print("Error: Invalid instruction. Use 'CR' or 'DB'.")
        return
    
    # Validate amount
    if not (0 <= amount <= 65535):
        print("Error: Amount must be between 0 and 65535.")
        return
    
    try:
        # Create TCP socket and connect to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
        
        # Pack instruction message: 2-byte instruction + 2-byte unsigned short amount
        instruction_bytes = instruction.encode('ascii')
        message = instruction_bytes + struct.pack('!H', amount)
        
        print(f"Sending: Instruction={instruction}, Amount={amount}")
        
        # Send instruction to server
        client_socket.sendall(message)
        
        # Receive 4-byte response
        response = client_socket.recv(4)
        
        if len(response) == 4:
            # Unpack response: 2-byte response code + 2-byte unsigned short value
            response_code = response[:2].decode('ascii')
            value = struct.unpack('!H', response[2:4])[0]
            
            # Print result
            if response_code == 'BA':
                print(f"\n=== SUCCESS ===")
                print(f"Current Balance: {value}")
            elif response_code == 'ER':
                print(f"\n=== ERROR ===")
                print(f"Operation failed. Error code returned.")
                if instruction == 'DB':
                    print("Reason: Insufficient balance for debit operation.")
                elif instruction == 'CR':
                    print("Reason: Credit would exceed maximum balance (65535).")
            else:
                print(f"Unknown response code: {response_code}")
        else:
            print("Error: Invalid response from server")
        
        # Close connection
        client_socket.close()
    
    except ConnectionRefusedError:
        print(f"Error: Could not connect to server at {HOST}:{PORT}")
        print("Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main function to run the client."""
    print("=== Digital Wallet Client ===\n")
    
    if len(sys.argv) == 3:
        # Command line mode: python client.py CR 1000
        instruction = sys.argv[1].upper()
        try:
            amount = int(sys.argv[2])
            send_instruction(instruction, amount)
        except ValueError:
            print("Error: Amount must be an integer.")
    else:
        # Interactive mode
        print("Usage: python client.py <INSTRUCTION> <AMOUNT>")
        print("Example: python client.py CR 1000")
        print("\nOr run interactively:\n")
        
        try:
            instruction = input("Enter instruction (CR/DB): ").upper()
            amount = int(input("Enter amount (0-65535): "))
            send_instruction(instruction, amount)
        except ValueError:
            print("Error: Invalid amount. Please enter an integer.")
        except KeyboardInterrupt:
            print("\nClient terminated.")

if __name__ == "__main__":
    main()