from pathlib import Path

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MOD = 26


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_inverse_2x2(matrix):
    a, b = matrix[0]
    c, d = matrix[1]

    det = (a*d - b*c) % MOD
    det_inv = mod_inverse(det, MOD)

    if det_inv is None:
        raise ValueError("Key matrix is not invertible modulo 26")

    return [
        [( d * det_inv) % MOD, (-b * det_inv) % MOD],
        [(-c * det_inv) % MOD, ( a * det_inv) % MOD]
    ]

def clean_text(text):
    return "".join(c for c in text.upper() if c.isalpha())

def hill_encrypt(plaintext, key):
    text = clean_text(plaintext)

    if len(text) % 2 != 0:
        text += "X"

    result = ""

    for i in range(0, len(text), 2):
        p1 = ALPHABET.index(text[i])
        p2 = ALPHABET.index(text[i+1])

        c1 = (key[0][0]*p1 + key[0][1]*p2) % MOD
        c2 = (key[1][0]*p1 + key[1][1]*p2) % MOD

        result += ALPHABET[c1] + ALPHABET[c2]

    return result


def hill_decrypt(ciphertext, key):
    inv_key = matrix_inverse_2x2(key)
    result = ""

    for i in range(0, len(ciphertext), 2):
        c1 = ALPHABET.index(ciphertext[i])
        c2 = ALPHABET.index(ciphertext[i+1])

        p1 = (inv_key[0][0]*c1 + inv_key[0][1]*c2) % MOD
        p2 = (inv_key[1][0]*c1 + inv_key[1][1]*c2) % MOD

        result += ALPHABET[p1] + ALPHABET[p2]

    return result


def main():
    print("\n=== Hill Cipher (2x2 Matrix) ===")
    choice = input("Enter E to Encrypt or D to Decrypt: ").upper()

    key = [
        [3, 3],
        [2, 5]
    ]  # Example valid key

    input_file = input("Enter input file name: ")
    output_file = input("Enter output file name: ")

    try:
        text = Path(input_file).read_text()

        if choice == "E":
            result = hill_encrypt(text, key)
            print("Encryption completed.")
        elif choice == "D":
            result = hill_decrypt(text, key)
            print("Decryption completed.")
        else:
            print("Invalid choice!")
            return

        Path(output_file).write_text(result)
        print(f"Output saved in {output_file}")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
