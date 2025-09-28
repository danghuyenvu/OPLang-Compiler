from utils import Parser


def test_001():
    """Test basic class with main method"""
    source = """class Program { static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_002():
    """Test method with parameters"""
    source = """class Math { int add(int a; int b) { return a + b; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_003():
    """Test class with attribute declaration"""
    source = """class Test { int x; static void main() { x := 42; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_004():
    """Test class with string attribute"""
    source = """class Test { string name; static void main() { name := "Alice"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_005():
    """Test final attribute declaration"""
    source = """class Constants { final float PI := 3.14159; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    """Test if-else statement"""
    source = """class Test { 
        static void main() { 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_007():
    """Test for loop with to keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 1 to 10 do { 
                i := i + 1; 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_008():
    """Test for loop with downto keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 10 downto 1 do { 
                io.writeInt(i); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_009():
    """Test array declaration and access"""
    source = """class Test { 
        static void main() { 
            int[3] arr := {1, 2, 3};
            int first;
            first := arr[0];
            arr[1] := 42;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_010():
    """Test string concatenation and object creation"""
    source = """class Test { 
        static void main() { 
            string result;
            Test obj;
            result := "Hello" ^ " " ^ "World";
            obj := new Test();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_011():
    """Test parser error: missing closing brace in class declaration"""
    source = """class Test { int x := 1; """  # Thiếu dấu }
    expected = "Error on line 1 col 25: <EOF>"
    assert Parser(source).parse() == expected

def test_012():
	"""test parser"""
	source = """class Test{
        static main(){
            int a := 19;
            int c := 20;
            if (a == b) {
                a := a + b * a;
            }
            else {
                a := b;
            }
        }
    }"""
	expected = "Error on line 2 col 19: ("
	assert Parser(source).parse() == expected

def test_013():
	""""""
	source = """class Test{
        final static int b := 9;
        static void main{
            int a := 3;
        }
    }"""
	expected = "Error on line 3 col 24: {"
	assert Parser(source).parse() == expected
     
def test_014():
	""""""
	source = """class Test{
        static final int b := 9;
        int sum(int a, b){
            return a + b;
        }
        static void main(){
            int a := Test.b;
            if this.sum(a, 5) == 2 then {
                a := a + 1;
            }
            else {
            }
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
     
def test_015():
	""""""
	source = """class Test{
        static int b := 5;
        static void main(){
            int& ref := b;
            b := 8;
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
     
def test_016():
	""""""
	source = """class Test{
        static void main (){}
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
     
def test_017():
	""""""
	source = """class Test{
        static void main(){
            for i := 5 to 5 + 5 do {
                io.writeInt(i);
            }
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
     
def test_018():
    """"""
    source = """class Test {
        static void main() {
            if (a > 0) then {
                if (a > 10) then {
                    io.writeStrLn("big");
                } else {
                    io.writeStrLn("small");
                }
            } else {
                io.writeStrLn("negative");
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected
      
def test_019():
	""""""
	source = """class Empty{}"""
	expected = "success"
	assert Parser(source).parse() == expected
     
def test_020():
	""""""
	source = """class A { int x; } class B extends A { static void main() {} }"""
	expected = "success"
	assert Parser(source).parse() == expected
      
def test_021():
	""""""
	source = """Program { int x; }"""
	expected = "Error on line 1 col 0: Program"
	assert Parser(source).parse() == expected
      
def test_022():
	""""""
	source = """class Test {
        Test() {
            io.writeStrLn("constructed");
        }
        destruct Test() {
            io.writeStrLn("destroyed");
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
      
def test_023():
	""""""
	source = """class Example1 {
        int factorial(int n){
            if n == 0 then return 1; else return n * this.factorial(n - 1);
        }

        void main(){
            int x;
            x := io.readInt();
            io.writeIntLn(this.factorial(x));
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
      
def test_024():
	""""""
	source = """class Shape {
        float length, width;
        float getArea() {}
        Shape(float length, width){
            this.length := length;
            this.width := width;
        }
    }

    class Rectangle extends Shape {
        float getArea(){
            return this.length * this.width;
        }
    }

    class Triangle extends Shape {
        float getArea(){
            return this.length * this.width / 2;
        }
    }

    class Example2 {
        void main(){
            Shape s;
            s := new Rectangle(3,4);
            io.writeFloatLn(s.getArea());
            s := new Triangle(3,4);
            io.writeFloatLn(s.getArea());
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
      
def test_025():
	""""""
	source = """class Rectangle {
        float length, width;
        static int count;
        
        # Default constructor
        Rectangle() {
            this.length := 1.0;
            this.width := 1.0;
            Rectangle.count := Rectangle.count + 1;
        }
        
        # Copy constructor
        Rectangle(Rectangle other) {
            this.length := other.length;
            this.width := other.width;
            Rectangle.count := Rectangle.count + 1;
        }
        
        # User-defined constructor
        Rectangle(float length, width) {
            this.length := length;
            this.width := width;
            Rectangle.count := Rectangle.count + 1;
        }
        
        # Destructor
        ~Rectangle() {
            Rectangle.count := Rectangle.count - 1;
            io.writeStrLn("Rectangle destroyed");
        }
        
        float getArea() {
            return this.length * this.width;
        }
        
        static int getCount() {
            return Rectangle.count;
        }
    }

    class Example3 {
        void main() {
            # Using different constructors
            Rectangle r1 := new Rectangle();           # Default constructor
            Rectangle r2 := new Rectangle(5.0, 3.0);   # User-defined constructor
            Rectangle r3 := new Rectangle(r2);         # Copy constructor
            
            io.writeFloatLn(r1.getArea());  # 1.0
            io.writeFloatLn(r2.getArea());  # 15.0
            io.writeFloatLn(r3.getArea());  # 15.0
            io.writeIntLn(Rectangle.getCount());  # 3
            
            # Destructors will be called automatically when objects go out of scope
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_026():
	"""reference type not initialized"""
	source = """class MathUtils {
        static void swap(int & a, b) {
            int temp := a;
            a := b;
            b := temp;
        }
        
        static void modifyArray(int[5] & arr; int index, value) {
            arr[index] := value;
        }
        
        static int & findMax(int[5] & arr) {
            int & max := arr[0];
            for i := 1 to 4 do {
                if (arr[i] > max) then {
                    max := arr[i];
                }
            }
            return max;
        }
    }

    class StringBuilder {
        string & content;
        
        StringBuilder(string & content) {
            this.content := content;
        }
        
        StringBuilder & append(string & text) {
            this.content := this.content ^ text;
            return this;
        }
        
        StringBuilder & appendLine(string & text) {
            this.content := this.content ^ text ^ "\\n";
            return this;
        }
        
        string & toString() {
            return this.content;
        }
    }

    class Example4 {
        void main() {
            # Reference variables
            int x := 10, y := 20;
            int & xRef := x;
            int & yRef := y;
            
            io.writeIntLn(xRef);  # 10
            io.writeIntLn(yRef);  # 20
            
            # Pass by reference
            MathUtils.swap(x, y);
            io.writeIntLn(x);  # 20
            io.writeIntLn(y);  # 10
            
            # Array references
            int[5] numbers := {1, 2, 3, 4, 5};
            MathUtils.modifyArray(numbers, 2, 99);
            io.writeIntLn(numbers[2]);  # 99
            
            # Reference return
            int & maxRef := MathUtils.findMax(numbers);
            maxRef := 100;
            io.writeIntLn(numbers[2]);  # 100
            
            # Method chaining with references
            string text := "Hello";
            StringBuilder & builder := new StringBuilder(text);
            builder.append(" ").append("World").appendLine("!");
            io.writeStrLn(builder.toString());  # "Hello World!\\n"
        }
    }"""
	expected = "Error on line 24 col 24: ;"
	assert Parser(source).parse() == expected
	
def test_027():
	""""""
	source = """class Program{
        static void main(){
		a := a + b + c + d + e + f + g;
		a.b.c.d.e.r.f.g.t.h.c();
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_028():
	""""""
	source = """class Program{
        static void main(){
            a.b.c.f.g.f.f.g.r.gr.gr.d := g.d.d.f.t.v.s.vds.vs.c.sdc.sc.s();
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_029():
	""""""
	source = """class Program{
        static void main(){
            a.b.c.f.g.f.f.g.r.gr.gr.d := g.d.d.f.t.v.s.vds.vs.c.sdc.sc.s();
			a := c.foo(b * 5 + 9 - a.fd.vcs.c(this.foo(1 + 2 + 3, c.d())));
			if this.foo(b * 5 + 9 - a.fd.vcs.c(this.foo(1 + 2 + 3 + c.d()))) < s.as.a.s.as.as.a.s.as.b() then this.b(); else this.c();
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_030():
	""""""
	source = """class Program{
        static void main(){
            a := c.foo(1 + a.c.foo(this.c(),e));
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_031():
	""""""
	source = """class Progam{
        static void main(){
            obj a := new obj();
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_032():
	""""""
	source = """class Progam{
        static void main(){
            (this.c(a + b, this.e()) < 5) < 6;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_033():
	""""""
	source = """class Program{
        static void main(){
            io.printStrLn("Hello World!");
			return 0;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_034():
	""""""
	source = """class Program{
        static int fibo(int n){}
        static void main(){
            int a := --5;
			return 0;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_035():
	""""""
	source = """class Program {
        static void main(){
            int a := 5;
			if a < this.foo(c, b) && a > this.foo(b, c) then a := a + 1; else
			if a > this.foo(c, b) then a := a - 1;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_036():
	""""""
	source = """class Program {
        static int pow(int a, b){
            if b <= 0 then return a;
			else return Program.pow(a * a, b - 1);
		}
        static void main(){
            int a := io.readInt();
			int b := io.readInt();
			io.writeIntLn(Program.pow(a, b));
			return 0;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_037():
	""""""
	source = """class Program{
        int a := 9;
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_038():
	""""""
	source = """class Program{
        static void main(){
            int a := 0;
			float & c := a;
			a := ((4/5/6/8+9*10%3/6) <= (58*7*9%3/7/8/9+5\\9+1)) && true;
			return 0;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_039():
	""""""
	source = """class Program{
        static void main(){
            int a := 0;
			float & c := a;
			a := ((4/5/6/8+9*10%3/6) <= (58*7*9%3/7/8/9+5\\9+1)) && (1.2312e-213 < 5.3242e8);
			return 0;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_040():
	"""array literal"""
	source = """class Program {
        static void main(){
            int[10] b := {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
			if b[5] > 6 then io.writeIntLn(b[5]);
			else io.writeIntLn(-b[5]);
            return 0;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_041():
	"""wrong array literal"""
	source = """class Program {
        static void main(){
            int[10] b := {1, 2, 3, 4, 5, a := 6, 7, 8, 9, 10};
			if b[5] > 6 then io.writeIntLn(b[5]);
			else io.writeIntLn(-b[5]);
            return 0;
		}
	}"""
	expected = "Error on line 3 col 41: a"
	assert Parser(source).parse() == expected
	
def test_042():
    source = """
        class Test {
            static void main() { 
            int 3[2] := 125;
            }
        }
    """  
    expected = "Error on line 4 col 16: 3"
    assert Parser(source).parse() == expected
    
def test_043():
    """wrong array type declaration"""
    source = """
        class Test {
            static void main() { 
            int arr[2] := 125;
            }
    }"""  
    expected = "Error on line 4 col 19: ["
    assert Parser(source).parse() == expected
	
def test_044():
	""""""
	source = """class Program{
        static void main(){
            int a := a < b && c;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_045():
	""""""
	source = """class Program {
        static void main(){
            a[5][9] := 8;
		}
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_046():
	""""""
	source = """class Program {
        static int main(){
            static a := 10;
			return 0;
		}
    }"""
	expected = "Error on line 3 col 12: static"
	assert Parser(source).parse() == expected
	
def test_047():
	""""""
	source = """
            class Test {
                static void main() {
                arr[6] + 125;
                }
            }
        """
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_048():
	""""""
	source = """class Program{
        static void main(){
            3 := 2;
            return 0;
        }
    }"""
	expected = "Error on line 3 col 14: :="
	assert Parser(source).parse() == expected
	
def test_049():
	""""""
	source = """class Program{
        static void main(){
            break;
			continue;
		}
	}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_050():
	""""""
	source = """class Example1 {
        static void main() {
        if a==b then 
        if a==b then
        if a==b then
        if a==b then
            for a:=1 to 5 do
                for b:=66+7+9/8+7*64 downto 57 do
                    for b:=this.foo(!false,!!true,a+b%c) downto this.exp(a==b,6e-5) do
                        if a==b then obj := new Cockatrice(this.foo(0),1.3); else continue;
        }
}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_051():
	""""""
	source = """class Example1 {
        static void main() {
        if (a.b.c(this.foo(a[5/8^5])," d\\tumb" ,1.5e19032)) then
            for i:=1*8+67/65 downto 89-84\\9+74/36+28-57*12 do
                {
                    obj := new obj("name");
                }
        else 
            randomgibberish.func(k[0]+x[9+this.foo(1.5e-7-9.0/5.687)]);
        }
}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_052():
	""""""
	source = """class Example1 {
        static void main() {
        if (a.b.c(this.foo(a[5/8^5])," d\\tumb" ,1.5e19032)) then
            for i:=1*8+67/65 to 89-84\\9+74/36+28-57*12 do
                {
                    obj := new obj("name");
                }
        }
}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_053():
	""""""
	source = """class Example1 {
        static void main() {
        return this.foo(a^b^c^"string"^5+7+8-87/56%78*98);
        }
}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_054():
    """Test string concatenation and object creation"""
    source = """class Example1 {
        static void main() {
        return (a==b)&&(this.foo())!=(a.tuck(a[5]+b[7+9+this.ex(5.0e-14)])>65);
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected
	
def test_055():
	""""""
	source = """class Example1 {
        static void main() {
        float & thi := asdf, asd := (6+5)/8.9%(6e10)+this.foo(a[0]+a.foo());
        }
}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_056():
	""""""
	source = """class Example1 {
        static void main() {
        float a := "string"^3+5/6.7+1.5e10;
        }
}"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_057():
	""""""
	source = """class Animal{
        string type;
        string moan;
		int legnum;
	}
	class Program{
        static void main(){
            Animal cat1 := new Animal();
			cat1.type := "Cat";
            cat1.moan := "Nyan";
			cat1.legnum := 4;
			
            return 0;
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_058():
	""""""
	source = """class Example1 {
        static void main() {
        Rectangle rectangle := new Rectangle(new Rectangle()) ;
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_059():
	""""""
	source = """class Test {
            static void main() { 
            arr[2] := new Rectangle();
            }
        }"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_060():
	""""""
	source = """class Test {
            static void main() { 
            3[2] := 125;
            }
        }"""
	expected = "Error on line 3 col 13: ["
	assert Parser(source).parse() == expected
	
def test_061():
	""""""
	source = """class Test {
            static void main() { 
            arr[6] + 125 := 3;
            }
        }"""
	expected = "Error on line 3 col 25: :="
	assert Parser(source).parse() == expected
	
def test_062():
	""""""
	source = """class Test {
            static void main() { 
            arr.[6] := 125;
            }
        }"""
	expected = "Error on line 3 col 16: ["
	assert Parser(source).parse() == expected
	
def test_063():
	""""""
	source = """class Program{
        static int main(){
            int[5] a := {a, b, c};
		}
	}"""
	expected = "Error on line 3 col 25: a"
	assert Parser(source).parse() == expected
	
def test_064():
	""""""
	source = """class Test {
            static void main() { 
            3 := 125;
            }
        }"""
	expected = "Error on line 3 col 14: :="
	assert Parser(source).parse() == expected
	
def test_065():
	""""""
	source = """class Test {
            static void main() { 
            a[String.Index()] := 125;
            }
        }"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_066():
	""""""
	source = """class Test {
            static void main() { 
            a["emyeutruongem"] := 125;  
            }
        }"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_067():
	""""""
	source = """class Program {
        static void main(){
            int a := 10;
            r := 2.0;
        }
    }"""
	expected = "success"
	assert Parser(source).parse() == expected
	
def test_068():
	""""""
	source = """class Program {
        static void main(){
            r := 2.0;
            int a := 10;
		}
    }"""
	expected = "Error on line 4 col 12: int"
	assert Parser(source).parse() == expected
	
def test_069():
	""""""
	source = """class Program {
        static void main(){
            for x := 1 upto 10 do {
        }"""
	expected = "Error on line 3 col 23: upto"
	assert Parser(source).parse() == expected
	
def test_070():
	""""""
	source = """class Program {
        static void main(){
            static a := 10;
			return 0;
		}
    }"""
	expected = "Error on line 3 col 12: static"
	assert Parser(source).parse() == expected

# def test_071():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_072():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_073():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_074():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_075():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_076():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_077():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_078():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_079():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_080():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_081():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_082():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_083():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_084():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_085():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_086():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_087():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_088():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_089():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_090():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_091():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_092():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_093():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_094():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_095():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_096():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_097():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_098():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_099():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected
# def test_0100():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Parser(source).parse() == expected

def test_071():
    source = """class Program {
        static void main(){
            int a := 5;
            for a < 10 do a := a + 1;
        }
    }"""
    expected = "Error on line 4 col 18: <"
    assert Parser(source).parse() == expected

def test_072():
    source = """class Program {
        static void main(){
            int a := 5;
            for (a < 10) {
                a := a + 1;
            }
        }
    }"""
    expected = "Error on line 4 col 16: ("
    assert Parser(source).parse() == expected

def test_073():
    source = """class Example {
        static void main(){
            if a < b then if b < c then if c < d then return 1; else return 2;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_074():
    source = """class Example {
        static void main(){
            return 0;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_075():
    source = """class Example {
        static void main(){
            return a + ;
        }
    }"""
    expected = "Error on line 3 col 23: ;"
    assert Parser(source).parse() == expected

def test_076():
    source = """class Example {
        Example() {}
        ~Example() {}
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_077():
    source = """class Example {
        int a := 10
    }"""
    expected = "Error on line 3 col 4: }"
    assert Parser(source).parse() == expected

def test_078():
    source = """class Program {
        static void main(){
            int[2][3] arr;
        }
    }"""
    expected = "Error on line 3 col 18: ["
    assert Parser(source).parse() == expected

def test_079():
    source = """class Program {
        static void main(){
            int[2] arr := {1, 2, 3};
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_080():
    source = """class Program {
        static void main(){
            int[2] arr := {1, 2, 3, 4};
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_081():
    source = """class Program {
        static void main(){
            this.foo().bar().baz();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_082():
    source = """class Program {
        static void main(){
            a := (b + c * (d - e);
        }
    }"""
    expected = "Error on line 3 col 33: ;"
    assert Parser(source).parse() == expected

def test_083():
    source = """class Program {
        static void main(){
            for i := 1 to 5 do
                for j := 1 to 5 do
                    for k := 1 to 5 do io.writeInt(i*j*k);
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_084():
    source = """class Program {
        static void main(){
            io.writeStrLn("Hello" ^ " " ^ "World");
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_085():
    source = """class Program {
        static void main(){
            new Unknown();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_086():
    source = """class Program {
        static void main(){
            a := 5 +;
        }
    }"""
    expected = "Error on line 3 col 20: ;"
    assert Parser(source).parse() == expected

def test_087():
    source = """class Program {
        static void main(){
            a := 1 < 2 < 3;
        }
    }"""
    expected = "Error on line 3 col 23: <"
    assert Parser(source).parse() == expected

def test_088():
    source = """class Program {
        static void main(){
            int a, b, c;
            a := b := c := 5;
        }
    }"""
    expected = "Error on line 4 col 19: :="
    assert Parser(source).parse() == expected

def test_089():
    source = """class Program {
        static void main(){
            int a := -- --5;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_090():
    source = """class Program {
        static void main(){
            (a + b)();
        }
    }"""
    expected = "Error on line 3 col 19: ("
    assert Parser(source).parse() == expected

def test_091():
    source = """class Program {
        static void main(){
            if a then return 1; else return 2;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_092():
    source = """class Program {
        static void main(){
            if (a) then return 1;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_093():
    source = """class Program {
        static void main(){
            for a < b do {
                continue;
            }
        }
    }"""
    expected = "Error on line 3 col 18: <"
    assert Parser(source).parse() == expected

def test_094():
    source = """class Program {
        static void main(){
            break;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_095():
    source = """class Program {
        static void main(){
            int x := 1.2.3;
        }
    }"""
    expected = "Error on line 3 col 24: ."
    assert Parser(source).parse() == expected

def test_096():
    source = """class Program {
        static void main(){
            int a := (1 + 2) * (3 + 4);
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_097():
    source = """class Program {
        static void main(){
            a := true && false || !true;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_098():
    source = """class Program {
        static void main(){
            int a := 0;
            if a == 0 then {
                if a < 1 then {
                    if a > -1 then {
                        a := 5;
                    }
                }
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_099():
    source = """class Program {
        static void main(){
            int a := 0;
            for i := 1 to 10 do {
                for j := 1 to 10 do {
                    if i*j == a then break;
                }
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_100():
    source = """class Program {
        static void main(){
            int a := ;
        }
    }"""
    expected = "Error on line 3 col 21: ;"
    assert Parser(source).parse() == expected
	
def test_101():
    source = """\""""
    expected = "Unclosed String: "
    assert Parser(source).parse() == expected
	
def test_102():
    source = """class Program {
        static void main(){}
		int[5] haha(){}
	}"""
    expected = "success"
    assert Parser(source).parse() == expected