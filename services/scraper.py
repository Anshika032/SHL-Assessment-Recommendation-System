import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/products/product-catalog/"


class SHLCatalogScraper:

    def __init__(self):

        self.session = requests.Session()

        self.assessments = []

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

    def fetch_page(self, url):

        response = self.session.get(
            url,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return BeautifulSoup(
            response.text,
            "lxml"
        )

    def extract_links(self, soup):

        links = set()

        for a in soup.find_all("a", href=True):

            href = a["href"]

            full_url = urljoin(
                BASE_URL,
                href
            )

            valid_patterns = [
                "/products/assessments/",
                "/products/product-catalog/view/"
            ]

            if any(
                pattern in full_url
                for pattern in valid_patterns
            ):

                if "javascript:" not in full_url:

                    links.add(full_url)

        return list(links)

    def scrape_product(self, url):

        try:

            soup = self.fetch_page(url)

            title = soup.find("h1")

            title = (
                title.get_text(strip=True)
                if title else None
            )

            meta_desc = soup.find(
                "meta",
                attrs={
                    "name": "description"
                }
            )

            description = (
                meta_desc.get("content")
                if meta_desc else ""
            )

            page_text = soup.get_text(
                " ",
                strip=True
            )

            assessment = {
                "name": title,
                "url": url,
                "description": description,
                "raw_text": page_text
            }

            return assessment

        except Exception as e:

            print(f"\nError scraping {url}")

            print(e)

            return None

    def scrape(self):

        print("Fetching catalog page...")

        soup = self.fetch_page(
            CATALOG_URL
        )

        links = self.extract_links(
            soup
        )

        print(
            f"Found {len(links)} candidate links"
        )

        for link in tqdm(links):

            data = self.scrape_product(
                link
            )

            if data and data["name"]:

                self.assessments.append(
                    data
                )

            time.sleep(1)

    def save(self):

        output_path = (
            "data/raw/catalog.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.assessments,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(
            f"Saved {len(self.assessments)} assessments"
        )


if __name__ == "__main__":

    scraper = SHLCatalogScraper()

    scraper.scrape()

    scraper.save()