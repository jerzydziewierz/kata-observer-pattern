import cython


def fib(n: cython.int) -> cython.int:
    a: cython.int
    b: cython.int
    c: cython.int
    a, b = 0, 1
    c = 0
    while c < n:
        a, b = b, a + b
        c += 1
    return b


def example01():

    print('Hello, World!')
    print('This is an example of a Python function.')

    n: cython.int
    z: cython.int
    n = 1000000
    z = fib(n)
    q = z.to_bytes(400, byteorder='big')
    print(f'fib({n}) = {q}')


if __name__ == '__main__':
    example01()

