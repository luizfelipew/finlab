from dotenv import load_dotenv
from groq import Groq
from guardrails.validators import (
    FailResult,
    PassResult,
    register_validator,
)

from guardrails import Guard

load_dotenv()

client = Groq()

SYSTEM_PROMPT = (
    "You are a financial analysis assistant. You have no real-time market data: "
    "when asked about current prices, do not refuse. Briefly say you lack live "
    "quotes, then give a useful overview from your general knowledge (business "
    "fundamentals, recent known trends, key drivers and risks)."
)


def groq_wrapper(*, messages, **kwargs) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages],
    )
    return response.choices[0].message.content


@register_validator(name="simple_topic_check", data_type="string")
def simple_topic_check(value, metadata):
    financial_keywords = [
        "stock",
        "apple",
        "investiment",
        "ticker",
        "finance",
        "market",
    ]

    if any(keyword in value.lower() for keyword in financial_keywords):
        return PassResult()
    else:
        return FailResult(error_message="Query is not about financial topics")


guard = Guard().use(simple_topic_check(on_fail="exception"))
# Desliga a telemetria do Guardrails (evita os erros do opentelemetry sem rede)
guard.configure(allow_metrics_collection=False)

queries = [
    "How is Apple Stock doing?",
    "What's the weather today?",
]

for query in queries:
    print(f"\nQuery: {query}")
    try:
        guard.validate(query)
        result = groq_wrapper(messages=[{"role": "user", "content": query}])
        print(result)
    except Exception as e:
        print(f"BLOCKED: {e}")
