#python2 & python3
class Node:
    def __init__(self,x,y):
        self.token_value = x
        self.code_value =  y
        self.children = []
        self.index=None

    def set_children(self,y):
        try:
            assert isinstance(y,list)
            for i in y:
                self.children.append(i)
        except:
            self.children.append(y)

class Parser:
    nodes_table={}
    tmp_index=0
    edges_table=[]

    def __init__(self):
        self.token=str
        self.tokens_list=['identifier',':=','identifier','+','number']
        self.code_list=['x',':=','x','+','5']
        self.tmp_index = 0
        self.token=self.tokens_list[self.tmp_index]
        self.parse_tree=None
        self.nodes_table=None
        self.edges_table=None

    #Set the token list and the code list
    def set_tokens_list_and_code_list(self,x,y):
        self.code_list = y
        self.tokens_list=x
        self.tmp_index = 0
        #Sets the next token
        self.token = self.tokens_list[self.tmp_index]

    #
    def next_token(self):
        if(self.tmp_index==len(self.tokens_list)-1):
            return False  # we have reachd the end of the list
        self.tmp_index = self.tmp_index + 1
        self.token=self.tokens_list[self.tmp_index]
        return True

    def match(self,x):
        if self.token==x:
            self.next_token()
            return True
        else:
            raise ValueError('Token Mismatch',self.token)

    def stmt_sequence(self):
        t=self.statement()
        p=t
        while self.token=='SEMICOLON':
            q=Node(None,None)
            self.match('SEMICOLON')
            q=self.statement()
            if q == None:
                break
            else:
                if t==None:
                    t=p=q
                else:
                    p.set_children(q)
                    p=q
        return t

    def statement(self):
        if self.token=='IF':
            t=self.if_stmt()
            return t
        elif self.token=='REPEAT':
            t=self.repeat_stmt()
            return t
        elif self.token=='IDENTIFIER':
            t=self.assign_stmt()
            return t
        elif self.token=='READ':
            t=self.read_stmt()
            return t
        elif self.token=='WRITE':
            t=self.write_stmt()
            return t
        else:
            raise ValueError('SyntaxError',self.token)
            ##Error here


    def if_stmt(self):
        t=Node('if',self.code_list[self.tmp_index])
        if self.token=='IF':
            self.match('IF')
            t.set_children(self.exp())
            self.match('THEN')
            t.set_children(self.stmt_sequence())
            if self.token=='ELSE':
                t.set_children(self.stmt_sequence())
            self.match('END')
        return t

    def exp(self):
        t=self.simple_exp()
        if self.token=='LESSTHAN' or self.token=='MORETHAN' or self.token=='EQUAL':
            p=Node(self.token,self.code_list[self.tmp_index])
            p.set_children(t)
            t=p
            self.comparison_op()
            t.set_children(self.simple_exp())
        return t

    def comparison_op(self):
        if self.token=='LESSTHAN':
            self.match('LESSTHAN')
        elif self.token=='MORETHAN':
            self.match('MORETHAN')
        elif self.token=='EQUAL':
            self.match('EQUAL')

    def simple_exp(self):
        t=self.term()
        while self.token=='PLUS' or self.token=='MINUS':
            p=Node('Opk',self.code_list[self.tmp_index])
            p.set_children(t)
            t=p
            self.addop()
            t.set_children(self.term())
        return t

    def addop(self):
        if self.token=='PLUS':
            self.match('PLUS')
        elif self.token=='MINUS':
            self.match('MINUS')

    def term(self):
        t=self.factor()
        while self.token=='MULT' or self.token=='DIV':
            p=Node('Opk',self.code_list[self.tmp_index])
            p.set_children(t)
            t=p
            self.mulop()
            p.set_children(self.factor())
        return t

    def mulop(self):
        if self.token=='MULT':
            self.match('MULT')
        elif self.token=='DIV':
            self.match('DIV')

    def factor(self):
        if self.token=='OPENBRACKET':
            self.match('OPENBRACKET')
            t=self.exp()
            self.match('CLOSEDBRACKET')
        elif self.token=='NUMBER':
            t=Node('ConstK',self.code_list[self.tmp_index])
            self.match('NUMBER')
        elif self.token=='IDENTIFIER':
            t=Node('Idk',self.code_list[self.tmp_index])
            self.match('IDENTIFIER')
        else:
            raise ValueError('SyntaxError',self.token)
            return False
        return t

    def repeat_stmt(self):
        t=Node('repeat',self.code_list[self.tmp_index])
        if self.token=='REPEAT':
            self.match('REPEAT')
            t.set_children(self.stmt_sequence())
            self.match('UNTIL')
            t.set_children(self.exp())
        return t

    def assign_stmt(self):
        t=Node('assign',self.code_list[self.tmp_index])
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        t.set_children(self.exp())
        return t

    def read_stmt(self):
        t=Node('read',self.code_list[self.tmp_index])
        self.match('READ')
        self.match('IDENTIFIER')
        return t

    def write_stmt(self):
        t=Node('write',self.code_list[self.tmp_index])
        self.match('WRITE')
        t.set_children(self.exp())
        return t

    def create_nodes_table(self,args=None):
        if args==None:
            self.parse_tree.index=Parser.tmp_index
            Parser.nodes_table.update({Parser.tmp_index:self.parse_tree.code_value})
            Parser.tmp_index=Parser.tmp_index+1
            if len(self.parse_tree.children) !=0:
                for i in self.parse_tree.children:
                    self.create_nodes_table(i)
        else:
            args.index=Parser.tmp_index
            Parser.nodes_table.update({Parser.tmp_index:args.code_value})
            Parser.tmp_index=Parser.tmp_index+1
            if len(args.children) !=0:
                for i in args.children:
                    self.create_nodes_table(i)

    def create_edges_table(self,args=None):
        if args==None:
            if len(self.parse_tree.children)!=0:
                for i in self.parse_tree.children:
                    Parser.edges_table.append((self.parse_tree.index,i.index))
                for j in self.parse_tree.children:
                    self.create_edges_table(j)
        else:
            if len(args.children)!=0:
                for i in args.children:
                    Parser.edges_table.append((args.index,i.index))
                for j in args.children:
                    self.create_edges_table(j)



    def run(self):
        self.parse_tree=self.stmt_sequence()    #create parse tree
        self.create_nodes_table()               #create nodes_table
        self.create_edges_table()               #create edges_table
        self.edges_table=Parser.edges_table     #save edges_table
        self.nodes_table=Parser.nodes_table     #save nodes_table
        if  self.tmp_index==len(self.tokens_list)-1:
            print('success')
        elif self.tmp_index<len(self.tokens_list):
            raise ValueError('SyntaxError',self.token)

    def clear_tables(self):
        self.nodes_table.clear()
        self.edges_table.clear()
