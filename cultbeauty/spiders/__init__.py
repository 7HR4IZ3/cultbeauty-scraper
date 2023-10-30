import json
import scrapy
from scrapy.http import TextResponse
import cultbeauty.settings as settings

def strip_query(url):
    return url.split("?")[0]

class CultBeautySpider(scrapy.Spider):
    name = "cultbeauty"
    start_urls = [settings.CULTBEAUTY_PRODUCTS_URL]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_ids = list()

    def parse(self, response: TextResponse):
        allowed_categories_suffix = [
            'Category', 'Product Type', 'Products'
        ]

        # Get product from each category
        for category in response.css(settings.CATEGORY_SELECTOR):
            category_name = category.css(settings.CATEGORY_NAME_SELECTOR).get()

            should_continue = False
            for item in allowed_categories_suffix:
                if item in category_name:
                    should_continue = True
                    break

            if not should_continue:
                continue

            for sub_category in category.css(settings.SUBCATEGORY_SELECTOR):
                key = sub_category.attrib['data-facet-key'].strip()
                value = sub_category.attrib['data-facet-value'].strip()
                
                url = strip_query(
                    response.url
                ) + f"?facetFilters={key}:{value}"

                yield response.follow(
                    url, lambda response: self.parse_products(
                        response, self.cleanup_category(category_name), url
                    )
                )

    def parse_products(
        self, response: TextResponse,
        category: str, url: str = None
    ):
        for product in response.css("li.productListProducts_product")[:3]:
            product_link = product.css('.productBlock_link::attr(href)').get()
            yield response.follow(
                settings.CULTBEAUTY_URL + product_link,
                lambda response: self.parse_product(response, category)
            )

        # Handle navigation to other product paage using pagination
        # if 'url' is specified.
        # Url option is only passed from the 'parse' function
        # to prevent recursion error since 'parse_product' is used
        # to handle each product page.

        if url:
            last_index = response.css(
                settings.PRODUCTS_LAST_PAGE_SELECTOR
            ).get("1")

            for index in range(2, int(last_index) + 1):
                yield response.follow(
                    url + f"&pageNumber={index}",
                    lambda response: self.parse_products(
                        response, category
                    )
                )

    def parse_product(self, response: TextResponse, category: str):
        data = {}

        schema = response.css("#productSchema::text").get(default="{}")
        if schema:
            schema = json.loads(schema)
        else:
            schema = {}

        identifier = schema.get('@id')
        if identifier and identifier in self.product_ids:
            return
        else: 
            self.product_ids.append(identifier)

        offer = [
            item for item in schema.get('offers', [])
            if item.get('priceCurrency') == "GBP"
        ]
        if len(offer):
            offer = offer[0]
        else:
            offer = {}

        brand_name = schema.get('brand', {}).get('name')
        price = float(offer.get('price', 0))

        if "InStock" in offer.get('availability'):
            stock_status = "In Stock"
        else:
            stock_status = "Out Of Stock"

        data.update({
            'name': schema.get('name', ''),
            'price': price,
            'stock': stock_status,
            'brand': brand_name,
            'shipping_cost': 0 if price > 25 else 3.95,
            'identifier': int(identifier),
            'sku': schema.get('sku'),
            'image_url': schema.get('image'),
            'page_url': response.url,
            'category': category,
            
            # Metadata
            **self.extract_metadata(response, schema)
        })

        options = response.css(settings.PRODUCT_OPTIONS_SELECTOR)

        options_labels = options.css('::attr("aria-label")').getall()

        if len(options_labels):
            for orig_label in options_labels:
                label = orig_label.strip()
                if label in ("Size",):
                    data['product_size'] = response.css(
                        settings.PRODUCT_SIZE_SELECTOR
                    ).get("").strip()
                    continue

                variation = options.css(f'[aria-label="{orig_label}"]')
                variation_type = variation.css(
                    settings.PRODUCT_VARIATION_TYPE_SELECTOR
                ).get("")

                if variation_type == "radio":
                    continue
                elif variation_type == "dropdown":
                    options_nodes = variation.css(
                        settings.PRODUCT_VARIATION_OPTION_SELECTOR
                    )

                    sub_data = data.copy()

                    for (option_id, option) in zip(
                        options_nodes.css(
                            '*::attr(value)'
                        ).getall(),
                        options_nodes.css('*::text').getall()
                    ):
                        if option_id and option_id in self.product_ids:
                            continue
                        else: 
                            self.product_ids.append(option_id)

                        option = (
                            option.strip()
                                .strip(' - Out of stock')
                                .strip()
                        )

                        if 'please choose' in option.lower():
                            continue

                        name = data['name'] + f" - {option}"

                        sub_data.update({
                            'name': name,
                            'identifier': int(option_id),
                            'price': float(response.css(
                                settings.PRODUCT_PRICE_SELECTOR
                            ).get('£0').strip()[1:]),
                        })

                        if label in ("Shade", "Colour"):
                            sub_data['colour'] = option
                        elif label in ("Option",):
                            sub_data['product_size'] = option

                        yield sub_data

        yield data

    def extract_metadata(self, response: TextResponse, schema: dict):
        rrp = response.css(settings.PRODUCT_RRP_SELECTOR).get()

        if rrp:
            rrp = rrp.strip()

        data = {
            'description': schema.get('description'),
            'reviews': self.extract_reviews(response),
            'rrp': rrp,
            'color': None,
            'product_size': None,
            'promotional_text': None,
        }
        multiple_options = {
            'mpn': [
                'supplier_code', 'model_number',
                'part_number', 'partno', 'code',
                'manufacturer part number',
                'manufacturer number'
            ],
            'ean': ['upc', 'gtin', 'barcode'],
            'asin': [],
            'isbn': [],
            'sku': ['id', 'partno', 'code', 'supplier_code']
        }
        for key, keys in multiple_options.items():
            value = schema.get(key)
            if not value:
                for pkey in keys:
                    value = schema.get(pkey)
                    if value:
                        break
            data[key] = value
        return data

    def cleanup_category(self, name: str):
        possible_ends = [
            'Category', 'Product Type', 'Products'
        ]
        name = name.strip()
        for item in possible_ends:
            name = name.rstrip(item)
        return item
    
    def extract_reviews(self, response: TextResponse):
        reviews = []

        for review in response.css(settings.PRODUCT_REVIEWS_SELECTOR):
            reviewText = review.css(
                settings.PRODUCT_REVIEW_TEXT_SELECTOR
            ).get("").strip().strip()
            reviews.append(reviewText)
        return reviews
