import sympy
import math

e = "e"

OPERATORS = {
    "+": 1,
    "*": 2,
    "/": 2,
    "^": 3,
    "ln": 4 
}

class Node:
    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.data = None
        self.isleave = False
    
    def __str__(self) -> str:
        left = str(self.left) if self.left else ""
        right = str(self.right) if self.right else ""
        return "(" + left + str(self.data) + right + ")"
    

class const(Node):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.data = value
        self.isleave = True

class var(Node):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.data = name
        self.isleave = True

class add(Node):
    def __init__(self, left, right) -> None:
        super().__init__()
        self.data = "+"
        self.left = left
        self.right = right


class mul(Node):
    def __init__(self, left, right) -> None:
        super().__init__()
        self.data = "*"
        self.left = left
        self.right = right

class pow(Node):
    def __init__(self, left, right) -> None:
        super().__init__()
        self.data = "^"
        self.left = left
        self.right = right

class func(Node):
    def __init__(self, name: str, arg) -> None:
        super().__init__()
        self.data = name
        self.left = arg
    
    def __str__(self) -> str:
        return self.data + "(" + str(self.left) + ")"

class Expr:

    def __init__(self, s: str) -> None:
        self.s = s.replace("-", "-1*")
        self.rpn = self.__toRPN()
    
    def __str__(self) -> str:
        return self.s
    
    def __splitEq(self, eq) -> list:

        elements = []
        stack = []

        for i in range(len(eq)): # iterate over Equation
            c = eq[i]
            if c in OPERATORS.keys() or c in "()": # check if current char is an operator

                if stack: # if stack is not empty append the current stack to elements
                    elements.append("".join(stack))
                    stack = []
                
                elements.append(c) # append operator to elements
            elif i+1 < len(eq) and c+eq[i+1] in OPERATORS.keys(): # check if current char and next char is a function
                if stack: # if stack is not empty append the current stack to elements
                    elements.append("".join(stack))
                    stack = []
                
                elements.append(c+eq[i+1]) # append function to elements
                i += 1
            else:
                stack.append(c) # append char (number) to stack
        
        if stack: # if stack is not empty append the remaining stack to elements
            elements.append("".join(stack))


        return elements
                

    def __toRPN(self) -> str:
        eq = self.__splitEq(self.s)
        stack = []  # stack for operators
        queue = []  # queue for output

        for token in eq:

            if token in OPERATORS.keys(): # if token is operator check for precedence and append to queue
                if stack:
                    if stack[-1] == "(":
                        pass
                    elif OPERATORS[token] <= OPERATORS[stack[-1]]:
                        queue.append(stack.pop())
                if token != "/": stack.append(token)
                else: stack.append("-1"); stack.append("^"); stack.append("*")
            
            elif token == "(":
                stack.append(token)
            
            elif token == ")": # if token is closing bracket append all operators to queue until opening bracket
                while stack:
                    if stack[-1] == "(":
                        stack.pop()
                        break
                    queue.append(stack.pop())
            
            else: # token has to be a number -> append to queue
                queue.append(token)
        
        while stack: # append remaining operators to queue
            queue.append(stack.pop())
        
        return queue

    def toTree(self) -> Node:
        stack = []
        for c in self.rpn:
            if c in OPERATORS.keys():
                if c == "+":
                    node = add(stack.pop(), stack.pop())
                elif c == "*":
                    node = mul(stack.pop(), stack.pop())
                elif c == "^":
                    node = pow(stack.pop(), stack.pop())
                else:
                    node = func(c, stack.pop())
                
                stack.append(node)
            else:
                if c.isalpha():
                    stack.append(var(c))
                else:
                    stack.append(const(float(c)))
        
        return stack.pop()

    def __diff(self, node: Node, var="x") -> Node:
        if node.isleave: # Basecase
            if node.data == var: # if node is variable return 1, else it is a constant, therefor return 0
                return const(1)
            else:
                return const(0)
            
        elif node.data == "+": # handle addition d(f+g) = df + dg
            return add(self.__diff(node.left, var), self.__diff(node.right, var))
        elif node.data == "*": # handle multiplication d(f*g) = f * dg + df * g
            return add(mul(self.__diff(node.left, var), node.right), mul(node.left, self.__diff(node.right, var)))
        elif node.data == "^": # handle power d(f^g) = d(e^(g*ln(f))) = e^(g*ln(f)) * d(g * ln(f)) = f^g * d(g * ln(f))
            return mul(pow(node.right, node.left), self.__diff(mul(node.left, func("ln", node.right)), var))
        elif node.data == "ln":
            return mul(pow(node.left, -1), self.__diff(node.left, var))

    def diff(self, var="x") -> str:
        root = self.toTree()
        root = self.__diff(root, var)
        return str(root)


if __name__ == "__main__":
    test = Expr("x^2")
    out = test.diff()
    print(out)
    print(sympy.simplify(out))

