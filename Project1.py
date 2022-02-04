# created by Christopher Kurcz
# PSU ID: cjk6056
# purpose of file:

# imports
import sys

# global constants
STRING, KEYWORD, EOI, INVALID = 1, 2, 3, 4
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
KEYWORDS = ["body","b","i","ul","li"]


class Token:
    def __init__ (self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val

    def __repr__(self):
        if self.type in [STRING, KEYWORD]:
            return self.val
        elif self.type == EOI:
            return ""
        else:
            return "invalid"


class Lexer:
    def __init__ (self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if self.ch.isalpha() or self.ch.isdigit():
                id = self.consumeChars(LETTERS+DIGITS)
                return Token(STRING, id)
            elif self.ch==' ': self.nextChar()
            elif self.ch=='<':
                self.nextChar()
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
            elif self.ch=='$':
                return Token(EOI,"")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)

    def nextChar(self):
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1

    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

    def checkChar(self, c):
        if (self.ch==c):
            self.nextChar()
            return True
        else: return False


class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()

    def run(self):
        self.webpage()

    def webpage(self):
        if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<body>":
            print(self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            while self.token.getTokenValue() != "</body>" or self.token.getTokenType() not in [STRING, KEYWORD]:
                self.text(1)
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</body>":
                print(self.token.getTokenValue())
                self.token = self.lexer.nextToken()
                if self.token.getTokenType() == EOI:
                    print("")
                    # end of run(); everything was successful
                else:
                    self.error("Syntax error: expecting EOI; saw:")
            else:
                self.error("Syntax error: expecting KEYWORD with value </body>; saw:")
        else:
            self.error("Syntax error: expecting KEYWORD with value <body>; saw:")

    def text(self,indentVal):
        indentation = "  " * indentVal
        if self.token.getTokenType() == STRING:
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
        elif self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<b>":
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            self.text(indentVal+1)
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</b>":
                print(indentation + self.token.getTokenValue())
                self.token = self.lexer.nextToken()
            else:
                self.error("Syntax error: expecting KEYWORD with value </b>; saw:")
        elif self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<i>":
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            self.text(indentVal+1)
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</i>":
                print(indentation + self.token.getTokenValue())
                self.token = self.lexer.nextToken()
            else:
                self.error("Syntax error: expecting KEYWORD with value </i>; saw:")
        elif self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<ul>":
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            while self.token.getTokenValue() != "</ul>" or self.token.getTokenType() not in [STRING, KEYWORD]:
                self.listItem(indentVal+1)
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</ul>":
                print(indentation + self.token.getTokenValue())
                self.token = self.lexer.nextToken()
            else:
                self.error("Syntax error: expecting KEYWORD with value </ul>; saw:")
        else:
            self.error("Syntax error: expecting token of type STRING or; saw:")

    def listItem(self,indentVal):
        indentation = "  " * indentVal
        if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "<li>":
            print(indentation + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            self.text(indentVal+1)
            if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "</li>":
                print(indentation + self.token.getTokenValue())
                self.token = self.lexer.nextToken()
            else:
                self.error("Syntax error: expecting KEYWORD with value <li>; saw:")
        else:
            self.error("Syntax error: expecting KEYWORD with value </li>; saw:")

    def matchTokenType(self, tp):
        val = self.token.getTokenValue()
        if (self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else: self.error(tp)
        return val

    def error(self,msg):
        print(msg+str(self.token))
        sys.exit(1)


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

print("Testing the parser: test 1")
parser = Parser ("<body> google <b><i><b> yahoo</b></i></b></body>")
parser.run()

print("Testing the parser: test 2")
parser = Parser ("<body> <b>Fall2022SemesterClasses</b> <ul><li>GEOG2N</li><li>CMPSC461</li><li>CMPSC465</li><li>STAT318</li><li>CMPEN331</li></ul> </body>")
parser.run()

print("Testing the parser: test 3")
parser = Parser ("<body>goodbye<kill>")
parser.run()