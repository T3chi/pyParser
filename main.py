# By Sohum Trivedi 
# program to compile a simple grammar to equivalent C++

# total: list to hold all significant tokens
total = [
        ';','=','+','-','*','/','%'
        'equals','for','while','and','or',
        'print','if','{','}','(',')','to',
        'loop','function','return',',','stop']

# ops: list to hold all mathematical operator tokens
ops = ['+','-','*','/','%','(',')']

# booleans: list to hold boolean operator tokens
booleans = ['&&','||','==','!']

# keywords: list to hold keyword operator tokens
keywords = ['for','while','and','or','print','if','equals','to','loop','iter']

# author note: lists will be replaced with tuples in final update

# keywordMapping: map to hold syntatical sugar conversions to C++ syntax
keywordMapping = {'equals':'==','and':'&&','or':'||','not':'!','loop':'for','to':'','mod':'%','stop':'break;'}

# tokens: list to hold all input file tokens
tokens = []

# var_stack: map to hold all variable values
var_stack = {}

# func_stack: map to hold all function definitions
func_stack = {}

# tok_index: records index of current token being processed
tok_index = 0

# current: holds current token being processed
current = ''

# code_buffer: holds generated C++ code
code_buffer = ''

# user_code: holds user-written C++ code
user_code = ''

# func_buffer: holds C++ function definitions
func_buffer = ''

# func_headers: holds C++ function headers
func_headers = ''

# debug: True if program is being debugged, used for strategic print statements
debug = True

# method that returns next string token to process
def getToken():
    if(debug):
      print("getToken()")
    global tok_index
    global tokens
    global current
    if(tok_index < len(tokens)):
        ret = tokens[tok_index]
        tok_index = tok_index + 1
        current = ret
        return ret
    else:
        current = "null"
        return "null"

# method that replaces a token back to the processing stream
def putBack():
  global tok_index
  global tokens
  global current
  if(tok_index > 0 and len(tokens) > 0):
        tok_index = tok_index - 1;
        current = tokens[tok_index]
        return tokens[tok_index]
  else:
        current = "null"
        return "null"

# method that removes user-defined C++ 'tags' from Code    
def removeC(string):
  try:
      while(True):
        f = string.index("<C++>")
        l = string.index("</C++>")
        string = string[0:f] + string[l+6:len(string)]
  except ValueError:
      return string

# method to add user-written C++ code to code buffer
def cTag(string):
  C = ''
  try:
    while(True):
      f = string.index("<C++>")
      l = string.index("</C++>")
      C += string[f+5:l]
      string = string.replace("<C++>",'',1)
      string = string.replace("</C++>",'',1)
  except ValueError:
    return C

# method to add needed C++ headers to generated code buffer    
def default_headers():
    print("#include <iostream>")
    print("#include <string>")
    print("using namespace std;")

# method that generates main method "driver" code
def printMain(code):
    print("int main()")
    print("{")
    print(code)
    print("}")

#prints final generated code buffer
def printCode():
    global func_buffer
    global code_buffer
    global user_code
    global func_headers
    default_headers()
    print(func_headers)
    print(func_buffer)
    print(user_code)
    printMain(code_buffer)

# quick method to check if a given string is a number
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# quick method to see if a given string is a syntactical string token
def isString(s):
    if(len(s) <= 1):
        return False
    if(s[0] == "\"" and s[len(s)-1]=="\""):
        return True
    else:
        return False

# method to remove unncessary white space from string buffer being parsed
def removeSpaces(string):
    string = string.strip()
    string = string.replace(" ","")
    return string

# method to remove comments from input code
def removeComments(s):
  try:
    while(True):
        f = s.index("/*")
        l = s.index("*/")
        s = s[0:f] + s[l+2:len(s)]
  except ValueError:
    return s

# method returns a list with only valid tokens
def removeEmptyTokens(toks):
  ret = list()
  for tok in toks:
    if(tok.isspace() or tok == ''):
      continue
    else:
      ret.append(tok)
  return ret

# method to replace my grammar's syntax with C++ syntax
def replaceKeywords(string):
  for mapping in keywordMapping:
    if(mapping in string):
      string = string.replace(mapping,keywordMapping[mapping])
  return string

# method formats spaces between operators
def addSpaces(string):
    for op in total:
        string = string.replace(op,' '+op+' ')
    return string

# method returns the input file's text as a string
def getFileText(file):
    with open(file, 'r') as myfile:
        data=myfile.read().replace('\n', '')
        return data

# method goes through steps from input to code generation with debug lines
def process(file):
    global user_code
    fileText = getFileText(file)
    print("File Input: \n" + fileText + "\n")
    fileText = removeComments(fileText)
    print("After comment removal: \n" + fileText + "\n")
    user_code += cTag(fileText)
    fileText = removeC(fileText)
    print("After C++ removal: \n" + fileText + "\n")
    abbreviated = removeSpaces(fileText)
    print("After space removal: \n" + abbreviated + "\n")
    tokenized = addSpaces(abbreviated)
    print("After space addition: \n" + tokenized + "\n")
    tokenized = replaceKeywords(tokenized)
    print("After keyword replacement: \n" + tokenized + "\n")
    print("Token List:")
    print(tokenized.split(" "))
    tokenized = tokenized.split(" ")
    tokenized = removeEmptyTokens(tokenized)
    print("Cleaned Token List:")
    print(tokenized)
    print()
    return tokenized

# method to parse an assignment expression
def checkAssignExpr(expr):
    global var_stack
    global func_stack
    i = 0
    while(i < len(expr)):
      tok = expr[i]
      # for tok in expr:
      if(tok in var_stack):
        i = i+1
        continue
      elif(isNumber(tok)):
        i = i+1
        continue
      elif(tok in ops):
        i = i+1
        continue
      elif(tok in func_stack):
        while(expr[i] != ')' and i < len(expr)):
          i = i+1
      elif(tok == "iter"):
        i = i+1
        continue
      else:
        print(tok+" is not valid for an assignment expression")
        return False
    return True

# quick method to check if a condition is likely to be valid (is not guarenteed)
def checkCondition(condition):
  for tok in condition:
        if(tok in var_stack):
            continue
        elif(isNumber(tok)):
            continue
        elif(tok in ops):
            continue
        elif(tok in booleans):
          continue
        else:
            print(tok+" is not valid for a condition expression")
            return False
  return True

# method returns a list of tokens stopping at the next semicolon
def getToSemi():
    expr = list()
    s = getToken()
    while(s != ";"):
        if(s == "null"):
            print("never received ;")
            return "null"
        if(s != ";"):
          if(debug):
            print("appending "+s)
          expr.append(s)
          s = getToken()
    return expr

# method returns a list of tokens to the next {
def getToBrace():
    expr = list()
    s = getToken()
    while(s != "{"):
        if(s == "null"):
            print("never received {")
            return "null"
        if(s != "{"):
          if(debug):
            print("appending "+s)
          expr.append(s)
        s = getToken()
    return expr

# method returns a list of tokens to the next )
def getToRParen():
    expr = list()
    s = getToken()
    while(s != ")"):
        if(s == "null"):
            print("never received )")
            return "null"
        if(s != ")"):
          if(debug):
            print("appending "+s)
          expr.append(s)
        s = getToken()
    return expr

# method generates code for a print statement
def iPrint(tok,special=False):
    global code_buffer
    if(isString(tok)):
        code_buffer +=  "\n cout << " + tok + "<< endl; \n"
    elif(isNumber(tok)):
        code_buffer += "\n cout <<"+tok+"<< endl; \n"
    elif(tok in var_stack):
        code_buffer += "\n cout << " + tok + " << endl; \n"
    elif(tok == "iter"):
      code_buffer+= "\n cout << iter << endl; \n"
    elif(special):
      code_buffer+= "\n cout << "+tok+" << endl; \n"
    else:
        print("iPrint failed to generate code")

# method generates code for an assignment statement
def iAssign(name,expr):
    global var_stack
    global code_buffer
    if(name in var_stack):
        code_buffer = code_buffer + "\n" + name + " = "
        for tok in expr:
            code_buffer = code_buffer + tok + " "
        code_buffer = code_buffer + "; \n"
    else:
        var_stack[name] = "valid"
        code_buffer = code_buffer + "\n double " + name + " = "
        for tok in expr:
            code_buffer = code_buffer + tok + " "
        code_buffer = code_buffer + "; \n"

# method generates code for an if statement
def iIf(condition):
  global code_buffer
  toks = str()
  for tok in condition:
    toks+=tok
  gen = "if("+toks+") \n{"
  code_buffer += gen

# method generates code for a for loop
def iFor(lower,upper):
  global code_buffer
  gen = "\nfor(int iter = "+ lower +"; iter < " + upper +"; iter++) \n"
  gen+="{\n"
  code_buffer += gen

# method generates a } to the code buffer to close a body of code (function, loop, etc)
def closeBody():
  global code_buffer
  code_buffer += "\n}"

# method to get a function's parameters
def getParams():
  Params = ''
  s = getToken()
  while(s != ")"):
    Params += s
    s = getToken()
  if(Params == ''):
    return []
  Params = Params.split(',')
  for param in Params:
    if(not param.isalpha()):
      print("Parameter: "+param+" is not valid")
      return 0
  return Params

# method to check a function's parameter's correctness (is not guarenteed to check all errors)
def checkParams(Params):
  for param in Params:
    if((not param in var_stack) or isNumber(param)):
      if(debug):
        print("Parameter: "+param+" is a valid variable or number")
      return False
  return True
  return Params

# method generates code for a function body
def iFunc(name,params,body):
  global func_headers
  global func_buffer
  global var_stack
  gen = 'double '+name+"("
  for i in range(0,len(params)):
    if(i==(len(params)-1)):
      gen+="double& "+params[i]
    else:
      gen+="double& "+params[i]+', '
  gen+=")"
  func_headers += gen+";\n"
  gen+="{\n"
  for word in body:
    gen+=word
  gen+="\n}\n"
  func_buffer+=gen
  func_stack[name] = "valid"

# method generates code for returning a value in a function
def iRet(vals):
    global code_buffer
    code_buffer += 'return '
    for val in vals:
      code_buffer += val
    code_buffer+=";"

# method generates code for generating a function call
def iFuncCall(name,params):
    global code_buffer
    gen = ' '+name+'('
    if(len(params)==1):
      gen+=params[0]+")"
    else:
      for i in range(0,len(params)):
        if(i==(len(params)-1)):
          gen+=params[i]+")"
        else:
          gen+=params[i]+','
    code_buffer+=gen

# method to recursively descend input code and generate C++ output as needed
def parse():
    global current
    global var_stack
    global func_buffer
    global code_buffer
    global func_stack
    
    s = getToken()
    
    if(debug):
      print("Parsing "+s)
    if(s == "null"):
        print("Finished Executing")
        return 0
    elif(s == ''):
      print("Skipping empty string in parse()")
      parse()
    elif(s == '}'):
      return "EndBody"
    elif(s == "print"):
        toPrint = getToken()
        if(toPrint.isalpha() or isString(toPrint) or isNumber(toPrint)):
            semi = getToken()
            if(semi == ";"):
                if(debug):
                  print("toPrint:" + toPrint)
                iPrint(toPrint)
                return parse()
            elif(toPrint in func_stack and semi == "("):
                args = ''
                for arg in getToSemi():
                  args+=arg
                func = toPrint+'('+args
                iPrint(func,True)
                parse()
            else:
              print("Expected ; got " + current)
            return 0
        print("Expected letter-only string got " + current)
        return 0
    elif(s == "if"):
      condition = getToBrace()
      iIf(condition)
      parse()
      closeBody()
      parse()
    elif(s == "for"):
      lower = getToken()
      upper = getToken()
      brace = getToken()
      if(not isNumber(lower)):
        print("Lower loop bound: " + lower + " must be number")
        return 0
      elif(not isNumber(upper)):
        print("Upper loop bound: " + upper +" must be number")
        return 0
      elif(brace != "{"):
        print("Expected { not: " + brace + " ")
        return 0
      else:
        iFor(lower,upper)
        parse()
        closeBody()
        parse()
    elif(s=="function"):
      name = getToken()
      lparen = getToken()
      params = getParams()
      temp_params=[]
      for param in params:
        if param not in var_stack:
          temp_params.append(param)
          var_stack[param] = "valid"
      lbrace = getToken()
      temp_code_buffer = code_buffer
      code_buffer = ''
      parse()
      body = code_buffer
      code_buffer = temp_code_buffer
      iFunc(name,params,body)
      for param in temp_params:
        del var_stack[param]
      parse()
      #prototype
    elif(s=="return"):
      val = getToSemi()
      iRet(val)
      parse()
    elif(s.isalpha() and s not in keywords):
            eq = getToken()
            if(eq == "="):
                expr = getToSemi()
                if(not checkAssignExpr(expr)):
                    print("Invalid Assignment expression ")
                    return 0
                else:
                    iAssign(s,expr)
                    parse()
            if(eq == '('):
              if s in func_stack:
                params = getToRParen()
                if(checkParams(params)):
                  iFuncCall(s,params)
                  parse()
              else:
                print("Function: "+s+" not previously defined")
                
    else:
        print("Error, unrecognized token: "+s)
        return 0

tokens = process("test.txt")
parse()
printCode()



