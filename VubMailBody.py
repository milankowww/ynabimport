# -*- coding: utf-8 -*-
import re

class VubMailBody:
	def __init__(self):
		pass

	def parse(self, body):
		m = re.search(r'Vážený klient,\s+na účte (\S+) dňa (\d+)\.(\d+)\.(\d+) o (\d+:\d+) bola uskutočnená autorizácia \S+ kartou \S+ vo výške ([0-9 ,]+?)\s+EUR\.\s*^Miesto autorizácie:\s+(.*?)$.*Vaša VÚB banka', body, re.MULTILINE | re.DOTALL)
		if m1:

			self.m_my_account = m1.group(1)
			self.m_day = int(m1.group(2))
			self.m_month = int(m1.group(3))
			self.m_year = int(m1.group(4))
			self.m_date = "%04d-%02d-%02d" % ( self.m_year, self.m_month, self.m_day )
			self.m_time = m1.group(5)

			op = 'debetná'

			#XXX self.m_amount = float(m1.group(6).replace(' ', '').replace(',','.'))
		elif m2:


		if op == 'debetná':
			self.m_amount = -self.m_amount

		self.m_other_account = m.group(8)

		m1 = re.search(r'^Referencia platitela: (.*?)$', body, re.MULTILINE | re.DOTALL)
		if m1:
			self.m_ref = m1.group(1)
		else:
			self.m_ref = ''
		m2 = re.search(r'^Informacie pre prijemcu: (.*?)$', body, re.MULTILINE | re.DOTALL)
		if m2:
			self.m_info = m2.group(1)
		else:
			self.m_info = ''

		return True

