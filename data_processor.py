def process_data(raw_data):
    contribution_totals = {}
    for item in raw_data:
        contributor = item.get("contributor", "Unknown")
        amount = item.get("amount", 0)
        contribution_totals[contributor] = contribution_totals.get(contributor, 0) + amount
    return contribution_totals