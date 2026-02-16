text="A well-organized paragraph supports or develops a single controlling idea, which is expressed in a sentence called the topic sentence. A topic sentence has several important functions: it substantiates or supports an essay’s thesis statement; it unifies the content of a paragraph and directs the order of the sentences; and it advises the reader of the subject to be discussed and how the paragraph will discuss it. Readers generally look to the first few sentences in a paragraph to determine the subject and perspective of the paragraph. That’s why it’s often best to put the topic sentence at the very beginning of the paragraph. In some cases, however, it’s more effective to place another sentence before the topic sentence—for example, a sentence linking the current paragraph to the previous one, or one providing background information."

print(text)

count_P = {}

for i in text:

    if i.isalpha():
        i.lower()

        if i in count_P:
            count_P[i] += 1
        else:
            count_P[i] = 1


print("\nPlaintext Frequnecy",count_P)


def Encrypt(txt, key):
    encrypted = ""

    for i, char in enumerate(txt):
        if char.isalpha():
            shift = key + (i % 5)

            base = ord('a') if char.islower() else ord('A')
            if i % 2 == 0:
                encrypted += chr((ord(char) - base + shift) % 26 + base)
            else:
                encrypted += chr((ord(char) - base - shift) % 26 + base)
        else:
            encrypted += char

    return encrypted


list = [0]*26
char_List = ['0']*26
count_C = {}

en_txt = Encrypt(text , 3)

print("\n",en_txt)

for i in en_txt:

    if i.isalpha():
        i.lower()

        if i in count_C:
            count_C[i] += 1
        else:
            count_C[i] = 1


print("\nEncrypted Frequnecy",count_C)




