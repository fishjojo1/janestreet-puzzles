# let V(b,s) be the expected value function for the state S(b,s)
# for each state S(b,s) the optimal ball and wait frequencies are given by
# f = p(4 - V(b,s+1)) / (V(b+1,s) - V(b,s+1) + p(4 - V(b,s+1)))
# V(4,s) = 0 for all s <3
# V(b,3) = 1 for all b <4
# when p occurs homerun is hit and the game is stopped

# V(b,s) = xy * V(b+1,s) + x(1-y) * V(b,s+1) + (1-x)y * V(b,s+1) + 4p * (1-x)(1-y) + (1-x)(1-y)(1-p) * V(b,s+1)

# let Q(b,s) be the probability 

# returns the value function for state S(b,s)
V_cache = {}
def V(b,s,p):
    if b == 4:
        return 1
    if s == 3:
        return 0
    key = (b, s)
    if key in V_cache:
        return V_cache[key]
    else:
        x_val = x(b, s, p)
        y_val = y(b, s, p)
        result = (
            x_val * y_val * V(b+1,s,p) + 
            x_val * (1 - y_val) * V(b,s+1,p) + 
            (1 - x_val) * y_val * V(b,s+1,p) + 
            4 * p * (1 - x_val) * (1 - y_val) + 
            (1 - x_val) * (1 - y_val) * (1 - p) * V(b,s+1,p)
        )
        V_cache[key] = result
        return result

# returns the optimal frequency for throwing a ball
def x(b,s,p):
    return (p * (4 - V(b,s+1,p))) / (V(b+1,s,p) - V(b,s+1,p) + p * (4 - V(b,s+1,p)))

# returns the optimal frequency for waiting
def y(b,s,p):
    return (p * (4 - V(b,s+1,p))) / (V(b+1,s,p) - V(b,s+1,p) + p * (4 - V(b,s+1,p)))


Q_cache = {}
# returns the probability of reaching state S(b,s)
def Q(b,s,p):
    # print((b,s,p))
    if b == 0 and s == 0:
        return 1
    
    if b < 0 or s < 0:
        return 0
    
    key = (b,s)
    if key in Q_cache:
        return Q_cache[key]
    
    else:
        res = (
            x(b-1,s,p) * y(b-1,s,p) * Q(b-1,s,p) +
            x(b,s-1,p) * (1 - y(b,s-1,p)) * Q(b,s-1,p) +
            (1 - x(b,s-1,p)) * y(b,s-1,p) * Q(b,s-1,p) +
            (1 - x(b,s-1,p)) * (1 - y(b,s-1,p)) * (1 - p) * Q(b,s-1,p)
        )

        Q_cache[key] = res
        return res

# import matplotlib.pyplot as plt
# x_vals = []
# y_vals = []
# for i in range(1,101):
#     V_cache = {}
#     Q_cache = {}
#     x_vals.append(i/100)
#     y_vals.append(Q(3,2,i/100))

# plt.plot(x_vals, y_vals)
# plt.show()

from scipy.optimize import minimize_scalar
def compute_q(p):
    V_cache.clear()
    Q_cache.clear()
    return -Q(3,2,p)
res = minimize_scalar(
    lambda p: compute_q(p),
    bounds=(0,1),
    method='bounded',
    options= {
        'disp': True
    }
)

# print("Optimal p:", f"{res.x:.10f}", "Resultant Q = ", f"{Q(3,2,res.x):.10f}") # 0.2269743428955392

# best_q = 0.2959679933
# a = 2269743429


