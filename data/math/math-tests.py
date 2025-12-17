# Auto-generated from HumanEval (faithful reconstruction)
import math
import unittest


# ===== HumanEval/39 (prime_fib) =====


def prime_fib(n):
    import math

    def is_prime(p):
        if p < 2:
            return False
        for k in range(2, min(int(math.sqrt(p)) + 1, p - 1)):
            if p % k == 0:
                return False
        return True

    f = [0, 1]
    while True:
        f.append(f[-1] + f[-2])
        if is_prime(f[-1]):
            n -= 1
        if n == 0:
            return f[-1]


class TestPrime_fib(unittest.TestCase):
    """Tests for prime_fib"""

    def test_case_1(self):
        self.assertEqual(prime_fib(1), 2)

    def test_case_2(self):
        self.assertEqual(prime_fib(2), 3)

    def test_case_3(self):
        self.assertEqual(prime_fib(3), 5)

    def test_case_4(self):
        self.assertEqual(prime_fib(4), 13)

    def test_case_5(self):
        self.assertEqual(prime_fib(5), 89)

    def test_case_6(self):
        self.assertEqual(prime_fib(6), 233)

    def test_case_7(self):
        self.assertEqual(prime_fib(7), 1597)

    def test_case_8(self):
        self.assertEqual(prime_fib(8), 28657)

    def test_case_9(self):
        self.assertEqual(prime_fib(9), 514229)

    def test_case_10(self):
        self.assertEqual(prime_fib(10), 433494437)


# ===== HumanEval/49 (modp) =====


def modp(n, p):
    ret = 1
    for i in range(n):
        ret = (2 * ret) % p
    return ret


class TestModp(unittest.TestCase):
    """Tests for modp"""

    def test_case_1(self):
        self.assertEqual(modp(3, 5), 3)

    def test_case_2(self):
        self.assertEqual(modp(1101, 101), 2)

    def test_case_3(self):
        self.assertEqual(modp(0, 101), 1)

    def test_case_4(self):
        self.assertEqual(modp(3, 11), 8)

    def test_case_5(self):
        self.assertEqual(modp(100, 101), 1)

    def test_case_6(self):
        self.assertEqual(modp(30, 5), 4)

    def test_case_7(self):
        self.assertEqual(modp(31, 5), 3)


# ===== HumanEval/59 (largest_prime_factor) =====


def largest_prime_factor(n):
    def is_prime(k):
        if k < 2:
            return False
        for i in range(2, k - 1):
            if k % i == 0:
                return False
        return True

    largest = 1
    for j in range(2, n + 1):
        if n % j == 0 and is_prime(j):
            largest = max(largest, j)
    return largest


class TestLargest_prime_factor(unittest.TestCase):
    """Tests for largest_prime_factor"""

    def test_case_1(self):
        self.assertEqual(largest_prime_factor(15), 5)

    def test_case_2(self):
        self.assertEqual(largest_prime_factor(27), 3)

    def test_case_3(self):
        self.assertEqual(largest_prime_factor(63), 7)

    def test_case_4(self):
        self.assertEqual(largest_prime_factor(330), 11)

    def test_case_5(self):
        self.assertEqual(largest_prime_factor(13195), 29)


# ===== HumanEval/60 (sum_to_n) =====


def sum_to_n(n):
    return sum(range(n + 1))


class TestSum_to_n(unittest.TestCase):
    """Tests for sum_to_n"""

    def test_case_1(self):
        self.assertEqual(sum_to_n(1), 1)

    def test_case_2(self):
        self.assertEqual(sum_to_n(6), 21)

    def test_case_3(self):
        self.assertEqual(sum_to_n(11), 66)

    def test_case_4(self):
        self.assertEqual(sum_to_n(30), 465)

    def test_case_5(self):
        self.assertEqual(sum_to_n(100), 5050)


# ===== HumanEval/75 (is_multiply_prime) =====


def is_multiply_prime(a):
    def is_prime(n):
        for j in range(2, n):
            if n % j == 0:
                return False
        return True

    for i in range(2, 101):
        if not is_prime(i):
            continue
        for j in range(2, 101):
            if not is_prime(j):
                continue
            for k in range(2, 101):
                if not is_prime(k):
                    continue
                if i * j * k == a:
                    return True
    return False


class TestIs_multiply_prime(unittest.TestCase):
    """Tests for is_multiply_prime"""

    def test_case_1(self):
        self.assertEqual(is_multiply_prime(5), False)

    def test_case_2(self):
        self.assertEqual(is_multiply_prime(30), True)

    def test_case_3(self):
        self.assertEqual(is_multiply_prime(8), True)

    def test_case_4(self):
        self.assertEqual(is_multiply_prime(10), False)

    def test_case_5(self):
        self.assertEqual(is_multiply_prime(125), True)

    def test_case_6(self):
        self.assertEqual(is_multiply_prime(3 * 5 * 7), True)

    def test_case_7(self):
        self.assertEqual(is_multiply_prime(3 * 6 * 7), False)

    def test_case_8(self):
        self.assertEqual(is_multiply_prime(9 * 9 * 9), False)

    def test_case_9(self):
        self.assertEqual(is_multiply_prime(11 * 9 * 9), False)

    def test_case_10(self):
        self.assertEqual(is_multiply_prime(11 * 13 * 7), True)


if __name__ == "__main__":
    unittest.main()
