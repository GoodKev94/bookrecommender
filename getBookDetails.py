
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



class book():
	def __init__(self, isbn):
		self.isbn = isbn
		self.getgoodreadsURL()

	def getgoodreadsURL(self):
		chromeDriverPath = '/Users/kevinbichoupan/drivers/chromedriver'
		driver = webdriver.Chrome(chromeDriverPath)
		driver.get('https://www.goodreads.com/')
	
		driver.find_element_by_name("query").click()
		driver.find_element_by_name("query").clear()
		driver.find_element_by_name("query").send_keys(self.isbn)
		driver.find_element_by_name("query").send_keys(Keys.ENTER)
		self.goodreadsURL  = driver.current_url
		driver.quit()

		#htmlRaw = urlopen(isbnSearchUrl)
		#htmlSoup = soup(htmlRaw.read(),"html.parser")
		#htmlRaw.close()

		#print(htmlSoup)
	
	def getGoodreadsBookDetails(self):
		htmlRaw = urlopen(self.goodreadsURL)
		htmlSoup = soup(htmlRaw.read()."html.parser")
		htmlRaw.close()



if __name__ == "__main__":
	x = book('9780451191137')
	print(x.goodreadsURL)




