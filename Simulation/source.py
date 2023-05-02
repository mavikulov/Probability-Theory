from collections import Counter
import random
import math


class Solution:
    def __init__(self, p, n):
        if any((0 > p > 1, type(n) is not int and n < 1)):
            raise ValueError("Invalid input data")
        self.p = p
        self.n = n
        self.sequence_length = [1] * self.n
        self.cnt = {}
        self.q = 1 - self.p

    def first_task(self):
        for i in range(self.n):
            rand_value = random.random()
            while rand_value > self.p:
                self.sequence_length[i] += 1
                rand_value = random.random()

        self.cnt = Counter(self.sequence_length)
        return sorted(self.cnt.most_common())

    def second_task(self):
        self.series = sorted(self.cnt.most_common())
        q = 1 - self.p
        E = 1 / self.p
        var = q / self.p**2
        sigma = math.sqrt(var)
        average = 0
        for x_i, n_i in self.series:
            average += x_i * n_i
        average /= self.n
        S_2 = 0
        for x_i, n_i in self.series:
            S_2 += (x_i - average)**2 * n_i
        S_2 /= self.n
        R = self.series[-1][0] - self.series[0][0]
        k = len(self.series) - 1
        Me = 0
        if len(self.series) % 2 == 0:
            Me = (self.series[k//2][0] + self.series[k//2 + 1][0]) / 2
        else:
            Me = self.series[k//2][0]
        return E, average, sigma, math.fabs(E - average), var, S_2, math.fabs(var - S_2), Me, R

    def generate_data_for_plot(self):
        q = 1 - self.p
        self.sums = [0] * len(self.series)
        self.sums[0] = self.p
        for i in range(1, len(self.series) - 1):
            self.sums[i] = self.sums[i - 1] + self.p * q**i
        self.sums[-1] = 1

        self.omegas = []
        for _, n_i in self.series:
            self.omegas.append(n_i / self.n)
        self.prefix_sums = [0] * len(self.series)
        self.prefix_sums[0] = self.omegas[0]
        for i in range(1, len(self.series)):
            self.prefix_sums[i] = self.prefix_sums[i - 1] + self.omegas[i]
        self.diff = 0
        for a, b in zip(self.prefix_sums, self.sums):
            if math.fabs(a - b) > self.diff:
                self.diff = math.fabs(a - b)


if __name__ == '__main__':
    p = float(input("p = "))
    n = int(input("n = "))
    solution = Solution(p, n)
    answer = solution.first_task()
    solution.second_task()
    solution.generate_data_for_plot()
