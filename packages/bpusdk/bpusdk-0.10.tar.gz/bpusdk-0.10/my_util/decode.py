def hex_to_signed_decimal(hex_str, bits=8):
    value = int(hex_str, 16)
    if value >= 2**(bits - 1):
        value -= 2**bits  
    return value

def hex_to_8bit_binary(hex_str):
    return format(int(hex_str, 16), '08b')

def signed_decimal_to_hex(signed_decimal):
    signed_decimal = int(signed_decimal)
    if signed_decimal < -128 or signed_decimal > 127:
        raise ValueError("Out of 8-bit signed integer range")
    hex_value = hex((signed_decimal + (1 << 8)) % (1 << 8))[2:]
    return hex_value.zfill(2).upper()  # Format as uppercase and zero-padded to 2 chars

def binary8bit_to_hex(binary_string):
    if len(binary_string) != 8:
        raise ValueError("Input must be an 8-bit binary string")
    hex_value = hex(int(binary_string, 2))[2:]
    return hex_value.zfill(2).upper()

def get_pos(x):
    row = x//4
    i = x-row*4
    return row+1, i

#tmp = get_pos(6403)
#print(tmp)
tmp = hex_to_signed_decimal("C0")
#tmp = signed_decimal_to_hex(f"{-85}")
#tmp= hex_to_8bit_binary("81")
# tmp = binary8bit_to_hex(tmp)

print(tmp)
