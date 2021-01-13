import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    pass


class BinOp(Symbol):
    def __init__(self, left, right):
        if isinstance(left, Symbol):
            self.left = left
        elif type(left) is int or type(left) is float:
            self.left = Num(left)
        else:
            self.left = Var(left)

        if isinstance(right, Symbol):
            self.right = right
        elif type(right) is int or type(right) is float:
            self.right = Num(right)
        else:
            self.right = Var(right)

    def toString(self, operator):
        right = str(self.right)
        left = str(self.left)
        if (operator in ['*', '/']):
            if (isinstance(self.left, (Add, Sub))):
                 left = f"({left})"
            if (isinstance(self.right, (Add, Sub))):
                 right = f"({right})"

        if (operator == '-') and isinstance(self.right, (Add, Sub)):
            right = f"({right})"
        if (operator == '/') and isinstance(self.right, (Mul, Div)):
            right = f"({right})"
                
        return f"{left} {operator} {right}"

    def toRepr(self, operation):
        return f"{operation}({repr(self.left)}, {repr(self.right)})"


class Add(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = "+"
        self.operation = "Add"

    def __str__(self):
        return super().toString(self.operator)

    def __repr__(self):
        return super().toRepr(self.operation)


class Sub(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = "-"
        self.operation = "Sub"

    def __str__(self):
        return super().toString(self.operator)

    def __repr__(self):
        return super().toRepr(self.operation)


class Mul(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = "*"
        self.operation = "Mul"

    def __str__(self):
        return super().toString(self.operator)

    def __repr__(self):
        return super().toRepr(self.operation)


class Div(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = "/"
        self.operation = "Div"

    def __str__(self):
        return super().toString(self.operator)

    def __repr__(self):
        return super().toRepr(self.operation)


class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'


class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'


if __name__ == '__main__':
    doctest.testmod()
