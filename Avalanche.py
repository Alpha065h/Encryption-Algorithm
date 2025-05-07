import json
import random

# Load the list of dictionaries from Codes.txt
with open('Codes.txt', 'r', encoding='utf-8') as file:
    temp = file.read()
codes = json.loads(temp)

#Load the dictionary from ascii.txt
with open('ascii.txt', 'r' , encoding='utf-8') as file:
    temp = file.read()
ascii_code = json.loads(temp)

#Load the dictionary from ascii_swap.txt
with open('ascii_swap.txt', 'r' , encoding='utf-8') as file:
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
            multipli = int(tempnum_group) / len(codes)
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


#function to covert decimal to 8-bit binary
def decimal_to_8bit_binary(decimal_values):
    binary_values = []
    for decimal_value in decimal_values:
        decimal_value = int(decimal_value)
        if decimal_value < 0 or decimal_value > 255:
            raise ValueError("Decimal value must be between 0 and 255")
       
        binary_value = ""
        for _ in range(8):
            binary_value = str(decimal_value % 2) + binary_value
            decimal_value //= 2
        
        binary_values.append(binary_value)

    return binary_values

def char_to_decimal(encrypted_pword):
    decimal_values = []
    for char in encrypted_pword:
        if char in ascii_code_swap:
            decimal_value = ascii_code_swap[char]
            decimal_values.append(decimal_value)
    return decimal_values


#function to compute avalanche score
def compute_avalanche_score(encrypted_pword, num_iterations = 100):
    keys_list = list(ascii_code.keys())
    halt_index = []
    ave_list = []
    for _ in range(num_iterations):
        done = False
        temp = char_to_decimal(encrypted_pword)
        temp2 = decimal_to_8bit_binary(temp)
        prev_binary = ''.join(temp2)

        while not done:
            random_index = random.randint(0,len(encrypted_pword)-1)
            random_charint = random.randint(0,len(keys_list)-1)
            key = keys_list[random_charint]

            if random_index not in halt_index:
                done = True
                halt_index.append(random_index)
                encrypted_pword = encrypted_pword[:random_index] + ascii_code[key] + encrypted_pword[random_index+1:]
                decimal_values = char_to_decimal(encrypted_pword)
                binary_equivalent = decimal_to_8bit_binary(decimal_values)
                temp3 = binary_equivalent
                present_binary = ''.join(temp3)
                result = ""         
                for x in range(len(present_binary)):
                    if prev_binary[x] == present_binary[x]:
                        result += "0"
                    else:
                        result += "1"
                counter = 0
                for y in result:
                    if y == "1":
                        counter+=1
                ave_list.append(counter/len(result))    

            if len(halt_index) == len(encrypted_pword):
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
avalanche_score = compute_avalanche_score(encrypted_result,num_iterations = 100)
print("Avalanche Score:", avalanche_score)
