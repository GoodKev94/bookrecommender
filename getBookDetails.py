
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


options = Options()
options.add_argument('--headless')



class book():
	def __init__(self, isbn):
		self.isbn = isbn
		self.getgoodreadsURL()
		self.getGoodreadsBookDetails()
		self.getBooksByAuthor()

	def getgoodreadsURL(self):
		chromeDriverPath = '/Users/kevinbichoupan/drivers/chromedriver'
		driver = webdriver.Chrome(chromeDriverPath, chrome_options=options)
		driver.get('https://www.goodreads.com/')
	
		driver.find_element_by_name("query").click()
		driver.find_element_by_name("query").clear()
		driver.find_element_by_name("query").send_keys(self.isbn)
		driver.find_element_by_name("query").send_keys(Keys.ENTER)
		self.goodreadsURL  = driver.current_url
		driver.quit()

	def getGoodreadsBookDetails(self):
		htmlRaw = urlopen(self.goodreadsURL)
		htmlSoup = soup(htmlRaw.read(), "html.parser")
		htmlRaw.close()
		metaContainer = htmlSoup.find(id = 'metacol', class_= 'last col')
		
		self.title = metaContainer.find(id = 'bookTitle').text.replace('\n','').strip()
		self.author = metaContainer.find(class_='authorName').text
		self.description  = metaContainer.find(id = 'descriptionContainer').text

	def getBooksByAuthor(self):
		chromeDriverPath = '/Users/kevinbichoupan/drivers/chromedriver'
		driver = webdriver.Chrome(chromeDriverPath, chrome_options=options)
		driver.get('https://www.goodreads.com/')
	
		driver.find_element_by_name("query").click()
		driver.find_element_by_name("query").clear()
		driver.find_element_by_name("query").send_keys(self.author)
		driver.find_element_by_name("query").send_keys(Keys.ENTER)
		self.booksByAuthorURL  = driver.current_url
		driver.quit()

if __name__ == "__main__":
	x = book('9780451191137')
	print(x.booksByAuthorURL)



