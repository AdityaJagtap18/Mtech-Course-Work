def encrypt_file(input_file, output_file, key):
    with open(input_file, "r") as f:
        text = f.read()

    encrypted = ""
    for i, char in enumerate(text):
        shift = key + (i % 5)

        if i % 2 == 0:
            encrypted += chr((ord(char) + shift) % 256)
        else:
            encrypted += chr((ord(char) - shift) % 256)

    with open(output_file, "w") as f:
        f.write(encrypted)

    print("Encryption successful")


def decrypt_file(input_file, output_file, key):
    with open(input_file, "r") as f:
        text = f.read()

    decrypted = ""
    for i, char in enumerate(text):
        shift = key + (i % 5)

        if i % 2 == 0:
            decrypted += chr((ord(char) - shift) % 256)
        else:
            decrypted += chr((ord(char) + shift) % 256)

    with open(output_file, "w") as f:
        f.write(decrypted)

    print("Decryption successful")


# -------- Main Program --------
choice = input("E = Encrypt, D = Decrypt: ").upper()
key = int(input("Enter base key: "))

if choice == "E":
    encrypt_file("plain.txt", "encrypted.txt", key)
elif choice == "D":
    decrypt_file("encrypted.txt", "plain.txt", key)
else:
    print("Invalid option")
