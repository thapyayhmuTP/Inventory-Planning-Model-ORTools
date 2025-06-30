# Inventory-Planning-Model-ORTools
Optimization model for multi-product, multi-period inventory planning using Google OR-Tools and Python. Solves for cost-minimizing supplier and inventory decisions.


This project solves a dynamic lot sizing problem using Google OR-Tools. It models and optimizes multi-period ordering, supplier selection, and inventory decisions for multiple products under storage and cost constraints. The solution minimizes total cost while fulfilling demand across a 3-period planning horizon.

Developed for **DAMO 610: Operations Analytics** at the University of Niagara Falls.

---

## Problem Overview

We modeled a dynamic inventory planning problem involving:

- 5 Products  
- 3 Suppliers  
- 3 Time Periods  
- Constraints on demand fulfillment, storage, and supplier usage

The model determines:

- How much of each product to order
- From which supplier
- In which time period
- Inventory levels to hold

---

## Objective

**Minimize total cost**, including:

- Ordering costs (per supplier per period)
- Purchasing costs (per unit per product-supplier pair)
- Holding costs (per unit carried across periods)

---

## Python Implementation

The model is implemented in Python using Google OR-Tools with the following variables:

- `x[i][j][t]`: Quantity of product *i* ordered from supplier *j* at time *t*
- `y[j][t]`: Binary indicator if supplier *j* is used at time *t*
- `I[i][t]`: Ending inventory of product *i* at time *t*

### Key Constraints

- **Inventory Balance:** Ensures proper inventory flow across periods  
- **Big-M Linking:** Links ordering to supplier usage  
- **Storage Capacity:** Ensures inventory doesn’t exceed available space  
- **Non-negativity & Binary Constraints**

---

## Results

The model produced the following cost breakdown:

- **Total Cost:** $480,543  
  - Ordering Cost: $24,108  
  - Purchasing Cost: $453,930  
  - Holding Cost: $2,505

### Operational Insights

- Supplier 3 was the most cost-efficient and used in all periods
- Supplier 1 was used selectively based on product-specific advantages
- Inventory was minimized to avoid unnecessary holding costs

---

## Tools Used

- **Language:** Python 3
- **Solver:** Google OR-Tools (SCIP backend)
- **Libraries:** `ortools.linear_solver`, `pandas`, `numpy` (optional)

---

## Files Included

- `inventory_optimization.py`: Full Python code

---

## Author

Tha Pyay Hmu  
