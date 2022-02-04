# created by Christopher Kurcz
# PSU ID: cjk6056
# purpose of file:

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
        if (self.type == STRING):
            return self.val
        elif (self.type == KEYWORD):
            return self.val
        elif (self.type == EOI):
            return 
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
lex = Lexer ("/<body>  <underline> underline </underline><i>indent<i/>bodyend</body>$")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

print("Testing the lexer: test 4")
lex = Lexer ("/,>.<<body<i>>123</</body><body/>bruh$")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")