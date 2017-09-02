def word_distribution(input):
    input = input.lower()
    ls = input.split()
    dt = {}
    for keys in ls:
        #print(keys)
        if not keys[-1].isalpha():
            keys = keys[:-1]
        if not keys[0].isalpha():
            keys = keys[1:]
        val = dt.get(keys)
        #print(dt)
        #print(val)
        if val is not None:
            val = val + 1
            #del dt[keys]
            dt[keys] = val
        else:
            dt[keys] = 1
    return dt