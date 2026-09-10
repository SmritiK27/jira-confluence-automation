# Calculate Compound Interest Instructions

Use the `compound_interest.py` tool when a user asks to calculate compound
interest from a principal, annual interest rate, compounding frequency, and
investment duration.

## Invocation

Run the script from the workspace root:

```bash
python3 tools/compound_interest.py <principal> <annual_rate> <compounds_per_year> <total_years>
```

Arguments must be supplied in this order:

- `principal`: Initial amount, as a non-negative number.
- `annual_rate`: Annual interest rate as a percentage. For example, use `7.34`
  for 7.34%, not `0.0734`.
- `compounds_per_year`: Positive integer, such as `12` for monthly
  compounding.
- `total_years`: Non-negative duration in years. Fractional years are allowed.

## Presenting results

Report both values from the command output:

- **Final amount**: The principal plus accumulated interest.
- **Interest earned**: The final amount minus the original principal.

Present monetary values to two decimal places with a currency symbol and
thousands separators. Include the input assumptions, especially the
compounding frequency and duration, so the result is unambiguous.
