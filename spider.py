import arch
from ui import SpiderUI

def run():
    spider = arch.Spider("https://www.loopnet.com", "Deland, FL", True)
    spider.run()


ui = SpiderUI("Spider v1.0")