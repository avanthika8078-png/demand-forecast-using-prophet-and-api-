# Calling an AI API from Python
!pip install groq
from groq import Groq
import time
import os

#  INITIALISE CLIENT
# Configure the API key.
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY", "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"), # Replace with your Groq API key or set environment variable
)
MODEL  = "llama-3.3-70b-versatile"

#  HELPER FUNCTION
def ask(prompt: str) -> str:
    """Send a single prompt to the API and return the text response."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL,
            temperature=0.0,
            max_tokens=500,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred during Groq API call: {e}")
        return "[API Error: An unexpected error occurred with Groq.]"

#  SAMPLE INPUTS
sample_prompts = [
    {
        "label"  : "1. Sentiment Analysis",
        "prompt" : (
            "Classify the sentiment of each sentence as Positive, Negative, or Neutral. "
            "Reply with a short bullet list.\n\n"
            "Sentences:\n"
            "- Our Q3 revenue grew 18% year-over-year.\n"
            "- The product launch was delayed by two months.\n"
            "- Inventory levels remained stable throughout the quarter.\n"
            "- Customer complaints about shipping time increased sharply.\n"
            "- The new pricing model was well received by most clients."
        ),
    },
    {
        "label"  : "2. Text Summarisation",
        "prompt" : (
            "Summarise the following passage in exactly two sentences:\n\n"
            "Retail demand forecasting involves predicting future customer demand for products "
            "so that supply chains can be optimised. Accurate forecasts reduce overstock and "
            "stockout situations, cutting costs and improving customer satisfaction. Modern "
            "approaches combine historical sales data with external signals like weather, "
            "promotions, and economic indicators to improve accuracy. Machine learning models "
            "such as Prophet, XGBoost, and LSTMs have become industry standards."
        ),
    },
    {
        "label"  : "3. Keyword Extraction",
        "prompt" : (
            "Extract the five most important keywords from the text below. "
            "Return them as a comma-separated list, nothing else.\n\n"
            "Text: Seasonal promotions in the electronics and clothing categories drive "
            "significant spikes in consumer demand, particularly in the North and West regions "
            "during summer and winter. Competitor pricing and discount strategies also play "
            "a critical role in shaping weekly sales volumes."
        ),
    },
    {
        "label"  : "4. Data Explanation",
        "prompt" : (
            "Explain what a 'demand forecast' is in plain English, "
            "as if talking to a store manager with no data background. "
            "Keep it under 60 words."
        ),
    },
    {
        "label"  : "5. Creative Rewrite",
        "prompt" : (
            "Rewrite the following dry data observation as an engaging one-sentence "
            "headline for a business newsletter:\n\n"
            "Observation: Average weekly demand increased by 29.8% during promotional periods "
            "compared to non-promotional periods across all product categories."
        ),
    },
]

#  RUN & PRINT
SEP  = "=" * 65
SEP2 = "-" * 65

print()
print(SEP)
print("   AI API BASICS —  Sample Prompts ")
print(f"   Model: {MODEL}")
print(SEP)

for i, item in enumerate(sample_prompts):
    print(f"\n{item['label']}")
    print(SEP2)
    print("PROMPT:")

    for line in item["prompt"].splitlines():
        print(f"  {line}")
    print("\nRESPONSE:")
    response = ask(item["prompt"])
    for line in response.strip().splitlines():
        print(f"  {line}")
    print()
    if i < len(sample_prompts) - 1:
        time.sleep(0.3)

print(SEP)
print("  All 5 API calls attempted.")
print(SEP)
print()
