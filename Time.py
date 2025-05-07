import json
import time

# Define the encrypt function that takes a password as input
def encrypt(pword):
    encrypted_pword = ""
    i = 0  # Initialize an index to keep track of the current character position

    # Iterate through the characters in the input password
    while i < len(pword):
        char = pword[i]

        # Check if the current character is a non-zero digit
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

            # Determine if the group of digits is greater than 51
            if int(tempnum_group) > 51:
                checker.append(1)
            else:
                checker.append(0)

            # Find the corresponding character in 'codes' based on 'num_equiv'
            for equiv in codes:
                if equiv["Num Equi"] == num_equiv:
                    encrypted_pword += equiv["Alpha Equi"]
                    break
        else:
            # If the character is not a digit, simply add it to the encrypted password
            encrypted_pword += char
            char_group.append(char)
            char_indexes.append(i)

        i += 1  # Move to the next character in the input password

    return encrypted_pword  # Return the encrypted password

# Define the decrypt function that takes an encrypted password as input
def decrypt(encrypted_pword):
    decrypted_pword = ""
    
    # Loop until the length of the decrypted password matches the input password
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
                            decrypted_pword = decrypted_pword[:num_indexes[x]] + str(num_equivs[x]) + decrypted_pword[num_indexes[x]:]
                            break

            for y in range(len(char_group)):
                decrypted_pword = decrypted_pword[:char_indexes[y]] + char_group[y] + decrypted_pword[char_indexes[y]:]

    return decrypted_pword  # Return the decrypted password

userinput = input("Enter a password: ")  # Prompt the user for a password input

# Start the timer for the whole program
start_time = time.time()

# Read the content of the 'Codes.txt' file and store it in the 'temp' variable
with open('Codes.txt', 'r', encoding='utf-8') as file:
    temp = file.read()

# Parse the JSON content from 'temp' and store it in the 'codes' variable
codes = json.loads(temp)

# Initialize various variables and lists for later use
multipli = 0
multiplist = []
num_indexes = []
num_equivs = []
char_group = []
char_indexes = []
checker = []


encrypted_result = encrypt(userinput)  # Call the encrypt function
print("Encrypted Password:", encrypted_result)

decrypted_result = decrypt(encrypted_result)  # Call the decrypt function
print("Decrypted Password:", decrypted_result)

# Stop the timer for the whole program
end_time = time.time()
elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
print("Total Execution Time: {:.20f} milliseconds".format(elapsed_time))
