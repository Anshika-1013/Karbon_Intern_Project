import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field


def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.
    """
    financials = data.get("financials", [])
    if financial_index < len(financials):
        # Get the P&L (Profit and Loss) data from financials at the given index
        pnl = financials[financial_index].get("pnl", {})
        # Retrieve the revenue from lineItems under pnl
        revenue = pnl.get("lineItems", {}).get("netRevenue", 0.0)
        return revenue
    return 0.0


def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data.
    """
    financials = data.get("financials", [])
    if financial_index < len(financials):
        # Get balance sheet (bs) data from financials at the given index
        bs = financials[financial_index].get("bs", {})
        # Sum long-term and short-term borrowings
        total_borrowings = bs.get("lineItems", {}).get("longTermBorrowings", 0.0) + \
                           bs.get("lineItems", {}).get("shortTermBorrowings", 0.0)
        # Get the total revenue by calling the total_revenue function
        revenue = total_revenue(data, financial_index)
        if revenue > 0:
            return total_borrowings / revenue
    return 0.0


def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.
    """
    financials = data.get("financials", [])
    if financial_index < len(financials):
        # Get P&L (Profit and Loss) data from financials at the given index
        pnl = financials[financial_index].get("pnl", {})
        # Calculate ISCR: (Profit before interest, tax, and depreciation + 1) / (Interest expenses + 1)
        profit_before_interest_and_tax = pnl.get("lineItems", {}).get("profitBeforeInterestAndTax", 0.0)
        depreciation = pnl.get("lineItems", {}).get("depreciation", 0.0)
        interest_expenses = pnl.get("lineItems", {}).get("interestExpenses", 0.0)
        iscr_value = (profit_before_interest_and_tax + depreciation + 1) / (interest_expenses + 1)
        return iscr_value
    return 0.0


def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ISCR value.
    """
    iscr_value = iscr(data, financial_index)
    if iscr_value >= 2:
        return FLAGS.GREEN
    else:
        return FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.
    """
    revenue = total_revenue(data, financial_index)
    if revenue >= 50_000_000:
        return FLAGS.GREEN
    else:
        return FLAGS.RED


def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.
    """
    borrowing_ratio = total_borrowing(data, financial_index)
    if borrowing_ratio <= 0.25:
        return FLAGS.GREEN
    else:
        return FLAGS.AMBER