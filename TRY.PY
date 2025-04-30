from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
