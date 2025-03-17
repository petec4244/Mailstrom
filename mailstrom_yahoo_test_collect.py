from imap_tools import MailBox, AND
import time
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Argument parser
parser = argparse.ArgumentParser(description='Scan Yahoo mailbox and count emails by sender')
parser.add_argument('--email', required=True, help='Yahoo email address')
parser.add_argument('--password', required=True, help='Yahoo app password')
args = parser.parse_args()

# Connect to Yahoo
try:
    logging.info("Connecting to Yahoo IMAP...")
    mailbox = MailBox('imap.mail.yahoo.com')
    logging.info(f"Logging in as {args.email}")
    mailbox.login(args.email, args.password)
    
    # Explicitly select INBOX
    logging.info("Selecting INBOX...")
    mailbox.folder.set('INBOX')

    # Fetch unread emails
    email_count = 0
    senders = {}
    logging.info("Fetching unread emails (limit 1000)...")
    for msg in mailbox.fetch(AND(seen=False), limit=1000):
        email_count += 1
        sender = msg.from_.lower()
        senders[sender] = senders.get(sender, 0) + 1
    
    print(f"Total emails scanned: {email_count}")
    print("Top senders:", sorted(senders.items(), key=lambda x: x[1], reverse=True)[:10])

except Exception as e:
    logging.error(f"Error: {str(e)}")
finally:
    mailbox.logout()
    logging.info("Logged out.")