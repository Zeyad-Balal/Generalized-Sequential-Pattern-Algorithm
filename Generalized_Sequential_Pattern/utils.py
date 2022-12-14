def substr(substr, str):
    # frequency array for both strings
    freq_substr = {}
    freq_str = {}

    for char in substr:
        if char not in freq_substr:
            freq_substr[char] = 1
        else:
            freq_substr[char] += 1

    for char in str:
        if char not in freq_str:
            freq_str[char] = 1
        else:
            freq_str[char] += 1

    # check if characters of substr are present in str
    for char in substr:
        if char not in freq_str:
            return False

        if freq_substr[char] > freq_str[char]:
            return False

    return True
