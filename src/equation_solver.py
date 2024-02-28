from sympy.solvers import solve
from sympy import Symbol

bf = Symbol('bf')
p_bf = Symbol('p_bf')
b_bf = Symbol("b_bf")

bi = Symbol('bi')
p_bi = Symbol('p_bi')
b_bi = Symbol('b_bi')

r = Symbol('r')
b_r = Symbol('b_r')

p = Symbol('p')
p_p = Symbol('p_p')
b_p = Symbol('b_p')

w = Symbol('w')

system = [
    bf - (bi+w+r+p),
    p_bf * bf - (p_bi * bi + p_p * p),
    b_bf * bf - (b_bi * bi + b_p * p + b_r * r),
    bf * (1 - b_bf - p_bf) - (bi * (1 - b_bi - p_bi) + p * (1 - p_p - b_p) + r * (1 - b_r) + w)
]

solution = solve(system, [bi, r, p])

print(solution)
