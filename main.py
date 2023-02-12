from flet import *

def main(page:Page):
	page.bgcolor="red"

	
	page.add(
	Column([
	Text("Success deploy to cloudflare",size=30,weight="bold")

		])

		)


flet.app(target=main)
