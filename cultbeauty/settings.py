# Scrapy settings for cultbeauty project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "cultbeauty"

SPIDER_MODULES = ["cultbeauty.spiders"]
NEWSPIDER_MODULE = "cultbeauty.spiders"


CULTBEAUTY_URL = "https://www.cultbeauty.co.uk"
CULTBEAUTY_PRODUCTS_URL = CULTBEAUTY_URL + "/elysium.search?search="

CATEGORY_SELECTOR = (
    "aside.responsiveProductListPage_facets div.responsiveF"
    "acets_content div.responsiveFacets_sectionContainer"
)

CATEGORY_NAME_SELECTOR = (
    "div.responsiveFacets_sectionHeadWrapper "
    "h3.responsiveFacets_sectionTitle::text"
)

SUBCATEGORY_SELECTOR  = (
    "div.responsiveFacets_sectionContentWrapper "
    "span.responsiveFacets_sectionItem"
)

PRODUCTS_LAST_PAGE_SELECTOR = (
    '#mainContent  div.responsiveProductListPage_topPagination'
    'li a.responsivePaginationButton--last::attr(data-page-number)'
)

PRODUCT_OPTIONS_SELECTOR = (
    "#mainContent div.athenaProductVariations"
    " div[data-product-variation]"
)

PRODUCT_SIZE_SELECTOR = (
    "#mainContent div.athenaProductPage_productVariations "
    "button.athenaProductVariations_box[data-selected]::text"
)

PRODUCT_VARIATION_TYPE_SELECTOR = (
    "*[data-product-variation-type]::"
    "attr(data-product-variation-type)"
)

PRODUCT_VARIATION_OPTION_SELECTOR = ".athenaProductVariations_dropdown option"

PRODUCT_PRICE_SELECTOR = (
    "#mainContent div.athenaProductPage_productPrice"
    " p[data-product-price='price']::text"
)

PRODUCT_RRP_SELECTOR = (
    "#mainContent div.athenaProductPage_product"
    "Details p.productPrice_rrp::text"
)

PRODUCT_REVIEWS_SELECTOR = (
    "#athenaProductReviewsComponent div.athenaProductReviews"
    "_summary_reviewContainer div.athenaProductReviews_topReviewSingle"
)

PRODUCT_REVIEW_TEXT_SELECTOR = (
    "p.athenaProductReviews_topReviewsExcerpt::text"
)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "cultbeauty (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "cultbeauty.middlewares.CultbeautySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "cultbeauty.middlewares.CultbeautyDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "cultbeauty.pipelines.CultbeautyPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
