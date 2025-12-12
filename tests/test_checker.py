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
    float b := this.a;
    void foo(){
        int a := this.b \\ 1;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(PostfixExpression(ThisExpression(this).b), \\, IntLiteral(1)))"
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
    float b := this.a;
    void foo(){
        int a := this.b + 1;
        final int b;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(a = BinaryOp(PostfixExpression(ThisExpression(this).b), +, IntLiteral(1)))]))"
    assert Checker(source).check_from_source() == expected

def test_012():
    """can cast int to float"""
    source = """
class Test {
    int a;
    int b := this.a;
    void foo(){
        float a := this.b + 1;
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
        float a := this.b + 1;
    }
    void main(){}
}

class child extends Test {
    int a := this.b;
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
        float a := this.b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int b := this.a.b;
    int c := this.a.c;
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(ThisExpression(this).a.c))"
    assert Checker(source).check_from_source() == expected

def test_019():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int b;
    static int c;
    void foo(){
        float a := this.b + 1;
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
        float a := this.b + 1;
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
        float a := this.b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    int c := this.b[4];
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
        float a := this.b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    final int c := this.b[4];
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).b[IntLiteral(4)]))"
    assert Checker(source).check_from_source() == expected

def test_023():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := this.b + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    int c := this.a.b[3];
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(PostfixExpression(ThisExpression(this).b), +, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_024():
    """some postfix tests"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := this.b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    int c := this.a.b[3];
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
        float a := this.b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a;
    int[5] b := {1, 2, 3, 4, 5};
    final int c := this.a.b[3];
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).a.b[IntLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_026():
    """obj create"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := this.b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a := new Test();
    int[5] b := {1, 2, 3, 4, 5};
    final int c := this.a.b[3];
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).a.b[IntLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_027():
    """obj create"""
    source = """
class Test {
    int a;
    int[5] b;
    static int c;
    void foo(){
        float a := this.b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a := new Test(15);
    int[5] b := {1, 2, 3, 4, 5};
    final int c := this.a.b[3];
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
        float a := this.b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a := new Test(15);
    int[5] b := {1, 2, 3, 4, 5};
    final int c := this.a.b[3];
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).a.b[IntLiteral(3)]))"
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
        float a := this.b[3] + 1;
    }
    void main(){}
}
class Child {
    Test a := new Test(15);
    int[5] b := {1, 2, 3, 4, 5};
    final int c := this.a.Test();
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(ThisExpression(this).a.Test()))"
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
        float a := this.b[3] + 1;
    }
    void main(){
        this.b := {1, 2, 3, 4, 5};
        this.a := this.b[1];
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
        float a := this.b[3] + 1;
    }
    void main(){
        this.b := {1, 2, 3, 4, 5};
        this.a := this.b[1];
        Test.c := this.b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(Test).c)) := PostfixExpression(ThisExpression(this).b)))"
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
        float a := this.b[3] + 1;
    }
    void main(){
        this.b := {1, 2, 3, 4, 5};
        this.a := this.b[1];
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
        float a := this.b[3] + 1;
    }
    void main(){
        this.b := {1, 2, 3, 4, 5};
        this.a := this.b[1];
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
        float a := this.b[3] + 1;
    }
    void main(){
        this.b := {1, 2, 3, 4, 5};
        this.a := this.b[1];
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
    expected = "IllegalMemberAccess(ThisExpression(this))"
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
    expected = "IllegalMemberAccess(ThisExpression(this))"
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
    expected = "IllegalMemberAccess(ThisExpression(this))"
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
    expected = "IllegalMemberAccess(ThisExpression(this))"
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
    expected = "IllegalMemberAccess(ThisExpression(this))"
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
    expected = "TypeMismatchInStatement(VariableDecl(ArrayType(PrimitiveType(int)[6]), [Variable(a = ArrayLiteral({Identifier(b), Identifier(b), Identifier(b), Identifier(b), Identifier(b), Identifier(b)}))]))"
    assert Checker(source).check_from_source() == expected

def test_043():
    """some array tests"""
    source = """
class Test {
    static void main(){
        int[3] b := {1, 2, 3};
        int[6] a;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_044():
    """some array tests"""
    source = """
class Test {
    static void main(){
        int[3] b := {1, 2, 3};
        int[6] a := {15 * 2, b[1], b[2], b[0], b[0 + 2], b[0 + 1]};
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_045():
    """reference tests"""
    source = """
class Test {
    static void main(){
        int a := 5;
        int& b := a;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_046():
    """reference tests"""
    source = """
class Test {
    static void main(){
        int a := 5;
        int& b := 5;
        a := b;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_047():
    """test io"""
    source = """
class Test {
    static void main(){
        int a := 5;
        int& b := 5;
        a := b;
        io.writeInt(a);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_048():
    """test io"""
    source = """
class Test {
    static void main(){
        int a := 5;
        int& b := 5;
        a := b;
        io.read(a);
    }
}
"""
    expected = "UndeclaredMethod(read)"
    assert Checker(source).check_from_source() == expected

def test_049():
    """test io"""
    source = """
class Test {
    static void main(){
        int a := 5;
        int& b := 5;
        a := b;
        io.readInt(a);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_050():
    """test io"""
    source = """
class Test {
    static void main(){
        int a := 5;
        int& b := 5;
        boolean c := io.readBool();
        a := b;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_051():
    """test io"""
    source = """
class Test {
    static void main(){
        int a := 5;
        int& b := 5;
        boolean c := io.readInt();
        a := b;
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(boolean), [Variable(c = PostfixExpression(Identifier(io).readInt()))]))"
    assert Checker(source).check_from_source() == expected

def test_052():
    """test io"""
    source = """
class Test {
    static void main(){
        int c := this.readInt();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_053():
    """test io"""
    source = """
class Test {
    static void main(){
        return this.main();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_054():
    """test io"""
    source = """
class Test {
    static void main(){
        int i;
        for i := 5 to io.readInt() do {
            io.printStrLn("haahahaha");
        }
    }
}
"""
    expected = "UndeclaredMethod(printStrLn)"
    assert Checker(source).check_from_source() == expected

def test_055():
    """test io"""
    source = """
class Test {
    static void main(){
        int i;
        for i := 5 to io.readInt() do {
            io.writeStrLn("haahahaha");
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_056():
    """test io"""
    source = """
class Test {
    static void main(){
        int i;
        for i := 5 to io.readInt() do {
            io.writeStrLn("haahahaha");
            if i > 10 then {
                break;
            }
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_057():
    """test io"""
    source = """
class Test {
    static void main(){
        int i, j, k;
        for i := 5 to io.readInt() do {
            for j := i + 1 to io.readInt() do {
                for k := j + 1 to io.readInt() do {
                    break;
                }
                break;
            }
            continue;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_058():
    """test io"""
    source = """
class Haha {
    static int b;
}
class Test {
    static int[3] a;
    static Haha[3] b;
    static void main(){
        
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_059():
    """test io"""
    source = """
class Haha {
    static int b;
}
class Test {
    static int[3] a;
    static Haha[3] b;
    static void main(){
        int c := a[io.readBool()];
    }
}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected

def test_060():
    """test io"""
    source = """
class Haha {
    static int b;
}
class Test {
    static int[3] a;
    static Haha[3] b;
    static void main(){
        int c := Test.a[io.readBool()];
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(Test).a[PostfixExpression(Identifier(io).readBool())]))"
    assert Checker(source).check_from_source() == expected

def test_061():
    """test io"""
    source = """
class Haha {
    static int b;
}
class Test {
    static int[3] a;
    static Haha[3] b;
    static void main(){
        Haha c := new Haha(this.a);
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_062():
    """test io"""
    source = """
class Haha {
    static int b;
}
class Test {
    static int[3] a;
    static Haha[3] b;
    static void main(){
        Haha c := new Haha(Test.a);
    }
}
"""
    expected = "TypeMismatchInExpression(ObjectCreation(new Haha(PostfixExpression(Identifier(Test).a))))"
    assert Checker(source).check_from_source() == expected

def test_063():
    """test io"""
    source = """
class Haha {
    static int b;
}
class Test {
    static int[3] a;
    static Haha[3] b;
    static void main(){
        Haha c := new Haha(this.a);
    }
    int main(){
    }
}
"""
    expected = "Redeclared(Method, main)"
    assert Checker(source).check_from_source() == expected

def test_064():
    """test io"""
    source = """
class Haha {
    static int b;
}
class Test {
    static int[3] a;
    static Haha[3] b;
    static void main(){
        Haha c := new Haha(this.a);
        break;
    }
    int main(){
    }
}
"""
    expected = "Redeclared(Method, main)"
    assert Checker(source).check_from_source() == expected

def test_065():
    """test io"""
    source = """
class Haha {
    static int b;
}
class Test {
    static int[3] a;
    static Haha[3] b := {new Haha(), new Haha(), new Haha()};
    static void main(){
        Haha c := new Haha(this.a);
    }
    int main(){
    }
}
"""
    expected = "Redeclared(Method, main)"
    assert Checker(source).check_from_source() == expected

def test_066():
    """test io"""
    source = """
class Test {
    static void main(){
    }

    int foo(int a; int b){
        return "hahaha";
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return StringLiteral('hahaha')))"
    assert Checker(source).check_from_source() == expected

def test_067():
    """test io"""
    source = """
class Test {
    static void main(){
        float[6] a := {1, 2, 3, 4, 5, 6};
    }

    int foo(int a; int b){
        return "hahaha";
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ArrayType(PrimitiveType(float)[6]), [Variable(a = ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4), IntLiteral(5), IntLiteral(6)}))]))"
    assert Checker(source).check_from_source() == expected

def test_068():
    """"""
    source = """
class Test {
    static void main(){
        int i := 5;
        for i := io.readFloat() downto 1 do {
        }
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := PostfixExpression(Identifier(io).readFloat()) downto IntLiteral(1) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_069():
    """"""
    source = """
class Test {
    static void main(){
        int i := 5;
        {{{{{{{for i := io.readFloat() downto 1 do {
        }}}}}}}}
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := PostfixExpression(Identifier(io).readFloat()) downto IntLiteral(1) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_070():
    """"""
    source = """
class Test {
    static void main(){
        int i := 5;
        if i == 5 then {
            int sum := 0;
            for i := 1 to 10 do {
                sum := sum + i;
                if sum % 2 == 0 then {
                    break;
                }
            }
        }
        else {
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_071():
    """"""
    source = """
class utils {
    static int max(int[100] a){
        int max := a[0], i := 1;
        for i := 1 to 99 do {
            if max < a[i] then {
                max := a[i];
            }
        }
        return max;
    }
}
class Test {
    static void main(){
        int[6] a := {1, 3, 2, 6, 5, 4};
        io.writeIntLn(utils.max(a));
    }
}
"""
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(PostfixExpression(Identifier(utils).max(Identifier(a)))))))"
    assert Checker(source).check_from_source() == expected

def test_071():
    """"""
    source = """
class utils {
    static int max(int[6] a){
        int max := a[0], i := 1;
        for i := 1 to 5 do {
            if max < a[i] then {
                max := a[i];
            }
        }
        return max;
    }
}
class Test {
    static int main(){
        int[6] a := {1, 3, 2, 6, 5, 4};
        io.writeIntLn(utils.max(a));
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_072():
    """"""
    source = """
class utils {
}
class Test {
    static int main(){
        int[10] a := {1, 3, 2, 6, 5, 4, 10, 8, 11, 15};
        int i;
        for i := 0 to 9 do {
            io.writeIntLn(a[i]);
        }
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_073():
    """merge sort"""
    source = """
class utils {
    static int max(int[6] a){
        int max := a[0], i := 1;
        for i := 1 to 5 do {
            if max < a[i] then {
                max := a[i];
            }
        }
        return max;
    }
    static int[10] merge_sort(int[10] a; int start; int end){
        int middle := (end - start) \\ 2 + start;
        int i, lp := start, rp := middle + 1;
        if start >= end then {
            return a;
        }
        else {
            int[10] left := utils.merge_sort(a, start, middle), right := utils.merge_sort(a, middle + 1, end);
            for i := start to end do {
                if lp >= middle + 1 || rp >= end then break;
                if left[lp] < right[rp] then {
                    a[i] := left[lp];
                    lp := lp + 1;
                }
                else {
                    a[i] := right[rp];
                    rp := rp + 1;
                }
            }
            if lp < middle then {
                int j;
                for j := lp to middle do {
                    a[i] := left[j];
                    i := i + 1;
                }
            }
            else if rp < end then {
                int j;
                for j := rp to end do {
                    a[i] := right[j];
                    i := i + 1;
                }
            }
            return a;
        }
    }
}
class Test {
    static int main(){
        int[10] a := {1, 3, 2, 6, 5, 4, 10, 8, 11, 15};
        int i;
        a := utils.merge_sort(a, 0, 9);
        for i := 0 to 9 do {
            io.writeIntLn(a[i]);
        }
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_074():
    """bubble sort"""
    source = """
class utils {
    static void swap(int& a; int& b){
        a := a + b;
        b := a - b;
        a := a - b;
    }
    static int[10] bubble_sort(int[10] arr){
        int curr, end := 9, i, it;
        for it := 9 downto 0 do {
            boolean swapped := false;
            for i := 0 to end - 1 do {
                if arr[i] > arr[i + 1] then {
                    utils.swap(arr[i], arr[i + 1]);
                    swapped := true;
                }
            }
            if !swapped || end == 0 then break;
            else end := end - 1;
        }
        return arr;
    }
}
class Test {
    static int main(){
        int[10] a := {1, 3, 2, 6, 5, 4, 10, 8, 11, 15};
        int i;
        a := utils.bubble_sort(a);
        for i := 0 to 9 do {
            io.writeIntLn(a[i]);
        }
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_075():
    """selection sort"""
    source = """
class utils {
    static void swap(int& a; int& b){
        a := a + b;
        b := a - b;
        a := a - b;
    }
    static int[10] selection_sort(int[10] arr){
        int i;
        for i := 0 to 8 do {
            int j, index := i;
            for j := i + 1 to 9 do {
                if arr[index] > arr[j] then {
                    index := j;
                }
            }
            if i != index then utils.swap(arr[i], arr[index]);
        }

        return arr;
    }
}
class Test {
    static int main(){
        int[10] a := {1, 3, 2, 6, 5, 4, 10, 8, 11, 15};
        int i;
        a := utils.selection_sort(a);
        for i := 0 to 9 do {
            io.writeIntLn(a[i]);
        }
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_076():
    """insertion_sort"""
    source = """
class utils {
    static void swap(int& a; int& b){
        a := a + b;
        b := a - b;
        a := a - b;
    }
    static int[10] insert(int[10] arr; int target; int dest){
        if target <= dest || target >= 10 || dest >= 10 || dest < 0 || target < 0 then return arr;
        else {
            int i;
            for i := dest to target - 1 do {
                utils.swap(arr[i], arr[target]);
            }
            return arr;
        }
    }
    static int[10] insertion_sort(int[10] arr){
        int bound := 0, i;
        for bound := 1 to 9 do {
            for i := 0 to bound - 1 do {
                if arr[bound] <= arr[i] then {
                    arr := utils.insert(arr, bound, i);
                    break;
                }
            }
        }

        return arr;
    }
}
class Test {
    static int main(){
        int[10] a := {1, 3, 2, 6, 5, 4, 10, 8, 11, 15};
        int i;
        a := utils.insertion_sort(a);
        for i := 0 to 9 do {
            io.writeIntLn(a[i]);
        }
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_077():
    """quick_sort"""
    source = """
class utils {
    static void swap(int& a; int& b){
        a := a + b;
        b := a - b;
        a := a - b;
    }
    static int[10] insert(int[10] arr; int target; int dest){
        if target <= dest || target >= 10 || dest >= 10 || dest < 0 || target < 0 then return arr;
        else {
            int i;
            for i := dest to target - 1 do {
                utils.swap(arr[i], arr[target]);
            }
            return arr;
        }
    }
    static void quick_sort(int[10]& arr; int start; int end){
        int i, pivot := start;
        if start < end then {
            for i := start + 1 to end do {
                if i != pivot && arr[i] < arr[pivot] then {
                    arr := utils.insert(arr, i, pivot);
                    pivot := pivot + 1;
                }
            }
            utils.quick_sort(arr, start, pivot);
            utils.quick_sort(arr, pivot + 1, end);
        }
    }
}
class Test {
    static int main(){
        int[10] a := {1, 3, 2, 6, 5, 4, 10, 8, 11, 15};
        int i;
        utils.quick_sort(a, 0, 9);
        for i := 0 to 9 do {
            io.writeIntLn(a[i]);
        }
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_078():
    """"""
    source = """
class utils {
    static void swap(int& a; int& b){
        a := a + b;
        b := a - b;
        a := a - b;
    }
    static int execute(int[10]& arr; int pos; int length){
        if pos < length then {
            int i;
            for i := pos to length - 1 do {
                utils.swap(arr[i], arr[i + 1]);
            }
            return length - 1;
        }
        else return length;
    }
    static void hihi_sort(int[10]& arr; int size){
        int i;
        for i := 1 to size - 1 do {
            if arr[i] < arr[i - 1] then {
                size := utils.execute(arr, i, size);
            }
        }
    }
}
class Test {
    static int main(){
        int[10] a := {1, 3, 2, 6, 5, 4, 10, 8, 11, 15};
        int i, size := 10;
        utils.hihi_sort(a, size);
        for i := 0 to size - 1 do {
            io.writeIntLn(a[i]);
        }
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_079():
    """"""
    source = """
class Test {
    int &a := 5;
    int b := a;
    static int main(){
        return 0;
    }
}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected

def test_080():
    """"""
    source = """
class Test {
    static int &a := 5;
    int b := Test.a;
    static int main(){
        return 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_081():
    """"""
    source = """
class Test {
    static int &a := 5;
    int b := Test.a;
    static int main(){
        return Test.main();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_082():
    """"""
    source = """
class Test {
    static int main(){
        string b := "a" ^ "c" + e;
    }
}
"""
    expected = "UndeclaredIdentifier(e)"
    assert Checker(source).check_from_source() == expected

def test_083():
    """"""
    source = """
class Test {
    static int main(){
        string b := "a" ^ "c" + 5;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(BinaryOp(StringLiteral('a'), ^, StringLiteral('c')), +, IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected

def test_084():
    """"""
    source = """
class Test {
    static int main(){
        boolean a := 1 < 2 || 2 > 3;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_085():
    """"""
    source = """
class Test {
    static int main(){
        int c := 5 * 3 + 7 * 2 - (10 / 2) + 5;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_086():
    """"""
    source = """
class Test {
    static int main(){
        {
            {
                break;
            }
        }
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_087():
    """"""
    source = """
class Test {
    static int main(){
        int i;
        for i := 5 to 6 do {
            for i := 7 to 8 do {
                for i := 8 to 9 do {
                    break;
                    break;
                    break;
                    break;
                }
            }
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_088():
    """"""
    source = """
class Test {
    static int main(){
        int i;
        for i := 5 to 6 do {
            for i := 7 to 8 do {
                for i := 8 to 9 do {
                    break;
                }
                    break;
            }
                    break;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_089():
    """"""
    source = """
class Test {
    static int main(){
        int i;
        for i := 5 to 6 do {
            for i := 7 to 8 do {
                for i := 8 to 9 do {
                    return (1 + 2);
                }
            }
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_090():
    """"""
    source = """
class Test {
    static void main(){
        return 0;
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test_091():
    """"""
    source = """
class Test {
    static void main(){
        continue;
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_092():
    """"""
    source = """
class Test {
    static void main(){
        int i;
        for i := 0 to 9 do {
            continue;
            continue;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_093():
    """"""
    source = """
class Test {
    static void main(){
        io.writeStrLn("Hello World!");
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_094():
    """"""
    source = """
class animal {
    string type, voice;
    animal(string voice){
        this.voice := voice;
    }
    void sound(){
        io.writeStrLn(this.voice);
    }
}
class Test {
    static void main(){
        animal cat := new animal("meow");
        cat.sound();
        return 0;
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test_095():
    """"""
    source = """
class animal {
    string type, voice;
    animal(string voice){
        this.voice := voice;
    }
    void sound(){
        io.writeStrLn(this.voice);
    }
}
class cat extends animal {
    cat(){
        this.voice := "meow";
    }
}
class Test {
    static void main(){
        cat cat := new cat();
        cat.sound();
        return 0;
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test_096():
    """"""
    source = """
class animal {
    string type, voice;
    animal(string voice){
        this.voice := voice;
    }
    void sound(){
        io.writeStrLn(this.voice);
    }
}
class cat extends animal {
    cat(){
        this.voice := "meow";
    }
}
class Test {
    static void main(){
        cat cat := new cat();
        cat.sound();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_097():
    """"""
    source = """
class animal {
    string type, voice;
    int limbs;
    animal(string voice; int limbs){
        this.voice := voice;
        this.lims := limbs;
    }
    void sound(){
        io.writeStrLn(this.voice);
    }
}
class cat extends animal {
    cat(){
        this.voice := "meow";
    }
}
class Test {
    static void main(){
        cat cat := new cat();
        cat.sound();
        io.writeIntLn(cat.limbs);
    }
}
"""
    expected = "UndeclaredAttribute(lims)"
    assert Checker(source).check_from_source() == expected

def test_098():
    """"""
    source = """
class Test {
    static void main(){
        cat cat := new cat();
        cat.sound();
        io.writeIntLn(cat.limbs);
    }
}
"""
    expected = "UndeclaredClass(cat)"
    assert Checker(source).check_from_source() == expected

def test_099():
    """"""
    source = """
class animal {
    string type, voice;
    int limbs;
    animal(string voice; int limbs){
        this.voice := voice;
        this.lims := limbs;
    }
    void sound(){
        io.writeStrLn(this.voice);
    }
}
class cat extends animal {
    cat(){
        this.voice := "meow";
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_100():
    """"""
    source = """
class Test {
    static void main(){int c; for c:=5 to 6 do {break;}}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected