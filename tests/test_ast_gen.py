from tests.utils import ASTGenerator


def test_001():
    """Test basic class declaration AST generation"""
    source = """class TestClass {
        int x;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)])])])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected


def test_002():
    """Test class with method declaration AST generation"""
    source = """class TestClass {
        void main() {
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003():
    """Test class with constructor AST generation"""
    source = """class TestClass {
        int x;
        TestClass(int x) {
            this.x := x;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)]), ConstructorDecl(TestClass([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004():
    """Test class with inheritance AST generation"""
    source = """class Child extends Parent {
        int y;
    }"""
    expected = "Program([ClassDecl(Child, extends Parent, [AttributeDecl(PrimitiveType(int), [Attribute(y)])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005():
    """Test static and final attributes AST generation"""
    source = """class TestClass {
        static final int MAX_SIZE := 100;
        final float PI := 3.14;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(static final PrimitiveType(int), [Attribute(MAX_SIZE = IntLiteral(100))]), AttributeDecl(final PrimitiveType(float), [Attribute(PI = FloatLiteral(3.14))])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006():
    """Test if-else statement AST generation"""
    source = """class TestClass {
        void main() {
            if x > 0 then {
                return x;
            } else {
                return 0;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[ReturnStatement(return Identifier(x))]), else BlockStatement(stmts=[ReturnStatement(return IntLiteral(0))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007():
    """Test for loop AST generation"""
    source = """class TestClass {
        void main() {
            int sum := 0;
            for i := 1 to 10 do {
                sum := sum + i;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(sum = IntLiteral(0))])], stmts=[ForStatement(for i := IntLiteral(1) to IntLiteral(10) do BlockStatement(stmts=[AssignmentStatement(IdLHS(sum) := BinaryOp(Identifier(sum), +, Identifier(i)))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_008():
    """Test array operations AST generation"""
    source = """class TestClass {
        void main() {
            int[5] arr;
            arr[0] := 42;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ArrayType(PrimitiveType(int)[5]), [Variable(arr)])], stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[IntLiteral(0)])) := IntLiteral(42))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009():
    """Test object creation and method call AST generation"""
    source = """class TestClass {
        void main() {
            Rectangle r := new Rectangle(5.0, 3.0);
            float area := r.getArea();
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Rectangle), [Variable(r = ObjectCreation(new Rectangle(FloatLiteral(5.0), FloatLiteral(3.0))))]), VariableDecl(PrimitiveType(float), [Variable(area = PostfixExpression(Identifier(r).getArea()))])], stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_010():
    """Test reference type AST generation"""
    source = """class TestClass {
        void swap(int & a; int & b) {
            int temp := a;
            a := b;
            b := temp;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) swap([Parameter(ReferenceType(PrimitiveType(int) &) a), Parameter(ReferenceType(PrimitiveType(int) &) b)]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(temp = Identifier(a))])], stmts=[AssignmentStatement(IdLHS(a) := Identifier(b)), AssignmentStatement(IdLHS(b) := Identifier(temp))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_011():
    """Test destructor AST generation"""
    source = """class TestClass {
        ~TestClass() {
            int x := 0;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [DestructorDecl(~TestClass(), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(x = IntLiteral(0))])], stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected



def test_012():
    """Test basic class declaration AST generation"""
    source = """class TestClass {
        int& x := y;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(ReferenceType(PrimitiveType(int) &), [Attribute(x)])])])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected

def test_013():
    """Test basic class declaration AST generation"""
    source = """class TestClass {
        void main(){
            x := 5 + 6;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(IntLiteral(5), +, IntLiteral(6)))]))])])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected

def test_014():
    """Test if-else statement AST generation"""
    source = """class TestClass {
        void main() {
            if x > 0 then {
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_015():
	""""""
	source = """class Calculator {
        int add(int a; int b) {
            return a + b;
        }
        float add(float a; float b) {
            return a + b;
        }
    }"""
	expected = "Program([ClassDecl(Calculator, [MethodDecl(PrimitiveType(int) add([Parameter(PrimitiveType(int) a), Parameter(PrimitiveType(int) b)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(Identifier(a), +, Identifier(b)))])), MethodDecl(PrimitiveType(float) add([Parameter(PrimitiveType(float) a), Parameter(PrimitiveType(float) b)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(Identifier(a), +, Identifier(b)))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
     
def test_016():
	""""""
	source = """class Point {
        int x;
        int y;
        Point() {
            x := 0;
            y := 0;
        }
        Point(int x; int y) {
            this.x := x;
            this.y := y;
        }
    }"""
	expected = "Program([ClassDecl(Point, [AttributeDecl(PrimitiveType(int), [Attribute(x)]), AttributeDecl(PrimitiveType(int), [Attribute(y)]), ConstructorDecl(Point([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(0)), AssignmentStatement(IdLHS(y) := IntLiteral(0))])), ConstructorDecl(Point([Parameter(PrimitiveType(int) x), Parameter(PrimitiveType(int) y)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x)), AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).y)) := Identifier(y))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
     
def test_017():
	""""""
	source = """class TestClass {
        void main() {
            Engine e := new Engine().init().start();
        }
    }"""
	expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Engine), [Variable(e = PostfixExpression(ObjectCreation(new Engine()).init().start()))])], stmts=[]))])])"
	assert str(ASTGenerator(source).generate()) == expected
     
def test_018():
	""""""
	source = """class A {
        int a;
    }
    class B extends A {
        int b;
    }
    class C extends B {
        int c;
    }"""
	expected = "Program([ClassDecl(A, [AttributeDecl(PrimitiveType(int), [Attribute(a)])]), ClassDecl(B, extends A, [AttributeDecl(PrimitiveType(int), [Attribute(b)])]), ClassDecl(C, extends B, [AttributeDecl(PrimitiveType(int), [Attribute(c)])])])"
	assert str(ASTGenerator(source).generate()) == expected
     
def test_019():
	""""""
	source = """class TestClass {
        void main() {
            for i := 0 to 5 do {
                if i % 2 == 0 then {
                    io.print(i);
                } else {
                    io.print("odd");
                }
            }
        }
    }"""
	expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(5) do BlockStatement(stmts=[IfStatement(if BinaryOp(BinaryOp(Identifier(i), %, IntLiteral(2)), ==, IntLiteral(0)) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(i))))]), else BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('odd'))))]))]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
     
def test_020():
	""""""
	source = """class Data {
        int id;
        float value;
        string name;
    }"""
	expected = "Program([ClassDecl(Data, [AttributeDecl(PrimitiveType(int), [Attribute(id)]), AttributeDecl(PrimitiveType(float), [Attribute(value)]), AttributeDecl(PrimitiveType(string), [Attribute(name)])])])"
	assert str(ASTGenerator(source).generate()) == expected
     
def test_021():
	""""""
	source = """class Math {
        int square(int x) {
            return x * x;
        }
    }"""
	expected = "Program([ClassDecl(Math, [MethodDecl(PrimitiveType(int) square([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(Identifier(x), *, Identifier(x)))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
     
def test_022():
	""""""
	source = """class Config {
        int timeout;
        Config() {
            timeout := 30;
        }
    }"""
	expected = "Program([ClassDecl(Config, [AttributeDecl(PrimitiveType(int), [Attribute(timeout)]), ConstructorDecl(Config([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(timeout) := IntLiteral(30))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
     
def test_023():
	""""""
	source = """class Greeter {
        void greet() {
            this.sayHello();
        }
        void sayHello() {
            io.print("Hello");
        }
    }"""
	expected = "Program([ClassDecl(Greeter, [MethodDecl(PrimitiveType(void) greet([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(ThisExpression(this).sayHello()))])), MethodDecl(PrimitiveType(void) sayHello([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('Hello'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected

def test_024():
	""""""
	source = """class Test {
        void main() {
            {
                int x := 1;
                {
                    int y := 2;
                }
            }
        }
    }"""
	expected = "Program([ClassDecl(Test, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(x = IntLiteral(1))])], stmts=[BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(y = IntLiteral(2))])], stmts=[])])]))])])"
	assert str(ASTGenerator(source).generate()) == expected
      
def test_025():
	""""""
	source = """class EmptyMethod {
        void doNothing() {
        }
    }"""
	expected = "Program([ClassDecl(EmptyMethod, [MethodDecl(PrimitiveType(void) doNothing([]), BlockStatement(stmts=[]))])])"
	assert str(ASTGenerator(source).generate()) == expected
      
def test_026():
	""""""
	source = """class Utils {
        static void log(string msg) {
            io.print(msg);
        }
    }"""
	expected = "Program([ClassDecl(Utils, [MethodDecl(static PrimitiveType(void) log([Parameter(PrimitiveType(string) msg)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(msg))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
      
def test_027():
	""""""
	source = """class Constants {
        final int MAX := 100;
    }"""
	expected = "Program([ClassDecl(Constants, [AttributeDecl(final PrimitiveType(int), [Attribute(MAX = IntLiteral(100))])])])"
	assert str(ASTGenerator(source).generate()) == expected
      
def test_028():
	""""""
	source = """class Factory {
        Product create() {
            return new Product();
        }
    }"""
	expected = "Program([ClassDecl(Factory, [MethodDecl(ClassType(Product) create([]), BlockStatement(stmts=[ReturnStatement(return ObjectCreation(new Product()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
      
def test_029():
	""""""
	source = """class TestClass {
        void main() {
            if x > 0 then {
                if y > 0 then {
                    io.print("positive quadrant");
                }
            }
        }
    }"""
	expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(y), >, IntLiteral(0)) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('positive quadrant'))))]))]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_030():
	""""""
	source = """class Chain {
        int run() {
            return this.step1().step2().finish();
        }
    }"""
	expected = "Program([ClassDecl(Chain, [MethodDecl(PrimitiveType(int) run([]), BlockStatement(stmts=[ReturnStatement(return PostfixExpression(ThisExpression(this).step1().step2().finish()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_031():
	""""""
	source = """class Test {
        void main() {
            int a := 1;
            float b := 2.5;
            a := a + b;
            io.print(a);
        }
    }"""
	expected = "Program([ClassDecl(Test, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(a = IntLiteral(1))]), VariableDecl(PrimitiveType(float), [Variable(b = FloatLiteral(2.5))])], stmts=[AssignmentStatement(IdLHS(a) := BinaryOp(Identifier(a), +, Identifier(b))), MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(a))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_032():
	""""""
	source = """class Math {
        void calc() {
            x := (a + b) * (c - d) / e;
        }
    }"""
	expected = "Program([ClassDecl(Math, [MethodDecl(PrimitiveType(void) calc([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(BinaryOp(ParenthesizedExpression((BinaryOp(Identifier(a), +, Identifier(b)))), *, ParenthesizedExpression((BinaryOp(Identifier(c), -, Identifier(d))))), /, Identifier(e)))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_033():
	""""""
	source = """class Test {
        void main() {
            a.b.c := 10;
        }
    }"""
	expected = "Program([ClassDecl(Test, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(a).b.c)) := IntLiteral(10))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_034():
	""""""
	source = """class Builder {
        Builder make() {
            return new Builder();
        }
    }"""
	expected = "Program([ClassDecl(Builder, [MethodDecl(ClassType(Builder) make([]), BlockStatement(stmts=[ReturnStatement(return ObjectCreation(new Builder()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_035():
	""""""
	source = """class Nested {
        void main() {
            for i := 0 to 3 do {
                for j := 0 to 2 do {
                    if i == j then {
                        io.print(i);
                    }
                }
            }
        }
    }"""
	expected = "Program([ClassDecl(Nested, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(3) do BlockStatement(stmts=[ForStatement(for j := IntLiteral(0) to IntLiteral(2) do BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(i), ==, Identifier(j)) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(i))))]))]))]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_036():
	""""""
	source = """class Arr {
        void process(int[10] nums) {
            io.print(nums[0]);
        }
    }"""
	expected = "Program([ClassDecl(Arr, [MethodDecl(PrimitiveType(void) process([Parameter(ArrayType(PrimitiveType(int)[10]) nums)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(PostfixExpression(Identifier(nums)[IntLiteral(0)]))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_037():
	""""""
	source = """class A {
        int val;
    }
    class B {
        void use() {
            A a := new A();
            a.val := 5;
        }
    }"""
	expected = "Program([ClassDecl(A, [AttributeDecl(PrimitiveType(int), [Attribute(val)])]), ClassDecl(B, [MethodDecl(PrimitiveType(void) use([]), BlockStatement(vars=[VariableDecl(ClassType(A), [Variable(a = ObjectCreation(new A()))])], stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(a).val)) := IntLiteral(5))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_038():
	""""""
	source = """class Hello {
        string greet() {
            return "hi";
        }
    }"""
	expected = "Program([ClassDecl(Hello, [MethodDecl(PrimitiveType(string) greet([]), BlockStatement(stmts=[ReturnStatement(return StringLiteral('hi'))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_039():
	""""""
	source = """class Calc {
        void main() {
            x := 1 + 2 * 3 - (4 / 2);
        }
    }"""
	expected = "Program([ClassDecl(Calc, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3))), -, ParenthesizedExpression((BinaryOp(IntLiteral(4), /, IntLiteral(2))))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_040():
	""""""
	source = """class Obj {
        int value;
        void setValue(int v) {
            this.value := v;
        }
    }"""
	expected = "Program([ClassDecl(Obj, [AttributeDecl(PrimitiveType(int), [Attribute(value)]), MethodDecl(PrimitiveType(void) setValue([Parameter(PrimitiveType(int) v)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).value)) := Identifier(v))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_041():
	""""""
	source = """class Printer {
        void print(int x) {
            io.print(x);
        }
        void print(string s) {
            io.print(s);
        }
    }"""
	expected = "Program([ClassDecl(Printer, [MethodDecl(PrimitiveType(void) print([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(x))))])), MethodDecl(PrimitiveType(void) print([Parameter(PrimitiveType(string) s)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(s))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_042():
	""""""
	source = """class Loop {
        void main() {
            for i := 0 to 3 do {
                {
                    int temp := i * 2;
                    io.print(temp);
                }
            }
        }
    }"""
	expected = "Program([ClassDecl(Loop, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(3) do BlockStatement(stmts=[BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(temp = BinaryOp(Identifier(i), *, IntLiteral(2)))])], stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(temp))))])]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_043():
	""""""
	source = """class Holder {
        Data d := new Data();
    }"""
	expected = "Program([ClassDecl(Holder, [AttributeDecl(ClassType(Data), [Attribute(d = ObjectCreation(new Data()))])])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_044():
	""""""
	source = """class Expr {
        int compute() {
            return a.f() + a.g(1, 2);
        }
    }"""
	expected = "Program([ClassDecl(Expr, [MethodDecl(PrimitiveType(int) compute([]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(PostfixExpression(Identifier(a).f()), +, PostfixExpression(Identifier(a).g(IntLiteral(1), IntLiteral(2)))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_045():
	""""""
	source = """class Runner {
        void start() {
            engine.init().run().stop();
        }
    }"""
	expected = "Program([ClassDecl(Runner, [MethodDecl(PrimitiveType(void) start([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(engine).init().run().stop()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_046():
	""""""
	source = """class Mix {
        int a := 5;
        float b;
        string name := "mix";
    }"""
	expected = "Program([ClassDecl(Mix, [AttributeDecl(PrimitiveType(int), [Attribute(a = IntLiteral(5))]), AttributeDecl(PrimitiveType(float), [Attribute(b)]), AttributeDecl(PrimitiveType(string), [Attribute(name = StringLiteral('mix'))])])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_047():
	""""""
	source = """class Box {
        int w; int h;
        Box() {
            this.w := 1;
			this.h := 1;
        }
        Box(int w; int h) {
            this.w := w;
            this.h := h;
        }
    }"""
	expected = "Program([ClassDecl(Box, [AttributeDecl(PrimitiveType(int), [Attribute(w)]), AttributeDecl(PrimitiveType(int), [Attribute(h)]), ConstructorDecl(Box([]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).w)) := IntLiteral(1)), AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).h)) := IntLiteral(1))])), ConstructorDecl(Box([Parameter(PrimitiveType(int) w), Parameter(PrimitiveType(int) h)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).w)) := Identifier(w)), AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).h)) := Identifier(h))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_048():
	""""""
	source = """class Cast {
        void main() {
            x := 3.14;
        }
    }"""
	expected = "Program([ClassDecl(Cast, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := FloatLiteral(3.14))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_049():
	""""""
	source = """class Logger {
        static void info(string msg) {
            io.print(msg);
        }
    }
    class App {
        void main() {
            Logger.info("Running");
        }
    }"""
	expected = "Program([ClassDecl(Logger, [MethodDecl(static PrimitiveType(void) info([Parameter(PrimitiveType(string) msg)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(msg))))]))]), ClassDecl(App, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(Logger).info(StringLiteral('Running'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_050():
	""""""
	source = """class Factory {
        Product make() {
            return new Product();
        }
    }"""
	expected = "Program([ClassDecl(Factory, [MethodDecl(ClassType(Product) make([]), BlockStatement(stmts=[ReturnStatement(return ObjectCreation(new Product()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_051():
	""""""
	source = """class ArrayMaker {
        int[3] create() {
            return {1, 2, 3};
        }
    }"""
	expected = "Program([ClassDecl(ArrayMaker, [MethodDecl(ArrayType(PrimitiveType(int)[3]) create([]), BlockStatement(stmts=[ReturnStatement(return ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)}))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_052():
	""""""
	source = """class Printer {
        void printRect(Rectangle r) {
            io.print(r.getArea());
        }
    }"""
	expected = "Program([ClassDecl(Printer, [MethodDecl(PrimitiveType(void) printRect([Parameter(ClassType(Rectangle) r)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(PostfixExpression(Identifier(r).getArea()))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_053():
	""""""
	source = """class Nested {
        void tripleLoop() {
            for i := 0 to 2 do {
                for j := 0 to 2 do {
                    for k := 0 to 2 do {
                        io.print(i + j + k);
                    }
                }
            }
        }
    }"""
	expected = "Program([ClassDecl(Nested, [MethodDecl(PrimitiveType(void) tripleLoop([]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(2) do BlockStatement(stmts=[ForStatement(for j := IntLiteral(0) to IntLiteral(2) do BlockStatement(stmts=[ForStatement(for k := IntLiteral(0) to IntLiteral(2) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(BinaryOp(BinaryOp(Identifier(i), +, Identifier(j)), +, Identifier(k)))))]))]))]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_054():
	""""""
	source = """class Test {
        void main() {
            arr[func.getIndex()] := 99;
        }
    }"""
	expected = "Program([ClassDecl(Test, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[PostfixExpression(Identifier(func).getIndex())])) := IntLiteral(99))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_055():
	""""""
	source = """class ObjArray {
        void main() {
            data[0].id := 7;
        }
    }"""
	expected = "Program([ClassDecl(ObjArray, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(data)[IntLiteral(0)].id)) := IntLiteral(7))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_056():
	""""""
	source = """class Config {
        static int version := 1;
    }
    class Main {
        void main() {
            io.print(Config.version);
        }
    }"""
	expected = "Program([ClassDecl(Config, [AttributeDecl(static PrimitiveType(int), [Attribute(version = IntLiteral(1))])]), ClassDecl(Main, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(PostfixExpression(Identifier(Config).version))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_057():
	""""""
	source = """class Node {
        Node next;
        Node(Node n) {
            this.next := n;
        }
    }"""
	expected = "Program([ClassDecl(Node, [AttributeDecl(ClassType(Node), [Attribute(next = NilLiteral(nil))]), ConstructorDecl(Node([Parameter(ClassType(Node) n)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).next)) := Identifier(n))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_058():
	""""""
	source = """class Expr {
        void eval() {
            result := obj.next().value + 3 * (2 + obj.calc());
        }
    }"""
	expected = "Program([ClassDecl(Expr, [MethodDecl(PrimitiveType(void) eval([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(result) := BinaryOp(PostfixExpression(Identifier(obj).next().value), +, BinaryOp(IntLiteral(3), *, ParenthesizedExpression((BinaryOp(IntLiteral(2), +, PostfixExpression(Identifier(obj).calc())))))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_059():
	""""""
	source = """class Test{
        static int func(int n){
            if (n == 1) then {
                return 1;
			}
			if (n == 2) then {
                return 1;
			}
			return 2;
		}
        static void main(){
            int n;
            io.readln(n);
			io.print(Test.func(n));
		}
	}"""
	expected = "Program([ClassDecl(Test, [MethodDecl(static PrimitiveType(int) func([Parameter(PrimitiveType(int) n)]), BlockStatement(stmts=[IfStatement(if ParenthesizedExpression((BinaryOp(Identifier(n), ==, IntLiteral(1)))) then BlockStatement(stmts=[ReturnStatement(return IntLiteral(1))])), IfStatement(if ParenthesizedExpression((BinaryOp(Identifier(n), ==, IntLiteral(2)))) then BlockStatement(stmts=[ReturnStatement(return IntLiteral(1))])), ReturnStatement(return IntLiteral(2))])), MethodDecl(static PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(n)])], stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).readln(Identifier(n)))), MethodInvocationStatement(PostfixExpression(Identifier(io).print(PostfixExpression(Identifier(Test).func(Identifier(n))))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_060():
	""""""
	source = """class Hehe{
        static int main(){
            io.println("TOO MANY TESTCASES");
		}
	}"""
	expected = "Program([ClassDecl(Hehe, [MethodDecl(static PrimitiveType(int) main([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).println(StringLiteral('TOO MANY TESTCASES'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_061():
	""""""
	source = """class Animal {
        void speak() { io.print("..."); }
    }
    class Dog extends Animal {
        void speak() { io.print("Woof!"); }
    }"""
	expected = "Program([ClassDecl(Animal, [MethodDecl(PrimitiveType(void) speak([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('...'))))]))]), ClassDecl(Dog, extends Animal, [MethodDecl(PrimitiveType(void) speak([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('Woof!'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_062():
	""""""
	source = """class Parent {
        void greet() { io.print("Hi"); }
    }
    class Child extends Parent {
        void greet() {
            super.greet();
            io.print(" there!");
        }
    }"""
	expected = "Program([ClassDecl(Parent, [MethodDecl(PrimitiveType(void) greet([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('Hi'))))]))]), ClassDecl(Child, extends Parent, [MethodDecl(PrimitiveType(void) greet([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(super).greet())), MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral(' there!'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_063():
	""""""
	source = """class Base {
        Base(int a) { this.x := a; }
    }
    class Derived extends Base {
        Derived() { this.super(10); }
    }"""
	expected = "Program([ClassDecl(Base, [ConstructorDecl(Base([Parameter(PrimitiveType(int) a)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(a))]))]), ClassDecl(Derived, extends Base, [ConstructorDecl(Derived([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(ThisExpression(this).super(IntLiteral(10))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_064():
	""""""
	source = """class A {
        void act() { io.print("A"); }
    }
    class B extends A {
        void act() {
            super.act();
            io.print("B");
        }
    }"""
	expected = "Program([ClassDecl(A, [MethodDecl(PrimitiveType(void) act([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('A'))))]))]), ClassDecl(B, extends A, [MethodDecl(PrimitiveType(void) act([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(super).act())), MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('B'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_065():
	""""""
	source = """class Shape {
        void draw() { io.print("Shape"); }
    }
    class Circle extends Shape {
        void draw() { io.print("Circle"); }
    }
    class Main {
        void main() {
            Shape s := new Circle();
            s.draw();
        }
    }"""
	expected = "Program([ClassDecl(Shape, [MethodDecl(PrimitiveType(void) draw([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('Shape'))))]))]), ClassDecl(Circle, extends Shape, [MethodDecl(PrimitiveType(void) draw([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('Circle'))))]))]), ClassDecl(Main, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Shape), [Variable(s = ObjectCreation(new Circle()))])], stmts=[MethodInvocationStatement(PostfixExpression(Identifier(s).draw()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_066():
	""""""
	source = """class A { }
    class B extends A { }
    class C extends B { }"""
	expected = "Program([ClassDecl(A, []), ClassDecl(B, extends A, []), ClassDecl(C, extends B, [])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_067():
	""""""
	source = """class Base {
        int id := 10;
    }
    class Sub extends Base {
        void printId() { io.print(super.id); }
    }"""
	expected = "Program([ClassDecl(Base, [AttributeDecl(PrimitiveType(int), [Attribute(id = IntLiteral(10))])]), ClassDecl(Sub, extends Base, [MethodDecl(PrimitiveType(void) printId([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(PostfixExpression(Identifier(super).id))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_068():
	""""""
	source = """class Invalid {
        Invalid() {
        }
    }"""
	expected = "Program([ClassDecl(Invalid, [ConstructorDecl(Invalid([]), BlockStatement(stmts=[]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_069():
	""""""
	source = """class Helo{
        static void main(){
		{
		{
		}
		}
		}
	}"""
	expected = "Program([ClassDecl(Helo, [MethodDecl(static PrimitiveType(void) main([]), BlockStatement(stmts=[BlockStatement(stmts=[BlockStatement(stmts=[])])]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_070():
	""""""
	source = """class A {
        int f() { return 1; }
    }
    class B extends A {
        float f() { return 1.0; }
    }"""
	expected = "Program([ClassDecl(A, [MethodDecl(PrimitiveType(int) f([]), BlockStatement(stmts=[ReturnStatement(return IntLiteral(1))]))]), ClassDecl(B, extends A, [MethodDecl(PrimitiveType(float) f([]), BlockStatement(stmts=[ReturnStatement(return FloatLiteral(1.0))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_071():
	""""""
	source = """class Control {
        void run() {
            if x > 0 then
                for i := 0 to 3 do
                    io.print(i);
            else
                io.print("done");
        }
    }"""
	expected = "Program([ClassDecl(Control, [MethodDecl(PrimitiveType(void) run([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then ForStatement(for i := IntLiteral(0) to IntLiteral(3) do MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(i))))), else MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('done')))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_072():
	""""""
	source = """class Init {
        static void init() {
            io.print("Initializing...");
        }
    }"""
	expected = "Program([ClassDecl(Init, [MethodDecl(static PrimitiveType(void) init([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('Initializing...'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_073():
	""""""
	source = """class RefReturn {
        int & getRef(int & x) {
            return x;
        }
    }"""
	expected = "Program([ClassDecl(RefReturn, [MethodDecl(ReferenceType(PrimitiveType(int) &) getRef([Parameter(ReferenceType(PrimitiveType(int) &) x)]), BlockStatement(stmts=[ReturnStatement(return Identifier(x))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_074():
	""""""
	source = """class Box {
        int size;
        Box() {
            size := 0;
        }
        Box(int s) {
            size := s;
        }
    }"""
	expected = "Program([ClassDecl(Box, [AttributeDecl(PrimitiveType(int), [Attribute(size)]), ConstructorDecl(Box([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(size) := IntLiteral(0))])), ConstructorDecl(Box([Parameter(PrimitiveType(int) s)]), BlockStatement(stmts=[AssignmentStatement(IdLHS(size) := Identifier(s))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_075():
	""""""
	source = """class Builder {
        void main() {
            House h := new House(new Room());
        }
    }"""
	expected = "Program([ClassDecl(Builder, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(House), [Variable(h = ObjectCreation(new House(ObjectCreation(new Room()))))])], stmts=[]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_076():
	""""""
	source = """class Decision {
        int choose(int x) {
            if x > 0 then return 1;
            else return -1;
        }
    }"""
	expected = "Program([ClassDecl(Decision, [MethodDecl(PrimitiveType(int) choose([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then ReturnStatement(return IntLiteral(1)), else ReturnStatement(return UnaryOp(-, IntLiteral(1))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_077():
	""""""
	source = """class Group {
        Person[10] members;
    }"""
	expected = "Program([ClassDecl(Group, [AttributeDecl(ArrayType(ClassType(Person)[10]), [Attribute(members)])])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_078():
	""""""
	source = """class Message {
        string greet(string name) {
            return "Hello, " ^ name;
        }
    }"""
	expected = "Program([ClassDecl(Message, [MethodDecl(PrimitiveType(string) greet([Parameter(PrimitiveType(string) name)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(StringLiteral('Hello, '), ^, Identifier(name)))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_079():
	""""""
	source = """class Relay {
        int getValue() {
            return this.compute();
        }
        int compute() {
            return 42;
        }
    }"""
	expected = "Program([ClassDecl(Relay, [MethodDecl(PrimitiveType(int) getValue([]), BlockStatement(stmts=[ReturnStatement(return PostfixExpression(ThisExpression(this).compute()))])), MethodDecl(PrimitiveType(int) compute([]), BlockStatement(stmts=[ReturnStatement(return IntLiteral(42))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_080():
	""""""
	source = """class Printer {
        void printDoc(Document d) {
            d.render();
        }
    }"""
	expected = "Program([ClassDecl(Printer, [MethodDecl(PrimitiveType(void) printDoc([Parameter(ClassType(Document) d)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(d).render()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_081():
	""""""
	source = """class Checker {
        void main() {
            for i := 0 to 5 do {
                if i == 3 then {
                    io.print("Three");
                } else {
                    io.print(i);
                }
            }
        }
    }"""
	expected = "Program([ClassDecl(Checker, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(5) do BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(i), ==, IntLiteral(3)) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(StringLiteral('Three'))))]), else BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).print(Identifier(i))))]))]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_082():
	""""""
	source = """class Factory {
        void main() {
            Widget w1 := new Widget();
            Widget w2 := new Widget();
            w1.activate();
            w2.activate();
        }
    }"""
	expected = "Program([ClassDecl(Factory, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Widget), [Variable(w1 = ObjectCreation(new Widget()))]), VariableDecl(ClassType(Widget), [Variable(w2 = ObjectCreation(new Widget()))])], stmts=[MethodInvocationStatement(PostfixExpression(Identifier(w1).activate())), MethodInvocationStatement(PostfixExpression(Identifier(w2).activate()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected

def test_083():
	""""""
	source = """class User {
        string name;
        User(string n) {
            if n == "" then {
                name := "Anonymous";
            } else {
                name := n;
            }
        }
    }"""
	expected = "Program([ClassDecl(User, [AttributeDecl(PrimitiveType(string), [Attribute(name)]), ConstructorDecl(User([Parameter(PrimitiveType(string) n)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(n), ==, StringLiteral('')) then BlockStatement(stmts=[AssignmentStatement(IdLHS(name) := StringLiteral('Anonymous'))]), else BlockStatement(stmts=[AssignmentStatement(IdLHS(name) := Identifier(n))]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected

def test_084():
	""""""
	source = """class Math {
        int complex() {
            return (2 + 3) * (4 - 1);
        }
    }"""
	expected = "Program([ClassDecl(Math, [MethodDecl(PrimitiveType(int) complex([]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(ParenthesizedExpression((BinaryOp(IntLiteral(2), +, IntLiteral(3)))), *, ParenthesizedExpression((BinaryOp(IntLiteral(4), -, IntLiteral(1))))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_085():
	""""""
	source = """class Init {
        int value := something.getDefault();
        int getDefault() {
            return 10;
        }
    }"""
	expected = "Program([ClassDecl(Init, [AttributeDecl(PrimitiveType(int), [Attribute(value = PostfixExpression(Identifier(something).getDefault()))]), MethodDecl(PrimitiveType(int) getDefault([]), BlockStatement(stmts=[ReturnStatement(return IntLiteral(10))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_086():
	""""""
	source = """class Chain {
        void main() {
            obj.init().build().run();
        }
    }"""
	expected = "Program([ClassDecl(Chain, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(obj).init().build().run()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_087():
	""""""
	source = """class Setup {
        int status;
        Setup() {
            status := this.initialize();
        }
        int initialize() {
            return 1;
        }
    }"""
	expected = "Program([ClassDecl(Setup, [AttributeDecl(PrimitiveType(int), [Attribute(status)]), ConstructorDecl(Setup([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(status) := PostfixExpression(ThisExpression(this).initialize()))])), MethodDecl(PrimitiveType(int) initialize([]), BlockStatement(stmts=[ReturnStatement(return IntLiteral(1))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_088():
	""""""
	source = """class ArrayUtil {
        int get(int[10] arr; int i) {
            return arr[i];
        }
    }"""
	expected = "Program([ClassDecl(ArrayUtil, [MethodDecl(PrimitiveType(int) get([Parameter(ArrayType(PrimitiveType(int)[10]) arr), Parameter(PrimitiveType(int) i)]), BlockStatement(stmts=[ReturnStatement(return PostfixExpression(Identifier(arr)[Identifier(i)]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_089():
	""""""
	source = """class Creator {
        void main() {
            Item i := new Item(new Config(10));
        }
    }"""
	expected = "Program([ClassDecl(Creator, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Item), [Variable(i = ObjectCreation(new Item(ObjectCreation(new Config(IntLiteral(10))))))])], stmts=[]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_090():
	""""""
	source = """class RefMath {
        int & double(int & x) {
            x := x * 2;
            return x;
        }
    }"""
	expected = "Program([ClassDecl(RefMath, [MethodDecl(ReferenceType(PrimitiveType(int) &) double([Parameter(ReferenceType(PrimitiveType(int) &) x)]), BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(x), *, IntLiteral(2))), ReturnStatement(return Identifier(x))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_091():
	""""""
	source = """class Config {
        int level;
        Config(int l) {
            if l < 0 then {
                level := 0;
            } else {
                if l > 10 then {
                    level := 10;
                } else {
                    level := l;
                }
            }
        }
    }"""
	expected = "Program([ClassDecl(Config, [AttributeDecl(PrimitiveType(int), [Attribute(level)]), ConstructorDecl(Config([Parameter(PrimitiveType(int) l)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(l), <, IntLiteral(0)) then BlockStatement(stmts=[AssignmentStatement(IdLHS(level) := IntLiteral(0))]), else BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(l), >, IntLiteral(10)) then BlockStatement(stmts=[AssignmentStatement(IdLHS(level) := IntLiteral(10))]), else BlockStatement(stmts=[AssignmentStatement(IdLHS(level) := Identifier(l))]))]))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_092():
	""""""
	source = """class Runner {
        void main() {
            result := obj.prepare().execute().finalize();
        }
    }"""
	expected = "Program([ClassDecl(Runner, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(result) := PostfixExpression(Identifier(obj).prepare().execute().finalize()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_093():
	""""""
	source = """class Formatter {
        string format(int x) {
            return "Value: " ^ x;
        }
    }"""
	expected = "Program([ClassDecl(Formatter, [MethodDecl(PrimitiveType(string) format([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(StringLiteral('Value: '), ^, Identifier(x)))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_094():
	""""""
	source = """class Caller {
        void main() {
            system.logger.log("Start");
        }
    }"""
	expected = "Program([ClassDecl(Caller, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(system).logger.log(StringLiteral('Start'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected

def test_095():
	""""""
	source = """class Calculator {
        int compute(int a; int b; int c) {
            return (a + b) * c;
        }
    }"""
	expected = "Program([ClassDecl(Calculator, [MethodDecl(PrimitiveType(int) compute([Parameter(PrimitiveType(int) a), Parameter(PrimitiveType(int) b), Parameter(PrimitiveType(int) c)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(ParenthesizedExpression((BinaryOp(Identifier(a), +, Identifier(b)))), *, Identifier(c)))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_096():
	""""""
	source = """class Processor {
        void handle(Task t) {
            t.prepare().execute();
        }
    }"""
	expected = "Program([ClassDecl(Processor, [MethodDecl(PrimitiveType(void) handle([Parameter(ClassType(Task) t)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(t).prepare().execute()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_097():
	""""""
	source = """class Manager {
        Task task;
        Manager() {
            task := new Task();
        }
    }"""
	expected = "Program([ClassDecl(Manager, [AttributeDecl(ClassType(Task), [Attribute(task = NilLiteral(nil))]), ConstructorDecl(Manager([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(task) := ObjectCreation(new Task()))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_098():
	""""""
	source = """class Math {
        int calc() {
            return (1 + 2) * (3 + 4);
        }
    }"""
	expected = "Program([ClassDecl(Math, [MethodDecl(PrimitiveType(int) calc([]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(ParenthesizedExpression((BinaryOp(IntLiteral(1), +, IntLiteral(2)))), *, ParenthesizedExpression((BinaryOp(IntLiteral(3), +, IntLiteral(4))))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_099():
	""""""
	source = """class Logger {
        void logAll() {
            system.log("Start");
            system.log("End");
        }
    }"""
	expected = "Program([ClassDecl(Logger, [MethodDecl(PrimitiveType(void) logAll([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(system).log(StringLiteral('Start')))), MethodInvocationStatement(PostfixExpression(Identifier(system).log(StringLiteral('End'))))]))])])"
	assert str(ASTGenerator(source).generate()) == expected
	
def test_0100():
	""""""
	source = """class RefBox {
        int size;
        RefBox(int & s) {
            size := s;
        }
    }"""
	expected = "Program([ClassDecl(RefBox, [AttributeDecl(PrimitiveType(int), [Attribute(size)]), ConstructorDecl(RefBox([Parameter(ReferenceType(PrimitiveType(int) &) s)]), BlockStatement(stmts=[AssignmentStatement(IdLHS(size) := Identifier(s))]))])])"
	assert str(ASTGenerator(source).generate()) == expected