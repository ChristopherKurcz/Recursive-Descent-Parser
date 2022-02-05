# created by Christopher Kurcz
# PSU ID: cjk6056
# purpose of file: A recursive descent parser for a simplified HTML language


# imports
import sys


# global constants
STRING, KEYWORD, EOI, INVALID = 1, 2, 3, 4
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
KEYWORDS = ["body","b","i","ul","li"]



# class representing a Token Object
# A Token object holds its type and tis value
class Token:
    # a token has two fields, its type and its value
    def __init__ (self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal


    # getters for token type and token value
    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val


    # different token types have different ways of representing themselves
    def __repr__(self):
        # STRINGs and KEYWORDs are just the value of the token
        if self.type in [STRING, KEYWORD]:
            return self.val
        # EOIs are just an empty string
        elif self.type == EOI:
            return ""
        # INVALIDs return a string
        else:
            return "invalid"



# class representing a Lexer Object
# A Lexer object goes through some input string and finds a seriers of tokens
class Lexer:
    # a lexer takes only one field, a statement string, but also keeps track of its index
    def __init__ (self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()


    # finds the next token in the statement string
    def nextToken(self):
        while True:
            # if the current character is a letter or a digit, 
            #   it will continuely take them in until it reaches another character type,
            #   and then return the token containing the string of letters and digits
            if self.ch.isalpha() or self.ch.isdigit():
                id = self.consumeChars(LETTERS+DIGITS)
                return Token(STRING, id)

            # if the current character is a space, it will move on to the next character
            elif self.ch==' ': self.nextChar()

            # if the current character is "<", it means it is the start of a keyword
            elif self.ch=='<':
                self.nextChar()

                # if the body of the keyword begins with a "/", then it means it is a closing keyword
                #   then, it will continuely get the letters in the body of the keyword
                #   if it matches one of the KEYWORDS and is closed with a ">", 
                #   then a token will be created for it
                if self.checkChar("/"):
                    if self.ch.isalpha():
                        id = self.consumeChars(LETTERS)
                        if id in KEYWORDS:
                            if self.checkChar(">"):
                                return Token(KEYWORD, "</"+id+">")
                            else:
                                self.nextChar()
                                return Token(INVALID, self.ch)
                        else:
                            self.nextChar()
                            return Token(INVALID, id)
                    else:
                        return Token(INVALID, self.ch)
                
                # if the body of the keyword begins with a letter, then it means it is an opening keyword
                #   then, it will continuely get the letters in the body of the keyword
                #   if it matches one of the KEYWORDS and is closed with a ">", 
                #   then a token will be created for it
                elif self.ch.isalpha():
                    id = self.consumeChars(LETTERS)
                    if id in KEYWORDS:
                        if self.checkChar(">"):
                            return Token(KEYWORD, "<"+id+">")
                        else:
                            self.nextChar()
                            return Token(INVALID, self.ch)
                    else:
                        self.nextChar()
                        return Token(INVALID, id)
                else:
                    return Token(INVALID, self.ch)
            
            # if the current character is a "$", then that means it has reached the end of the statement
            #   so, an EOI typed token is created
            elif self.ch=='$':
                return Token(EOI,"")
            
            # for any other character, and invalid token for it is created
            else:
                self.nextChar()
                return Token(INVALID, self.ch)


    # saves the next character of the statement string to self.ch and increments the index
    def nextChar(self):
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1


    # continualy gets and characters part of (charSet) in the statement string and returns the built string
    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r


    # checks if (c) is equal to the current character
    def checkChar(self, c):
        if (self.ch==c):
            self.nextChar()
            return True
        else: return False



# class representing a Parser Object
# A Parser uses a Lexer Object to go through a series of token from a given input string,
#   and then prints the visual of the statement based on the EBNF grammar
class Parser:
    # a Parser takes in one field, a statement string, and creates its Lexer object and saves the first token
    def __init__(self, s):
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()


    # starts the process of displaying the visual of the statement string
    def run(self):
        self.webpage()


    # prints a WEBPAGE nonterminal
    def webpage(self):
        # a WEBPAGE nonterminal needs to start with <body>, and will print it out
        if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<body>":
            print(self.token.getTokenValue())
            self.token = self.lexer.nextToken()

            # continualy looks for TEXT nonterminals
            while self.token.getTokenValue() != "</body>" or self.token.getTokenType() not in [STRING, KEYWORD]:
                self.text(1)
            
            # after all the TEXT nonterminals, a </body> token is needed and then printed
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</body>":
                print(self.token.getTokenValue())
                self.token = self.lexer.nextToken()

                # the last token required is a EOI token
                if self.token.getTokenType() == EOI:
                    print("")
                    # end of run(); everything was successful
                else:
                    # if an EOI token is not the last token, an error is outputed
                    self.error("Syntax error: expecting EOI; saw:")
            else:
                # if </body> is not found at the end of the WEBPAGE nonterminal, an error is outputed
                self.error("Syntax error: expecting KEYWORD with value </body>; saw:")
        else:
            # if <body> is not found at the start of the WEBPAGE nonterminal, an error is outputed
            self.error("Syntax error: expecting KEYWORD with value <body>; saw:")


    #prints a TEXT nonterminal
    def text(self,indentVal):
        # starts by finding what indentation it should print at
        indentation = "  " * indentVal

        # if the token is a STRING, it will print it out
        if self.token.getTokenType() == STRING:
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
        
        # checks for the start of a <b> branch of the TEXT grammar
        elif self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<b>":
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            self.text(indentVal+1)

            # after a TEXT nonerminal, the grammar expects a closing </b> token
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</b>":
                print(indentation + self.token.getTokenValue())
                self.token = self.lexer.nextToken()
            else:
                # if </b> is not found at the after the TEXT nonterminal, an error is outputed
                self.error("Syntax error: expecting KEYWORD with value </b>; saw:")
        
        # checks for the start of a <i> branch of the TEXT grammar
        elif self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<i>":
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            self.text(indentVal+1)

            # after a TEXT nonterminal, the grammar expects a closing </i> token
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</i>":
                print(indentation + self.token.getTokenValue())
                self.token = self.lexer.nextToken()
            else:
                # if </i> is not found at the after the TEXT nonterminal, an error is outputed
                self.error("Syntax error: expecting KEYWORD with value </i>; saw:")
        
        # checks for the start of a <ul> branch of the TEXT grammar
        elif self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<ul>":
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()

            # continualy creates LISTITEMs until a closing </ul> token is found
            while self.token.getTokenValue() != "</ul>" or self.token.getTokenType() not in [STRING, KEYWORD]:
                self.listItem(indentVal+1)
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</ul>":
                print(indentation + self.token.getTokenValue())
                self.token = self.lexer.nextToken()
            else:
                # if </ul> is not found at the after all the LISTITEM nonterminals, an error is outputed
                self.error("Syntax error: expecting KEYWORD with value </ul>; saw:")
        else:
            # if the token found is not part of the TEXT nonterminal grammar, an error is outputed
            self.error("Syntax error: expecting KEYWORD or STRING; saw:")


    # prints a LISTITEM nontermnial
    def listItem(self,indentVal):
        # starts by finding what indentation it should print at
        indentation = "  " * indentVal

        # a LISTITEM nonterminal requres a <li> token at the beginning, and will print it out, followed by a TEXT nonterminal
        if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<li>":
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            self.text(indentVal+1)

            # after the TEXT nonterminal, the grammar expects a closing </li> token
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</li>":
                print(indentation + self.token.getTokenValue())
                self.token = self.lexer.nextToken()
            else:
                # if </li> is not found at the after the TEXT nonterminal, an error is outputed
                self.error("Syntax error: expecting KEYWORD with value </li>; saw:")
        else:
            # if <li> is not found at the beginning the LISTITEM nonterminal, an error is outputed
            self.error("Syntax error: expecting KEYWORD with value <li>; saw:")


    # prints out the error message along with the current token that caused the error, then immediatly exits
    def error(self,msg):
        print(msg+str(self.token))
        sys.exit(1)



#TESTS FOR LEXER
print("Testing the lexer: test 1")
lex = Lexer ("<body> </body> <b> </b> <i> </i> <ul> </ul> <li> </li>$")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

print("Testing the lexer: test 2")
lex = Lexer ("<body> google <b><i>123<b> yahoo</b></i></b></body>$")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

print("Testing the lexer: test 3")
lex = Lexer ("!<body> apple <underline>bottom</underline> <i>jeans</i> </body>$")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")



# TESTS FOR PARSER
print("Testing the parser: test 1")
parser = Parser ("<body> google <b><i><b> yahoo</b></i></b></body>")
parser.run()

print("Testing the parser: test 2")
parser = Parser ("<body> <b>Fall2022SemesterClasses</b> <ul><li>GEOG2N</li><li>CMPSC461</li><li>CMPSC465</li><li>STAT318</li><li>CMPEN331</li></ul> </body>")
parser.run()

print("Testing the parser: test 3")
parser = Parser ("<body>goodbye<kill>")
parser.run()