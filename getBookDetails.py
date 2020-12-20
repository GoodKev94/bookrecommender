
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


options = Options()
options.add_argument('--headless')



class book():
	def __init__(self, isbn):
		self.isbn = isbn
		self.getGoodreadsURL()
		self.getGoodreadsBookDetails()
		self.getGoodreadsBooksByAuthorURL()

	def getGoodreadsURL(self):
		chromeDriverPath = '/Users/kevinbichoupan/drivers/chromedriver'
		driver = webdriver.Chrome(chromeDriverPath, options=options)
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

	def getGoodreadsBooksByAuthorURL(self):
		chromeDriverPath = '/Users/kevinbichoupan/drivers/chromedriver'
		driver = webdriver.Chrome(chromeDriverPath, options=options)
		driver.get('https://www.goodreads.com/')
	
		driver.find_element_by_name("query").click()
		driver.find_element_by_name("query").clear()
		driver.find_element_by_name("query").send_keys(self.author)
		driver.find_element_by_name("query").send_keys(Keys.ENTER)
	
		self.goodreadsBooksByAuthorURL  = driver.current_url + "&page=1"
	
		driver.quit()

	def getGoodreadsBooksByAuthor(self):
		htmlRaw = urlopen(self.goodreadsBooksByAuthorURL)
		htmlSoup = soup(htmlRaw.read(), "html.parser")
		htmlRaw.close()
		
		a = htmlSoup.find(style = 'float: right').text
		finalPos = a.find(' next')
		startPos = a[:finalPos].rfind(' ')
		maxPage = int(a[startPos+1:finalPos])
		
		booksByAuthor = []		

		for p in range(1,maxPage+1):
			newURL = self.goodreadsBooksByAuthorURL[0:-1] + str(p)
			htmlRaw = urlopen(newURL)
			htmlSoup = soup(htmlRaw.read(), "html.parser")
			htmlRaw.close()

			bookContainers = htmlSoup.findAll(itemtype = "http://schema.org/Book")

			for i in bookContainers:
				preRatingText = i.find(class_ = 'minirating')
				unwanted = preRatingText.find('span')
				unwanted.extract()			
				ratingText = preRatingText.text
			
				bookDetails = {
				'title' : i.find(itemprop = 'name').text,
				'average rating' : float(ratingText[1:5]),
				'no. ratings' : int(ratingText[ratingText.find(' — ')+3 : ratingText.rfind(' rating')].replace(',',''))
				}

				booksByAuthor.append(bookDetails)

		self.goodreadsBooksByAuthor = pd.DataFrame(booksByAuthor)


if __name__ == "__main__":
	x = book('9780451191137')
	x.getGoodreadsBooksByAuthor()
	print(x.goodreadsBooksByAuthor)


