#########################################################
# Tutorial from https://www.thonky.com/qr-code-tutorial/
#########################################################

###########################
# Importing useful modules
###########################

from copy import copy


#########################################################
# Stage 1: Data Analysis
# https://www.thonky.com/qr-code-tutorial/data-analysis
#########################################################

def determine_encoding(data: str) -> str:
    """
    Description:
        Returns 4 bits representing the encoding type to be used in the QR code; only supports up to byte mode for now
        \n\n\tNumeric mode -> 0001
        \n\tAlphanumeric Mode -> 0010
        \n\tByte Mode -> 0011

    Args:
        data (str): The data to be encoded in the QR code

    Returns:
        str: Binary correlating to encoding modes
    """
    
    digits = "0123456789"
    alphanumeric_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
    iso_8859_1 = ''.join(chr(i) for i in range(256))
    
    # Numeric mode
    if all(i in digits for i in data):
        return '0001'
    
    # Alphanumeric mode
    if all(i in alphanumeric_chars for i in data):
        return '0010'
    
    # Byte mode
    # Possible issue:
    # https://www.thonky.com/qr-code-tutorial/data-analysis#a-note-about-utf8
    if all(i in iso_8859_1 for i in data):
        return '0011'
    
    # Not supporting other encodings yet, raises NotImplemented otherwise
    raise NotImplementedError("Invalid encoding mode detected. Only Numeric, Alphanumeric, and Byte modes are implemented.")


########################################################
# Stage 2: Data Encoding
# https://www.thonky.com/qr-code-tutorial/data-encoding
########################################################

# Step 1: Choose the Error Correction Level
# Each level needs more space than the previous, so the QR code must be larger

# There are 4 levels to choose from:
# L: Low - Recovers 7% of data
# M: Medium - Recovers 15% of data
# Q: Quartile - Recovers 25% of data
# H: High - Recovers 30% of data

# Version Capacity Table:
# https://www.thonky.com/qr-code-tutorial/character-capacities

# As far as I can tell (for now, at least), this must be chosen before the encoding can begin
# Potential TODO when done: find the highest EC level on the lowest version where the data still fits


# Step 2: Determine the Smallest Version
# The version depends on the length of the data, the chosen error correction level, and the encoding type

def determine_version(encoding_type: str, ec_level: str, data: str) -> int:
    """
    Description:
        Returns an integer representing the smallest version of QR code for the given EC level and input text

    Args:
        encoding_type (str): Binary representation of encoding type (e.g., 0001, 0010, 0011)
        ec_level (str): Error Correction Level. Single Character (e.g., 'L', 'M', 'Q', 'H')
        data (str): Text to be encoded into the QR code

    Returns:
        int: Version of the QR code
    """
    
    version_capacities = {
        'L': {
            '0001': ['41', '77', '127', '187', '255', '322', '370', '461', '552', '652', '772', '883', '1022', '1101', '1250', '1408', '1548', '1725', '1903', '2061', '2232', '2409', '2620', '2812', '3057', '3283', '3517', '3669', '3909', '4158', '4417', '4686', '4965', '5253', '5529', '5836', '6153', '6479', '6743', '7089'],
            '0010': ['25', '47', '77', '114', '154', '195', '224', '279', '335', '395', '468', '535', '619', '667', '758', '854', '938', '1046', '1153', '1249', '1352', '1460', '1588', '1704', '1853', '1990', '2132', '2223', '2369', '2520', '2677', '2840', '3009', '3183', '3351', '3537', '3729', '3927', '4087', '4296'],
            '0011': ['17', '32', '53', '78', '106', '134', '154', '192', '230', '271', '321', '367', '425', '458', '520', '586', '644', '718', '792', '858', '929', '1003', '1091', '1171', '1273', '1367', '1465', '1528', '1628', '1732', '1840', '1952', '2068', '2188', '2303', '2431', '2563', '2699', '2809', '2953']
        },
        'M': {
            '0001': ['34', '63', '101', '149', '202', '255', '293', '365', '432', '513', '604', '691', '796', '871', '991', '1082', '1212', '1346', '1500', '1600', '1708', '1872', '2059', '2188', '2395', '2544', '2701', '2857', '3035', '3289', '3486', '3693', '3909', '4134', '4343', '4588', '4775', '5039', '5313', '5596'],
            '0010': ['20', '38', '61', '90', '122', '154', '178', '221', '262', '311', '366', '419', '483', '528', '600', '656', '734', '816', '909', '970', '1035', '1134', '1248', '1326', '1451', '1542', '1637', '1732', '1839', '1994', '2113', '2238', '2369', '2506', '2632', '2780', '2894', '3054', '3220', '3391'],
            '0011': ['14', '26', '42', '62', '84', '106', '122', '152', '180', '213', '251', '287', '331', '362', '412', '450', '504', '560', '624', '666', '711', '779', '857', '911', '997', '1059', '1125', '1190', '1264', '1370', '1452', '1538', '1628', '1722', '1809', '1911', '1989', '2099', '2213', '2331']
        },
        'Q': {
            '0001': ['27', '48', '77', '111', '144', '178', '207', '259', '312', '364', '427', '489', '580', '621', '703', '775', '876', '948', '1063', '1159', '1224', '1358', '1468', '1588', '1718', '1804', '1933', '2085', '2181', '2358', '2473', '2670', '2805', '2949', '3081', '3244', '3417', '3599', '3791', '3993'], 
            '0010': ['16', '29', '47', '67', '87', '108', '125', '157', '189', '221', '259', '296', '352', '376', '426', '470', '531', '574', '644', '702', '742', '823', '890', '963', '1041', '1094', '1172', '1263', '1322', '1429', '1499', '1618', '1700', '1787', '1867', '1966', '2071', '2181', '2298', '2420'],
            '0011': ['11', '20', '32', '46', '60', '74', '86', '108', '130', '151', '177', '203', '241', '258', '292', '322', '364', '394', '442', '482', '509', '565', '611', '661', '715', '751', '805', '868', '908', '982', '1030', '1112', '1168', '1228', '1283', '1351', '1423', '1499', '1579', '1663']
        },
        'H': {
            '0001': ['17', '34', '58', '82', '106', '139', '154', '202', '235', '288', '331', '374', '427', '468', '530', '602', '674', '746', '813', '919', '969', '1056', '1108', '1228', '1286', '1425', '1501', '1581', '1677', '1782', '1897', '2022', '2157', '2301', '2361', '2524', '2625', '2735', '2927', '3057'],
            '0010': ['10', '20', '35', '50', '64', '84', '93', '122', '143', '174', '200', '227', '259', '283', '321', '365', '408', '452', '493', '557', '587', '640', '672', '744', '779', '864', '910', '958', '1016', '1080', '1150', '1226', '1307', '1394', '1431', '1530', '1591', '1658', '1774', '1852'],
            '0011': ['7', '14', '24', '34', '44', '58', '64', '84', '98', '119', '137', '155', '177', '194', '220', '250', '280', '310', '338', '382', '403', '439', '461', '511', '535', '593', '625', '658', '698', '742', '790', '842', '898', '958', '983', '1051', '1093', '1139', '1219', '1273']
        }
    }
    
    num_of_chars = len(data)
    
    for version in range(1, 41):
        if num_of_chars <= int(version_capacities[ec_level][encoding_type][version - 1]):
            return version
    
    if ec_level == "L":
        raise Exception("Input too long, even with lowest EC level.")
    else:
        raise Exception("Input too long. Use a lower EC level or use a shorter input.")


# Step 3: Add the Mode Indicator
# Already retrieved by the determine_encoding function


# Step 4: Add the Character Count Indicator
# Number of bits used for the character count indicator depends on the QR code version and encoding mode

def determine_character_count_indicator(version: int, encoding_mode: str) -> int:
    """
    Description:
        Returns an integer representing the length of the character count indicator, given the specified version and encoding mode

    Args:
        version (int): The version that the QR code is using
        encoding_mode (str): The encoding mode that the QR code is using

    Returns:
        int: The length of the character count indicator
    """
    
    if version <= 9:
        if encoding_mode == '0001':
            return 10
        if encoding_mode == '0010':
            return 9
        if encoding_mode == '0011':
            return 8
    if version <= 26:
        if encoding_mode == '0001':
            return 12
        if encoding_mode == '0010':
            return 11
        if encoding_mode == '0011':
            return 16
    if version <= 40:
        if encoding_mode == '0001':
            return 14
        if encoding_mode == '0010':
            return 13
        if encoding_mode == '0011':
            return 16
    
    raise Exception("Invalid version or encoding mode.")


# Step 5: Encode Using the Selected Mode
# Each encoding mode must be handled differently

def convert_to_binary(encoding_mode: str, data: str) -> str:
    """
    Description:
        Returns a concatenated string of binary after correctly converting the data to binary for the given encoding mode

    Args:
        encoding_mode (str): String of binary representing the encription mode for the given data
        data (str): The data to be encoded into the QR code

    Returns:
        list[str]: A string containing the data converted into binary via the specific method for the encoding type
    """
    
    split_up_data = None
    
    # Numeric Mode
    if encoding_mode == '0001':
        split_up_data = [data[i:i + 3] for i in range(0, len(data), 3)]
        
        # Turn into binary
        for i in range(len(split_up_data)):
            if len(split_up_data[i]) == 3:
                if split_up_data[i][0:2] == '00':
                    split_up_data[i] = bin(int(split_up_data[i]))[2:].zfill(4)
                elif split_up_data[i][0] == '0':
                    split_up_data[i] = bin(int(split_up_data[i]))[2:].zfill(7)
                else:
                    split_up_data[i] = bin(int(split_up_data[i]))[2:].zfill(10)
            elif len(split_up_data[i]) == 2:
                if split_up_data[i][0] == '0':
                    split_up_data[i] = bin(int(split_up_data[i]))[2:].zfill(4)
                else:
                    split_up_data[i] = bin(int(split_up_data[i]))[2:].zfill(10)
            else:
                split_up_data[i] = bin(int(split_up_data[i]))[2:].zfill(4)
    
    # Alphanumeric Mode
    elif encoding_mode == '0010':
        char_mapping = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'A': 10,
            'B': 11,
            'C': 12,
            'D': 13,
            'E': 14,
            'F': 15,
            'G': 16,
            'H': 17,
            'I': 18,
            'J': 19,
            'K': 20,
            'L': 21,
            'M': 22,
            'N': 23,
            'O': 24,
            'P': 25,
            'Q': 26,
            'R': 27,
            'S': 28,
            'T': 29,
            'U': 30,
            'V': 31,
            'W': 32,
            'X': 33,
            'Y': 34,
            'Z': 35,
            ' ': 36,
            '$': 37,
            '%': 38,
            '*': 39,
            '+': 40,
            '-': 41,
            '.': 42,
            '/': 43,
            ':': 44
        }
        
        split_up_data = [data[i:i + 2] for i in range(0, len(data), 2)]
        
        # Turn into binary
        for i in range(len(split_up_data)):
            if len(split_up_data[i]) == 1:
                split_up_data[i] = bin(char_mapping[split_up_data[i]])[2:].zfill(6)
            else:
                split_up_data[i] = bin(char_mapping[split_up_data[i][0]]*45 + char_mapping[split_up_data[i][1]])[2:].zfill(11)
    
    # Byte Mode
    elif encoding_mode == '0011':
        split_up_data = list(data)
        
        # Turn into binary
        for i in range(len(split_up_data)):
            # Thonky says to convert to hex, then to binary, but I will skip straight to binary
            print(bin(ord(split_up_data[i]))[2:].zfill(8))
    
    if split_up_data is not None:
        return ''.join(split_up_data)

    raise Exception("Data not encoded in a supported mode.")


# Step 6: Up into 8-bit Codewords and Add Pad Bytes if Necessary

# Helper function to get the number of EC codewords for a specific version and EC level
def get_num_of_codewords(version: int, ec_level: str, block: int) -> int:
    """
    
    Args:
        version (int): The version of the QR code
        ec_level (str): The error correction level of the QR code
        block (int): Which block to get the codeword count for. 0 returns the total number of codewords for the given version and EC level

    Returns:
        int: The number of codewords needed for the specified version and EC level
    """
    
    num_of_codewords = {
		"1-L": [19, 7],
		"1-M": [16, 10],
		"1-Q": [13, 13],
		"1-H": [9, 17],
		"2-L": [34, 10],
		"2-M": [28, 16],
		"2-Q": [22, 22],
		"2-H": [16, 28],
		"3-L": [55, 15],
		"3-M": [44, 26],
		"3-Q": [34, 18],
		"3-H": [26, 22],
		"4-L": [80, 20],
		"4-M": [64, 18],
		"4-Q": [48, 26],
		"4-H": [36, 16],
		"5-L": [108, 26],
		"5-M": [86, 24],
		"5-Q": [62, 18],
		"5-H": [46, 22],
		"6-L": [136, 18],
		"6-M": [108, 16],
		"6-Q": [76, 24],
		"6-H": [60, 28],
		"7-L": [156, 20],
		"7-M": [124, 18],
		"7-Q": [88, 18],
		"7-H": [66, 26],
		"8-L": [194, 24],
		"8-M": [154, 22],
		"8-Q": [110, 22],
		"8-H": [86, 26],
		"9-L": [232, 30],
		"9-M": [182, 22],
		"9-Q": [132, 20],
		"9-H": [100, 24],
		"10-L": [274, 18],
		"10-M": [216, 26],
		"10-Q": [154, 24],
		"10-H": [122, 28],
		"11-L": [324, 20],
		"11-M": [254, 30],
		"11-Q": [180, 28],
		"11-H": [140, 24],
		"12-L": [370, 24],
		"12-M": [290, 22],
		"12-Q": [206, 26],
		"12-H": [158, 28],
		"13-L": [428, 26],
		"13-M": [334, 22],
		"13-Q": [244, 24],
		"13-H": [180, 22],
		"14-L": [461, 30],
		"14-M": [365, 24],
		"14-Q": [261, 20],
		"14-H": [197, 24],
		"15-L": [523, 22],
		"15-M": [415, 24],
		"15-Q": [295, 30],
		"15-H": [223, 24],
		"16-L": [589, 24],
		"16-M": [453, 28],
		"16-Q": [325, 24],
		"16-H": [253, 30],
		"17-L": [647, 28],
		"17-M": [507, 28],
		"17-Q": [367, 28],
		"17-H": [283, 28],
		"18-L": [721, 30],
		"18-M": [563, 26],
		"18-Q": [397, 28],
		"18-H": [313, 28],
		"19-L": [795, 28],
		"19-M": [627, 26],
		"19-Q": [445, 26],
		"19-H": [341, 26],
		"20-L": [861, 28],
		"20-M": [669, 26],
		"20-Q": [485, 30],
		"20-H": [385, 28],
		"21-L": [932, 28],
		"21-M": [714, 26],
		"21-Q": [512, 28],
		"21-H": [406, 30],
		"22-L": [1006, 28],
		"22-M": [782, 28],
		"22-Q": [568, 30],
		"22-H": [442, 24],
		"23-L": [1094, 30],
		"23-M": [860, 28],
		"23-Q": [614, 30],
		"23-H": [464, 30],
		"24-L": [1174, 30],
		"24-M": [914, 28],
		"24-Q": [664, 30],
		"24-H": [514, 30],
		"25-L": [1276, 26],
		"25-M": [1000, 28],
		"25-Q": [718, 30],
		"25-H": [538, 30],
		"26-L": [1370, 28],
		"26-M": [1062, 28],
		"26-Q": [754, 28],
		"26-H": [596, 30],
		"27-L": [1468, 30],
		"27-M": [1128, 28],
		"27-Q": [808, 30],
		"27-H": [628, 30],
		"28-L": [1531, 30],
		"28-M": [1193, 28],
		"28-Q": [871, 30],
		"28-H": [661, 30],
		"29-L": [1631, 30],
		"29-M": [1267, 28],
		"29-Q": [911, 30],
		"29-H": [701, 30],
		"30-L": [1735, 30],
		"30-M": [1373, 28],
		"30-Q": [985, 30],
		"30-H": [745, 30],
		"31-L": [1843, 30],
		"31-M": [1455, 28],
		"31-Q": [1033, 30],
		"31-H": [793, 30],
		"32-L": [1955, 30],
		"32-M": [1541, 28],
		"32-Q": [1115, 30],
		"32-H": [845, 30],
		"33-L": [2071, 30],
		"33-M": [1631, 28],
		"33-Q": [1171, 30],
		"33-H": [901, 30],
		"34-L": [2191, 30],
		"34-M": [1725, 28],
		"34-Q": [1231, 30],
		"34-H": [961, 30],
		"35-L": [2306, 30],
		"35-M": [1812, 28],
		"35-Q": [1286, 30],
		"35-H": [986, 30],
		"36-L": [2434, 30],
		"36-M": [1914, 28],
		"36-Q": [1354, 30],
		"36-H": [1054, 30],
		"37-L": [2566, 30],
		"37-M": [1992, 28],
		"37-Q": [1426, 30],
		"37-H": [1096, 30],
		"38-L": [2702, 30],
		"38-M": [2102, 28],
		"38-Q": [1502, 30],
		"38-H": [1142, 30],
		"39-L": [2812, 30],
		"39-M": [2216, 28],
		"39-Q": [1582, 30],
		"39-H": [1222, 30],
		"40-L": [2956, 30],
		"40-M": [2334, 28],
		"40-Q": [1666, 30],
		"40-H": [1276, 30],
	}
    
    return num_of_codewords[f"{version}-{ec_level}"][block]


def convert_to_codewords(version: int, ec_level: str, encoding_type: str, char_count_indicator: str, binary_data: str) -> list[str]:
    """
    Description:
        Ensures the encoded data contains the correct amount of bits, then returns the full encoded binary data as a list of the binary string separated into bytes. 

    Args:
        version (int): Version of the QR code
        ec_level (str): Error Correction level used in the QR code
        encoding_type (str): Encoding mode used in the QR code
        char_count_indicator (str): Binary string containing the character count indicator
        binary_data (str): Data to be encoded into the QR code in a string of binary

    Returns:
        list: Returns a list containing the full binary data, separated into bytes
    """
    
    num_of_bits = get_num_of_codewords(version, ec_level, 0) * 8
    
    bit_string = encoding_type + char_count_indicator + binary_data
    
    # Add up to 4 0s as a terminator
    if len(bit_string) <= num_of_bits:
        bit_string += '0' * min(num_of_bits - len(bit_string), 4)
    
    # Add padding 0s to the end until it is a multiple of 8 bits
    while len(bit_string)%8 != 0:
        bit_string += '0'
    
    repeating_bytes = ["11101100","00010001"]
    
    while len(bit_string) != num_of_bits:
        bit_string += repeating_bytes[int((num_of_bits - len(bit_string))/8)%2]
    
    
    return [bit_string[i:i+8] for i in range(0,len(bit_string),8)]


####################################
# Stage 3: Error Correction Coding
# https://www.thonky.com/qr-code-tutorial/error-correction-coding

####################################

# Step 1: Break Data Codewords into Blocks if Necessary
# TODO come back to this


# Step 2: Polynomial Long Division
# TODO come back to this


# TODO Steps 3-6


# Step 7: The Generator Polynomial
# Start by generating the Message Polynomial
def generate_message_polynomial(codewords: list[str]) -> list[int]:
    """
    Takes the codewords, broken into 8-bit bytes, and returns the alpha_exponents of the polynomial, starting with the highest coefficient at index 0

    Args:
        codewords (list[str]): An array of codewords broken into 8-bit bytes

    Returns:
        list[int]: Returns a list containing the alpha_exponents of the polynomial, starting with the highest coefficient at index 0
    """
    
    converted_to_ints = []
    
    for i in range(len(codewords)):
        converted_to_ints.append(int(codewords[i], base=2))
    
    return converted_to_ints

# Helper function for the Galois Field
def gf256(exp: int) -> int:
    """Returns the value of 2**exp inside the Galois Field 256

    Args:
        exp (int): The exponent of 2**exp

    Returns:
        int: Returns 2**exp in the Galois Field 256
    """
    
    if exp > 255:
        exp %= 285
    
    if exp < 0:
        return -1
    if exp <= 7:
        return 2**exp
    
    num = (2**8)^285
    for _ in range(8, exp):
        num *= 2
        if num > 255:
            num ^= 285
    
    return num

# Helper function to reverse the Galois Field
def reverse_gf256(n: int) -> int:
    for i in range(256):
        if gf256(i) == n:
            return i
    
    return -1

# Sepcialised helper function for bracket expansion
def expand_brackets(expr1: list[str], expr2: list[str]) -> list[str]:
    """Takes 2 polynomials as input, multiplies them together, and returns a list of strings that contain the coefficients of x in the new polynomial

    Args:
        expr1 (list[str]): A list of strings containing the coefficients of x. The first term should be 1; all other terms should be in alpha notation
        expr2 (list[str]): A list of strings containing the coefficients of x. The first term should be 1; the other term should be in alpha notation

    Returns:
        list[str]: Returns a list of strings that contain the coefficients of x in the polynomial
    """
    
    # Make a copy to multiply by a{n}
    temp = copy(expr1)
    
    temp[0] = str(gf256(int(expr2[1].replace('a', ''))))
    
    for i in range(1, len(temp)):
        temp[i] += expr2[1]
        temp[i] = str(gf256(eval(temp[i].replace('a', '+')[1:])))
    
    # Multiply the original by x
    expr1 += ['0']
    
    for i in range(1, len(expr1)-1):
        expr1[i] = str(gf256(int(expr1[i].replace('a', ''))))
    
    # Add the 2 expressions together and simplify
    for i in range(1, len(expr1)):
        expr1[i] = str(int(expr1[i]) ^ int(temp[i-1]))
        expr1[i] = 'a' + str(reverse_gf256(int(expr1[i])))
    
    return expr1

# Next, generate the Generator Polynomial
def generate_generator_polynomial(version: int, ec_level: str, block: int) -> list[int]:
    """Generates the Generator Polynomial used for Reed-Solomon Error Correction. Returns a list of integers containing the coefficients of x

    Args:
        version (int): The QR code's version
        ec_level (str): The QR code's error correction level
        block (int): Which block to check the number of needed codewords

    Returns:
        list[int]: A list of integers containing the coefficients of x in the generator polynomial
    """
    
    num_of_codewords = get_num_of_codewords(version, ec_level, block)
    
    polynomial = ['1', 'a0']
    
    for i in range(1, num_of_codewords):
        polynomial = expand_brackets(polynomial, ['1', f"a{i}"])
    
    alpha_exponents = [0]
    
    for i in range(1, len(polynomial)):
        alpha_exponents.append(int(polynomial[i].replace('a', '')))
    
    return alpha_exponents


# Step 9: Divide the Message Polynomial by the Generator Polynomial
def polynomial_division(version: int, ec_level: str, poly1: list[int], poly2: list[int]) -> list[int]:
    """_summary_

    Args:
        version (int): The version of the QR code
        ec_level (str): The error coding level for the QR code
        poly1 (list[int]): The message polynomial
        poly2 (list[int]): The generator polynomial

    Returns:
        list[int]: Returns the error codewords to be put into the QR code
    """
    
    msg_poly = copy(poly1)
    msg_poly += [0] * get_num_of_codewords(version, ec_level, 1)

    for _ in range(get_num_of_codewords(version, ec_level, 0)):
        gen_poly = copy(poly2)
    
        # Convert message polynomial to alpha notation
        msg_poly = [-1 if msg_poly[i] == 1 else msg_poly[i] for i in range(len(msg_poly))]
        msg_poly = [reverse_gf256(msg_poly[i]) if msg_poly[i] != 0 else msg_poly[i] for i in range(len(msg_poly))]
    
        # Multiply the generator polynomial by the lead term of the message polynomial
        gen_poly = [gen_poly[i] + msg_poly[0] for i in range(len(gen_poly))]
        
        for i in range(len(gen_poly)):
            if gen_poly[i] > 255:
                gen_poly[i] %= 255
        
        # Convert both polynomials to integer notation
        msg_poly = [gf256(msg_poly[i]) if msg_poly[i] != 0 else msg_poly[i] for i in range(len(msg_poly))]
        gen_poly = [gf256(gen_poly[i]) if gen_poly[i] != 0 else gen_poly[i] for i in range(len(gen_poly))]
        
        msg_poly = [1 if msg_poly[i] == -1 else msg_poly[i] for i in range(len(msg_poly))]
        
        # Add 0s to the end of gen_poly to make it the same length as msg_poly
        gen_poly += [0] * (len(msg_poly) - len(gen_poly))
        
        # XOR the two polynomials together
        msg_poly = [msg_poly[i] ^ gen_poly[i] for i in range(len(msg_poly))]
        
        # Remove the leading 0
        if msg_poly[0] == 0:
            del msg_poly[0]
        
        # Convert gen_poly back to alpha notation for the next loop
        gen_poly = [gf256(gen_poly[i]) for i in range(len(gen_poly))]
    
    return msg_poly







# Function to combina all the stages and generate the complete QR code
def generate_qr_code(data: str, ec_level: str, output: bool = False) -> None:
    """
    Description:
        Takes the desired data and EC level and generates a QR code

    Args:
        data (str): Data to be encoded into a QR code
        ec_level (str): Predefined Error Correction Level (e.g., 'L, 'M', 'Q', 'H')
        output (bool, optional): Whether or not it should print relevant info. Defaults to False.
    """
    
    if output:
        print("Data:", data)
    
    encoding_type = determine_encoding(data)
    if output:
        print("Encoding:", encoding_type)
    
    version = determine_version(encoding_type, ec_level, data)
    if output:
        print("Version:", version)
    
    if output:
        print("Error Correction level:", ec_level)
    
    character_count_indicator = bin(len(data))[2:].zfill(determine_character_count_indicator(version, encoding_type))
    if output:
        print("Character count indicator:", character_count_indicator)
    
    binary_data = convert_to_binary(encoding_type, data)
    if output:
        print("Binary data:", binary_data)
    
    codewords = convert_to_codewords(version, ec_level, encoding_type, character_count_indicator, binary_data)
    if output:
        print("Codewords:", codewords)
    
    message_polynomial = generate_message_polynomial(codewords)
    if output:
        print("Message polynomial:", message_polynomial)
    
    generator_polynomial = generate_generator_polynomial(version, ec_level, 1)
    if output:
        print("Generator polynomial:", generator_polynomial)
    
    error_codewords = polynomial_division(version, ec_level, message_polynomial, generator_polynomial)
    if output:
        print("Error codewords:", error_codewords)
    
    return



def main() -> None:
    data = "HELLO WORLD"
    error_correction_level = "M"
    
    print("Running main...\n")
    generate_qr_code(data, error_correction_level, True)
    
    return

if __name__ == "__main__":
    main()