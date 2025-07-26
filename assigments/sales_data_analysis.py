sales_data = [
    ("Q1", [("Jan", 1000), ("Feb", 1200), ("Mar", 1100)]),
    ("Q2", [("Apr", 1300), ("May", 1250), ("Jun", 1400)]),
    ("Q3", [("Jul", 1350), ("Aug", 1450), ("Sep", 1300)])
]

total_sales_per_quarter = []
for quarter, months in sales_data:
    total = sum(sales for month, sales in months)
    total_sales_per_quarter.append((quarter, total))
    print(f"{quarter}: {total}")

all_monthly_sales = []
for quarter, months in sales_data:
    for month, sales in months:
        all_monthly_sales.append((month, sales))

highest_month = max(all_monthly_sales, key=lambda x: x[1])
print(f"Highest sales month: {highest_month[0]} with {highest_month[1]} sales")

flat_monthly_sales = [(month, sales) for quarter, months in sales_data for month, sales in months]
print("Flat list of monthly sales:", flat_monthly_sales)

for quarter, months in sales_data:
    print(f"\n{quarter}:")
    for month, sales in months:
        print(f"  {month}: {sales}")
