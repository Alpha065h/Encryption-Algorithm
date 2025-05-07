import json
import random
import numpy as np
from math import erf
from scipy.stats import chi2_contingency

with open('Codes.txt', 'r', encoding='utf-8') as file:
    temp = file.read()

codes = json.loads(temp)
multipli = 0
multiplist = []
num_indexes = []
num_equivs = []
char_group = []
char_indexes = []
checker = []


def symbols(char):
    symbs = "\\~!@#$%^&*()_-+=[{]}}|;:'\"/?.>,<"
    return char in symbs


def digitis(char):
    digits = "0123456789"
    return char in digits


def alphaa(char):
    alphaas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return char in alphaas


def runs_test(bits):
    runs = [1]
    for i in range(1, len(bits)):
        if bits[i] != bits[i - 1]:
            runs.append(1)
        else:
            runs[-1] += 1
    n1 = sum(run for run in runs if run == 1)
    n2 = sum(run for run in runs if run == 2)

    mean_runs = (2 * n1 * n2) / (n1 + n2) + 1
    std_dev_runs = (mean_runs - 1) * ((mean_runs - 2) / (n1 + n2 - 1)) ** 0.5

    z_score = (len(runs) - mean_runs) / std_dev_runs
    p_value = erfc(abs(z_score) / (2 ** 0.5))

    return p_value


def erfc(x):
    return 1.0 - (0.5 * (1.0 + erf(x / 2 ** 0.5)))


def generate_random_bits(length):
    return ''.join(random.choice(['0', '1']) for _ in range(length))


def serial_test(bits, m=3):
    count_dict = {}
    for i in range(len(bits) - m + 1):
        substring = bits[i:i+m]
        if substring in count_dict:
            count_dict[substring] += 1
        else:
            count_dict[substring] = 1

    total_substrings = len(bits) - m + 1
    expected_frequency = total_substrings / (2 ** m)

    chi_squared = sum(((count - expected_frequency) ** 2) / expected_frequency for count in count_dict.values())

    degrees_of_freedom = 2 ** m - 1
    p_value = chi2_contingency_cdf(chi_squared, degrees_of_freedom)

    return p_value


def chi2_contingency_cdf(x, k):
    if x < 0:
        return 0

    summation = 0
    for i in range(k):
        summation += ((-1) ** i) * (x ** (2 * i)) / factorial(2 * i)
    
    cdf_value = 1 - (2 ** (-k / 2)) * summation
    return max(0, min(1, cdf_value))  # Ensure the result is within [0, 1]



def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def approximate_entropy_test(bits, m=3):
    pattern_counts = {}
    for i in range(len(bits) - m + 1):
        pattern = bits[i:i+m]
        if pattern in pattern_counts:
            pattern_counts[pattern] += 1
        else:
            pattern_counts[pattern] = 1

    observed = list(pattern_counts.values())
    expected = [len(bits) / (2 ** m)] * len(observed)

    _, p_value, _, _ = chi2_contingency([observed, expected])

    return p_value


def encrypt(pword):
    encrypted_pword = ""
    i = 0
    while i < len(pword):
        char = pword[i]
        if digitis(char) and char != '0':
            num_equiv = int(char)
            num_indexes.append(i)
            tempnum_group = char
            while i + 1 < len(pword) and digitis(pword[i + 1]):
                tempnum_group += pword[i + 1]
                i += 1
                num_equiv = int(tempnum_group) % len(codes)
                num_equiv = int(tempnum_group) % len(codes)
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
        elif symbols(char) == True:
            iterations = random.randint(1, 199)
            alph = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+=[';/.>,m';]"
            for x in range(iterations):
                shift = random.randint(0, 86)
                encrypted_char = alph[shift]
                encrypted_pword += encrypted_char
            char_group.append(char)
            char_indexes.append(i)

        elif alphaa(char):
            iterations = random.randint(1, 99)
            alph = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
            for x in range(iterations):
                shift = random.randint(0, 94)
                encrypted_char = alph[shift]
                if x == 0:
                    encrypted_pword += encrypted_char
                else:
                    randomindex = random.randint(0, len(encrypted_pword) - 1)
                    encrypted_pword = encrypted_pword[:randomindex] + encrypted_char + encrypted_pword[randomindex:]
            char_group.append(char)
            char_indexes.append(i)
        else:
            iterations = random.randint(1, 99)
            alph = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+=[';/.>,m';]"
            for x in range(iterations):
                shift = random.randint(0, 86)
                encrypted_char = alph[shift]
                encrypted_pword += encrypted_char
            char_group.append(char)
            char_indexes.append(i)

        i += 1

    return encrypted_pword


# Example usage:
userinput = input("Enter a password: ")
# Encrypt the user input
encrypted_result = encrypt(userinput)
# Generating a longer sequence of random bits
random_bits_sequence = generate_random_bits(1000)
# Apply the runs test to assess randomness
runs_p_value = runs_test(random_bits_sequence)
# Applying the serial test to assess randomness
serial_test_length = 3
serial_p_value = serial_test(random_bits_sequence, m=serial_test_length)
# Applying the approximate entropy test
approx_entropy_p_value = approximate_entropy_test(random_bits_sequence, m=2)

print("Encrypted Password:", encrypted_result)
print(f'P-value for Runs Test: {round(runs_p_value, 2)}')
print(f'Serial Test P-value: {round(serial_p_value, 5)}')
print(f'Approximate Entropy Test P-value: {round(approx_entropy_p_value, 5)}')
