from dataclasses import dataclass
from typing import Dict, Tuple


STANDARD_DEDUCTION = 75000
CESS_RATE = 0.04
STCG_RATE = 0.2
LTCG_RATE = 0.125
LTCG_EXCEMPTION = 125000


def round_to_nearest_10(amount: float) -> int:
    whole_rupees = int(amount)
    return ((whole_rupees + 5) // 10) * 10


def slab_tax(taxable_income: int) -> int:
    slabs = [
        (400000, 0.00),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
        (float("inf"), 0.30),
    ]

    tax = 0.0
    lower = 0
    for upper, rate in slabs:
        amount_in_slab = max(0, min(taxable_income, upper) - lower)
        tax += amount_in_slab * rate
        if taxable_income <= upper:
            break
        lower = upper

    return int(round(tax))


@dataclass
class SalaryInputs:
    total_salary: float = 0
    other_dividend_income: float = 0
    other_interest_income: float = 0
    other_eligible_deductions: float = 0
    tds_already_deducted: float = 0
    short_term_capital_gains: float = 0
    long_term_capital_gains: float = 0


def calculate_tax(data: SalaryInputs) -> Dict[str, float]:
    
    total_income_from_salary = max(0, data.total_salary - STANDARD_DEDUCTION)
    total_income_before_rounding = max(0, total_income_from_salary + data.other_dividend_income + data.other_interest_income - data.other_eligible_deductions)
    total_income = round_to_nearest_10(total_income_before_rounding)

    tax_before_cess = slab_tax(total_income)
    stcg_tax = data.short_term_capital_gains * STCG_RATE
    ltcg_tax = max(0, data.long_term_capital_gains - LTCG_EXCEMPTION) * LTCG_RATE
    capital_gain_tax_before_cess = stcg_tax + ltcg_tax
    cess = int(round((tax_before_cess + capital_gain_tax_before_cess) * CESS_RATE))
    final_tax = tax_before_cess + capital_gain_tax_before_cess + cess

    balance = final_tax - int(max(0, data.tds_already_deducted))

    return {
        "total_income_before_rounding": total_income_before_rounding,
        "total_income": total_income,
        "tax_before_cess": tax_before_cess,
        "stcg_tax": stcg_tax,
        "ltcg_tax": ltcg_tax,
        "capital_gain_tax_before_cess": capital_gain_tax_before_cess,
        "cess": cess,
        "final_tax": final_tax,
        "balance": balance,
    }


def ask_amount(label: str, default: float = 0) -> float:
    raw = input(f"{label} [default {default:,.0f}]: ").strip().replace(",", "")
    if not raw:
        return default
    try:
        value = float(raw)
        if value < 0:
            raise ValueError
        return value
    except ValueError:
        print("Please enter a non-negative number.")
        return ask_amount(label, default)


def collect_inputs() -> SalaryInputs:
    print("\nEnter ANNUAL amounts in rupees. Press Enter for 0.")

    x = SalaryInputs()
    x.total_salary = ask_amount("Total income from salary")
    x.other_dividend_income = ask_amount("Income from dividend")
    x.other_interest_income = ask_amount("Income from interests")
    x.other_eligible_deductions = ask_amount("Eligible deductions (excl. 75k standard deduction)")
    x.tds_already_deducted = ask_amount("TDS already deducted during the year")
    x.short_term_capital_gains = ask_amount("Short-term Capital Gains")
    x.long_term_capital_gains = ask_amount("Long-term Capital Gains")
    return x


def print_report(r: Dict[str, float]) -> None:
    print("\n" + "=" * 62)
    print(f"INDIA INCOME TAX ESTIMATE")
    print("=" * 62)

    rows = [
        ("Total taxable income", r["total_income_before_rounding"]),
        ("Total taxable income (rounded)", r["total_income"]),
        ("Tax on income", r["tax_before_cess"]),
        (f"Tax on short term capital gains ({int(STCG_RATE*100)}%)", r["stcg_tax"]),
        (f"Tax on long term capital gains ({LTCG_RATE*100}%)", r["ltcg_tax"]),
        ("Total tax on capital gains", r["capital_gain_tax_before_cess"]),
        (f"Health & Education Cess ({int(CESS_RATE*100)}%)", r["cess"]),
        ("FINAL TAX", r["final_tax"]),
    ]

    for label, value in rows:
        print(f"{label:<48} {value:>12}")
    print("-" * 62)
    if r["balance"] > 0:
        print(f"{'BALANCE TAX PAYABLE':<48} {r['balance']:>12}")
    elif r["balance"] < 0:
        print(f"{'POTENTIAL REFUND':<48} {-r['balance']:>12}")
    else:
        print(f"{'NO BALANCE TAX / REFUND':<48} {0:>12}")



def print_monthly_deduction(r: float) -> None:
    print("=" * 62)
    total_income = round_to_nearest_10(r - STANDARD_DEDUCTION)    
    tax_before_cess = slab_tax(total_income)
    cess = int(round(tax_before_cess * CESS_RATE))
    final_tax = tax_before_cess + cess
    print("\nIndicative monthly tax deduction:", final_tax / 12)
    print("=" * 62)


def main() -> None:
    data = collect_inputs()
    result = calculate_tax(data)
    print_report(result)
    print_monthly_deduction(data.total_salary)


if __name__ == "__main__":
    main()
