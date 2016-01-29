class Transaction(object):
	def __init__(self, settings):
		self.m_settings = settings

	def normalize(self):
		self.m_when = self.m_settings['date_format'] % { 'day':self.m_day, 'month':self.m_month, 'year':self.m_year }
		if self.m_my_account in self.m_settings['account_map']:
			self.m_ynab_account = self.m_settings['account_map'][self.m_my_account]
		else:
			self.m_ynab_account = None

	def dump(self):
		print self.m_when
		print self.m_ynab_account
		print self.m_amount
		print self.m_other_account
		print self.m_ref
		print self.m_info
