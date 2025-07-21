from openai import OpenAI

# Read the key from the file
with open("openai_key.txt", "r") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

# Test API
models = client.models.list()
print([m.id for m in models.data])
