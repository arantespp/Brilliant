''' Problem can be found at:
    https://brilliant.org/problems/numbers-of-another-world/
'''

from itertools import permutations

class AlienLanguage(object):
    def __init__(self, equation):
        self.equation = equation
        mult, self.result = equation.replace(' ', '').split('=')
        self.value1, self.value2 = mult.split('x')
        self.chars = set(self.value1) | set(self.value2) | set(self.result)
        self.single_solution = {}
        for char in self.chars:
            self.single_solution.update({char: None})
        self.solutions = [self.single_solution]

        self.set_solutions()
        self.check_solutions()

    def message(self, msg):
        for solution in self.solutions:
            for key, value in solution.items():
                if value is not None:
                    msg = msg.replace(key, value)
            print(msg)

    def decode(self, solution):
        value1 = self.value1
        value2 = self.value2
        result = self.result
        for key, value in solution.items():
            if value is not None:
                value1 = value1.replace(key, value)
                value2 = value2.replace(key, value)
                result = result.replace(key, value)
        return value1, value2, result

    def check_solutions(self):
        tmp_solutions = []
        while self.solutions:
            sol = self.solutions.pop()
            value1, value2, result = self.decode(sol)
            if int(value1)*int(value2) == int(result):
                tmp_solutions.append(sol)
        self.solutions = tmp_solutions

    def set_solutions(self, order=None):
        if order is None:
            order = max(len(self.value1), len(self.value2))
        if order != 1:
            self.set_solutions(order-1)
        tmp_solutions = []
        while self.solutions:
            solutions = []
            char1, char2, charr = map(lambda expr: expr[-min(order, len(expr))],
                                      [self.value1, self.value2, self.result])
            sol = self.solutions.pop()
            for idx1, idx2, idxr in permutations('0123456789', 3):
                _sol = sol.copy()
                _sol[char1] = str(idx1) if not _sol[char1] else _sol[char1]
                _sol[char2] = str(idx2) if not _sol[char2] else _sol[char2]
                _sol[charr] = str(idxr) if not _sol[charr] else _sol[charr]
                value1, value2, result = self.decode(_sol)
                v1, v2, vr = map(lambda v: int(v[-min(order, len(v)):]), [value1, value2, result])
                if (v1*v2 - vr) % 10**order == 0:
                    values = [v for v in list(_sol.values()) if v]
                    if len(values) == len(set(values)):
                        solutions.append(_sol)
            tmp_solutions += [dict(t) for t in set([tuple(d.items()) for d in solutions])]
        self.solutions = [dict(t) for t in set([tuple(d.items()) for d in tmp_solutions])]

if __name__ == '__main__':
    al = AlienLanguage('JBEMRAxPTPMIR=IBSMTBRERMAS')
    al.message('EABMRPSTJIRB')
