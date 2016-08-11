def compress(str1):
    prev = ''
    count = 1
    res = ''
    total = len(str1)
    counter = 0
    for i in str1:
        counter += 1
        if prev == i:
            count += 1
        else:
            if count > 1:
                res += str(count)
            res += i
            count = 1
        prev = i
        if total == counter and count > 1:
            res += str(count)
    return res
