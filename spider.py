import arch

# spider_ui = ui.SpiderUI("Spider UI")
def run():
    spider = arch.Spider("https://www.loopnet.com", "Deland, FL", True)
    spider.run()

run()