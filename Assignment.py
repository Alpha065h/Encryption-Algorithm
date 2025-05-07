# Dictionary representing the encryption key for each letter
keysE = {"A":"Q", "B":"W", "C":"E", "D":"R", "E":"T",
          "F":"Y", "G":"U", "H":"I", "I":"O", "J":"P", "K":"A", "L":"S", "M":"D",
        "N":"F", "O":"G", "P":"H", "Q":"J", "R":"K", "S":"L", "T":"Z", "U":"X", 
        "V":"C", "W":"V", "X":"B", "Y":"N", "Z":"M"}

# Dictionary to convert lowercase letters to uppercase
ups   = {"a":"A", "b":"B", "c":"C", "d":"D", "e":"E", "f":"F", "g":"G", "h":"H", "i":"I", "j":"J", "k":"K", "l":"L", "m":"M",
         "n":"N", "o":"O", "p":"P", "q":"Q", "r":"R", "s":"S", "t":"T", "u":"U", "v":"V", "w":"W", "x":"X", "y":"Y","z":"Z"}

# Encryption key for selecting encryption or decryption
keyE  = "MeOw"
keyD  = "aW"

# Function to convert lowercase letters to uppercase
def i_upperMoBeybi(in_put):
    """
    Takes a string as input and converts all lowercase letters to uppercase.

    Args:
    in_put (str): The input string.

    Returns:
    str: The input string with lowercase letters converted to uppercase.
    """
    y = ""
    for a in in_put:
        if a in ups:
            y = y + ups[a]
        else:
            y = y + a
    return y

# Function to encrypt a message
def encrypt(in_putL):
    """
    Encrypts a message using the provided encryption key.

    Args:
    in_putL (str): The input message in uppercase.

    Returns:
    str: The encrypted message.
    """
    z = ""
    for x in in_putL:
        z = z + keysE[x]
    return z

# Function to decrypt a message
def decrypt(in_putL):
    """
    Decrypts a message using the provided encryption key.

    Args:
    in_putL (str): The input message in uppercase.

    Returns:
    str: The decrypted message.
    """
    w = ""
    for p in in_putL:
        for key in keysE:
            if keysE[key] == p:
                w = w + key
    return w

# Main function
if __name__ == "__main__":
    # Get user input for the message and key
    in_put  = input("Enter the message: ")
    key_put = input("Enter the key: ")
    
    # Convert input message to uppercase
    in_putL = i_upperMoBeybi(in_put)
    
    # Check if the key matches encryption or decryption key
    if key_put == keyE:
        encrypted_message = encrypt(in_putL)
        print(encrypted_message)
    elif key_put == keyD:
        decrypted_message = decrypt(in_putL)
        print(decrypted_message)
    else:
        print("Invalid Key")
