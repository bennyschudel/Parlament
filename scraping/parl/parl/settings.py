# Scrapy settings for parl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'parl'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['parl.spiders']
NEWSPIDER_MODULE = 'parl.spiders'
DEFAULT_ITEM_CLASS = 'parl.items.Subject'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

