def convertHex(hexdata):
#https://www.binaryhexconverter.com/hex-to-decimal-converter
# https://www.w3schools.com/python/ref_func_int.asp
# Trim '0x' from beginning of string
    hexdataTrimed = hexdata[2:]

    # Split trimmed string every 64 characters
    n = 64
    dataSplit = [hexdataTrimed[i:i+n] for i in range(0, len(hexdataTrimed), n)]

    # Fill new list with converted decimal values
    data = []
    for val in range(len(dataSplit)):
        toDec = int(dataSplit[val], 16)
        data.append(toDec)

    return data
