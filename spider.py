import arch
import exceltool

websites = []


def run():
    spider = arch.Spider("https://www.loopnet.com", "Orlando, FL")
    spider.lookup_location_action()
    spider.store_current_listings()
    spider.scan_listings()

# spider_ui = sgui.SpiderUI("Spider UI v1.0")
