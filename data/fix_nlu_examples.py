import yaml

with open("data/nlu.yml", "r") as f:
    data = yaml.safe_load(f)

for intent in data["intents"]:
    for i, example in enumerate(intent["examples"]):
        if not example["text"].startswith("-"):
            example["text"] = f"- {example['text']}"

with open("data/nlu.yml", "w") as f:
    yaml.dump(data, f)    