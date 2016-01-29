import re
import Transaction

class TbMailBody(Transaction.Transaction):
	def __init__(self, settings):
		super(TbMailBody, self).__init__(settings)

	def parse(self, body):
		m = re.search(r'Vazeny klient,\s+(\d+)\.(\d+)\.(\d+)\s+(\d+:\d+) bol zostatok Vasho uctu (\S+) (zvyseny|znizeny) o ([0-9 ,]+?)\s+EUR\..*^Popis transakcie:\s+(.*?)$.*S pozdravom.*TATRA BANKA, a.s.', body, re.MULTILINE | re.DOTALL)
		if not m:
			return False

		self.m_day = int(m.group(1))
		self.m_month = int(m.group(2))
		self.m_year = int(m.group(3))
		self.m_time = m.group(4)
		self.m_my_account = m.group(5)

		op = m.group(6)

		self.m_amount = float(m.group(7).replace(' ', '').replace(',','.'))
		if op == 'znizeny':
			self.m_amount = -self.m_amount

		self.m_other_account = m.group(8)

		m1 = re.search(r'^Referencia platitela: (.*?)$', body, re.MULTILINE | re.DOTALL)
		if m1:
			self.m_ref = m1.group(1)
		else:
			self.m_ref = ''
		m2 = re.search(r'^Informacia pre prijemcu: (.*?)$', body, re.MULTILINE | re.DOTALL)
		if m2:
			self.m_info = m2.group(1)
		else:
			self.m_info = ''

		self.normalize()
		return True

#Vazeny klient,
#
#5.1.2016 7:50 bol zostatok Vasho uctu SK561100000000XXXXXXXXXX znizeny o 9 731,05 EUR.
#uctovny zostatok:                             XX XXX,XX EUR
#aktualny zostatok:                            XX XXX,XX EUR
#disponibilny zostatok:                        XX XXX,XX EUR
#
#Popis transakcie: CCINT XXXX/XXXXXX-XXXXXXXXXX
#Referencia platitela: /VSXXXXXXXXXX/SS/KS                
#Informacia pre prijemcu: XXXXXXXX
#
#S pozdravom
#
#TATRA BANKA, a.s.
#
#http://www.tatrabanka.sk
#
#Poznamka: Vase pripomienky alebo otazky tykajuce sa tejto spravy alebo inej nasej sluzby nam poslite, prosim, pouzitim kontaktneho formulara na nasej Web stranke.
#
#Odporucame Vam mazat si po precitani prichadzajuce bmail notifikacie. Historiu uctu najdete v ucelenom tvare v pohyboch cez internet banking a nemusite ju pracne skladat zo starych bmailov.
