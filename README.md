# Ynab Import

This is kludge that reads bank transactions from the IMAP account, and enters them into YNAB through the web interface. It requires Selenium and currently only is tested on Google Chrome.

This project includes:

1) a YnabControl class that uses Selenium to control YNAB through the web interface (currently only login and entering a new transaction is supported)

2) another class that parses e-mail notifications from Slovak bank "Tatra Banka"

3) a glue code that downloads the e-mails from IMAP account, parses the transactions and feeds them to YNAB. All messages are then moved to a separate IMAP folder.

The code is Alpha quality with "works for me" status. Improvements are welcome. In order to get it working you probably have to have an experience with Python development.

How to install:

1) install selenium
pip install -U selenium configparser

2) install google chrome driver: https://sites.google.com/a/chromium.org/chromedriver/

3) configure ynab-import.ini
