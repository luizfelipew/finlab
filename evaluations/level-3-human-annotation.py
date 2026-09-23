import json
import os
import time

import requests
from dotenv import load_dotenv
from langfuse import observe, get_client

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def load_test_case(filename: str) -> dict:
    with open(f"test_cases/{filename}", "r") as f:
        return json.load(f)

@observe()
def call_agent_endpoint(query: str, limit: int = 3):
    response = requests.post(
        f"{API_BASE_URL}/agent", json={"query": query, "limit": limit}
    )

    langfuse = get_client()
    langfuse.update_current_span(
        metadata={
            "status_code": response.status_code,
            "query_length": len(query),
        },
    )    

    return response

@observe()
def test_agent_endpoint_apple():
    test_case = load_test_case("apple_test.json")

    response = call_agent_endpoint(test_case["query"])

    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == test_case["expected_ticker"]
    assert "fundamental_analysis" in data
    assert "momentum_analysis" in data
    assert "sentiment_analysis" in data
    assert "final_recommendation" in data

    langfuse = get_client()
    langfuse.update_current_span(
        name="test_agent_apple",
        metadata={
            "test_type": test_case["test_type"],
            "expected_ticker": test_case["expected_ticker"],
            "actual_ticker": data["ticker"],
            "has_all_analysis": True,
        },
        input={"query": test_case["query"]},
        output=data,
    )


    return data
    
@observe()
def test_agent_endpoint_ibm():
    time.sleep(25)
    test_case = load_test_case("ibm_test.json")

    response = call_agent_endpoint(test_case["query"])

    if response.status_code != 200:
        print(f"Error response: {response.json()}")
        
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == test_case["expected_ticker"]

    langfuse = get_client()
    langfuse.update_current_span(
        name="test_agent_ibm",
        metadata={
            "test_type": test_case["test_type"],
            "expected_ticker": test_case["expected_ticker"],
            "actual_ticker": data["ticker"],
            "has_all_analysis": True,
        },
        input={"query": test_case["query"]},
        output=data,
    )


    return data
    
@observe()
def test_agent_endpoint_no_company():
    time.sleep(25)
    test_case = load_test_case("no_company_test.json")

    response = call_agent_endpoint(test_case["query"])
    
    assert response.status_code == 400

    langfuse = get_client()
    langfuse.update_current_span(
        name="test_agent_no_company",
        metadata={
            "test_type": test_case["test_type"],
            "expected_status": 400,
            "actual_status": response.status_code,
        },
        input={"query": test_case["query"]},
        output={"status_code": response.status_code}
    )

    
@observe()
def test_agent_endpoint_natural_language():
    time.sleep(25)
    test_case = load_test_case("natural_language_test.json")

    response = call_agent_endpoint(test_case["query"])
    
    if response.status_code != 200:
        print(f"Error response: {response.json()}")
        
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == test_case["expected_ticker"]
    assert data["final_recommendation"]["action"] in ["BUY", "SELL", "HOLD"]

    langfuse = get_client()
    langfuse.update_current_span(
        name="test_agent_natural_language",
        metadata={
            "test_type": test_case["test_type"],
            "expected_ticker": test_case["expected_ticker"],
            "actual_ticker": data["ticker"],
            "recommendation_action": data["final_recommendation"]["action"],
        },
        input={"query": test_case["query"]},
        output=data,
    )


    return data

def run_evaluation_pipeline():
    tests = [
        ("Apple (Static Mapping)", test_agent_endpoint_apple),
        ("IBM (LLM Fallback)", test_agent_endpoint_ibm),
        ("No Company (Error Handling)", test_agent_endpoint_no_company),
        ("Natural Language (Complex Query)", test_agent_endpoint_natural_language),
    ]

    passed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            print(f"PASS {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL {test_name}: {e}")
        except Exception as e:
            print(f"ERROR {test_name}: {e}")
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")

if __name__ == "__main__":
    run_evaluation_pipeline()

    