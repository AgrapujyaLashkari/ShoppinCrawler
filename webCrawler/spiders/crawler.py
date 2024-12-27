from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class DynamicCrawlingSpider(CrawlSpider):
    name = "dynamic_crawler"
    
    start_urls = ["https://www.flipkart.com/"]
    allowed_domains = ["flipkart.com"]
    
    # Follow all links on the site
    rules = (
        Rule(LinkExtractor(), callback="filter_product_urls", follow=True),
    )

    def filter_product_urls(self, response):
        """
        Dynamically identify and filter product URLs based on heuristic rules.
        Print product URLs directly to the terminal.
        """
        url = response.url

        # Heuristic: Check if the URL likely belongs to a product
        if self.is_product_url(url, response):
            print(f"Discovered product URL: {url}")  # Print to terminal
            yield {'url': url}  # Yield product URLs if required for pipeline/storage

    def is_product_url(self, url, response):
        """
        Apply heuristics to determine if a URL is a product page.
        """
        # Check if the URL contains keywords like "product", "p", "item", etc.
        keywords = ['product', 'p', 'item', 'sku', 'prd']
        if any(keyword in url.lower() for keyword in keywords):
            return True

        # Check if the URL ends in a typical product identifier (like numbers)
        if url.split("/")[-1].isdigit():
            return True

        # Look for content clues on the page (e.g., product-specific HTML elements)
        if response.css("div[class*=price], button[class*=add-to-cart], h1::text").get():
            return True

        # Default: Not a product page
        return False