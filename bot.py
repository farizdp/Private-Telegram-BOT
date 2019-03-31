import telepot
import datetime
import time, os, sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from telepot.loop import MessageLoop

def handle(msg) :
	content_type, chat_type, chat_id = telepot.glance(msg)
	if (chat_id == id_telegram) :
		if (content_type == 'text' and '.cin' in msg['text'].lower()) :
			presensi('in', link_hris, id_telegram)

		if (content_type == 'text' and '.cout' in msg['text'].lower()) :
			presensi('out', link_hris, id_telegram)

		if (content_type == 'text' and '.slip' in msg['text'].lower()) :
			capture(link_hris, link_epayslip, id_telegram)

		if (content_type == 'text' and '.hist' in msg['text'].lower()) :
			capture(link_hris, link_history, id_telegram)

		if (content_type == 'text' and '.help' in msg['text'].lower()) :
			text = "Command : \n*.cin* : Clock In\n*.cout* : Clock Out\n*.slip* : Payment Slip\n*.hist* : History Presensi"
			bot.sendMessage(chat_id, text, 'Markdown')
	else :
		bot.sendMessage(chat_id, "Anda tidak punya akses!")

def presensi(tipe, link_hris, id_telegram) :
	driver = webdriver.Chrome()
	driver.set_page_load_timeout(60)
	try :
		driver.get(link_hris)
		driver.get("***Link HRIS Clock***" + tipe + "&captcha=1&captchaInput=1")
		element = driver.find_element_by_id('captcha')
		captcha = element.get_attribute('value')
		inputElement = driver.find_element_by_id("captchaInput")
		inputElement.send_keys(captcha)
		try :
			telat = Select(driver.find_element_by_id('reasonLate'))
			selected_option = telat.select_by_index(1)
		except :
			bot.sendMessage(id_telegram, 'Semangat pagi!', 'Markdown')
		inputElement.send_keys(Keys.ENTER)
		try :
			jsalert = driver.switch_to.alert
			jsalert.accept()
		except :
			bot.sendMessage(id_telegram, 'Semangat pagi!', 'Markdown')
		text = 'Clock' + tipe + ' *' + datetime.datetime.now().strftime("%a, %b %d") + '* is successful!'
		driver.quit()
		bot.sendMessage(id_telegram, text, 'Markdown')
	except TimeoutException:
		driver.quit()
		bot.sendMessage(id_telegram, 'Timeout!', 'Markdown')

def capture(link_hris, link_capture, id_telegram) :
	driver = webdriver.Chrome()
	driver.set_page_load_timeout(60)
	try :
		driver.get(link_hris)
		driver.get(link_capture)
		driver.save_screenshot('capture.png')
		driver.quit()
		pic = open('capture.png', 'rb')
		bot.sendPhoto(id_telegram, pic)
		pic.close()
	except TimeoutException:
		driver.quit()
		bot.sendMessage(id_telegram, 'Timeout!', 'Markdown')
	
link_hris = "***Link HRIS Pribadi***"
link_history = "***Link HRIS History Presensi***"
link_epayslip = "***Link HRIS Payment Slip***"

id_telegram = ***ID Telegram***
token = '***Token BOT Telegram***'

bot = telepot.Bot(token)
MessageLoop(bot, handle).run_as_thread()

while 1:
	time.sleep(10)
