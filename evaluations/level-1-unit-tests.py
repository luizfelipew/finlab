import sys
import os

# Add the parent directory to sys.path to allow importing from the 'api' package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'api'))

from api.config.company_mappings import COMPANY_TICKER_MAPPINGS
import json

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(base_url="Https://api.groq.com/openai/v1")

def load_test_case(filename: str) -> dict:
    with open(f"test_cases/{filename}", "r") as f:
        return json.load(f)

COMPANY_TICKER_MAPPINGS ={
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "tesla": "TSLA",
    "meta": "META",
}

from api.services.ticker_extractor import TickerExtractor

extractor = TickerExtractor()

def extract_ticker(query: str) -> str | None:
    return extractor.extract_ticker(query)

def test_static_mapping_apple():
    test_case = load_test_case("apple_test.json")
    result = extract_ticker(test_case["query"])
    assert result == test_case["expected_ticker"]

def test_llm_fallback_ibm():
    test_case = load_test_case("ibm_test.json")
    result = extract_ticker(test_case["query"])
    assert result == test_case["expected_ticker"], (
        f"Expected {test_case['expected_ticker']}, got {result}"
    )

def test_no_company_mentioned():
    test_case = load_test_case("no_company_test.json")
    result = extract_ticker(test_case["query"])
    assert result == test_case["expected_ticker"]

def test_natural_language_query():
    test_case = load_test_case("natural_language_test.json")
    result = extract_ticker(test_case["query"])
    assert result == test_case["expected_ticker"]


if __name__ == "__main__":
    tests = [
        test_static_mapping_apple,
        test_llm_fallback_ibm,
        test_no_company_mentioned,
        test_natural_language_query
    ]
    passed = 0

    for test in tests:
        print(f"Running test: {test.__name__}")
        try:
            test()
            passed += 1
            print(f"✅ PASS {test.__name__}")
        except AssertionError as e:
            print(f"❌ FAIL {test.__name__}: {e}")
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    if passed == len(tests):
        print("🎉 All tests passed!")
        