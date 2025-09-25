from utils import Tokenizer


def test_001():
    """Test basic identifier tokenization"""
    source = "abc"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_002():
    """Test keywords recognition"""
    source = "class extends static final if else for do then to downto new this void boolean int float string true false nil break continue return"
    expected = "class,extends,static,final,if,else,for,do,then,to,downto,new,this,void,boolean,int,float,string,true,false,nil,break,continue,return,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_003():
    """Test integer literals"""
    source = "42 0 255 2500"
    expected = "42,0,255,2500,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_004():
    """Test float literals"""
    source = "9.0 12e8 1. 0.33E-3 128e+42"
    expected = "9.0,12e8,1.,0.33E-3,128e+42,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_005():
    """Test boolean literals"""
    source = "true false"
    expected = "true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_006():
    """Test unclosed string literal error"""
    source = '"Hello World'
    expected = "Unclosed String: Hello World"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_007():
    """Test illegal escape sequence error"""
    source = '"Hello \\x World"'
    expected = "Illegal Escape In String: Hello \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_008():
    """Test error character (non-ASCII or invalid character)"""
    source = "int x := 5; @ invalid"
    expected = "int,x,:=,5,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009():
    """Test valid string literals with escape sequences"""
    source = '"This is a string containing tab \\t" "He asked me: \\"Where is John?\\""'
    expected = "This is a string containing tab \\t,He asked me: \\\"Where is John?\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009a():
    """Test string literals return content without quotes"""
    source = '"Hello World"'
    expected = "Hello World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009b():
    """Test empty string literal"""
    source = '""'
    expected = ",EOF"  # Empty string content
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_010():
    """Test operators and separators"""
    source = "+ - * / \\ % == != < <= > >= && || ! := ^ new . ( ) [ ] { } , ; :"
    expected = "+,-,*,/,\\,%,==,!=,<,<=,>,>=,&&,||,!,:=,^,new,.,(,),[,],{,},,,;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_011():
    """Test line comments"""
    source = "#This is /*a line comment"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_012():
    """Test block comments"""
    source = """/*This is a block comment" 
    "#hahahahahahaha" 
    "hahahahahahaahah*/"""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_013():
    """Test block comments without closing"""
    source = """/*This is a block comment with no closing 
    #hahahahahahaha 
    hahahahahahaahah"""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    """Test block comments without closing and prioritizing"""
    source = """/*This is a block comment with no closing \\n 
    #hahahahahahaha
    hahahahahahaahah"""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    """test tokenizer"""
    source = """class Test { 
        static void main() { 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }
        }
    }"""
    expected = "class,Test,{,static,void,main,(,),{,if,(,x,>,0,),then,{,io,.,writeStrLn,(,positive,),;,},else,{,io,.,writeStrLn,(,negative,),;,},},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_016():
    """block comment in a proper file"""
    source = """class Test { 
        static void main() { /* 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }*/
        }
    }"""
    expected = "class,Test,{,static,void,main,(,),{,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_017():
    """Test block comments without closing"""
    source = """/*This is a block comment with no "closing */"
    #hahahahahahaha 
    hahahahahahaahah"""
    expected = "Unclosed String: "
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_018():
    """"""
    source = """class Constants { final float PI = 3.14159; static void main() {} }"""
    expected = "class,Constants,{,final,float,PI,Error Token ="
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_019():
    """"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 1 to 10 do { 
                i := i + 1; 
            }
        }
    }"""
    expected = "class,Test,{,static,void,main,(,),{,int,i,;,for,i,:=,1,to,10,do,{,i,:=,i,+,1,;,},},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_020():
    """"""
    source = """class Test { 
        static void main() { 
            string result;
            result := "Hello" ^ " " ^ "World";
            Test obj;
            #obj := new Test();
        }
    }"""
    expected = "class,Test,{,static,void,main,(,),{,string,result,;,result,:=,Hello,^, ,^,World,;,Test,obj,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# def test_021():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_022():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_023():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_024():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_025():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_026():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_027():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_028():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_029():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_030():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_031():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_032():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_033():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_034():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_035():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_036():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_037():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_038():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_039():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_040():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_041():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_042():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_043():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_044():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_045():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_046():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_047():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_048():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_049():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_050():
#     """"""
#     source = """"""
#     expected = ""
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_051():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_052():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_053():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_054():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_055():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_056():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_057():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_058():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_059():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_060():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_061():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_062():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_063():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_064():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_065():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_066():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_067():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_068():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_069():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_070():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_071():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_072():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_073():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_074():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_075():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_076():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_077():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_078():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_079():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_080():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_081():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_082():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_083():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_084():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_085():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_086():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_087():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_088():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_089():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_090():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_091():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_092():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_093():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_094():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_095():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_096():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_097():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_098():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected
# def test_099():
# 	""""""
# 	source = """"""
# 	expected = ""
# 	assert Tokenizer(source).get_tokens_as_string() == expected

def test_021():
    """Identifier with underscores and digits"""
    source = "my_var1 anotherVar2"
    expected = "my_var1,anotherVar2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_022():
    """Identifier that looks like keyword prefix"""
    source = "classify continuex"
    expected = "classify,continuex,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    """Single digit integers"""
    source = "0 5 9"
    expected = "0,5,9,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    """Float without fraction"""
    source = "1."
    expected = "1.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    """Float with exponent only"""
    source = "1e10 2E-3 5E+7"
    expected = "1e10,2E-3,5E+7,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    """Invalid float with two dots"""
    source = "1.2.3"
    expected = "1.2,.,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    """Unclosed float exponent"""
    source = "12e"
    expected = "12,e,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    """String with escaped quote"""
    source = '"He said: \\"Hello\\""'
    expected = "He said: \\\"Hello\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_029():
    """String with newline inside (illegal)"""
    source = '"Hello\nWorld"'
    expected = "Unclosed String: Hello"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_030():
    """String with tab escape"""
    source = '"Line1\\tLine2"'
    expected = "Line1\\tLine2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_031():
    """Illegal escape in string"""
    source = '"Bad\\qEscape"'
    expected = "Illegal Escape In String: Bad\\q"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    """Operators basic"""
    source = "+ - * / %"
    expected = "+,-,*,/,% ,EOF".replace(" ,",",")  # tidy
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    """Operators with assignment and comparison"""
    source = "== != <= >= := ="
    expected = "==,!=,<=,>=,:=,Error Token ="
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_034():
    """Logical operators"""
    source = "&& || !"
    expected = "&&,||,!,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    """Concatenation operator"""
    source = '"Hello" ^ "World"'
    expected = "Hello,^,World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_036():
    """Separators"""
    source = "( ) [ ] { } , ; : ."
    expected = "(,),[,],{,},,,;,:,.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_037():
    """Line comment mid-code"""
    source = "int x; # this is comment"
    expected = "int,x,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    """Block comment between code"""
    source = "int /* comment */ y;"
    expected = "int,y,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    """Nested-like block comment (should close at first */)"""
    source = "/* outer /* inner */ still comment */"
    expected = "still,comment,*,/,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_040():
    """Unterminated block comment"""
    source = "/* never closed"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_041():
    """Error character $"""
    source = "int $var"
    expected = "int,Error Token $"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_042():
    """Unicode character error"""
    source = "int π = 3;"
    expected = "int,Error Token π"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_043():
    """Nil literal"""
    source = "nil"
    expected = "nil,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_044():
    """Boolean literals with capitalized variants (should be identifiers)"""
    source = "True False"
    expected = "True,False,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_045():
    """Identifier same as keyword but with suffix"""
    source = "returnX staticVar"
    expected = "returnX,staticVar,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_046():
    """Large integer literal"""
    source = "999999999999999999999"
    expected = "999999999999999999999,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_047():
    """Float with leading zeros"""
    source = "00012.34"
    expected = "00012.34,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_048():
    """Identifier with only underscores"""
    source = "___"
    expected = "___,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_049():
    """Two string literals concatenated by whitespace (not operator)"""
    source = '"abc" "def"'
    expected = "abc,def,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_050():
    """String literal with escaped backslash"""
    source = '"C:\\\\path"'
    expected = "C:\\\\path,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_051():
    """Empty program"""
    source = ""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_052():
    """Mixed tokens: assignment"""
    source = "int x := 10;"
    expected = "int,x,:=,10,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_053():
    """Mixed tokens: method call"""
    source = "obj.method(42)"
    expected = "obj,.,method,(,42,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_054():
    """Static method invocation"""
    source = "Math.add(1,2)"
    expected = "Math,.,add,(,1,,,2,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_055():
    """Array declaration"""
    source = "int[5] arr;"
    expected = "int,[,5,],arr,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_056():
    """Array access"""
    source = "arr[10]"
    expected = "arr,[,10,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_057():
    """Ternary-like? (should tokenize separately)"""
    source = "a ? b : c"
    expected = "a,Error Token ?"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_058():
    """Keyword sequence"""
    source = "if then else for do break continue return"
    expected = "if,then,else,for,do,break,continue,return,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_059():
    """String with many escapes"""
    source = '"Line1\\nLine2\\tTabbed\\\\"'
    expected = "Line1\\nLine2\\tTabbed\\\\,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_060():
    """Illegal string with backspace escape"""
    source = '"Hello\\bWorld"'
    expected = "Hello\\bWorld,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_061():
    """Floating-point with capital E exponent"""
    source = "6.02E23"
    expected = "6.02E23,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_062():
    """Zero float"""
    source = "0.0"
    expected = "0.0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_063():
    """Zero exponent float"""
    source = "1e0"
    expected = "1e0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_064():
    """Chained operators"""
    source = "a+++b"
    expected = "a,+,+,+,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_065():
    """Concatenation of identifiers and numbers"""
    source = "x1y2z3"
    expected = "x1y2z3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_066():
    """Illegal escape with unicode"""
    source = '"\\u1234"'
    expected = "Illegal Escape In String: \\u"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_067():
    """Multiple lines code"""
    source = """class A {
        int x;
        void foo() {}
    }"""
    expected = "class,A,{,int,x,;,void,foo,(,),{,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_068():
    """String with colon and semicolon"""
    source = '"a:b;c"'
    expected = "a:b;c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_069():
    """Assignment operator vs colon"""
    source = "a := b : c"
    expected = "a,:=,b,:,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_070():
    """Multiple identifiers with digits"""
    source = "a1 b2 c3d4"
    expected = "a1,b2,c3d4,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_071():
    """Decimal int and float"""
    source = "123 123.456"
    expected = "123,123.456,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_072():
    """Invalid number with letters"""
    source = "12abc"
    expected = "12,abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_073():
    """Unclosed string empty"""
    source = '"'
    expected = "Unclosed String: "
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_074():
    """String with only escaped quote"""
    source = '"\\""'
    expected = "\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_075():
    """Multiline comment with keywords inside"""
    source = "/* class int float string */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_076():
    """Identifier chain with dot"""
    source = "io.writeStrLn"
    expected = "io,.,writeStrLn,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_077():
    """String with escaped single quote (treated as normal char)"""
    source = '"hahhaIt\\\'"'
    expected = "Illegal Escape In String: hahhaIt\\\'"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_078():
    """Empty array brackets"""
    source = "[]"
    expected = "[,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_079():
    """Comment at end without newline"""
    source = "int x; # comment"
    expected = "int,x,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_080():
    """Random illegal character ~"""
    source = "~"
    expected = "~,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_081():
    """Identifier with mixed case"""
    source = "CamelCaseVar"
    expected = "CamelCaseVar,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_082():
    """Number starting with dot"""
    source = ".5"
    expected = ".,5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_083():
    """Number ending with e"""
    source = "3.5e"
    expected = "3.5,e,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_084():
    """Identifier starting with underscore"""
    source = "_hidden"
    expected = "_hidden,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_085():
    """Multiple block comments"""
    source = "/*one*/ /*two*/ int"
    expected = "int,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_086():
    """Block comment with operator inside"""
    source = "/* a + b */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_087():
    """Keyword used as identifier part"""
    source = "intValue floatNumber"
    expected = "intValue,floatNumber,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_088():
    """Escape sequence at end of string"""
    source = '"abc\\'
    expected = "Unclosed String: abc"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_089():
    """Multiple escaped quotes"""
    source = '"\\"a\\"b\\""'
    expected = "\\\"a\\\"b\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_090():
    """Hex-like number (invalid)"""
    source = "0x123"
    expected = "0,x123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_091():
    """Octal-like number (just int)"""
    source = "0777"
    expected = "0777,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_092():
    """Expression with modulus and int division"""
    source = "a % b \\ c"
    expected = "a,%,b,\\,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_093():
    """Expression with float division"""
    source = "a / b"
    expected = "a,/,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_094():
    """Expression with logical not"""
    source = "!true"
    expected = "!,true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_095():
    """Two keywords stuck together"""
    source = "forwhile"
    expected = "forwhile,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_096():
    """Chained string literals with ^"""
    source = '"a"^"b"^"c"'
    expected = "a,^,b,^,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_097():
    """Block comment containing star-slash sequence inside string"""
    source = '/* \"*/\" */ int'
    expected = "Unclosed String:  */ int"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_098():
    """Nested blocks in code"""
    source = "class A { { { } } }"
    expected = "class,A,{,{,{,},},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_099():
    """Identifier starting with digit error"""
    source = "123abc"
    expected = "123,abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_0100():
    """String with escaped single quote (treated as normal char)"""
    source = '"hahhaIt \\a a"'
    expected = "Illegal Escape In String: hahhaIt \\a"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_0101():
    """String with escaped single quote (treated as normal char)"""
    source = '"🤦🤦漢"'
    expected = "Unclosed String: "
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_0102():
    """String with escaped single quote (treated as normal char)"""
    source = "🤦🤦漢"
    expected = "Error Token 🤦"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_0103():
    """String with escaped single quote (treated as normal char)"""
    source = """\""""
    expected = "Unclosed String: "
    assert Tokenizer(source).get_tokens_as_string() == expected