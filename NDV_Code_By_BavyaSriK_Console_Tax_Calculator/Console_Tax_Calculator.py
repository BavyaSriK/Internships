import math
print("---Console Based Tax Calculator---")
    
try:
    ctc=float(input("ENTER YOUR CTC:"))
    bonus=float(input("ENTER YOUR BONUS:"))
except ValueError:
    print("Invalid input. Please enter numerical values for CTC and Bonus. ")

total_income=ctc+bonus
print(f"\nTOTAL INCOME: RS.{total_income:,.0f}")

def calculate_old_regime_tax(total_income,standard_deduction,section_80c_deduction):
    """
    Calculates tax under the Old Regime for individuals below 60 years.
    Assumes standard deduction and 80C deduction are applied.
    """
    # Cap 80C deduction at the maximum allowed
    max_80c_deduction=150000
    actual_80c_deduction=min(section_80c_deduction, max_80c_deduction)

    # Total deductions for Old Regime
    total_deductions=standard_deduction+actual_80c_deduction
    
    # Ensure taxable income doesn't go below zero
    taxable_income=max(0,total_income-total_deductions)

    tax=0

    # Old Regime Slabs (FY 2024-25 / AY 2025-26)
    if taxable_income<=250000:
        tax=0
    elif taxable_income<=500000:
        tax=(taxable_income-250000)*0.05
    elif taxable_income<=1000000:
        tax=12500+(taxable_income-500000)*0.20
    else:
        tax=112500+(taxable_income-1000000)*0.30

    # Section 87A Rebate for Old Regime: Full tax rebate if taxable income is up to ₹5,00,000
    if taxable_income<=500000:
        tax=min(tax,12500) # Rebate is up to ₹12,500

    # Health and Education Cess (4%)
    tax_with_cess=tax*1.04
    return math.ceil(tax_with_cess) # Round up to the nearest rupee

def calculate_new_regime_tax(total_income,standard_deduction):
    """
    Calculates tax under the New Regime for individuals below 60 years.
    Assumes standard deduction is applied.
    """
    # Standard deduction is applicable in New Regime from FY 2023-24
    taxable_income=max(0,total_income-standard_deduction)

    tax=0

    # New Regime Slabs (FY 2024-25 / AY 2025-26)
    if taxable_income<=300000:
        tax=0
    elif taxable_income<=600000:
        tax=(taxable_income-300000)*0.05
    elif taxable_income<=900000:
        tax=15000+(taxable_income-600000)*0.10
    elif taxable_income<=1200000:
        tax=45000+(taxable_income-900000)*0.15
    elif taxable_income<=1500000:
        tax=90000+(taxable_income-1200000)*0.20
    else:
        tax=150000+(taxable_income-1500000)*0.30

    # Section 87A Rebate for New Regime: Full tax rebate if taxable income is up to ₹7,00,000
    if taxable_income<=700000:
        tax=0 # Full rebate makes tax zero

    # Health and Education Cess (4%)
    tax_with_cess=tax *1.04
    return math.ceil(tax_with_cess) # Round up to the nearest rupee

# Assumptions for Old Regime deductions
old_regime_std_deduction=50000
old_regime_80c_deduction=150000 # Assuming maximum 80C utilization

# Assumptions for New Regime deductions
standard_deduction=75000

tax_old_regime=calculate_old_regime_tax(total_income,old_regime_std_deduction,old_regime_80c_deduction)
tax_new_regime=calculate_new_regime_tax(total_income,standard_deduction) 
print(f"OLD REGIME TAX DEDUCTION: RS.{tax_old_regime:,.0f}")
print(f"NEW REGIME TAX DEDUCTION: RS.{tax_new_regime:,.0f}")

if tax_old_regime<tax_new_regime:
    saving=tax_new_regime-tax_old_regime
    print(f"\nYOU SAVE RS.{saving:,.0f} MORE USING THE OLD REGIME")
elif tax_new_regime<tax_old_regime:
    saving=tax_old_regime-tax_new_regime
    print(f"\nYOU SAVE RS.{saving:,.0f} MORE USING THE NEW REGIME")
else:
    print("\nTAX DEDUCTIONS ARE THE SAME FOR BOTH REGIMES.")

print("\nThankYou")
