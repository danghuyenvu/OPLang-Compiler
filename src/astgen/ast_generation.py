"""
AST Generation module for OPLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.OPLangVisitor import OPLangVisitor
from build.OPLangParser import OPLangParser
from src.utils.nodes import *


class ASTGeneration(OPLangVisitor):
    def __init__(self):
        super().__init__()

    def visitProgram(self, ctx): #this returns a Program object
        return Program(self.visit(ctx.classdecllist()))
    

    def visitClassdecllist(self, ctx): # this returns a list of classDecl objects
        classlist = [self.visit(ctx.classdecl())]
        if (ctx.classdecllist()):
            classlist += self.visit(ctx.classdecllist())
        
        return classlist
    

    def visitClassdecl(self, ctx): # this returns an object of ClassDecl
        superId = ctx.IDENTIFIERS(1).getText() if (ctx.IDENTIFIERS(1)) else None
        return ClassDecl(ctx.IDENTIFIERS(0).getText(), superId, self.visit(ctx.memberblock()))
    

    def visitMemberblock(self, ctx): # this calls visit to memberlist
        return self.visit(ctx.memberlist())


    def visitMemberlist(self, ctx): # this returns a list of ClassMember objects
        memberlist = [self.visit(ctx.classmember())] if ctx.classmember() else []
        if (ctx.membertail()):
            memberlist += self.visit(ctx.membertail())

        return memberlist

    
    def visitMembertail(self, ctx): # this also returns a list of ClassMember objects
        if (ctx.classmember()):
            return [self.visit(ctx.classmember())] + self.visit(ctx.membertail())
        return []
    

    def visitClassmember(self, ctx): 
        return self.visit(ctx.getChild(0))
        if (ctx.attributedecl()):
            return self.visit(ctx.attributedecl())
        elif (ctx.methoddecl()):
            return self.visit(ctx.methoddecl())
        elif (ctx.constructor()):
            return self.visit(ctx.constructor())
        elif (ctx.destructor()):
            return self.visit(ctx.destructor())
        

    def visitAttributedecl(self, ctx): # this returns an object of type AttributeDecl
        if (ctx.referencememdecl()):
            return self.visit(ctx.referencememdecl())
        memspecs = [self.visit(x) for x in ctx.memberspec()]
        is_static = "static" in memspecs
        is_final = "final" in memspecs
        attr_type = self.visit(ctx.vartype())
        attr_list = self.visit(ctx.attrlist())
        if (isinstance(attr_type, ClassType)):
            for x in attr_list:
                if x.init_value == None:
                    x.init_value = NilLiteral()
        return AttributeDecl(is_static, is_final, attr_type, attr_list)
    

    def visitReferencememdecl(self, ctx): # this returns an object of type AttributeDecl but for reference declaration
        memspecs = [self.visit(x) for x in ctx.memberspec()]
        is_static = "static" in memspecs
        is_final = "final" in memspecs
        return AttributeDecl(is_static, is_final, ReferenceType(self.visit(ctx.vartype())), self.visit(ctx.attrlist()))
    

    def visitMemberspec(self, ctx): #return a memspec
        if (ctx.FINAL()):
            return "final"
        elif (ctx.STATIC()):
            return "static"


    def visitAttrlist(self, ctx): # this returns a list of Attribute objects
        return [self.visit(ctx.attrunit())] + (self.visit(ctx.attrtail()) if ctx.attrtail() else None)


    def visitAttrtail(self, ctx): # this returns a list of Attribute objects
        if (ctx.attrunit()):
            return [self.visit(ctx.attrunit())] + self.visit(ctx.attrtail())
        return []
    

    def visitAttrunit(self, ctx): # this returns an Attribute object
        if (ctx.IDENTIFIERS()):
            return Attribute(ctx.IDENTIFIERS().getText())
        else:
            return self.visit(ctx.assign())
        

    def visitAssign(self, ctx): # this returns an Attribute object but with assigning expression
        return Attribute(ctx.IDENTIFIERS().getText(), self.visit(ctx.expression()))


    def visitVartype(self, ctx): # this returns an object of Type
        if (ctx.INT()):
            return PrimitiveType(ctx.INT().getText())
        elif (ctx.FLOAT()):
            return PrimitiveType(ctx.FLOAT().getText())
        elif (ctx.BOOLEAN()):
            return PrimitiveType(ctx.BOOLEAN().getText())
        elif (ctx.STRING()):
            return PrimitiveType(ctx.STRING().getText())
        elif (ctx.IDENTIFIERS()):
            return ClassType(ctx.IDENTIFIERS().getText())
        else:
            return self.visit(ctx.arraytype())
        

    def visitArraytype(self, ctx): # returns ArrayType object
        return ArrayType(self.visit(ctx.elementtype()), int(ctx.INTLIT().getText()))
    

    def visitElementtype(self, ctx): #return PrimitiveType object
        ref = ctx.REFERENCE() != None
        if (ctx.INT()):
            return PrimitiveType(ctx.INT().getText()) if not ref else ReferenceType(PrimitiveType(ctx.INT().getText()))
        elif (ctx.FLOAT()):
            return PrimitiveType(ctx.FLOAT().getText()) if not ref else ReferenceType(PrimitiveType(ctx.FLOAT().getText()))
        elif (ctx.BOOLEAN()):
            return PrimitiveType(ctx.BOOLEAN().getText()) if not ref else ReferenceType(PrimitiveType(ctx.BOOLEAN().getText()))
        elif (ctx.STRING()):
            return PrimitiveType(ctx.STRING().getText()) if not ref else ReferenceType(PrimitiveType(ctx.STRING().getText()))
        else:
            return ClassType(ctx.IDENTIFIERS().getText()) if not ref else ReferenceType(ClassType(ctx.IDENTIFIERS().getText()))
        
        

    def visitConstructor(self, ctx): #returns ConstructorDecl object
        if (ctx.defaultconstructor()):
            return self.visit(ctx.defaultconstructor())
        elif (ctx.copyconstructor()):
            return self.visit(ctx.copyconstructor())
        else:
            return self.visit(ctx.userdefinedconstructor())


    def visitDefaultconstructor(self, ctx): #returns ConstructorDecl object for default constructor
        return ConstructorDecl(ctx.IDENTIFIERS().getText(), [], self.visit(ctx.blockstatement()))


    def visitCopyconstructor(self, ctx): #returns ConstructorDecl object for copy constructor
        return ConstructorDecl(ctx.IDENTIFIERS(0).getText(), [ctx.IDENTIFIERS(1).getText()], self.visit(ctx.blockstatement()))


    def visitUserdefinedconstructor(self, ctx): #returns ConstructorDecl object for user-defined constructor
        return ConstructorDecl(ctx.IDENTIFIERS().getText(), self.visit(ctx.paramlistblock()), self.visit(ctx.blockstatement()))

    
    def visitDestructor(self, ctx): #returns DestructorDecl object
        return DestructorDecl(ctx.IDENTIFIERS().getText(), self.visit(ctx.blockstatement()))


    def visitMethoddecl(self, ctx): #returns MethodDecl object
        return MethodDecl("static" == self.visit(ctx.memberspec()), self.visit(ctx.returntype()), ctx.IDENTIFIERS().getText(), self.visit(ctx.paramlistblock()), self.visit(ctx.blockstatement()))


    def visitReturntype(self, ctx): #returns an object of Type
        ref = ctx.REFERENCE() != None
        if (ctx.INT()):
            return PrimitiveType(ctx.INT().getText()) if not ref else ReferenceType(PrimitiveType(ctx.INT().getText()))
        elif (ctx.FLOAT()):
            return PrimitiveType(ctx.FLOAT().getText()) if not ref else ReferenceType(PrimitiveType(ctx.FLOAT().getText()))
        elif (ctx.STRING()):
            return PrimitiveType(ctx.STRING().getText()) if not ref else ReferenceType(PrimitiveType(ctx.STRING().getText()))
        elif (ctx.BOOLEAN()):
            return PrimitiveType(ctx.BOOLEAN().getText()) if not ref else ReferenceType(PrimitiveType(ctx.BOOLEAN().getText()))
        elif (ctx.IDENTIFIERS()):
            return ClassType(ctx.IDENTIFIERS().getText()) if not ref else ReferenceType(ClassType(ctx.IDENTIFIERS().getText()))
        elif (ctx.VOID()):
            return PrimitiveType(ctx.VOID().getText()) if not ref else ReferenceType(PrimitiveType(ctx.VOID().getText()))
        elif (ctx.arraytype()):
            return self.visit(ctx.arraytype()) if not ref else ReferenceType(self.visit(ctx.arraytype()))
        

    def visitParamlistblock(self, ctx): #returns a list of Parameter objects
        return self.visit(ctx.paramlist())
    

    def visitParamlist(self, ctx): #returns a list of Parameter objects
        if (ctx.parameter()):
            return self.visit(ctx.parameter()) + self.visit(ctx.paramtail())
        return []
    

    def visitParamtail(self, ctx): #returns a list of Parameter objects
        if (ctx.parameter()):
            return self.visit(ctx.parameter()) + self.visit(ctx.paramtail())
        return []
    

    def visitParameter(self, ctx): #returns a list of parameter object
        var_list = self.visit(ctx.idlist())
        param_type = self.visit(ctx.paramtype())
        return [Parameter(param_type, x) for x in var_list]
    

    def visitIdlist(self, ctx): #returns list of variable string
        return [ctx.IDENTIFIERS().getText()] + self.visit(ctx.idtail())


    def visitIdtail(self, ctx):
        if (ctx.IDENTIFIERS()):
            return [ctx.IDENTIFIERS()] + self.visit(ctx.idtail())
        return []
    

    def visitParamtype(self, ctx): #returns a Type object for parameter types
        if (ctx.REFERENCE()):
            return ReferenceType(self.visit(ctx.vartype()))
        
        return self.visit(ctx.vartype())

    
    def visitBlockstatement(self, ctx): #returns a BlockStatement object
        return self.visit(ctx.blockstatementbody())
    

    def visitBlockstatementbody(self, ctx): #returns a BlockStatement object
        return BlockStatement(self.visit(ctx.vardecllist()), self.visit(ctx.statementlist()))
    

    def visitVardecllist(self, ctx): #returns a list of VariableDecl
        if (ctx.vardecl()):
            return [self.visit(ctx.vardecl())] + self.visit(ctx.vardecllist())
        
        return []
    

    def visitVardecl(self, ctx): #returns a VariableDecl object
        if (ctx.referencedecl()):
            return self.visit(ctx.referencedecl())
        var_type = self.visit(ctx.vartype())
        var_list = self.visit(ctx.varlist())
        if (isinstance(var_type, ClassType)):
            for x in var_list:
                if x.init_value == None:
                    x.init_value = NilLiteral() 
        return VariableDecl(self.visit(ctx.varspec()), var_type, var_list)


    def visitVarspec(self, ctx):
        return ctx.FINAL() is not None


    def visitVarlist(self, ctx): #returns list of Variable objects
        return [self.visit(ctx.varunit())] + (self.visit(ctx.vartail()) if ctx.vartail() else None)
    

    def visitVartail(self, ctx): #returns list of Variable objects
        if (ctx.varunit()):
            return [self.visit(ctx.varunit())] + self.visit(ctx.vartail())
        return []
    

    def visitVarunit(self, ctx): #return a Variable object
        if (ctx.assignvar()):
            return self.visit(ctx.assignvar())
        
        return Variable(ctx.IDENTIFIERS().getText())
    

    def visitAssignvar(self, ctx): #returns a Variable object when assigning
        return Variable(ctx.IDENTIFIERS().getText(), self.visit(ctx.expression()))
    

    def visitReferencedecl(self, ctx): #returns a VariableDecl object with references
        return VariableDecl(self.visit(ctx.varspec()), ReferenceType(self.visit(ctx.vartype())), self.visit(ctx.varlist()))
    

    def visitStatementlist(self, ctx): #returns a list of Statement objects
        if (ctx.statement()):
            return [self.visit(ctx.statement())] + self.visit(ctx.statementlist())
        return []
    

    def visitStatement(self, ctx): #returns a Statement object
        if (ctx.expression()):
            return MethodInvocationStatement(self.visit(ctx.expression()))
        if ctx.getChild(0):
            return self.visit(ctx.getChild(0))
        # if (ctx.reassign()):
        #     return self.visit(ctx.reassign())
        # elif (ctx.expression()):
        #     pass
        # elif (ctx.blockstatement):
        #     return self.visit(ctx.blockstatement())
        # elif (ctx.ifstatement()):
        #     return self.visit(ctx.ifstatement())
        # elif (ctx.forstatement()):
        #     return self.visit(ctx.forstatement())
        # elif (ctx.breakstatement()):
        #     return self.visit(ctx.breakstatement())
        # elif (ctx.returnstatement()):
        #     return self.visit(ctx.returnstatement())
        # else:
        #     return self.visit(ctx.continuestatement())
        

    def visitReassign(self, ctx): #return an object of type AssignmentStatement
        return AssignmentStatement(self.visit(ctx.lhs()), self.visit(ctx.expression()))
    

    def visitLhs(self, ctx): #return an object of type LHS
        if (ctx.IDENTIFIERS()):
            return IdLHS(ctx.IDENTIFIERS().getText())
        return PostfixLHS(self.visit(ctx.postfixexp()))
        
    

    def visitPostfixexp(self, ctx): #returns an object of type PostfixExpression
        postlist = self.visit(ctx.postfixlist())
        if (len(postlist) >= 1):
            return PostfixExpression(self.visit(ctx.unaryfactor()), self.visit(ctx.postfixlist())) 
        return self.visit(ctx.unaryfactor())


    def visitPostfixlist(self, ctx): #returns a list of postfixOp
        if (ctx.lhspostfix()):
            return [self.visit(ctx.lhspostfix())] + self.visit(ctx.postfixlist())
        return []
    

    def visitLhspostfix(self, ctx): #returns an object of type PostfixOp
        if (ctx.memaccess()):
            return MemberAccess(self.visit(ctx.memaccess()))
        elif (ctx.methodinvoke()):
            return self.visit(ctx.methodinvoke())
        else:
            return ArrayAccess(self.visit(ctx.indexing()))
        

    def visitMemaccess(self, ctx): #returns a string for member name
        return ctx.IDENTIFIERS().getText()
    

    def visitMethodinvoke(self, ctx): #returns object of MethodCall type
        return MethodCall(ctx.IDENTIFIERS().getText(), self.visit(ctx.expressionlist()))
    

    def visitIndexing(self, ctx): #returns an object of type Expression
        return self.visit(ctx.expression())
    

    def visitExpressionlist(self, ctx): #returns list of expressions for methodcall
        return [self.visit(ctx.expression())] + self.visit(ctx.expressiontail()) if ctx.expression() else []
    

    def visitExpressiontail(self, ctx):
        if (ctx.expression()):
            return [self.visit(ctx.expression())] + self.visit(ctx.expressiontail())
        return []


    def visitIfstatement(self, ctx): #return an object of type IfStatement
        then_stmt = self.visit(ctx.statement()) if ctx.statement() else self.visit(ctx.blockstatement())
        else_stmt = self.visit(ctx.iftail()) if ctx.iftail() else None
        return IfStatement(self.visit(ctx.expression()), then_stmt, else_stmt)
    

    def visitIftail(self, ctx): #returns Statement object when visiting else statement
        if (ctx.blockstatement()):
            return self.visit(ctx.blockstatement())
        elif (ctx.statement()):
            return self.visit(ctx.statement())


    def visitForstatement(self, ctx): #return a ForStatement object
        if (ctx.statement()):
            for_stmt = self.visit(ctx.statement())
        else:
            for_stmt = self.visit(ctx.blockstatement())
        return ForStatement(self.visit(ctx.scalar()), self.visit(ctx.expression(0)), self.visit(ctx.fordirection()), self.visit(ctx.expression(1)), for_stmt)
    

    def visitScalar(self, ctx): #return a string indicating the scalar variable used in for statement
        return ctx.IDENTIFIERS().getText()
    

    def visitFordirection(self, ctx): #return a string indicating the direction in for statement
        if (ctx.TO()):
            return ctx.TO().getText()
        return ctx.DOWNTO().getText()


    def visitBreakstatement(self, ctx): #return a BreakStatement object
        return BreakStatement()


    def visitReturnstatement(self, ctx): #return a ReturnStatement object
        return ReturnStatement(self.visit(ctx.expression()))


    def visitContinuestatement(self, ctx): #return a ContinueStatement object
        return ContinueStatement()


    def visitExpression(self, ctx): #return an object of type Expression
        return self.visit(ctx.orexpression())
    
    def visitOrexpression(self, ctx):
        if (ctx.orexpression()):
            return BinaryOp(self.visit(ctx.orexpression()), ctx.LOGICOR().getText(), self.visit(ctx.andexpression()))
        return self.visit(ctx.andexpression())


    def visitAndexpression(self, ctx):
        if (ctx.andexpression()):
            return BinaryOp(self.visit(ctx.andexpression()), ctx.LOGICAND().getText(), self.visit(ctx.relationalexpression()))
        return self.visit(ctx.relationalexpression())
    

    def visitRelationalexpression(self, ctx):
        if (ctx.getChildCount() > 1):
            return BinaryOp(self.visit(ctx.arithmeticexpression(0)), self.visit(ctx.relationaloperators()), self.visit(ctx.arithmeticexpression(1)))
        return self.visit(ctx.arithmeticexpression(0))
    

    def visitRelationaloperators(self, ctx):
        return ctx.getChild(0).getText()
    

    def visitArithmeticexpression(self, ctx):
        if (ctx.getChildCount() > 1):
            return BinaryOp(self.visit(ctx.arithmeticexpression()), ctx.getChild(1).getText(), self.visit(ctx.terms()))
        return self.visit(ctx.terms())


    def visitTerms(self, ctx):
        if (ctx.terms()):
            return BinaryOp(self.visit(ctx.terms()), self.visit(ctx.termoperators()), self.visit(ctx.factor()))
        return self.visit(ctx.factor())
    

    def visitTermoperators(self, ctx):
        return ctx.getChild(0).getText()


    def visitFactor(self, ctx):
        if (ctx.factor()):
            return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.factor()))
        elif (ctx.postfixexp()):
            return self.visit(ctx.postfixexp())
        return self.visit(ctx.primaryfactor())
        

    def visitUnaryfactor(self, ctx): #returns an object of type Expression for unaryfactor
        if (ctx.IDENTIFIERS()):
            return Identifier(ctx.IDENTIFIERS().getText())
        elif (ctx.THIS()):
            return ThisExpression()
        elif (ctx.objcreate()):
            return self.visit(ctx.objcreate())
        else:
            return ParenthesizedExpression(self.visit(ctx.expression()))
        

    def visitObjcreate(self, ctx):
        return ObjectCreation(ctx.IDENTIFIERS().getText(), self.visit(ctx.expressionlist()))


    def visitPrimaryfactor(self, ctx):
        if (ctx.arraylit()):
            return self.visit(ctx.arraylit())
        elif (ctx.INTLIT()):
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif (ctx.FLOATLIT()):
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif (ctx.STRINGLIT()):
            return StringLiteral(ctx.STRINGLIT().getText())
        else:
            return BoolLiteral(True if ctx.TRUE() is not None else False)


    def visitArraylit(self, ctx):
        return ArrayLiteral(self.visit(ctx.literallist()))


    def visitLiterallist(self, ctx):
        return [self.visit(ctx.anyliteral())] + self.visit(ctx.literallisttail()) if (ctx.literallisttail()) else [self.visit(ctx.anyliteral())]
    

    def visitLiterallisttail(self, ctx):
        return [self.visit(ctx.anyliteral())] + self.visit(ctx.literallisttail()) if (ctx.literallisttail()) else []
    

    def visitAnyliteral(self, ctx):
        if (ctx.boollit()):
            return self.visit(ctx.boollit())
        elif (ctx.INTLIT()):
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif (ctx.FLOATLIT()):
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        else:
            return StringLiteral(ctx.STRINGLIT().getText())
        
    
    def visitBoollit(self, ctx):
        return BoolLiteral(True if ctx.TRUE() else False)