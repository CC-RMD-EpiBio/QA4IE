import re

def tokenizer(text):

    tokens = []
    offset = 0
    for token in re.split(r'(\W+)', text):
        if token.rstrip():
            tokens.append((offset, offset + len(token.rstrip()), token.rstrip()))
        offset += len(token)

    return tokens

