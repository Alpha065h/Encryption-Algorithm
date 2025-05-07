import json

with open('Codes.txt', 'r', encoding='utf-8') as file: #open list of dictionaries
    temp = file.read()

codes = json.loads(temp)
multipli = 0
multiplist = []
num_indexes = []
num_equivs = []
char_group = []
char_indexes = []
checker = []

def encrypt(pword):
    encrypted_pword = ""
    i = 0  # Initialize an index to keep track of the current character position
    while i < len(pword):
        char = pword[i]
        if char.isdigit() and int(char) != 0:
            num_equiv = int(char)
            num_indexes.append(i)
            # Check if the next characters are also digits and form a group
            tempnum_group = char
            while i + 1 < len(pword) and pword[i + 1].isdigit():
                tempnum_group += pword[i + 1]
                i += 1 
            num_equiv = int(tempnum_group) % len(codes)  # Apply modulo
            num_equivs.append(num_equiv)
            multipli = int(tempnum_group)/len(codes)
            multiplist.append(int(multipli))
            if int(tempnum_group) > 51:
                checker.append(1)
            else:
                checker.append(0)

            for equiv in codes:
                if equiv["Num Equi"] == num_equiv:
                    encrypted_pword += equiv["Alpha Equi"]
                    break
        else:
            encrypted_pword += char
            char_group.append(char)
            char_indexes.append(i)
        i += 1

    return encrypted_pword




userinput = input("Enter a password: ")
encrypted_result = encrypt(userinput)
print("Encrypted Password:", encrypted_result)

