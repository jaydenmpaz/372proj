import re
from Lexer import Lexer
from Token import Token
class Parser:
    def __init__(self,path,destination):
        f = open(path,'r')
        lines = f.readlines()
        program = []
        for line in lines:
            line.strip('\n')
            program.append(self.run_lexer(line))
        python_program = self.traverse(program)
        f.close()
        f = open(destination,'w')
        f.write(python_program)
        f.close()

    def run_lexer(self,text):
        lexer = Lexer(text)
        token = lexer.get_next_token()
        list_of_tokens = [token]
        while token.type != 'EOF':
            token = lexer.get_next_token()
            list_of_tokens.append(token)
        return list_of_tokens
    
    def traverse(self,program):
        final = ''
        tabs = 0
        statements = []
        for line in program:
            continuous = []
            for token in line:
                if token.value==';' or token.value=='{' or token.value=='}':
                    if token.value=='}':
                        tabs-=1
                    statements.append((continuous,tabs))
                    if token.value=='{':
                        tabs+=1
                    continuous = []
                else:
                    continuous.append(token)
            if continuous!=[] and continuous[0].type!='EOF':
                if continuous[-1].type=='EOF':
                    continuous.pop(-1)
                statements.append((continuous,tabs))
        x=0
        conversion = ''
        increment = []
        tabs = []
        while x<len(statements):
            stmtType = None
            stmt = statements[x]
            print(stmt)
            for tkn in stmt[0]:
                if tkn.type=='IF' or tkn.type=='ELSE' or tkn.type=='FUNC' or tkn.type=='FOR' or tkn.type=='ASSIGN' or tkn.type=='PRINT':
                    stmtType= tkn.type
                    break
                elif tkn.type=='INT_TYPE' or tkn.type=='BOOL_TYPE' or tkn.type=='STRING_TYPE':
                    stmtType='DECL'
                elif tkn.type=='EOF' and stmtType==None:
                    stmtType='EXPR'
            
            if tabs!=[]:
                if stmt[1]==tabs[-1]:
                    conversion+=increment[-1]
                    tabs.pop(-1)
                    increment.pop(-1)

            if stmtType=='IF':
                conversion+=self.ifStmt(stmt)
            elif stmtType=='ELSE':
                conversion+=('\t'*stmt[1]+'else:\n')
            elif stmtType=='DECL':
                conversion+=self.declStmt(stmt)
            elif stmtType=='FUNC':
                conversion+=self.funcStmt(stmt)
            elif stmtType=='FOR':
                loop,incre = self.forStmt(stmt,statements[x+1],statements[x+2])
                conversion+=loop
                increment.append(incre)
                tabs.append(stmt[1])
                x+=2
            elif stmtType=='PRINT':
                conversion+=self.printStmt(stmt)
            elif stmtType=='ASSIGN':
                conversion+=self.assignStmt(stmt)
            else:
                conversion+=self.expr(stmt)
            x+=1
        conversion+='\n'
        return conversion

    def funcStmt(self,stmt):
        conversion='\t'*stmt[1]+"def "
        for tkn in stmt[0][2:]:
            if tkn.type!='INT_TYPE' and tkn.type!='STRING_TYPE' and tkn.type!='BOOL_TYPE':
                conversion+=tkn.value
        conversion+=':\n'
        return conversion


    def declStmt(self, stmt):
        conversion='\t'*stmt[1]
        for tkn in stmt[0]:
            if tkn.type=='IDENTIFIER':
                conversion+=(tkn.value+' = None\n')
                break
        return conversion

    def ifStmt(self,stmt):
        conversion = '\t'*stmt[1] + 'if'
        for tkn in stmt[0][2:len(stmt[0])-1]:
            if tkn.type=='STRING_LITERAL':
                conversion+= ' "'+tkn.value+'"'
            elif tkn.type=='AND':
                conversion += ' and'
            elif tkn.type=='OR':
                conversion += ' or'
            elif tkn.type=='NOT':
                conversion += ' not'
            else:
                conversion+=(' '+str(tkn.value))
        conversion+=':\n'
        return conversion
    
    def forStmt(self, stmt,condition,incr):
        conversion = '\t'*stmt[1]
        x=0
        while(stmt[0][x].type!='IDENTIFIER'):
            x+=1
        conversion = conversion + str(stmt[0][x].value) + ' ' +str(stmt[0][x+1].value) + ' ' +str(stmt[0][x+2].value) + '\n' +'\t'*stmt[1] + 'while'
        for tkn in condition[0]:
            if tkn.type=='STRING_LITERAL':
                conversion += '"'+tkn.value+'"'
            elif tkn.type=='AND':
                conversion += ' and'
            elif tkn.type=='OR':
                conversion += ' or'
            elif tkn.type=='NOT':
                conversion += ' not'
            else:
                conversion+=(' '+str(tkn.value))
        conversion+=':\n'
        increment = '\t'*(stmt[1]+1)
        for tkn in incr[0]:
            if tkn.value!=')' and tkn.type!='EOF':
                increment = increment+str(tkn.value)
        increment+='\n'
        return conversion,increment

    def printStmt(self,stmt):
        conversion = '\t'*stmt[1]+'print'
        for tkn in stmt[0]:
            if tkn.type!='PRINT':
                if tkn.type=='STRING_LITERAL':
                    conversion += '"'+tkn.value+'"'
                elif tkn.type=='AND':
                    conversion += ' and'
                elif tkn.type=='OR':
                    conversion += ' or'
                elif tkn.type=='NOT':
                    conversion += ' not'
                else:
                    conversion+=(' '+str(tkn.value))
        return conversion+'\n'
    
    def assignStmt(self,stmt):
        x=0
        conversion = '\t'*stmt[1]
        while stmt[0][x].type!='IDENTIFIER':
            x+=1
        conversion+=stmt[0][x].value
        x+=1
        for tkn in stmt[0][x:]:
            if tkn.type=='STRING_LITERAL':
                conversion += '"'+tkn.value+'"'
            elif tkn.type=='AND':
                conversion += ' and'
            elif tkn.type=='OR':
                conversion += ' or'
            elif tkn.type=='NOT':
                conversion += ' not'
            else:
                conversion+=(' '+str(stmt[0][x].value))
            x+=1
        return conversion+'\n'
    
    def expr(self,stmt):
        if stmt[0]==[]:
            return ''
        conversion = '\t'*stmt[1]
        first = False
        for tkn in stmt[0]:
            if tkn.type=='STRING_LITERAL':
                conversion += '"'+tkn.value+'"'
            elif tkn.type=='AND':
                conversion += ' and'
            elif tkn.type=='OR':
                conversion += ' or'
            elif tkn.type=='NOT':
                conversion += ' not'
            elif not first:
                conversion += str(tkn.value)
                first = True
            else:
                conversion+=(' '+str(tkn.value))
        return conversion+'\n'

source = input('Name of file to parse: ')
dest = input('Name of file to put converted file in: ')
Parser(source,dest)