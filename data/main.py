# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bf
import re
import json
import time
import base64
import sys

def postProcessingContent(text):
	pattern1 = re.compile(r"\[[0-9]+\]")

	text = text.strip().lower()
	text = pattern1.sub("", text)

	text.split(" ")

	return text

def make_uchr(code: str):
	return chr(int(code.lstrip("U+").zfill(8), 16))

def getData(pattern):
	r = requests.get("https://en.wikipedia.org/wiki/Braille_pattern_dots-"+pattern)
	html = bf(r.text, 'html.parser')

	output = {
		"dotPattern": pattern,
		"meanings": {},
	}

	# Meanings
	try:
		table = html.findAll("table")[3]
		for element in table.findAll("tr"):
			header = element.th.text.strip().lower()
			meaning = postProcessingContent(element.td.text)

			output["meanings"][header] = meaning
	except:
		print("Meaning not found")

	# Encodings
	try:
		table2 = html.findAll("table")[2]
		encodings = table2.findAll("tr")[3]
		output["unicode"] = make_uchr(encodings.findAll("td")[2].text.strip())
	except:
		print("Encodings not found")

	# Image
	try:
		imageUrl = table2.findAll("tr")[0].findAll("th")[1].img["src"]
		imageUrl = "https:"+imageUrl # Add protocol to url
		imageUrl = imageUrl.replace("40px", "200px")
		output["imageUrl"] = imageUrl
	except:
		print("Image not found")

	# Base64 of image
	try:
		output["imageBase64"] = base64.b64encode(requests.get(imageUrl).content).decode("UTF-8")
	except:
		print("Base64 couldn't be calculated")

	return output

def writeData(data):
	with open("data.json", "w") as file:
		file.write(json.dumps(data, indent=4, sort_keys=True))

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\n' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


if __name__ == '__main__':
	DEBUG = False
	data = []
	start = 0 if not DEBUG else 2**6-2
	try:
		for i in range(start, 2**6):
			radix = 6
			numbers = [a+1 for a in range(radix)]
			pattern = "".join([str(a) for a in numbers if bin(i)[2:].zfill(radix)[a-1] == "1"]) if not i == 0 else "0"

			progress(i,2**6-1, "Fetching dot pattern "+pattern)
			time.sleep(1)
			
			data.append(getData(pattern))
	except KeyboardInterrupt:
		pass
	finally:
		data = sorted(data, key=lambda x: int(x["dotPattern"]))
		print("Data sorted")
		writeData(data)
		print("Data written to data.json")
		print("Done")