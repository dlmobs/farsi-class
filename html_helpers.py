# helper functions for html files

def capitalize_each_word(s):
    ''' perform capitalization for a given english phrase in frontend call '''
    return ' '.join(word.capitalize() for word in s.split())


def capitalize_first_word(s):
    return s[0].upper() + s[1:]


def combine_list(l):
    ''' combine the words in a given list '''
    combined = ""
    for word in l:
        combined = combined + word + " "
    
    combined = combined.strip()
    return combined

