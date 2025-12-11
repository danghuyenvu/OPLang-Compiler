grammar OPLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

//                                           Comments
LINECOMMENT: '#'~[\n\r]* -> skip;
BLOCKCOMMENT: '/*'(~[*]|'*'~[/])*'*/' -> skip;
UNCLOSEDBLOCKCOMMENT: '/*'(~[*]|'*'~[/])* ->skip;

//                                           Keywords
BOOLEAN: 'boolean';
BREAK: 'break';
CLASS: 'class';
CONTINUE: 'continue';
DO: 'do';
ELSE: 'else';
EXTENDS: 'extends';
FLOAT: 'float';
IF: 'if';
INT: 'int';
NEW: 'new';
STRING: 'string';
THEN: 'then';
FOR: 'for';
RETURN: 'return';
TRUE: 'true';
FALSE: 'false';
VOID: 'void';
NIL: 'nil';
THIS: 'this';
FINAL: 'final';
STATIC: 'static';
TO: 'to';
DOWNTO: 'downto';





//                                           Operators
ADDOP: '+';
SUBOP: '-';
MULOP: '*';
FLOATDIVOP: '/';
INTDIVOP: '\\';            //all operand in integer required or typemissmatch
MODULUS: '%';             //all operand in integer required or typemissmatch
NOTEQ: '!=';
EQ: '==';
LESSTHAN: '<';
GREATERTHAN: '>';
LESSEQ: '<=';
GREATEREQ: '>=';
LOGICOR: '||';
LOGICAND: '&&';
LOGICNOT: '!';
CONCAT: '^';
ASSIGNING: ':=';

//                                           Separators
LSQUAREBRACKET: '[';
RSQUAREBRACKET: ']';
LPAREN: '{';
RPAREN: '}';
LBRACKET: '(';
RBRACKET: ')';
SEMICOLON: ';';
COLON: ':';
DOT: '.';
COMMA: ',';

//                                           Special Characters
REFERENCE: '&';
DESTRUCT: '~';


//                                           Identifiers
IDENTIFIERS: [a-zA-Z'_'][a-zA-Z0-9'_']*;

//                                           Literals
fragment Digit: [0-9];
INTLIT: Digit+;

FLOATLIT: Digit+ '.' Digit*([eE][+-]?Digit+)? | Digit+[eE][+-]?Digit+;

fragment ESC: '\\'[bfrnt"\\];
fragment ASCII: [\u0000-\u0009\u000B-\u0021\u0023-\u005B\u005D-\u007F]; //excluding ["] and [\]

ILLEGAL_ESCAPE: '"'(ESC|ASCII)*'\\'~[bfrnt"\\]{
    raise IllegalEscape(self.text[1:])
};

STRINGLIT: '"'(ESC|ASCII)*'"'{self.text = self.text[1:-1]};


WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs 

UNCLOSE_STRING:'"'(ESC|ASCII)*{
    self.text = self.text[1:]
    raise UncloseString(self.text)
};

ERROR_CHAR: .;



//                                           Context-free Grammar
program: classdecllist EOF; // write for program rule here using vardecl and funcdecl

classdecllist
    : classdecl classdecllist 
    | classdecl
    ;

classdecl
    : CLASS IDENTIFIERS memberblock
    | CLASS IDENTIFIERS EXTENDS IDENTIFIERS memberblock
    ;

memberblock
    : LPAREN memberlist RPAREN
    ;

memberlist
    : classmember membertail
    |
    ;

membertail
    : classmember membertail
    | 
    ;

classmember
    : attributedecl
    | methoddecl
    | constructor
    | destructor
    ;

attributedecl
    : memberspec memberspec vartype attrlist SEMICOLON
    | referencememdecl
    ;

memberspec
    : STATIC
    | FINAL
    |
    ;

vartype
    : BOOLEAN
    | FLOAT
    | INT
    | STRING
    | IDENTIFIERS //for class type
    | arraytype
    ;

arraytype
    : elementtype LSQUAREBRACKET INTLIT RSQUAREBRACKET
    ;

elementtype
    : INT REFERENCE?
    | BOOLEAN REFERENCE?
    | FLOAT REFERENCE?
    | STRING REFERENCE?
    | IDENTIFIERS REFERENCE?
    ;

attrlist
    : attrunit attrtail
    | attrunit
    ;

attrtail
    : COMMA attrunit attrtail
    | 
    ;

attrunit
    : assign
    | IDENTIFIERS 
    ;

assign
    : IDENTIFIERS ASSIGNING expression
    ;

referencememdecl
    : memberspec memberspec vartype REFERENCE attrlist ASSIGNING expression SEMICOLON
    ;

methoddecl
    : memberspec returntype IDENTIFIERS paramlistblock blockstatement
    ;

returntype
    : INT REFERENCE 
    | FLOAT REFERENCE
    | BOOLEAN REFERENCE
    | STRING REFERENCE
    | IDENTIFIERS REFERENCE
    | INT
    | FLOAT
    | BOOLEAN
    | STRING
    | VOID
    | IDENTIFIERS //for class type
    | arraytype
    ;

paramlistblock
    : LBRACKET paramlist RBRACKET
    ;

paramlist
    : parameter paramtail
    | 
    ;

paramtail
    : SEMICOLON parameter paramtail
    | 
    ;

parameter
    : paramtype idlist
    ;

idlist
    : IDENTIFIERS idtail
    ;

idtail
    : COMMA IDENTIFIERS idtail
    |
    ;

paramtype
    : vartype REFERENCE // for reference type
    | vartype
    ;

constructor
    : defaultconstructor
    | copyconstructor
    | userdefinedconstructor
    ;

defaultconstructor
    : IDENTIFIERS LBRACKET RBRACKET blockstatement
    ;

copyconstructor
    : IDENTIFIERS LBRACKET IDENTIFIERS RBRACKET blockstatement
    ;

userdefinedconstructor
    : IDENTIFIERS paramlistblock blockstatement
    ;

destructor
    : DESTRUCT IDENTIFIERS LBRACKET RBRACKET blockstatement
    ;

expression : orexpression;

orexpression
    : orexpression LOGICOR andexpression
    | andexpression
    ;

andexpression
    : andexpression LOGICAND relationalexpression
    | relationalexpression
    ;

relationalexpression
    : arithmeticexpression relationaloperators arithmeticexpression
    | arithmeticexpression
    ;

relationaloperators
    : EQ
    | NOTEQ
    | GREATERTHAN
    | LESSTHAN
    | GREATEREQ
    | LESSEQ
    ;

arithmeticexpression
    : arithmeticexpression ADDOP terms
    | arithmeticexpression SUBOP terms
    | terms
    ;

terms
    : terms termoperators factor
    | factor
    ;

termoperators
    : MULOP
    | FLOATDIVOP
    | INTDIVOP
    | MODULUS
    | CONCAT
    ;

factor
    : ADDOP factor
    | SUBOP factor
    | LOGICNOT factor
    | postfixexp
    | primaryfactor
    ;

postfixexp
    : unaryfactor postfixlist
    ;

unaryfactor
    : objcreate
    | LBRACKET expression RBRACKET
    | IDENTIFIERS
    | THIS
    ;

postfixlist
    : lhspostfix postfixlist
    | 
    ;

primaryfactor
    : INTLIT
    | FLOATLIT
    | STRINGLIT
    | arraylit
    | TRUE
    | FALSE
    ;

indexing
    : LSQUAREBRACKET expression RSQUAREBRACKET
    ;

memaccess
    : DOT IDENTIFIERS
    ;

expressionlist
    : expression expressiontail 
    |
    ;

expressiontail
    : COMMA expression expressiontail 
    | 
    ;

methodinvoke
    : DOT IDENTIFIERS LBRACKET expressionlist RBRACKET
    ;

objcreate
    : NEW IDENTIFIERS LBRACKET expressionlist RBRACKET
    ;

blockstatement
    : LPAREN blockstatementbody RPAREN
    ;

blockstatementbody
    : vardecllist statementlist
    ;

vardecllist
    : vardecl vardecllist
    | 
    ;

vardecl
    : varspec vartype varlist SEMICOLON
    | referencedecl
    ;

referencedecl
    : varspec vartype REFERENCE varlist ASSIGNING expression SEMICOLON
    ;

varspec
    : FINAL
    | 
    ;

varlist
    : varunit vartail
    | varunit
    ;

vartail
    : COMMA varunit vartail
    | 
    ;

varunit
    : assignvar
    | IDENTIFIERS 
    ;

assignvar
    : IDENTIFIERS ASSIGNING expression
    ;

statementlist
    : statement statementlist
    | 
    ;

reassign
    : lhs ASSIGNING expression
    ;

lhspostfix
    : memaccess
    | methodinvoke
    | indexing
    ;

lhs
    : IDENTIFIERS
    | postfixexp
    ;

statement
    : reassign SEMICOLON
    | expression SEMICOLON
    | blockstatement
    | ifstatement
    | forstatement
    | breakstatement
    | continuestatement
    | returnstatement
    ;

ifstatement
    : IF expression THEN blockstatement iftail
    | IF expression THEN statement iftail
    ;

iftail
    : ELSE blockstatement
    | ELSE statement
    | 
    ;

forstatement
    : FOR scalar ASSIGNING expression fordirection expression DO blockstatement
    | FOR scalar ASSIGNING expression fordirection expression DO statement
    ;

scalar
    : IDENTIFIERS
    ;

fordirection
    : TO
    | DOWNTO
    ;

breakstatement
    : BREAK SEMICOLON
    ;

continuestatement
    : CONTINUE SEMICOLON
    ;

returnstatement
    : RETURN expression SEMICOLON
    ;

arraylit                                       //Array literal
    : LPAREN literallist RPAREN
    ;

literallist
    : expression literallisttail
    | expression
    ;

literallisttail
    : COMMA expression literallisttail
    |
    ;