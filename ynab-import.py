#! /usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import configparser
import codecs
from TbMailBody import TbMailBody
from YnabControl import YnabControl

import imaplib
import email
import email.charset
import email.generator

def get_charset(message, default="ascii"):
	if message.get_content_charset():
		return message.get_content_charset()

	if message.get_charset():
		return message.get_charset()

	return default

def parse_email_parts(settings, part,lvl=0):
	#if lvl != 0:
	#	print "";
	#print "  "*lvl,"Content type: ",part.get_content_type()
	#print "  "*lvl,"Charset:      ",get_charset(part)
	#print "  "*lvl,"Disposition:  ",part.get('Content-Disposition')
	#print "  "*lvl,"Filename:     ", part.get_filename()

	# leaf node
	if not part.is_multipart():
		if part.get_content_type() == 'text/plain' and part.get('Content-Disposition') == None:
			charset = get_charset(part)
			payload = part.get_payload(decode=1)
			mb = parse_text_part(settings, payload.decode(charset))
			if mb != None:
				return mb
		return None

	# multipart node

	for subpart in part.get_payload():
		mb = parse_email_parts(settings, subpart, lvl+1)
		if mb != None:
			return mb

	return None


def parse_text_part(settings, body):

	# print body

	mb = TbMailBody(settings)
	if not mb.parse(body):
		return None
	if mb.m_ynab_account == None:
		return None
	mb.dump()
	return mb

def main():
	# parse options
	cp = configparser.RawConfigParser()
	cp.optionxform = str
	cp.readfp(codecs.open('ynab-import.ini', 'r', 'utf-8'))
	settings = dict(cp.items('ynab'))
	settings['account_map'] = dict(cp.items('accounts'))
	settings['imap'] = dict(cp.items('imap'))

	# connect to mail folder
	imap = imaplib.IMAP4(settings['imap']['host'])
	imap.login_cram_md5(str(settings['imap']['login']), str(settings['imap']['password']))
	imap.select(settings['imap']['mailbox'])

	typ, data = imap.search(None, 'ALL')
	imap_message_ids = data[0].split()

	if not imap_message_ids:
		imap.close()
		imap.logout()
		return 0

	# login to YNAB
	yc = YnabControl(settings['login'], settings['password'], settings['budget'])
	yc.login()

	#mb = parse_single_mail(settings, sys.stdin.read())

	# parse imap messages
	for num in imap_message_ids:
		typ, data = imap.fetch(num, '(RFC822)')

		for response_part in data:
			if isinstance(response_part, tuple):
				# print 'Message %s\n%s\n' % (num, data[0][1])
				msg = email.message_from_string(response_part[1])

				mb = parse_email_parts(settings, msg)

				if mb != None:
					# parse and upload the transaction
					yc.open_account(mb.m_ynab_account)
					yc.add_transaction(mb.m_when, mb.m_info+';'+mb.m_other_account+';'+mb.m_ref, mb.m_amount)

		# delete the message
		imap.copy(num, settings['imap']['seen_mailbox'])
		imap.store(num, '+FLAGS', '\\Deleted')

	imap.expunge()
	imap.close()
	imap.logout()

	return 0

if  __name__ =='__main__':
	sys.exit(main())

