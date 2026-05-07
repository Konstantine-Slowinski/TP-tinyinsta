import csv
import os

def csv_to_markdown(filename, title):
    if not os.path.exists(filename):
        return f"\n### {title}\n*No data found yet.*\n"
    
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        return f"\n### {title}\n*Empty file.*\n"

    # Clean up the instance column if it contains raw gcloud output (multiple lines of IDs)
    header = rows[0]
    
    # Find the index of the column, ignoring case (handles 'NB instances' or 'Nb instances')
    inst_idx = -1
    for idx, col in enumerate(header):
        if col.lower() == "nb instances":
            inst_idx = idx
            break

    if inst_idx != -1:
        for i in range(1, len(rows)):
            val = rows[i][inst_idx].strip()
            if "id=" in val:
                # Count occurrences of 'id=' to get the clean number of instances
                count = val.count('id=')
                rows[i][inst_idx] = str(count)

    # Build Markdown Table
    md = f"\n### {title}\n\n"
    md += "| " + " | ".join(header) + " |\n"
    md += "| " + " | ".join(["---"] * len(header)) + " |\n"
    for row in rows[1:]:
        md += "| " + " | ".join(row) + " |\n"
    return md

if __name__ == "__main__":
    print("# Benchmark Results Report")
    print(csv_to_markdown('out/conc.csv', 'Task 1: Concurrency Benchmark'))
    print(csv_to_markdown('out/fanout.csv', 'Task 2: Fanout Benchmark'))
    print("\nCopy the output above into your README.md")