import re

class Tokenizer:
    def __init__(self):
        self.tokens = []
        self.tokenizers = []
        self.current = 0

        self.keywords = [
            'class ', 'constructor ', 'function ', 'method ', 'field ', 'static ', 'var ', 'int ', 'char ', 'boolean ',
            'void ', 'true', 'false', 'null', 'this', 'let ', 'do ', 'while ', 'if ', 'else ', 'return '
        ]
        self.symbols = [
            '\{', '\}', '\(', '\)', '\[', '\]', '\.', '\,', '\;', '\+',
            '\-', '\=', '\*', '\/', '\&', '\|', '\<', '\>', '\~'
        ]

        self.tokenizeLexicon('keyword', self.keywords)
        self.tokenizeLexicon('symbol', self.symbols)
        self.tokenizeLexicon('whitespace', [r'\s+'])
        self.tokenizeLexicon('integerConstant', [r'\d+'])
        self.tokenizeLexicon('stringConstant', [r'".*?"'])
        self.tokenizeLexicon('identifier', [r'_*[a-zA-Z]+[0-9_]*[a-zA-Z]*'])

    # tokenize the supplied file
    def tokenize(self, file):
        # checks for comments and eliminates them
        inCommentMode = False
        for line in file:
            if line == '\n': continue
            if line.find('/**') > -1:
                inCommentMode = True
            if line.find('*/') > -1:
                inCommentMode = False
                continue
            if inCommentMode: continue
            singleLineCommentIndex = line.find('//')
            if singleLineCommentIndex > -1:
                line = line[:singleLineCommentIndex]

            # track the current point in the currently being processed line
            self.current = 0

            while self.current < len(line):
                tokenized = False

                # for each token, loop through all the tokenizer functions
                for token_function in self.tokenizers:
                    if tokenized : break # if already tokenized, break out of 'for' loop
                    isTokenized = token_function['regex'].match(r'{0}'.format(line[self.current:]))

                    if isTokenized is not None: # if a token match is found at the beginning of current line
                        if token_function['type'] == 'whitespace': # discard if whitespace
                            self.current += 1
                        else:
                            token_value = {}
                            token_value['type'] = token_function['type']
                            if token_function['type'] == 'stringConstant':
                                token_value['value'] = isTokenized.group()[1:-1] # remove the quotes at begining and end
                            else:
                                token_value['value'] = isTokenized.group().strip()

                            self.tokens.append(token_value) # add token to tokens list

                            # advance line by the length of token just found
                            tokenSpan = isTokenized.span()
                            self.current += tokenSpan[1] - tokenSpan[0]

                        # sets tokenized to 'True'
                        tokenized = True

                # raise exception if no token function recognises token
                if not tokenized:
                    raise Exception('Token {0} not recognized'.format(line[self.current]))
        return self.tokens


    # creates a token function for each elemnt of the supplied list
    def tokenizeLexicon(self, tokenType, lexiconList):
        for lexicon in lexiconList:
            self.build_tokenizer(tokenType, lexicon)

    # builds the tokenizer function
    def build_tokenizer(self, tokenType, lexicon):
        token_function = {}
        token_function['type'] = tokenType
        token_function['regex'] = re.compile(lexicon)
        self.tokenizers.append(token_function)