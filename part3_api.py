from datetime import datetime

# FORMATTER FUNCTIONS

def divider(char="=", width=65):
    return char * width

def centre(text, width=65, char=" "):
    return text.center(width, char)

def format_value(val):
    """Nicely format ints, floats, booleans, lists, and strings."""
    if isinstance(val, bool):
        return "Yes" if val else "No"
    if isinstance(val, float):
        if val >= 1_000:
            return f"${val:,.2f}"
        return f"{val:.2f}"
    if isinstance(val, int):
        if val >= 1_000:
            return f"{val:,}"
        return str(val)
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    return str(val)

def print_report(title: str, sections: dict, width: int = 65):
    """
    Render a multi-section report from a nested dictionary.

    sections = {
        "Section Name": {
            "Field Label": value,
            ...
        },
        ...
    }
    """
    pad = 2
    label_width = 30

    print()
    print(divider("=", width))
    print(centre(f"  {title.upper()}  ", width, " "))
    generated = datetime.now().strftime("%d %b %Y  %H:%M")
    print(centre(f"Generated: {generated}", width))
    print(divider("=", width))

    for section_name, fields in sections.items():
        print()
        print(f"  ▌ {section_name.upper()}")
        print(divider("-", width))

        if isinstance(fields, dict):
            for label, value in fields.items():
                formatted = format_value(value)
                dots = "." * max(2, label_width - len(label))
                print(f"  {label}{dots} {formatted}")

        elif isinstance(fields, list):
            # List of dicts → mini table
            if fields and isinstance(fields[0], dict):
                headers = list(fields[0].keys())
                col_widths = [max(len(h), max(len(format_value(row.get(h, "")))
                                             for row in fields)) + 2
                              for h in headers]
                header_row = "  " + "  ".join(
                    h.ljust(col_widths[i]) for i, h in enumerate(headers))
                print(header_row)
                print("  " + "-" * (sum(col_widths) + len(headers) * 2))
                for row in fields:
                    data_row = "  " + "  ".join(
                        format_value(row.get(h, "")).ljust(col_widths[i])
                        for i, h in enumerate(headers))
                    print(data_row)
            else:
                for item in fields:
                    print(f"    • {item}")

        else:
            print(f"  {fields}")

    print()
    print(divider("=", width))
    print()

# SAMPLE DATA — built from demand_forecasting.csv summary 

#  Report 1: Overall Business Summary
business_summary = {
    "Dataset Overview": {
        "Source file"        : "demand_forecasting_2.csv",
        "Total records"      : 76000,
        "Date range"         : "01 Jan 2022 – 30 Jan 2024",
        "Stores"             : 5,
        "Unique products"    : 20,
        "Categories"         : 5,
    },
    "Sales Performance": {
        "Total units sold"   : 7928320,
        "Total revenue ($)"  : 532961600.0,
        "Avg unit price ($)" : 67.73,
        "Avg demand / row"   : 104.32,
        "Max demand recorded": 430,
    },
    "Promotion Impact": {
        "Avg demand – no promo"    : 95.0,
        "Avg demand – with promo"  : 123.3,
        "Promotion uplift"         : "+29.8%",
        "Rows with promotion active": "~30%",
    },
    "Data Quality Flags": {
        "Rows with zero units ordered" : "62.0%",
        "Rows: price below competitor" : "49.8%",
        "Missing values in dataset"    : "None",
        "Negative demand rows"         : 0,
    },
}

#  Report 2: Category Breakdown
category_breakdown = {
    "Revenue by Category": [
        {"Category": "Electronics", "Revenue ($)": "$115M+",  "Avg Price ($)": "88.50", "Promo %": "30%"},
        {"Category": "Clothing",    "Revenue ($)": "$108M+",  "Avg Price ($)": "67.20", "Promo %": "31%"},
        {"Category": "Groceries",   "Revenue ($)": "$105M+",  "Avg Price ($)": "61.40", "Promo %": "29%"},
        {"Category": "Furniture",   "Revenue ($)": "$102M+",  "Avg Price ($)": "110.30","Promo %": "30%"},
        {"Category": "Toys",        "Revenue ($)": "$98M+",   "Avg Price ($)": "26.80", "Promo %": "30%"},
    ],
    "Key Takeaways": [
        "Electronics leads revenue despite mid-range transaction volume",
        "Toys has the lowest avg price but competes on volume",
        "Furniture has the highest avg unit price across all categories",
        "Promotion rates are evenly distributed (~30%) across categories",
    ],
}

#  Report 3: Regional & Seasonal Performance
regional_report = {
    "Demand by Region": [
        {"Region": "North", "Total Units": "2,012,480", "Rank": "1st"},
        {"Region": "South", "Total Units": "1,997,240", "Rank": "2nd"},
        {"Region": "East",  "Total Units": "1,979,600", "Rank": "3rd"},
        {"Region": "West",  "Total Units": "1,939,000", "Rank": "4th"},
    ],
    "Avg Demand by Season": {
        "Summer (highest)" : "108.2 units",
        "Spring"           : "105.1 units",
        "Fall"             : "103.8 units",
        "Winter (lowest)"  : "100.2 units",
    },
    "Recommendations": [
        "Increase North region stock levels ahead of each season",
        "Run promotions in Summer — demand is naturally highest",
        "Monitor West region for margin erosion vs competitors",
    ],
}

#  Report 4: Product-Level Spot Check
product_spot_check = {
    "Top 5 Products by Demand": [
        {"Product ID": "P0003", "Total Units": "425,600", "Avg Price ($)": "80.34", "Issues": "None"},
        {"Product ID": "P0014", "Total Units": "421,900", "Avg Price ($)": "80.13", "Issues": "None"},
        {"Product ID": "P0012", "Total Units": "418,200", "Avg Price ($)": "84.48", "Issues": "None"},
        {"Product ID": "P0002", "Total Units": "415,500", "Avg Price ($)": "67.10", "Issues": "None"},
        {"Product ID": "P0009", "Total Units": "412,000", "Avg Price ($)": "70.95", "Issues": "Missing cat"},
    ],
    "Quality Issues Found": {
        "Missing descriptions" : 3,
        "Zero/negative prices" : 2,
        "Cost exceeds price"   : 10,
        "Missing categories"   : 2,
        "Duplicate SKU rows"   : 8,
    },
}

# PRINT ALL REPORTS

print_report("Business Performance Summary",   business_summary)
print_report("Category Performance Breakdown", category_breakdown)
print_report("Regional & Seasonal Report",     regional_report)
print_report("Product Spot Check",             product_spot_check)

print("  All 4 reports printed successfully.")
print()
