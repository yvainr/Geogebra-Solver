output_num = 6 
#number of output strings

def input_str(inp_str):
    inp_str = inp_str.split('/n')
    return inp_str

#func for input split

def print_ret(inp_str):
    print(inp_str)
    for i in range(output_num):
        if ord(inp_str[i][0]) == 32:
            inp_str[i] = inp_str[i][1:]
        print(inp_str[i])
        # print(";)")

#func for final output

def spaces_normalize(inp_str):
    for i in range(len(inp_str) - 1):
        try:
            if ord(inp_str[i]) == 32:
                if ord(inp_str[i+1]) == 32:
                    inp_str = inp_str[:i] + inp_str[i+1:]
        except:
            pass
    return inp_str

#func for deleting extra spaces

def comma_normalize(inp_str):
    for i in range(len(inp_str) - 1):
        try:
            if ord(inp_str[i]) == 44:
                if ord(inp_str[i+1]) == 44:
                    inp_str = inp_str[:i] + inp_str[i+1:]
        except:
            pass
    return inp_str

#func for deleting extra commas

inp = "ABC    /n BD,, CD /n ABC 30 /n '' /n '' /n '' "

inp = spaces_normalize(inp)
inp = comma_normalize(inp)
inp = input_str(inp)
print_ret(inp)

#_____________working code_________________
