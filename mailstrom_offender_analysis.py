import sqlite3
import os
from collections import Counter

# List database files
db_files = [f for f in os.listdir('.') if f.startswith('mailstrom') and (f.endswith('.db') or 'OLD' in f)]
print(f"Found databases: {db_files}")

# Aggregate sender counts
sender_counts = Counter()

for db_file in db_files:
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT sender, COUNT(*) FROM emails GROUP BY sender")
        rows = c.fetchall()
        for sender, count in rows:
            sender_counts[sender] = sender_counts.get(sender, 0) + count
        total_in_db = sum(count for _, count in rows)
        print(f"Processed {db_file}: {total_in_db} emails")
        conn.close()
    except sqlite3.Error as e:
        print(f"Error processing {db_file}: {e}")

# Total emails analyzed
total_emails = sum(sender_counts.values())
print(f"Total emails analyzed: {total_emails}")

# Top offenders
top_offenders = sender_counts.most_common(20)
print("\nTop repeat offenders:")
for sender, count in top_offenders:
    print(f"{sender}: {count} emails ({count/total_emails*100:.2f}%)")

# Save to file
with open('junk_senders.txt', 'w') as f:
    for sender, _ in top_offenders:
        f.write(f"{sender}\n")
print("Saved top offenders to 'junk_senders.txt'")