
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('mailstrom.db')
c = conn.cursor()

# Define rules
ten_years_ago = (datetime.now() - timedelta(days=10*365)).isoformat()
junk_senders = {'noreply@', 'promotion@', 'deals@', 'bauer@em.eddiebauer.com', '@palmettostatearmory.com'}

try:  # Load junk senders txt file the output of mailstrom_offender_analysis
    with open('junk_senders.txt', 'r') as f:
        junk_senders.update(line.strip() for line in f)
    print("Loaded junk senders from 'junk_senders.txt'")
    #fail gracefully
except FileNotFoundError:
    print("Warning: 'junk_senders.txt' not found, using default junk senders list")


junk_keywords = ['unsubscribe', 'sale', 'win', 'free', 'score' , 'discount', '!!!', '$', '% OFF', '% Off' , \
                 'Save', 'SAVE', 'clearance', 'Newsletter', 'newsletter', 'seriouspete3', 'announced']

# Delete: Junk senders
placeholders = ' OR '.join(['sender LIKE ?'] * len(junk_senders))
c.execute(f"UPDATE emails SET status = 'delete' WHERE {placeholders}", tuple(junk_senders))

# Delete: Junk keywords or old
keyword_conditions = ' OR '.join([f"subject LIKE '%{kw}%'" for kw in junk_keywords])
c.execute(f"UPDATE emails SET status = 'delete' WHERE {keyword_conditions} OR date < ?", (ten_years_ago,))

# Flag: Potential keepers
c.execute("UPDATE emails SET status = 'flag' WHERE sender LIKE '%@gmail.com' OR sender LIKE '%@outlook.com'")

# Archive: The rest
c.execute("UPDATE emails SET status = 'archive' WHERE status = 'pending'")

# Summary
c.execute("SELECT status, COUNT(*) FROM emails GROUP BY status")
print("Categorization:", c.fetchall())

conn.commit()
conn.close()