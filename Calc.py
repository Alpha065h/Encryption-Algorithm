def decimal_to_half_precision(mantissa, exponent):
    # Check if the inputs are valid floats
    try:
        mantissa = float(mantissa)
        exponent = int(exponent)
    except ValueError:
        print("Invalid input. Please enter a valid mantissa (decimal) and exponent (integer).")
        return

    # Handle negative mantissa
    sign_bit = '0' if mantissa >= 0 else '1'
    mantissa = abs(mantissa)

    # Initialize exponent and significand
    exponent = 15  # Bias for half-precision
    significand = ''

    # Convert the mantissa part to binary
    integer_part = int(mantissa)
    fractional_part = mantissa - integer_part

    integer_binary = bin(integer_part)[2:]
    fractional_binary = ''

    while fractional_part > 0 and len(fractional_binary) < 10:
        fractional_part *= 2
        bit = '1' if fractional_part >= 1 else '0'
        fractional_binary += bit
        fractional_part -= int(bit)

    if len(integer_binary) > 1:
        exponent += len(integer_binary) - 1
        integer_binary = integer_binary[1:]

    exponent_binary = bin(exponent)[2:].zfill(5)

    significand = integer_binary + fractional_binary

    # Ensure the significand is exactly 10 bits
    significand = significand[:10].ljust(10, '0')

    # Combine the components
    binary_representation = sign_bit + exponent_binary + significand

    print(f"The half-precision binary representation is:")
    print(binary_representation)

    # Convert binary to hexadecimal
    hexadecimal_representation = hex(int(binary_representation, 2))[2:].zfill(4)
    print(f"The half-precision hexadecimal representation is:")
    print(hexadecimal_representation)


# Take user input for mantissa and exponent
mantissa_input = input("Enter the mantissa (decimal part): ")
exponent_input = input("Enter the exponent (integer part): ")

decimal_to_half_precision(mantissa_input, exponent_input)
