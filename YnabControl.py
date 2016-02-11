#! /usr/local/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class YnabControl:

	def __init__(self, login, password, budget):
		self.b = webdriver.Chrome()
		self.m_login = login
		self.m_password = password
		self.m_budget = budget

	def _check_exists_by_css_selector(self, selector):
		try:
			self.b.find_element_by_css_selector(selector)
		except NoSuchElementException:
			return False
		return True

	def _check_update(self):
		#self._check_exists_by_css_selector('.modal-actions button.')
		pass

	def login(self):
		self.b.get('https://app.youneedabudget.com')
		wait = WebDriverWait(self.b,30)
		wait.until(EC.presence_of_all_elements_located( (By.CSS_SELECTOR, 'input.login-password,input.login-username')) )
		time.sleep(1)	
		e_login = self.b.find_element_by_css_selector('input.login-username')
		e_password = self.b.find_element_by_css_selector('input.login-password')
		e_login.send_keys(self.m_login)
		e_password.send_keys(self.m_password)

		e_signin = wait.until(EC.element_to_be_clickable(  (By.XPATH, "//button[contains(.,'Sign In')]")  ))
		e_signin.click()

		e_budget = wait.until(EC.element_to_be_clickable(  (By.XPATH, "//button[contains(.,'"+self.m_budget.replace("'", "''")+"') and contains(@class,'select-budget')]")  ))
		e_budget.click()

		e_budget = wait.until(EC.presence_of_element_located( (By.CSS_SELECTOR, 'div.budget-header-totals-amount-label')  ))
		time.sleep(1)

	def open_account(self, account):
		wait = WebDriverWait(self.b,30)
		e = wait.until(EC.presence_of_element_located( (By.CSS_SELECTOR, 'div.nav-account-name[title="'+account.replace('"', '\\"')+'"] div.nav-account-name-val')  ))
		e.click()
		wait.until(EC.presence_of_element_located( (By.CSS_SELECTOR, 'div.accounts-header-total-inner-label[title="'+account.replace('"', '\\"')+'"]')  ))

	def open_budget(self):
		pass

	def add_transaction(self, date, memo, amount):
		wait = WebDriverWait(self.b,30)
		e = wait.until(EC.element_to_be_clickable(  (By.XPATH, "//button[contains(.,'Add a transaction') and contains(@class,'add-transaction')]")  ))
		e.click()

		e = wait.until(EC.element_to_be_clickable(  (By.CSS_SELECTOR, 'div.ynab-grid-cell-date input')  ))
		e.click()
		time.sleep(0.2)
		e.clear()
		time.sleep(0.2)
		e.send_keys(date)
		time.sleep(0.1)
		e.send_keys(Keys.RETURN)

		e = wait.until(EC.element_to_be_clickable(  (By.CSS_SELECTOR, 'div.ynab-grid-cell-memo input')  ))
		e.clear()
		e.send_keys(memo)

		if amount >= 0:
			e = wait.until(EC.element_to_be_clickable(  (By.CSS_SELECTOR, 'div.ynab-grid-cell-inflow input')  ))
		else:
			e = wait.until(EC.element_to_be_clickable(  (By.CSS_SELECTOR, 'div.ynab-grid-cell-outflow input')  ))
			amount = -amount
		e.clear()
		e.send_keys(str(amount))

		e = wait.until(EC.element_to_be_clickable(  (By.CSS_SELECTOR, 'div.ynab-grid-actions button.button-primary:not(.button-another)') ))
		e.click()
		wait.until(EC.invisibility_of_element_located(  (By.CSS_SELECTOR, 'div.ynab-grid-actions button.button-primary:not(.button-another)') ))

	def __del__(self):
		self.b.quit()
		pass

