import time
import arch
import sgui

websites = []


def run():
    spider = arch.Spider("https://www.loopnet.com", "Orlando, FL")
    spider.lookup_location_action()
    spider.store_current_listings()
    spider.scan_listings()


spider_ui = sgui.SpiderUI("Spider UI v1.0")
