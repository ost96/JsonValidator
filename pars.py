class Parser:

    ##### Parser header #####
    def __init__(self, scanner):
        self.next_token = scanner.next_token
        self.should_be_colon = scanner.should_be_colon
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error("Unexpected token: %s" % token_type)
        if token_type != 'EOF':
            self.token = self.next_token()

    def check_last_semicolon(self):
        if self.token.type != 'ENDBRACKET':
            if self.token.type == 'NEXT':
                self.error("Colon after last element is unnecessary")
            else:
                self.error("Unexpected token: %s" % self.token.type)

    def error(self, msg):
        raise RuntimeError('Parser error, %s' % msg)

    ##### Parser body #####

    # Starting symbol
    def start(self):
        # start -> program EOF
        self.take_token('STARTBRACKET')
        if self.token.type == '"$id"' or self.token.type == '"$shema"' or self.token.type == 'ID' or self.token.type == 'EOF' or self.token.type == 'IF':
            self.program()
            self.take_token('ENDBRACKET')
            self.take_token('EOF')
            print("json_stm OK")
        else:
            self.error("Epsilon not allowed")

    def program(self):
        # program -> statement program
        if self.token.type == '"$id"' or self.token.type == '"$shema"' or self.token.type == 'ID' or self.token.type == 'IF':
            self.statement()
            self.program()
        # program -> eps
        else:
            pass

    def statement(self):
        # statement -> id_stmt
        if self.token.type == '"$id"':
            self.id_stmt()
        # statement -> shema_stmt
        elif self.token.type == '"$shema"':
            self.shema_stmt()
        # statement -> assign_stmt
        elif self.token.type == 'ID':
            self.assign_stmt()
        # statement -> if_stmt
        elif self.token.type == 'IF':
            self.if_stmt()
        else:
            self.error("Epsilon not allowed")

    # shema_stmt -> $shema_stmt ASSIGN value NEXT END
    def shema_stmt(self):
        if self.token.type == '"$shema"':
            self.take_token('"$shema"')
            self.take_token('ASSIGN')
            self.value()
            if self.should_be_colon():
                self.take_token('NEXT')
            else:
                self.check_last_semicolon()
            print("shema_stmt OK")
        else:
            self.error("Epsilon not allowed")

    # id_stmt -> $id ASSIGN value NEXT END
    def id_stmt(self):
        if self.token.type == '"$id"':
            self.take_token('"$id"')
            self.take_token('ASSIGN')
            self.value()
            if self.should_be_colon():
                self.take_token('NEXT')
            else:
                self.check_last_semicolon()
            print("id_stmt OK")
        else:
            self.error("Epsilon not allowed")

    # assign_stmt -> ID ASSIGN value END
    def assign_stmt(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('ASSIGN')
            self.value()
            self.take_token('END')
            print("assign_stmt OK")
        else:
            self.error("Epsilon not allowed")

    def value(self):
        # value -> NUMBER
        if self.token.type == 'NUMBER':
            self.take_token('NUMBER')
        # value -> ID
        elif self.token.type == 'ID':
            self.take_token('ID')
        else:
            self.error("Epsilon not allowed")

    def if_stmt(self):
        # if_stmt -> IF ID THEN program ENDIF END
        if self.token.type == 'IF':
            self.take_token('IF')
            self.take_token('ID')
            self.take_token('THEN')
            self.program()
            self.take_token('ENDIF')
            self.take_token('END')
            print("if_stmt OK")
        else:
            self.error("Epsilon not allowed")
