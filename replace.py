def replace(test_string="", replace_string=""):
	if replace_string == "":
        return test_string
    n = test_string.find(replace_string)
    return_string = ""
    if n == -1:
        return_string = test_string
    else:
        return_string = test_string[0:n] + "bodega" + \
            test_string[n + len(replace_string) - 1:]

    return return_string
print (replace("Hi how are you?", "you"))
