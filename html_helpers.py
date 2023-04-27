def capitalize_each_word(s):
    ''' perform capitalization for a given english phrase in frontend call '''
    return ' '.join(word.capitalize() for word in s.split())


def combine_written(l):
    ''' combine the words in a given list for written '''
    combined = ""
    for word in l:
        combined = combined + word + " "
    
    combined = combined.strip()
    return combined

