from openai import OpenAI
from dotenv import load_dotenv
from guardrails import Guard
from guardrails.hub import ProfanityFree

load_dotenv()

client = OpenAI(base_url="https://api.groq.com/openai/v1")


def groq_wrapper(*, messages, **kwargs) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
    )
    return response.choices[0].message.content


guard = Guard().use(ProfanityFree(on_fail="exception"))
query = "FAANG representa quais fucking empresas de tecnologia?"
try:
    guard.validate(query)
except Exception as e:
    print(e)

validated_response = guard(
    groq_wrapper,
    messages=[
        {
            "role": "user",
            "content": query,
        }
    ],
)

print(validated_response.validated_output)
