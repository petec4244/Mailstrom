import sqlite3

conn = sqlite3.connect('mailstrom.db')
c = conn.cursor()
c.execute("SELECT folder, COUNT(*) FROM emails GROUP BY folder")
print("Emails per folder:", c.fetchall())
c.execute("SELECT COUNT(DISTINCT uid) FROM emails")
print("Unique emails:", c.fetchone()[0])
conn.close()