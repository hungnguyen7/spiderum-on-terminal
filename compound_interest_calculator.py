# pylint: skip-file

def compound_interest(P, r, n, t, additional_investment):
    # * Calculate the final amount with annual contributions
    A = P * (1 + r/n)**(n*t)
    for i in range(1, t+1):
        A += additional_investment * (1 + r/n)**(n*(t-i))
    return A

def format_currency(amount):
    return f"{amount:,.0f} VND"


if __name__ == "__main__":
    # * Given values
    P = 40_000_000      # * initial principal in VND
    r = 0.25        # * annual interest rate
    n = 1       # * number of times the interest is compounded per year
    additional_investment = 500_000_000     # * additional yearly investment
    years = [1, 2, 3, 5, 7, 10, 15, 20, 30]        # * number of years to calculate the final amount
    
    
    print(f"Initial principal: {format_currency(P)}")
    print(f"Annual interest rate: {r*100}%")
    print(f"Number of times interest is compounded per year: {n}")
    for t in years:
        A = compound_interest(P, r, n, t, additional_investment)
        print(f"Final amount after {t} years: {format_currency(A)}")
        print(f"Profit after {t} years: {format_currency(A - P - additional_investment*t)}")
        print("--------------------")