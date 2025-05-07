import json
import random

# Load the list of dictionaries from Codes.txt
with open('Codes.txt', 'r', encoding='utf-8') as file:
    temp = file.read()
codes = json.loads(temp)

# Load the dictionary from ascii.txt
with open('ascii.txt', 'r', encoding='utf-8') as file:
    temp = file.read()
ascii_code = json.loads(temp)

# Load the dictionary from ascii_swap.txt
with open('ascii_swap.txt', 'r', encoding='utf-8') as file:
    temp = file.read()
ascii_code_swap = json.loads(temp)

multipli = 0
multiplist = []
num_indexes = []
num_equivs = []
char_group = []
char_indexes = []
checker = []

# Define your encrypt function
def encrypt(pword):
    encrypted_pword = ""
    temp = 0
    i = 0  # Initialize an index to keep track of the current character position
    while i < len(pword):
        char = pword[i]
        if char.isdigit() and char != '0':
            try:
                num_equiv = int(char)
            except:
                num_equiv = random.randint(1,9)
            num_indexes.append(i)
            # Check if the next characters are also digits and form a group
            try:
                tempnum_group = char
            except:
                tempnum_group = random.randint(1,9)
            while i + 1 < len(pword) and pword[i + 1].isdigit():
                try:
                    tempnum_group += pword[i + 1]
                except:
                    tempnum_group += random.randint(1,9)
                i += 1
            try:
                num_equiv = int(tempnum_group) % len(codes)  # Apply modulo
            except:
                temp = random.randint(1,999999)
                num_equiv = temp % len(codes)
            num_equivs.append(num_equiv)
            try:
                multipli = int(tempnum_group) / len(codes)
            except:
                multipli = temp / len(codes)
            multiplist.append(int(multipli))
            if temp > 51:
                checker.append(1)
            else:
                checker.append(0)

            for equiv in codes:
                if equiv["Num Equi"] == num_equiv:
                    encrypted_pword += equiv["Alpha Equi"]
                    break
        elif symbols(char) == True:
            shift = random.randint(1,25)
            encrypted_char = chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
            encrypted_pword += encrypted_char
            char_group.append(char)
            char_indexes.append(i)

        else:
            # Use a simple Caesar cipher for alphabet characters
            shift = random.randint(1, 25)  # Random shift between 1 and 25
            encrypted_char = chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
            encrypted_pword += encrypted_char
            char_group.append(char)
            char_indexes.append(i)
        i += 1

    return encrypted_pword

def symbols(char):
    symbs = "\\~!@#$%^&*()_-+=[{]}}|;:'\"/?.>,<"
    if char in symbs:
        return True
    else:
        return False


# Define your decrypt function
def decrypt(encrypted_pword):
    decrypted_pword = ""
    while True:
        if len(decrypted_pword) == len(userinput):
            break
        else:
            for x in range(len(num_indexes)):
                if checker[x] == 1:
                    temp1 = (multiplist[x] * len(codes)) + num_equivs[x]
                    decrypted_pword = decrypted_pword[:num_indexes[x]] + str(temp1) + decrypted_pword[num_indexes[x]:]
                else:
                    for equiv in codes:
                        if equiv["Num Equi"] == num_equivs[x]:
                            decrypted_pword = decrypted_pword[:num_indexes[x]] + str(
                                num_equivs[x]) + decrypted_pword[num_indexes[x]:]
                            break

            for y in range(len(char_group)):
                decrypted_pword = decrypted_pword[:char_indexes[y]] + char_group[y] + decrypted_pword[char_indexes[y]:]

    return decrypted_pword


# Function to convert decimal to fixed-size binary
def decimal_to_fixed_size_binary(decimal_values, fixed_size=8):
    binary_values = []
    for decimal_value in decimal_values:
        decimal_value = int(decimal_value)
        if decimal_value < 0 or decimal_value > 255:
            raise ValueError("Decimal value must be between 0 and 255")

        binary_value = bin(decimal_value)[2:].zfill(fixed_size)
        binary_values.append(binary_value)

    return binary_values

# Function to convert character to fixed-size binary
def char_to_fixed_size_binary(encrypted_pword, fixed_size=8):
    decimal_values = []
    for char in encrypted_pword:
        if char in ascii_code_swap:
            decimal_value = ascii_code_swap[char]
            decimal_values.append(decimal_value)
    return decimal_to_fixed_size_binary(decimal_values, fixed_size)


# Function to compute avalanche score
def compute_avalanche_score(userinput, num_iterations=100):
    keys_list = list(ascii_code.keys())
    halt_index = []
    ave_list = []
    encrypted_pword = encrypt(userinput)
    for _ in range(num_iterations):
        done = False
        temp = char_to_fixed_size_binary(encrypted_pword)
        temp2 = ''.join(temp)

        while not done:
            random_index = random.randint(0, len(userinput) - 1)
            random_charint = random.randint(0, len(keys_list) - 1)
            key = keys_list[random_charint]

            if random_index not in halt_index:
                done = True
                halt_index.append(random_index)
                userinput = userinput[:random_index] + ascii_code[key] + userinput[random_index + 1:]
                encrypted_pword = encrypt(userinput)
                decimal_values = char_to_fixed_size_binary(encrypted_pword)
                present_binary = ''.join(decimal_values)

                # Pad or truncate to the length of the longer binary string
                max_length = max(len(temp2), len(present_binary))
                temp2 = temp2.ljust(max_length, '0')
                present_binary = present_binary.ljust(max_length, '0')

                result = ""
                for x in range(len(temp2)):
                    if temp2[x] == present_binary[x]:
                        result += "0"
                    else:
                        result += "1"
                counter = 0
                for y in result:
                    if y == "1":
                        counter += 1
                ave_list.append(counter / len(result))

            if len(halt_index) == len(userinput):
                halt_index = []
    deci_list = [ave / 100 for ave in ave_list]
    total = sum(deci_list)
    avalanche_score = total * 100
    return avalanche_score


# Get user input for the password
userinput = input("Enter a password: ")

# Encrypt the password
encrypted_result = encrypt(userinput)
print("Encrypted Password:", encrypted_result)

# Decrypt the password
decrypted_result = decrypt(encrypted_result)
print("Decrypted Password:", decrypted_result)

# Compute the avalanche score
avalanche_score = compute_avalanche_score(userinput, num_iterations=100)
print("Avalanche Score:", avalanche_score)
