from imap_tools import MailBox
import sqlite3
import logging
import time
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Argument parser
parser = argparse.ArgumentParser(description='Scan Yahoo mailbox and count emails by sender')
parser.add_argument('--email', required=True, help='Yahoo email address')
parser.add_argument('--password', required=True, help='Yahoo app password')
args = parser.parse_args()

conn = sqlite3.connect('mailstrom.db')
c = conn.cursor()

try:
    logging.info("Connecting to Yahoo IMAP...")
    mailbox = MailBox('imap.mail.yahoo.com')
    logging.info(f"Logging in as {args.email}")
    mailbox.login(args.email, args.password)
    mailbox.folder.set('Inbox')

    # Delete tagged emails
    c.execute("SELECT uid FROM emails WHERE status = 'delete' AND folder = 'Inbox'")
    uids_to_delete = [row[0] for row in c.fetchall()]
    if uids_to_delete:
        logging.info(f"Deleting {len(uids_to_delete)} emails from Inbox...")
        mailbox.delete(uids_to_delete)
        c.execute("DELETE FROM emails WHERE status = 'delete' AND folder = 'Inbox'")
        conn.commit()
        logging.info("Deleted from Inbox and database.")

    # Archive tagged emails in batches with read flag
    c.execute("SELECT uid FROM emails WHERE status = 'archive' AND folder = 'Inbox'")
    uids_to_archive = [row[0] for row in c.fetchall()]
    if uids_to_archive:
        batch_size = 1000
        for i in range(0, len(uids_to_archive), batch_size):
            batch_uids = uids_to_archive[i:i + batch_size]
            logging.info(f"Marking {len(batch_uids)} emails as read in Inbox (batch {i//batch_size + 1})...")
            mailbox.flag(batch_uids, 'Seen', True)
            logging.info(f"Archiving {len(batch_uids)} emails from Inbox to Archive (batch {i//batch_size + 1})...")
            mailbox.move(batch_uids, 'Archive')
            c.execute("UPDATE emails SET folder = 'Archive' WHERE uid IN ({})".format(','.join('?' * len(batch_uids))), batch_uids)
            conn.commit()
            logging.info(f"Batch {i//batch_size + 1} marked as read and moved to Archive.")
            time.sleep(1)

    # Summary
    c.execute("SELECT COUNT(*) FROM emails WHERE folder = 'Inbox'")
    remaining = c.fetchone()[0]
    print(f"Remaining in Inbox (DB): {remaining}")

except Exception as e:
    logging.error(f"Error: {str(e)}")
finally:
    mailbox.logout()
    conn.close()
    logging.info("Done.")