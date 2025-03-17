### Categorize and delete old emails

import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('mailstrom.db')
c = conn.cursor()

# Define time thresholds
nine_months_ago = (datetime.now() - timedelta(days=9*30)).isoformat()  # ~270 days
eight_years_ago = (datetime.now() - timedelta(days=8*365)).isoformat()

# Define rules
junk_senders = {'noreply@', 'promotion@', 'deals@', 'bauer@em.eddiebauer.com', '@palmettostatearmory.com'}

try:  # Load junk senders txt file the output of mailstrom_offender_analysis
    with open('junk_senders.txt', 'r') as f:
        junk_senders.update(line.strip() for line in f)
    print("Loaded junk senders from 'junk_senders.txt'")
except FileNotFoundError:
    print("Warning: 'junk_senders.txt' not found, using default junk senders list")

junk_keywords = ['unsubscribe', 'sale', 'win', 'free', 'score' , 'discount', '!!!', '$', '% OFF', '% Off' , \
                 'Save', 'SAVE', 'clearance', 'Newsletter', 'newsletter', 'seriouspete3', 'announced', 'daily']

# Delete: Junk senders
placeholders = ' OR '.join(['sender LIKE ?'] * len(junk_senders))
c.execute(f"UPDATE emails SET status = 'delete' WHERE {placeholders}", tuple(junk_senders))

# Delete: Junk keywords or very old
keyword_conditions = ' OR '.join([f"subject LIKE '%{kw}%'" for kw in junk_keywords])
c.execute(f"UPDATE emails SET status = 'delete' WHERE {keyword_conditions} OR date < ?", (eight_years_ago,))

# Flag: Potential keepers
c.execute("UPDATE emails SET status = 'flag' WHERE sender LIKE '%@gmail.com' OR sender LIKE '%@outlook.com'")

# Delete: Older than 9 months (overrides archive)
c.execute("UPDATE emails SET status = 'delete' WHERE date < ? AND status != 'flag'", (nine_months_ago,))

# Archive: The rest (newer than 9 months, not flagged or deleted)
c.execute("UPDATE emails SET status = 'archive' WHERE status = 'pending'")

# Summary
c.execute("SELECT status, COUNT(*) FROM emails GROUP BY status")
print("Categorization:", c.fetchall())

conn.commit()
conn.close()