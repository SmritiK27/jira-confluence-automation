"""Calculate compound interest from command-line inputs."""

import argparse


def calculate_compound_interest(
    principal: float, annual_rate: float, compounds_per_year: int, total_years: float
) -> tuple[float, float]:
    """Return the final amount and interest earned.

    ``annual_rate`` is expressed as a percentage, such as 7.34 for 7.34%.
    """
    amount = principal * (
        1 + (annual_rate / 100) / compounds_per_year
    ) ** (compounds_per_year * total_years)
    return amount, amount - principal


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate compound interest with periodic compounding."
    )
    parser.add_argument("principal", type=float, help="Initial principal amount")
    parser.add_argument(
        "annual_rate", type=float, help="Annual interest rate as a percentage"
    )
    parser.add_argument(
        "compounds_per_year",
        type=int,
        help="Number of compounding periods per year",
    )
    parser.add_argument("total_years", type=float, help="Investment duration in years")
    args = parser.parse_args()

    if args.principal < 0:
        parser.error("principal must be non-negative")
    if args.annual_rate < 0:
        parser.error("annual_rate must be non-negative")
    if args.compounds_per_year <= 0:
        parser.error("compounds_per_year must be greater than zero")
    if args.total_years < 0:
        parser.error("total_years must be non-negative")

    amount, interest = calculate_compound_interest(
        args.principal,
        args.annual_rate,
        args.compounds_per_year,
        args.total_years,
    )
    print(f"Final amount: ${amount:,.2f}")
    print(f"Interest earned: ${interest:,.2f}")


if __name__ == "__main__":
    main()
