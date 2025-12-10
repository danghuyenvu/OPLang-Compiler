"""
Static Semantic Checker for OPLang Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the OPLang object-oriented programming language. It performs type checking,
scope management, inheritance validation, and detects all semantic errors as 
specified in the OPLang language specification.
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ClassDecl, AttributeDecl, Attribute, MethodDecl,
    ConstructorDecl, DestructorDecl, Parameter, VariableDecl, Variable,
    AssignmentStatement, IfStatement, ForStatement, BreakStatement,
    ContinueStatement, ReturnStatement, MethodInvocationStatement,
    BlockStatement, PrimitiveType, ArrayType, ClassType, ReferenceType,
    IdLHS, PostfixLHS, BinaryOp, UnaryOp, PostfixExpression, PostfixOp,
    MethodCall, MemberAccess, ArrayAccess, ObjectCreation, Identifier,
    ThisExpression, ParenthesizedExpression, IntLiteral, FloatLiteral,
    BoolLiteral, StringLiteral, ArrayLiteral, NilLiteral, Type
)
from .static_error import (
    StaticError, Redeclared, UndeclaredIdentifier, UndeclaredClass,
    UndeclaredAttribute, UndeclaredMethod, CannotAssignToConstant,
    TypeMismatchInStatement, TypeMismatchInExpression, TypeMismatchInConstant,
    MustInLoop, IllegalConstantExpression, IllegalArrayLiteral,
    IllegalMemberAccess, NoEntryPoint
)




class StaticChecker(ASTVisitor):
    """
    Stateless static semantic checker for OPLang using visitor pattern.
    
    Checks for all 10 error types specified in OPLang semantic constraints:
    1. Redeclared - Variables, constants, attributes, classes, methods, parameters ----> pass 0
    2. Undeclared - Identifiers, classes, attributes, methods  ---------> pass 0 for iden, classes, pass 1 for attributes, methods
    3. CannotAssignToConstant - Assignment to final variables/attributes --------> pass 1
    4. TypeMismatchInStatement - Type incompatibilities in statements ---------> pass 1
    5. TypeMismatchInExpression - Type incompatibilities in expressions ----------> pass 1
    6. TypeMismatchInConstant - Type incompatibilities in constant declarations -----------> pass 1
    7. MustInLoop - Break/continue outside loop contexts -----------> 
    8. IllegalConstantExpression - Invalid expressions in constant initialization
    9. IllegalArrayLiteral - Inconsistent types in array literals
    10. IllegalMemberAccess - Improper access to static/instance members

    Also checks for valid entry point: static void main() with no parameters.
    """

    def compareType(self, left : "Type", right: "Type", environment: Any = None, coercible: bool = True):
        """
        Method for type compatible check
        """
        if isinstance(left, PrimitiveType) and isinstance(right, PrimitiveType):
            if left.type_name == "float":
                if (coercible):
                    if right.type_name not in ["int", "float"]:
                        return False
                    else:
                        return True
                else:
                    return right.type_name == left.type_name
            else:
                return left.type_name == right.type_name
        elif isinstance(left, ClassType) and isinstance(right, ClassType):
            if (coercible):
                env = environment
                if env.get("program") is None:
                    while env.get("global") is not None:
                        env = env.get("global")

                if env.get("program") is not None:
                    env = env.get("program")
                parentlist = [right.class_name]
                if env.get(right.class_name) is not None:
                    parent = env.get(right.class_name)[1]
                    while parent is not None:
                        parentlist.append(parent)
                        parent = env.get(parent)[1]

                return left.class_name in parentlist
            else:
                return left.class_name == right.class_name
        elif isinstance(left, ArrayType) and isinstance(right, ArrayType):
            if self.compareType(left.element_type, right.element_type, coercible=False, environment=environment):
                return left.size == right.size
            else:
                return False
        elif isinstance(left, ReferenceType) and isinstance(right, ReferenceType):
            return self.compareType(left.referenced_type, right.referenced_type, environment=environment)
        else:
            return False



    def check_program(self, node):
        self.visit(node)
    # _________________________________Program and class declarations_________________________________
    def visit_program(self, node: "Program", o: Any = None):
        #double pass, o:{pass, local:list, entry:boolean}
        Op = 0 #0:get class struct, 1:validate and 
        env = {} #env will be like: "name": (localenv:{}, supername)
        entry = []
        [self.visit(x, (Op, env, entry)) for x in node.class_decls]

        if len(entry) < 1:
            raise NoEntryPoint()
        
        Op = 1
        [self.visit(x, (Op, env)) for x in node.class_decls]


    def visit_class_decl(self, node: "ClassDecl", o: Any = None): 
        #pass 0 get class struct and members (name, parent, classenv)
        if o[0] == 0:
            if o[1].get(node.name):
                raise Redeclared("Class", node.name)
            else:
                super_class = node.superclass
                env = {}            #classenv will be like: {"name": {"type", "is_static", "is_final", "params"}}
                Op = 0
                [self.visit(x, (Op, env, o[1], node.name)) for x in node.members]

                #check for entry
                if env.get("main"):
                    if len(env["main"]["params"]) > 0:
                        pass
                    o[2].append(1)

                #get environment of superclass here since it needs to be declared before use
                if super_class is not None:
                    if o[1].get(super_class):
                        pass
                    else:
                        raise UndeclaredClass(super_class)

                if super_class is not None:
                    superenv = o[1].get(super_class)[0].copy()

                    superenv.update(env)

                    o[1][node.name] = (superenv, super_class)
                else:
                    o[1][node.name] = (env, super_class)

            
            #pass 1 validate attribute init values, check method bodies
        else:
            Op = 1
            [self.visit(x, (Op, o[1], node.name)) for x in node.members]


    # _________________________________Attribute declarations_________________________________
    def visit_attribute_decl(self, node: "AttributeDecl", o: Any = None):
        #Pass 0: 
        #Pass 1: check for type mismatch, init values check
        if o[0] == 0:
            #pass 0: o: (Op, classenv, programenv, classname)
            final = node.is_final
            static = node.is_static
            attrType = node.attr_type
            Op = 0
            [self.visit(x, (Op, o[1], o[3], attrType, final, static)) for x in node.attributes]
        
        else:
            #pass 1: o: (Op, programenv, classname)
            #check for type
            Op = 1
            classenv = o[1].get(o[2])[0]
            attrType = node.attr_type

            self.visit(attrType, o[1])

            [self.visit(x, (Op, o[1], classenv, node, o[2])) for x in node.attributes]


    def visit_attribute(self, node: "Attribute", o: Any = None):
        #pass 0: return attribute name
        #pass 1: validate attribute initvalue
        if o[0] == 0:
            #pass 0: o: (Op, classenv, classname, type, final, static)
            if node.name == o[2] or o[1].get(node.name):
                raise Redeclared("Attribute", node.name)

            o[1][node.name] = {
                "type" : o[3],
                "is_final" : o[4],
                "is_static" : o[5],
            }
        else:
            #pass 1: o: (Op=1, programenv, classenv, declarenode, classname)
            #check for initialization for final and reference type
            attr = o[2].get(node.name)
            if attr["is_final"]:
                if isinstance(node.init_value, NilLiteral) or node.init_value is None:
                    raise IllegalConstantExpression(NilLiteral())

            if not isinstance(node.init_value, NilLiteral) and node.init_value is not None:
                env = {
                    "program" : o[1],
                    "class" : o[2],
                    "name": o[4]
                }
                init_type, eval = self.visit(node.init_value, env)
                attr_type = attr.get("type")
                if not self.compareType(attr_type, init_type, o[1]):
                    if attr["is_final"]:
                        raise TypeMismatchInConstant(o[3])
                    else:
                        raise TypeMismatchInStatement(o[3])
                if attr["is_final"] and not eval:
                    raise IllegalConstantExpression(node.init_value)
            else:
                if attr["is_final"]:
                    raise IllegalConstantExpression(NilLiteral())

    # _________________________________Method declarations_________________________________
    def visit_method_decl(self, node: "MethodDecl", o: Any = None):
        #pass 0: get method signatures: name, params
        #pass 1: validate type mismatch for initvalues, statements
        if o[0] == 0:
            #pass 0: o: (Op, classenv, programenv, classname)
            if node.name == o[3] or o[1].get(node.name):
                raise Redeclared("Method", node.name)
            Op = 0
            paramlist = {} #so paramlist will be like {"name": "type"}
            static = node.is_static
            
            #check legitimate of return type
            retType = node.return_type
            self.visit(node.return_type, (0, o[2]))

            #get environment of method (parameters + var decl inside)
            [self.visit(x, (Op, paramlist)) for x in node.params]

            #get the type
            paramlist = list(paramlist.values())

            o[1][node.name] = {
                "type" : retType,
                "is_static" : static,
                "is_final" : False,
                "params" : paramlist
            }

        else:
            #pass 1: get inside, check param type legit and return type legit
            #o : (Op=1, programenv, classname)
            self.visit(node.return_type, o[1])
            paramlist = {}
            [self.visit(x, (o[0], o[1], o[2], paramlist)) for x in node.params]

            classenv = o[1].get(o[2])[0]
            retType = classenv.get(node.name)["type"]
            env = {
                "class" : classenv.copy(),
                "program" : o[1], 
                "type": retType,
                "name": o[2]
            }

            self.visit(node.body, (env, paramlist))


    def visit_constructor_decl(self, node: "ConstructorDecl", o: Any = None):
        if o[0] == 0:
            #pass 0: o: (Op, classenv, programenv, classname)
            name = node.name

            if name != o[3]:
                raise UndeclaredMethod("Constructor")
            
            Op = 0
            paramlist = {}

            #get paramlist and vardecl inside
            [self.visit(x, (Op, paramlist)) for x in node.params]

            paramlist = list(paramlist.values())

            #Tuple for constructor decl: (name, params:list, methodenv:list) (size 2)
            if o[1].get(name) is None:
                o[1][name] = {
                    "constructor": [paramlist]
                }
            elif o[1][name].get("constructor") is not None:
                constructor = o[1][name].get("constructor")
                for params in constructor:
                        if params is not None:
                            if all(self.compareType(x, y, o) for x, y in zip(params, paramlist)):
                                raise Redeclared("Constructor", name)
                o[1][name]["constructor"].append(paramlist)
            else:
                o[1][name]["constructor"] = [paramlist]
            
        else:
            #pass 1: get inside, check param type legit
            #o : (Op=1, programenv, classname)
            paramlist = {}
            [self.visit(x, (o[0], o[1], o[2], paramlist)) for x in node.params]

            classenv = o[1].get(o[2])[0]
            env = {
                "class" : classenv.copy(),
                "program" : o[1],
                "name": o[2]
            }

            self.visit(node.body, env)

    def visit_destructor_decl(self, node: "DestructorDecl", o: Any = None):
        if o[0] == 0:
            #pass 0: o: (Op, classenv, programenv, classname)
            name = node.name

            if name != o[3]:
                raise UndeclaredMethod("Destructor")

            #Tuple for destructor decl: (name, params:list, methodenv:list) (size 2)
            if o[1].get(name) is None:
                o[1][name] = {
                    "destructor": []
                }
            elif o[1][name].get("destructor") is not None:
                raise Redeclared("Destructor", name)
            else:
                o[1][name]["destructor"] = []

        else:
            #pass 1: get inside
            #o : (Op=1, programenv, classname)
            classenv = o[1].get(o[2])[0]
            env = {
                "class" : classenv.copy(),
                "program" : o[1],
                "name": o[2]
            }

            self.visit(node.body, env)

    def visit_parameter(self, node: "Parameter", o: Any = None):
        #pass 0: get name, type tuple
        #pass 1: dunno bro
        if o[0] == 0:
            #pass 0: o: (Op, paramlist)
            if o[1].get(node.name):
                raise Redeclared("Parameter", node.name)
            
            o[1][node.name] = node.param_type
        else:
            #pass 1: o: (Op=1, programenv, classname)
            #check for type legit
            o[3][node.name] = {
                "type": node.param_type,
                "is_final": False
            }
            self.visit(node.param_type, o[1])


    # _________________________________Type system_________________________________
    def visit_primitive_type(self, node: "PrimitiveType", o: Any = None):
        #o : programenv
        pass

     
    def visit_array_type(self, node: "ArrayType", o: Any = None):
        #pass 0: check for illegal classtype as elementtype
        #o: programenv
        self.visit(node.element_type, o)

     
    def visit_class_type(self, node: "ClassType", o: Any = None):
        #pass 0: check for undeclared class type
        #o : programenv
        if o.get(node.class_name) is None:
            raise UndeclaredClass(node.class_name)
     
    def visit_reference_type(self, node: "ReferenceType", o: Any = None):
        #pass 0: check for reference to illegal class type
        #o : programenv
        self.visit(node.referenced_type, o)

    # _________________________________Statements_________________________________
     
    def visit_block_statement(self, node: "BlockStatement", o: Any = None):
        #o: global environment type: dict {"program", "class"}
        env = None
        if isinstance(o, tuple):
            env = {
                "local": o[1],
                "global": o[0]
            }
        else:
            env = {
                "local" : {},
                "global" : o
            }

        [self.visit(x, env) for x in node.var_decls]
        [self.visit(x, env) for x in node.statements]


     
    def visit_variable_decl(self, node: "VariableDecl", o: Any = None):
        #o : env
        v_type = node.var_type
        programenv = o
        while programenv.get("program") is None:
            programenv = programenv.get("global")
        programenv = programenv.get("program")

        # validate type    
        self.visit(v_type, programenv)

        final = node.is_final
        [self.visit(x, (o, v_type, final, node)) for x in node.variables]

     
    def visit_variable(self, node: "Variable", o: Any = None):
        # o: (env, type, final, declnode)
        env = o[0]
        v_type = o[1]
        is_final = o[2]
        declStatement = o[3]

        if env["local"].get(node.name) is not None:
            raise Redeclared("Variable", node.name)
        else:
            env["local"][node.name] = {
                "type" : v_type,
                "is_final" : is_final
            }
            if node.init_value is not None and not isinstance(node.init_value, NilLiteral):
                init_type, eval = self.visit(node.init_value, env)
                if not self.compareType(v_type, init_type, o[0]):
                    if is_final:
                        raise TypeMismatchInConstant(declStatement)
                    else:
                        raise TypeMismatchInStatement(declStatement)
                else:
                    if is_final and not eval:
                        raise IllegalConstantExpression(node.init_value)
            else:
                if is_final:
                    raise IllegalConstantExpression(declStatement)
            

     
    def visit_assignment_statement(self, node: "AssignmentStatement", o: Any = None):
        env = o
        lhs, is_final = self.visit(node.lhs, env)
        rhs, eval = self.visit(node.rhs, env)
        if is_final:
            raise CannotAssignToConstant(node)
        if not self.compareType(lhs, rhs, env):
            raise TypeMismatchInStatement(node)



     
    def visit_if_statement(self, node: "IfStatement", o: Any = None):
        cond, _ = self.visit(node.condition, o)
        if not isinstance(cond, PrimitiveType):
            raise TypeMismatchInStatement(node)
        if cond.type_name != "boolean":
            raise TypeMismatchInStatement(node)
        
        env = {
            "global": o,
            "local": {}
        }
        self.visit(node.then_stmt, env)

        if node.else_stmt is not None:
            else_env = {
                "global": o,
                "local": {}
            }
            self.visit(node.else_stmt, else_env)



     
    def visit_for_statement(self, node: "ForStatement", o: Any = None):
        env = o

        found = False
        while env.get("local") is not None and not found:
            iden = env["local"].get(node.variable)
            if iden is not None:
                idType = iden["type"]
                if not isinstance(idType, PrimitiveType) or idType.type_name != "int":
                    raise TypeMismatchInStatement(node)
                found = True
            else:
                env = env.get("global")
        if not found:
            iden = env["class"].get(node.variable)
            if iden is not None:
                idType = iden["type"]
                if not isinstance(idType, PrimitiveType) or idType.type_name != "int":
                    raise TypeMismatchInStatement(node)
            else:
                raise UndeclaredIdentifier(node.variable)

        exp1, _ = self.visit(node.start_expr, o)
        if not isinstance(exp1, PrimitiveType) or exp1.type_name != "int":
            raise TypeMismatchInStatement(node)
        exp2, _ = self.visit(node.end_expr, o)
        if not isinstance(exp2, PrimitiveType) or exp2.type_name != "int":
            raise TypeMismatchInStatement(node)
        
        stmt_env = {
            "local": {},
            "global": o,
            "for": True
        }
        self.visit(node.body, stmt_env)

     
    def visit_break_statement(self, node: "BreakStatement", o: Any = None):
        env = o
        while env.get("global") is not None:
            if env.get("for") is not None:
                return
            env = env.get("global")
        
        raise MustInLoop(node)


     
    def visit_continue_statement(self, node: "ContinueStatement", o: Any = None):
        env = o
        while env.get("global") is not None:
            if env.get("for") is not None:
                return
            env = env.get("global")
        
        raise MustInLoop(node)

     
    def visit_return_statement(self, node: "ReturnStatement", o: Any = None):
        env = o
        expType, _ = self.visit(node.value, o)
        while env.get("global") is not None:
            env = env.get("global")
        
        if env.get("type") is None or not self.compareType(env["type"], expType):
            raise TypeMismatchInStatement(node)

     
    def visit_method_invocation_statement(
        self, node: "MethodInvocationStatement", o: Any = None
    ):
        try:
            type, _ = self.visit(node.method_call, o)
            # if not isinstance(type, PrimitiveType):
            #     raise TypeMismatchInStatement(node)
            # elif type.type_name != "void":
            #     raise TypeMismatchInStatement(node)
        except TypeMismatchInExpression:
            raise TypeMismatchInStatement(node)

    # _________________________________Left-hand side (LHS)_________________________________
     
    def visit_id_lhs(self, node: "IdLHS", o: Any = None):
        env = o
        while env.get("local") is not None:
            item = env["local"].get(node.name)
            if item is not None:
                return item.get("type"), item.get("is_final")
            else:
                env = env.get("global")
        
        env = env.get("class")
        if env.get(node.name) is None:
            raise UndeclaredIdentifier(node.name)
        else:
            item = env.get(node.name)
            return item["type"], item["is_final"]


     
    def visit_postfix_lhs(self, node: "PostfixLHS", o: Any = None):
        return self.visit(node.postfix_expr, (o, 1))

    # _________________________________Expressions_________________________________
    # visit expressions returning the type of the result
    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        #op: +,-,*,/,\,%,>,<,>=,<=,!=,==,&&,||,^
        #o : env
        env = o

        left, l_eval = self.visit(node.left, o)
        right, r_eval = self.visit(node.right, o)

        if node.operator in ["\\", "%"]:
            if not (isinstance(left, PrimitiveType) and isinstance(right, PrimitiveType)):
                raise TypeMismatchInExpression(node)
            else:
                if left.type_name != "int" or right.type_name != "int":
                    raise TypeMismatchInExpression(node)
                else:
                    return PrimitiveType("int"), l_eval and r_eval
        elif node.operator in ["+", "-", "*", "/", ">", "<", ">=", "<="]:
            if not (isinstance(left, PrimitiveType) and isinstance(right, PrimitiveType)):
                raise TypeMismatchInExpression(node)
            else:
                if left.type_name not in ["int", "float"] or right.type_name not in ["int", "float"]:
                    raise TypeMismatchInExpression(node)
                else:
                    if node.operator in [">", "<", ">=", "<="]:
                        return PrimitiveType("boolean"), l_eval and r_eval
                    if left.type_name == right.type_name:
                        return PrimitiveType(left.type_name), l_eval and r_eval
                    else:
                        return PrimitiveType("float"), l_eval and r_eval
        elif node.operator in ["==", "!="]:
            if not (isinstance(left, PrimitiveType) and isinstance(right, PrimitiveType)):
                raise TypeMismatchInExpression(node)
            else:
                if left.type_name not in ["int", "boolean"] or right.type_name not in ["int", "boolean"] or right.type_name != left.type_name:
                    raise TypeMismatchInExpression(node)
                else:
                    return PrimitiveType("boolean"), l_eval and r_eval
        elif node.operator in ["&&", "||"]:
            if not (isinstance(left, PrimitiveType) and isinstance(right, PrimitiveType)):
                raise TypeMismatchInExpression(node)
            else:
                if left.type_name != "boolean" or right.type_name != "boolean":
                    raise TypeMismatchInExpression(node)
                else:
                    return PrimitiveType("boolean"), l_eval and r_eval
        elif node.operator == "^":
            if not (isinstance(left, PrimitiveType) and isinstance(right, PrimitiveType)):
                raise TypeMismatchInExpression(node)
            else:
                if left.type_name == "string" and right.type_name == "string":
                    return PrimitiveType("string"), l_eval and r_eval
                else:
                    raise TypeMismatchInExpression(node)

     
    def visit_unary_op(self, node: "UnaryOp", o: Any = None):
        env = o

        operand, eval = self.visit(node.operand, o)

        if node.operator == "!":
            if isinstance(operand, PrimitiveType):
                if operand.type_name == "boolean":
                    return PrimitiveType("boolean"), eval
                else:
                    raise TypeMismatchInExpression(node)
            else:
                raise TypeMismatchInExpression(node)
        else:
            if isinstance(operand, PrimitiveType):
                if operand.type_name in ["int", "float"]:
                    return PrimitiveType(operand.type_name), eval
                else:
                    raise TypeMismatchInExpression(node)
            else:
                raise TypeMismatchInExpression(node)

     
    def visit_postfix_expression(self, node: "PostfixExpression", o: Any = None):
        env = o if not isinstance(o, tuple) else o[0]

        pType = None
        pName = None
        if not isinstance(node.primary, Identifier):
            pType, isFinal = self.visit(node.primary, env)
        else:
            pType, isFinal = self.visit(node.primary, (env, 1))

        if pType is not None:
            if not (isinstance(pType, ClassType) or isinstance(pType, ArrayType) or isinstance(pType, str)):
                raise TypeMismatchInExpression(node)

            primaryType = pType
            try:
                if isinstance(o, tuple):
                    for i, x in enumerate(node.postfix_ops):
                        retType, is_Final = self.visit(x, (primaryType, env))
                        if i == len(node.postfix_ops) - 1:
                            if isinstance(x, MethodCall):
                                return None, None
                            elif isinstance(x, ArrayAccess):
                                return retType, isFinal
                            else:
                                return retType, is_Final
                        
                        isFinal = is_Final
                        primaryType = retType
                        
                else:
                    for x in node.postfix_ops:
                        retType, is_Final = self.visit(x, (primaryType, env))

                        isFinal = isFinal and is_Final
                        primaryType = retType
            except TypeMismatchInExpression:
                raise TypeMismatchInExpression(node)
            except IllegalMemberAccess:
                raise IllegalMemberAccess(node)

            return primaryType, isFinal
        else:
            raise TypeMismatchInExpression(node)


    # _________________________________Postfix ops_________________________________
    #o: (primarytype, env)
    #return the type of the result and is final
    def visit_method_call(self, node: "MethodCall", o: Any = None):
        primary = o[0]
        env = o[1]
        if isinstance(primary, ArrayType):
            raise TypeMismatchInExpression(node)
        
        while env.get("global") is not None:
            env = env.get("global")

        env = env.get("program")
        if isinstance(primary, ClassType):
            #instance access
            if env.get(primary.class_name):
                env, _ = env.get(primary.class_name)
                if node.method_name == primary.class_name:
                    raise IllegalMemberAccess(node)
                ret = env.get(node.method_name)
                if ret is None:
                    raise UndeclaredMethod(node.method_name)
                elif ret.get("type") is None or ret.get("is_static"):
                    raise IllegalMemberAccess(node)
                else:
                    argument = list(map(lambda x: x[0], [self.visit(it, o[1]) for it in node.args]))
                    params = ret.get("params")
                    if all(self.compareType(x,y, o[1]) for x, y in zip(params, argument)):
                        return ret.get("type"), False
                    else:
                        raise TypeMismatchInExpression(node)
            else:
                raise UndeclaredClass(primary.class_name)
        else:
            #static mem access
            if env.get(primary):
                env, _ = env.get(primary)
                if node.method_name == primary:
                    raise IllegalMemberAccess(node)
                ret = env.get(node.method_name)
                if ret is None:
                    raise UndeclaredMethod(node.method_name)
                elif ret.get("type") is None or not ret.get("is_static"):
                    raise IllegalMemberAccess(node)
                else:
                    argument = list(map(lambda x: x[0], [self.visit(it, o[1]) for it in node.args]))
                    params = ret.get("params")
                    if all(self.compareType(x, y) for x, y in zip(params, argument, o[1])):
                        return ret.get("type"), False
                    else:
                        raise TypeMismatchInExpression(node)
            else:
                raise UndeclaredClass(primary)

     
    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        primary = o[0]
        env = o[1]
        if isinstance(primary, ArrayType):
            raise TypeMismatchInExpression(node)
        while env.get("global") is not None:
            env = env.get("global")
        
        env = env.get("program")

        if isinstance(primary, ClassType):
            #instance memaccess
            if env.get(primary.class_name):
                env, _ = env.get(primary.class_name)
                if node.member_name == primary.class_name:
                    raise IllegalMemberAccess(node)
                ret = env.get(node.member_name)
                if ret is None:
                    raise UndeclaredAttribute(node.member_name)
                elif ret.get("is_static"):
                    raise IllegalMemberAccess(node)
                else:
                    return ret.get("type"), ret.get("is_final")
            else:
                raise UndeclaredClass(primary.class_name)
        else:
            #static memaccess
            if env.get(primary):
                env, _ = env.get(primary)
                if node.member_name == primary:
                    raise IllegalMemberAccess(node)
                ret = env.get(node.member_name)
                if ret is None:
                    raise UndeclaredAttribute(node.member_name)
                elif not ret.get("is_static"):
                    raise IllegalMemberAccess(node)
                else:
                    return ret.get("type"), ret.get("is_final")
            else:
                raise UndeclaredClass(primary)


    def visit_array_access(self, node: "ArrayAccess", o: Any = None):
        primary = o[0]
        env = o[1]
        if not isinstance(primary, ArrayType):
            raise TypeMismatchInExpression(node)
        else:
            index, _ = self.visit(node.index, env)
            if not isinstance(index, PrimitiveType):
                raise TypeMismatchInExpression(node)
            if index.type_name != "int":
                raise TypeMismatchInExpression(node)
            return primary.element_type, False

    # _________________________________Back to expressions_________________________________
    def visit_object_creation(self, node: "ObjectCreation", o: Any = None):
        env = o
        while env.get("global") is not None:
            env = env.get("global")
        
        env = env.get("program")
        if env.get(node.class_name) is None:
            raise UndeclaredClass(node.class_name)
        else:
            args = list(map(lambda x: x[0], [self.visit(it, o) for it in node.args]))
            if len(args) == 0:
                #default constructor
                return ClassType(node.class_name), True
            else:
                env, _ = env.get(node.class_name)
                if env.get(node.class_name) is not None:
                    constructor = env[node.class_name].get("constructor")
                    for params in constructor:
                        if params is not None:
                            if all(self.compareType(x, y, o) for x, y in zip(params, args)):
                                return ClassType(node.class_name), True
                raise TypeMismatchInExpression(node)


     
    def visit_identifier(self, node: "Identifier", o: Any = None):
        if isinstance(o, tuple):
            env = o[0]

            found = False
            while env.get("local") is not None:
                iden = env["local"].get(node.name)
                if iden is not None:
                    return iden["type"], iden["is_final"]
                else:
                    env = env.get("global")
            if not found:
                iden = env["class"].get(node.name)
                if iden is not None:
                    return iden["type"], iden["is_final"]
                else:
                    iden = env["program"].get(node.name)
                    if iden is None:
                        raise UndeclaredIdentifier(node.name)
                    else:
                        return node.name, None
        else:
            env = o

            found = False
            while env.get("local") is not None:
                iden = env["local"].get(node.name)
                if iden is not None:
                    return iden["type"], iden["is_final"]
                else:
                    env = env.get("global")
            if not found:
                iden = env["class"].get(node.name)
                if iden is not None:
                    return iden["type"], iden["is_final"]
                else:
                    raise UndeclaredIdentifier(node.name)



     
    def visit_this_expression(self, node: "ThisExpression", o: Any = None):
        env = o
        while env.get("global") is not None:
            env = env.get("global")
        
        class_name = env.get("name")
        return ClassType(class_name), False


     
    def visit_parenthesized_expression(
        self, node: "ParenthesizedExpression", o: Any = None
    ):
        return self.visit(node.expr, o)

    # _________________________________Literals_________________________________
     
    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        return PrimitiveType("int"), True

     
    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        return PrimitiveType("float"), True

     
    def visit_bool_literal(self, node: "BoolLiteral", o: Any = None):
        return PrimitiveType("boolean"), True

     
    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return PrimitiveType("string"), True

     
    def visit_array_literal(self, node: "ArrayLiteral", o: Any = None):
        env = o
        ele = list(map(lambda x: x[0], [self.visit(it, env) for it in node.value]))
        if not all(type(x) == type(ele[0]) for x in ele):
            raise IllegalArrayLiteral(node)
        if not all(self.compareType(x, ele[0], environment=env, coercible=False) for x in ele):
            raise IllegalArrayLiteral(node)
        else:
            return ArrayType(ele[0], len(ele)), True

     
    def visit_nil_literal(self, node: "NilLiteral", o: Any = None):
        pass








#DOODOO
    def visit_static_method_invocation(
        self, node, o: Any = None
    ):
        pass

    def visit_static_member_access(self, node, o: Any = None):
        pass

    def visit_method_invocation(self, node, o: Any = None):
        pass