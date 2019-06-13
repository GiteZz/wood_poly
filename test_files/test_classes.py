class A:
    def __init__(self, value):
        self.value = value

    def print_a(self):
        print(self.value)

class B(A):
    def __init__(self, obj):
        super().__
        pass


a_test = A(12)
B_class = B(a_test)
B_class.print_a()