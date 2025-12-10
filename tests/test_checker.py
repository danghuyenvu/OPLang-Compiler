from utils import Checker


def test_001():
    """Test a valid program that should pass all checks"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int y := x + 1;
    }
}
"""
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_002():
    """Test redeclared variable error"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int x := 10;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_003():
    """Test undeclared identifier error"""
    source = """
class Test {
    static void main() {
        int x := y + 1;
    }
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected

def test_004():
    """Test type mismatch error"""
    source = """
class Test {
    static void main() {
        int x := "hello";
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = StringLiteral('hello'))]))"
    assert Checker(source).check_from_source() == expected

def test_005():
    """Test break not in loop error"""
    source = """
class Test {
    static void main() {
        break;
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_006():
    """Test cannot assign to constant error"""
    source = """
class Test {
    static void main() {
        final int x := 5;
        x := 10;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(10)))"
    assert Checker(source).check_from_source() == expected

def test_007():
    """Test illegal array literal error - alternative case"""
    source = """
class Test {
    static void main() {
        boolean[2] flags := {true, 42};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected

def test_008():
    """No entry point"""
    source = """
class Test {
    void foo(){
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_009():
    """Test simple type missmatch"""
    source = """
class Test {
    int a := 5;
    float b := a;
    void foo(){
        int a := b \\ 1;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(b), \\, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_010():
    """Illegal constant"""
    source = """
class Test {
    final int a;
    float b := a;
    void foo(){
        int a := b \\ 1;
    }
    static void main(){}
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected

def test_011():
    """cannot cast float to int"""
    source = """
class Test {
    int a;
    float b := a;
    void foo(){
        int a := b + 1;
        final int b;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(a = BinaryOp(Identifier(b), +, IntLiteral(1)))]))"
    assert Checker(source).check_from_source() == expected

def test_012():
    """can cast int to float"""
    source = """
class Test {
    int a;
    int b := a;
    void foo(){
        float a := b + 1;
    }
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_013():
    """declaration test"""
    source = """
class Test extends A {
    int a;
    int b := a;
    void foo(){
        float a := b + 1;
    }
    static void main(){}
}
class A {}
"""
    expected = "UndeclaredClass(A)"
    assert Checker(source).check_from_source() == expected

def test_014():
    """undeclared class"""
    source = """
class Test {
    int a;
    Cat b;
    void foo(){
        float a := b + 1;
    }
    static void main(){}
}
"""
    expected = "UndeclaredClass(Cat)"
    assert Checker(source).check_from_source() == expected

def test_015():
    """"""
    source = """
class Test {
    int a;
    Cat b;
    void foo(){
        float a := b + 1;
    }
    void main(){}
}
"""
    expected = "UndeclaredClass(Cat)"
    assert Checker(source).check_from_source() == expected

def test_016():
    """some inheritance test"""
    source = """
class Test {
    int a;
    int b;
    void foo(){
        float a := b + 1;
    }
    void main(){}
}

class child extends Test {
    int a := b;
    void haha(){
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_017():
    """"""
    source = """
class Test {
    int a := (1 + 2).foo();
    void foo(){
    }
    void main(){
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(ParenthesizedExpression((BinaryOp(IntLiteral(1), +, IntLiteral(2)))).foo()))"
    assert Checker(source).check_from_source() == expected

def test_018():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int b;
    static int c;
    void foo(){
        float a := b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int b := a.b;
    int c := a.c;
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(a).c))"
    assert Checker(source).check_from_source() == expected

def test_019():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int b;
    static int c;
    void foo(){
        float a := b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int b := Test.b;
    int c := a.c;
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Test).b))"
    assert Checker(source).check_from_source() == expected

def test_020():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int b;
    static int c;
    void foo(){
        float a := b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int b := Test.c;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_021():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int b;
    static int c;
    void foo(){
        float a := b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    int c := b[4];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_022():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int b;
    static int c;
    void foo(){
        float a := b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    final int c := b[4];
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(b)[IntLiteral(4)]))"
    assert Checker(source).check_from_source() == expected

def test_023():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    int c := a.b[3];
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(b), +, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_024():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    int c := a.b[3];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_025():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    final int c := a.b[3];
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(a).b[IntLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_026():
    """obj create"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a := new Test();
    int[5] b := {1, 2, 3, 4, 5};
    final int c := a.b[3];
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(a).b[IntLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_027():
    """obj create"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a := new Test(15);
    int[5] b := {1, 2, 3, 4, 5};
    final int c := a.b[3];
}
"""
    expected = "TypeMismatchInExpression(ObjectCreation(new Test(IntLiteral(15))))"
    assert Checker(source).check_from_source() == expected

def test_028():
    """obj create"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    Test(int c){
    }
    void foo(){
        float a := b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a := new Test(15);
    int[5] b := {1, 2, 3, 4, 5};
    final int c := a.b[3];
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(a).b[IntLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_029():
    """obj create"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    Test(int c){
    }
    void foo(){
        float a := b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a := new Test(15);
    int[5] b := {1, 2, 3, 4, 5};
    final int c := a.Test();
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(a).Test()))"
    assert Checker(source).check_from_source() == expected


def test_030():
    """obj create"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    Test(int c){
    }
    void foo(){
        float a := b[3] + 1;
    }
    void main(){
        b := {1, 2, 3, 4, 5};
        a := b[1];
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_031():
    """obj create"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    Test(int c){
    }
    void foo(){
        float a := b[3] + 1;
    }
    void main(){
        b := {1, 2, 3, 4, 5};
        a := b[1];
        c := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(c) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_032():
    """test program 2 pass"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    Haha e;
    Test(int c){
    }
    void foo(){
        float a := b[3] + 1;
    }
    void main(){
        b := {1, 2, 3, 4, 5};
        a := b[1];
    }
}
class Haha{
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_033():
    """doo doo test"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    Test(int c){
    }
    void foo(){
        float a := b[3] + 1;
    }
    void main(){
        b := {1, 2, 3, 4, 5};
        a := b[1];
    }
}
class jajaja{
    static int b := 3;
}

class jejjee extends jajaja{
    static void foo(){
        int c := jejjee.b;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_034():
    """this cannot access static mem"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    Test(int c){
    }
    void foo(){
        float a := b[3] + 1;
    }
    void main(){
        b := {1, 2, 3, 4, 5};
        a := b[1];
    }
}
class jajaja{
    static int b := 3;
}

class jejjee extends jajaja{
    static void foo(){
        int c := this.b;
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(ThisExpression(this).b))"
    assert Checker(source).check_from_source() == expected

def test_035():
    """doodoo chcker"""
    source = """
class Test {
    jajaja laugh := new jajaja();
    void foo(){
        int a := this.laugh.c;
        this.foo();
    }
    static void main(){
        this.foo();
    }
}
class jajaja{
    static int b := 3;
    int c := 9;
}

class jejjee extends jajaja{
    static void foo(){
        int c := jajaja.b;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_036():
    """doodoo chcker"""
    source = """
class Test {
    jajaja laugh := new jajaja();
    void foo(){
        int a := this.laugh.c;
        this.foo();
    }
    static void main(){
        this.foo();
    }
}
class jajaja{
    static int b := 3;
    int c := 9;
    static int[5] d := {1, 2, 3, 4, 5};
}

class jejjee extends jajaja{
    static void foo(){
        int c := jajaja.b;
        float[5] e := jajaja.d;
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ArrayType(PrimitiveType(float)[5]), [Variable(e = PostfixExpression(Identifier(jajaja).d))]))"
    assert Checker(source).check_from_source() == expected

def test_037():
    """doodoo chcker"""
    source = """
class Test {
    jajaja laugh := new jajaja();
    void foo(){
        int a := this.laugh.c;
        this.foo();
    }
    static void main(){
        this.foo();
    }
}
class jajaja{
    static int b := 3;
    int c := 9;
    static int[5] d := {1, 2, 3, 4, 5};
}

class jejjee extends jajaja{
    static void foo(){
        int c := jajaja.b;
        float[5] e := {1, 2, 3, 5.5, 6};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3), FloatLiteral(5.5), IntLiteral(6)}))"
    assert Checker(source).check_from_source() == expected

def test_038():
    """doodoo chcker"""
    source = """
class Test {
    jajaja laugh := new jajaja();
    void foo(){
        int a := this.laugh.c;
        this.foo();
    }
    static void main(){
        this.foo();
    }
}
class jajaja{
    static int b := 3;
    int c := 9;
    static int[5] d := {1, 2, 3, 4, 5};
}

class jejjee extends jajaja{
    static void foo(){
        int c := jajaja.b;
        float[5] e := {1, 2, 3, 5, 6};
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ArrayType(PrimitiveType(float)[5]), [Variable(e = ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(5), IntLiteral(6)}))]))"
    assert Checker(source).check_from_source() == expected

def test_039():
    """redeclared constructor"""
    source = """
class Test {
    static void main(){
    }
}
class Haha{
    Haha(int a; int b){
    }
    Haha(int b; int c){
    }
}
"""
    expected = "Redeclared(Constructor, Haha)"
    assert Checker(source).check_from_source() == expected

def test_040():
    """redeclared destructor"""
    source = """
class Test {
    static void main(){
    }
}
class Haha{
    Haha(int a; int b){
    }
    ~Haha(){
    }
    ~Haha(){
    }
}
"""
    expected = "Redeclared(Destructor, Haha)"
    assert Checker(source).check_from_source() == expected

def test_041():
    """some array tests"""
    source = """
class Test {
    static void main(){
        int[6] a := {1, 2, 3, 4, 5, 6, 7, 8};
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ArrayType(PrimitiveType(int)[6]), [Variable(a = ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4), IntLiteral(5), IntLiteral(6), IntLiteral(7), IntLiteral(8)}))]))"
    assert Checker(source).check_from_source() == expected

def test_042():
    """some array tests"""
    source = """
class Test {
    static void main(){
        int[3] b := {1, 2, 3};
        int[6] a := {b, b, b, b, b, b};
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ArrayType(PrimitiveType(int)[6]), [Variable(a = ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4), IntLiteral(5), IntLiteral(6), IntLiteral(7), IntLiteral(8)}))]))"
    assert Checker(source).check_from_source() == expected