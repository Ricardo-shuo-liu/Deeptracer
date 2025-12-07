def func1():
    a = [1, 2, 3]
    b = [4, 5, 6]
    return a + b


def func2():
    c = func1()
    d = [1, 1, 1]
    return c


if __name__ == '__main__':
    func2()  