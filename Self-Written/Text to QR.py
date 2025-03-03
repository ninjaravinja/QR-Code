
# https://www.thonky.com/qr-code-tutorial/
# https://www.thonky.com/qr-code-tutorial/data-encoding

# https://www.sproutqr.com/blog/how-do-qr-codes-work

# Storing on GitHub to track changes
# https://github.com/ninjaravinja/QR-Code-Game/tree/main


# Starting with a version 1 (21x21) for simplicity
# and to understand the concept


# This will hold all bits for the final code
# (may need reworking)
codeSections = []


# STEP 1: ERROR CORRECTION LEVEL

# I will only be using Error Correction level M for now




# STEP 2: SMALLEST VERSION FOR THE DATA

# hard-coding for now
version = 1

# (will come back with automation, for now defaulting to 21x21/V1)
# Also probably won't add support for every version (straight away)
# as v40 has 31329 pixels which would be a lot to manage

# Error correction character capacities:
# https://www.thonky.com/qr-code-tutorial/character-capacities

# Content to be displayed in the QR code
message = "HELLO WORLD" # short enough for V1 w/ EC level M
# could automate version by checking length
maxChars = 8 * 16

# The rest of this code is written in the encoding section
# as it needs to be handled differently depending on the mode




# STEP 3: ADD THE MODE INDICATOR

# I will not be using any mode above byte code as VSCode uses
# UTF-8 by default so a larger charset will not be needed

# Indicate which mode the data is in (defined later)
modeIndicator = ""

# Numeric (0001) - 0-9
# Alphanumeric (0010) - A-Z, 0-9, $, %, *, +, -, ., /, :
# Byte (0100) - all chars from ISO-8859-1 or UTF-8

# Lists to check message chars against
numeric = "0123456789"
alphanumeric = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

# Automating the Mode Indicator by checking chars against the allowed
# charsets (defined in the lists above)
if any(message[i] not in alphanumeric for i in range(len(message))):
    modeIndicator = "0100"
elif any(message[i] not in numeric for i in range(len(message))):
    modeIndicator = "0010"
else:
    modeIndicator = "0001"

#print(modeIndicator)
codeSections.append(modeIndicator)




# STEP 4: ADD THE CHARACTER COUNT INDICATOR

# How many unique characters are the data
# Look at character capacity table
charCount = 0
for i in range(len(message)):
    charCount += 1

binCharCount = bin(charCount)[2:]

# Amount of bits depends on version and mode
# I have skipped modes I am not using
fillNum = 8 # Will never be less than 8 so I chose to default to this

def fillBits():
    if 0 < version < 10:
        if modeIndicator == "0001":
            fillNum = 10
        elif modeIndicator == "0010":
            fillNum = 9
        elif modeIndicator == "0100":
            fillNum = 8
    elif 9 < version < 27:
        if modeIndicator == "0001":
            fillNum = 12
        elif modeIndicator == "0010":
            fillNum = 11
        elif modeIndicator == "0100":
            fillNum = 16
    elif 26 < version < 41:
        if modeIndicator == "0001":
            fillNum = 14
        elif modeIndicator == "0010":
            fillNum = 13
        elif modeIndicator == "0100":
            fillNum = 16
    return fillNum

binCharCount = binCharCount.zfill(fillBits())
codeSections.append(binCharCount)




# STEP 5: ENCODE USING THE SELECTED MODE

# https://www.thonky.com/qr-code-tutorial/data-encoding#step-3-encode-using-the-selected-mode

# Each mode needs to be encoded differently

# Convert the string into a list of chars to be popped
tempMessage = []

for i in range(len(message)):
    tempMessage.append(message[i])


# Numeric:
def pop3():
    hold = ""
    count = 0
    while count < 3 and len(tempMessage) != 0:
        hold += tempMessage.pop(0)
        count += 1
    hold = bin(int(hold[:]))[2:].zfill(4)
        
    return hold

def numericEncoding():
    result = []
    if len(tempMessage)%3 != 0:
        for i in range(len(tempMessage)//3 + 1):
            result.append(pop3())

    elif len(tempMessage)%3 == 0:
        for i in range(len(tempMessage)//3):
            result.append(pop3())
    
    return result


# Alphanumeric:
# (45*{1st letter value from table}) + {2nd letter value from table}
# https://www.thonky.com/qr-code-tutorial/alphanumeric-table
def pop2():
    hold = ""
    count = 0
    while count < 2 and len(tempMessage) != 0:
        hold += tempMessage.pop(0)
        count += 1
    
    return hold

def alphanumericEncoding():
    values = [0, 0]
    result = []
    oddChars = False
    if len(tempMessage)%2 != 0:
        for i in range(len(tempMessage)//2 + 1):
            value = []
            singleChars = []
            twoChars = pop2()
            for j in range(len(twoChars)):
                singleChars.append(twoChars[j])
            #print(singleChars)
            if len(singleChars) == 2:
                for k in range(len(singleChars)):
                    for l in range(len(alphanumeric)):
                        if alphanumeric[l] == singleChars[k]:
                            if k == 0:
                                values[0] = l
                            elif k == 1:
                                values[1] = l
                #print(values, (45*values[0])+values[1])
                result.append((45*values[0])+values[1])
            elif len(singleChars) == 1:
                oddChars = True
                for k in range(len(alphanumeric)):
                    if alphanumeric[k] == singleChars[0]:
                        value = k
                result.append(value)
        #print(result)

    elif len(tempMessage)%2 == 0:
        for i in range(len(tempMessage)//2):
            twoChars = pop2()
            singleChars = []
            for j in range(len(twoChars)):
                singleChars.append(twoChars[j])
            #print(singleChars)
            if len(singleChars) == 2:
                for k in range(len(singleChars)):
                    for l in range(len(alphanumeric)):
                        if alphanumeric[l] == singleChars[k]:
                            if k == 0:
                                values[0] = l
                            elif k == 1:
                                values[1] = l
                #print(values, (45*values[0])+values[1])
                result.append((45*values[0])+values[1])

    
    for i in range(len(result)):
        result[i] = bin(result[i])[2:].zfill(11)
    if oddChars == True:
        result[-1] = result[-1][len(result[-1])-6:]

    return result


# Byte Mode:
# https://www.thonky.com/qr-code-tutorial/byte-mode-encoding
def byteEncoding(): # Convert each character to ISO 8859-1
    byteEncoded = []
    for i in range(len(tempMessage)):
        byteEncoded.append(bin(ord(tempMessage[i]))[2:].zfill(8))
    #print(byteEncoded)
    
    return byteEncoded


# Depending on the mode indicator, encode the message
if modeIndicator == "0001":
    bits = numericEncoding()
elif modeIndicator == "0010":
    bits = alphanumericEncoding()
elif modeIndicator == "0100":
    bits = byteEncoding()

# Add the encoded message to the total progress
for i in range(len(bits)):
    codeSections.append(bits[i])




# STEP 6: BREAK UP INTO 8-BIT CODEWORDS AND ADD PAD BYTES IF NECESSARY
# https://www.thonky.com/qr-code-tutorial/error-correction-table

# 16 * 8 = 128
def terminator():
    bitString = ""
    terminator = ""
    for i in range(len(codeSections)):
        bitString = bitString + codeSections[i]

    if len(bitString) < maxChars:
        if len(bitString) > 100:
            terminator = ["0" for i in range(maxChars-len(bitString))]
        elif len(bitString) <= 100:
            terminator = "0000"
    return terminator

#print(len(bitString), terminator)
codeSections.append(terminator())


# The total length of the bits must now be a multiple of 8
totalLength = 0
for i in range(len(codeSections)):
    for j in range(len(codeSections[i])):
        totalLength += 1

if totalLength%8 != 0:
    for i in range(8-(totalLength%8)):
        codeSections[-1] = codeSections[-1] + "0"
        totalLength += 1


# Add Pad Bytes if the String is Still too Short
# keep adding '11101100 00010001' in a repeating pattern
# until it is the corect length

bytesToAdd = (maxChars-totalLength)//8
for i in range(bytesToAdd):
    if i%2 != 0:
        codeSections.append("00010001")
    elif i%2 == 0:
        codeSections.append("11101100")
    totalLength += 8
# print(totalLength)


#print(codeSections)



# ERROR CORRECTION CODING
# https://www.thonky.com/qr-code-tutorial/error-correction-coding

# Step 1 can be skipped for v1 codes

# Polynomial long division


# Galois Field
# will always be GF(256) for QR Codes
# Uses absolute values of numbers (no negatives)

# Byte-Wise modulo
# 1 + 1 = 2 % 2 = 0
# also written as 1 ^ 1 = 0
# equivalent to XOR



# Logs and Antilogs
def logGen():
    log = {}
    overflow = 0
    for i in range(8):
        log[i] = 2**i
    for i in range(8,255):
        if overflow == 0:
            overflow = int(2**i) ^ 285
        elif overflow >= 256:
            overflow = overflow ^ 285
        elif overflow < 256:
            overflow = overflow * 2
            if overflow > 255:
                overflow = overflow ^ 285
        log[i] = overflow
    
    return log # Key is exponent of a, value is integer
                # e.g., 5: 32

logs = logGen() # [integer]:[exponent of a]


def antilogGen():
    antilog = {}
    overflow = 0
    for i in range(1,8):
        antilog[2**i] = i
    for i in range(8,256):
        if overflow == 0:
            overflow = int(2**i) ^ 285
        elif overflow >= 256:
            overflow = overflow ^ 285
        elif overflow < 256:
            overflow = overflow * 2
            if overflow > 255:
                overflow = overflow ^ 285
        antilog[overflow] = i
    
    return antilog # Key is integer, value is exponent of a
                    # e.g., 32: 5

antilogs = antilogGen() # [exponent of a]:[integer]


def codewords():
    bitString = ""
    for i in range(len(codeSections)):
        for j in range(len(codeSections[i])):
            bitString += codeSections[i][j]
    
    # print(bitString)
    
    codeBits = []
    for i in range(len(bitString)//8):
        temp = ""
        temp += bitString[i*8:(i*8)+8]
        
        codeBits.append(temp)
    # print(codeBits)
    
    return codeBits

codeBits = codewords()
# print(codeBits)


def msgToAlpha():
    msgInts = []
    for i in range(len(codeBits)):
        msgInts.append(int(codeBits[i], 2))
    
    return msgInts

msgInts = msgToAlpha()


def intToAlpha():
    alphaExps = []
    for i in range(len(msgInts)):
        msgKey = [val for key, val in antilogs.items() if key == msgInts[i]][0]
        alphaExps.append(msgKey)
    
    print(alphaExps)
    
    return alphaExps

msgAlphaExps = intToAlpha()






