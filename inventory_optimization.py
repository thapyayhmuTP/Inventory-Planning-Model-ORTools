#Group 4 - Team members: 
#Lhagii Tsogtbayar (NF1012437) 
#Tha Pyay Hmu (NF1017569) 
#Mihir Bhadreshkumar Parikh (NF1011072) 

#(a) Developing the Python model for the given optimization problem.

# The symbolic model for this assignment, as provided in the brief, represents a dynamic lot sizing problem.
# It includes an objective function to minimize total costs and constraints to ensure inventory balance,
#supplier ordering logic, storage capacity limits, and non-negativity.

# Since symbolic models are abstract and do not contain specific values, they are not directly runnable.
# Therefore, we proceed to implement this model using actual numerical data in Part (b), where we solve it using Google OR-Tools.

#(b) Solving an instance with five products, three time periods, and three suppliers using the given data.
from ortools.linear_solver import pywraplp
import pandas as pd

# Indices
I = 5  # Products
J = 3  # Suppliers
T = 3  # Time Periods

# Initial inventory for each product at the start of period 1 (t = 0)
I0 = [0, 0, 0, 0, 0]

# Demand [product][period]
d = [
    [57, 72, 92],
    [90, 73, 89],
    [58, 95, 95],
    [92, 97, 53],
    [54, 88, 87]
]

# Purchase cost [product][supplier]
c = [
    [209, 997, 578],
    [719, 362, 133],
    [503, 582, 750],
    [857, 731, 589],
    [530, 930, 467]
]

# Holding cost per product
h = [15.0, 10.0, 15.0, 18.0, 16.0]

# Ordering cost per supplier
f = [5895, 1856, 4106]

# Storage space available per period
Wt = [3500, 4200, 6000]

# Storage space required per unit of product
s = [10, 15, 20, 25, 30]

M = 10000  # Big M

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x = [[[solver.NumVar(0, solver.infinity(), f'x[{i}][{j}][{t}]')
       for t in range(T)] for j in range(J)] for i in range(I)]
y = [[solver.IntVar(0, 1, f'y[{j}][{t}]') for t in range(T)] for j in range(J)]
Ivar = [[solver.NumVar(0, solver.infinity(), f'I[{i}][{t}]') for t in range(T)] for i in range(I)]

# Objective function
ordering_cost = solver.Sum(f[j] * y[j][t] for j in range(J) for t in range(T))
purchasing_cost = solver.Sum(c[i][j] * x[i][j][t] for i in range(I) for j in range(J) for t in range(T))
holding_cost = solver.Sum(h[i] * Ivar[i][t] for i in range(I) for t in range(T))
solver.Minimize(ordering_cost + purchasing_cost + holding_cost)

# Constraints 

# 1. Inventory balance
for i in range(I):
    for t in range(T):
        total_order = solver.Sum(x[i][j][t] for j in range(J))
        if t == 0:
            solver.Add(Ivar[i][t] == I0[i] + total_order - d[i][t])
        else:
            solver.Add(Ivar[i][t] == Ivar[i][t-1] + total_order - d[i][t])

# 2. x[i][j][t] only allowed if y[j][t] == 1
for i in range(I):
    for j in range(J):
        for t in range(T):
            solver.Add(x[i][j][t] <= M * y[j][t])

# 3. Storage constraint 
for t in range(T):
    solver.Add(solver.Sum(s[i] * Ivar[i][t] for i in range(I)) <= Wt[t]) 
#Based on the inventory balance equation, I_it represents ending inventory after demand is met, so only this is used in the storage constraint.

# 4. Binary constraint for y[j][t] (already enforced by IntVar(0, 1), but stated here for completeness)
for j in range(J):
    for t in range(T):
        solver.Add(y[j][t] >= 0)
        solver.Add(y[j][t] <= 1)

# 5. Non-negativity for x and I (already enforced by NumVar(0, ∞), but stated explicitly)
for i in range(I):
    for j in range(J):
        for t in range(T):
            solver.Add(x[i][j][t] >= 0)
    for t in range(T):
        solver.Add(Ivar[i][t] >= 0)

#Solver
status = solver.Solve()

# Output results
if status == pywraplp.Solver.OPTIMAL:
    print(f"\n Total Cost: {solver.Objective().Value():,.2f}")
    print(f"  • Ordering Cost: {ordering_cost.solution_value():,.2f}")
    print(f"  • Purchasing Cost: {purchasing_cost.solution_value():,.2f}")
    print(f"  • Holding Cost: {holding_cost.solution_value():,.2f}\n")

    for t in range(T):
        print(f"--- Period {t+1} ---")
        for j in range(J):
            if y[j][t].solution_value() > 0:
                print(f"Supplier {j+1} placed an order.")
        for i in range(I):
            for j in range(J):
                qty = x[i][j][t].solution_value()
                if qty > 0:
                    print(f"Product {i+1} ordered {qty:.0f} units from Supplier {j+1}")
            inv_val = Ivar[i][t].solution_value()
            print(f"End Inventory for Product {i+1}: {round(inv_val, 2) if abs(inv_val) > 1e-3 else 0.00}")
        print()
else:
    print(" No optimal solution found.")

# Summary of total units per product/supplier (
print("\n--- Summary of total units per product/supplier ---")
for i in range(I):
    total_units = sum(x[i][j][t].solution_value() for j in range(J) for t in range(T))
    print(f"Total units ordered for Product {i+1}: {total_units:.0f}")

#(c) Presenting the Results

#The results are clearly printed in an interpretable format using Python, showing order quantities, inventory levels, & cost breakdowns.
#A detailed interpretation of these results is provided in the accompanying report.