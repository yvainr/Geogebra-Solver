output_num = 6 
#number of output strings

extra_symbols = {33, 35, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 58, 60, 61, 62, 63, 64, 92, 93, 94, 95, 96, 123, 124, 125, 126}
#ord of extra symbols

def extra_symbols_deleting(inp_str):
    input_str = ""
    for i in range(len(inp_str)):
        try:
            if ord(inp_str[i]) not in extra_symbols:
                input_str = input_str[:] + str(inp_str[i])            
        except:
            pass
    return input_str

def input_str(inp_str):
    #func for input split
    inp_str = inp_str.split(';')
    return inp_str


def print_ret(inp_str):
    #func for final output
    # print(inp_str)
    for i in range(output_num):
        if ord(inp_str[i][0]) == 32:
            inp_str[i] = inp_str[i][1:]
        print(inp_str[i])


def spaces_normalize(inp_str):
    #func for deleting extra spaces
    for i in range(len(inp_str) - 2):
        try:
            if ord(inp_str[i]) == 32:
                if ord(inp_str[i+1]) == 32 or ord(inp_str[i+1]) == 44:
                    inp_str = inp_str[:i+1] + inp_str[i+2:]
        except:
            pass
    return inp_str


def comma_normalize(inp_str):   
    #func for deleting extra commas
    for i in range(len(inp_str) - 1):
        try:
            if ord(inp_str[i]) == 44:
                if ord(inp_str[i+1]) == 44:
                    inp_str = inp_str[:i] + inp_str[i+1:]
                if ord(inp_str[i+1]) == 32 and (ord(inp_str[i+2]) == 44 or ord(inp_str[i+2]) == 32):
                    inp_str = inp_str[:i+1] + inp_str[i+2:]
        except:
            pass
    return inp_str


inp = "ABC    ; BD,, % ***** ,CD ; ABC 30 ; '' ; } ]]'' ; '' "

inp = extra_symbols_deleting(inp)
inp = spaces_normalize(inp)
inp = comma_normalize(inp)
inp = input_str(inp)
print_ret(inp)
