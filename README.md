# Mailstrom
A swirling vortex of cluttered email recovery.


I have a yahoo email that is full of junk mail, over 124,000 unread emails, and a gmail account that has over 24,000. I finally have time (due to my recent layoff) to address this issue and this is the code that will do it. I will create a few scripts, for each mailbox. They will sort,delete,unsubscribe, catagorize etc...

requirements for Yahoo: python3 imap_tools


Steps for Yahoo:

Ok first you need to setup your yahoo mail to have an associated "App password" this is a randomly generated password and it differs from your regular password. 

Next run the "yahoo_test_collect_sort.py" this will fetch 1000 unread emails and sort them by sender occurance.
    If it works you should see who has the most emails of the first 1000

Then you can run the yahoo_collect_and_sort.py  - you can use the --folder argument to add additional folders beyond Inbox if desired. 

Yahoo Imap seems to timeout if you go beyond 1000 email fetches at a time and it seems to limit queries to 10,000 emails at a time. In otherwords if your inbox has 124,000 unread emails (like mine) it will only allow you to pull 10,000 (unread) at a time. I am unsure if you index beyond the 10k what happens, if anything.



