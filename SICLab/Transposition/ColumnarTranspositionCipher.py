import math
from pathlib import Path

def key_order(key):
    key = key.upper()
    indexed = list(enumerate(key))
    sorted_key = sorted(indexed, key=lambda x: (x[1], x[0]))
    return [idx for idx, _ in sorted_key]

def encrypt_transposition(plaintext, key, pad_char="X"):
    k = len(key)
    rows = math.ceil(len(plaintext) / k)
    total = rows * k

    plaintext += pad_char * (total - len(plaintext))
    grid = [plaintext[i:i+k] for i in range(0, total, k)]

    order = key_order(key)
    cipher = ""

    for col in order:
        for r in range(rows):
            cipher += grid[r][col]

    return cipher

def decrypt_transposition(ciphertext, key, pad_char="X"):
    k = len(key)
    rows = math.ceil(len(ciphertext) / k)
    order = key_order(key)

    grid = [[""] * k for _ in range(rows)]
    index = 0

    for col in order:
        for r in range(rows):
            grid[r][col] = ciphertext[index]
            index += 1

    plaintext = ""
    for row in grid:
        plaintext += "".join(row)

    return plaintext.rstrip(pad_char)


def main():
    print("\n=== Columnar Transposition Cipher ===")
    choice = input("Enter E to Encrypt or D to Decrypt: ").strip().upper()

    if choice not in ["E", "D"]:
        print("Invalid choice!")
        return

    key = input("Enter key word: ")

    input_file = input("Enter input file name (example: plain.txt): ")
    output_file = input("Enter output file name (example: cipher.txt): ")

    try:
        text = Path(input_file).read_text()

        if choice == "E":
            result = encrypt_transposition(text, key)
            print("\nEncryption completed successfully.")
        else:
            result = decrypt_transposition(text, key)
            print("\nDecryption completed successfully.")

        Path(output_file).write_text(result)
        print(f"Output written to: {output_file}")

    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
