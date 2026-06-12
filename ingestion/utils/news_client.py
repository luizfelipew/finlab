from email import contentmanager
from importlib import metadata
from typing import List, Dict

import trafilatura
import yfinance as yf


class NewsClient:
    def fetch_news(self, ticker: str, max_stories: int = 10) -> List[Dict[str, any]]:
        data = yf.Ticker(ticker)
        news = data.news

        news_data = []

        for item in news[:max_stories]:
            content = item.get("content", {})
            # content_type = item.get("content_type")
            content_type = content.get("contentType")

            if content_type != "STORY":
                continue

            # canonical_url = content.get("canonical_url")
            url_data = (
                content.get("clickThroughUrl") or content.get("canonicalUrl") or {}
            )
            title = content.get("title")
            date = content.get("pubDate")
            url = url_data.get("url", "")
            # url = canonical_url.get("url")

            if "finance.yahoo.com" not in url:
                continue

            download = trafilatura.fetch_url(url)
            text_content = trafilatura.extract(download)

            if text_content:
                metadata = {
                    "ticker": ticker,
                    "title": title,
                    "url": url,
                    "date": date,
                    "source": "yahoo_finance",
                }
                news_data.append({"text": text_content, "metadata": metadata})

        return news_data
