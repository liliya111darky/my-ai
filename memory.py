import json from pathlib import Path
MEMORY_FILE = Path("memory.json")
def load_memory(): if not MEMORY_FILE.exists(): return {"knowledge": []}
with open(MEMORY_FILE, "r", encoding="utf-8") as file:
    return json.load(file)
def save_memory(memory): with open(MEMORY_FILE, "w", encoding="utf-8") as file: json.dump(memory, file, ensure_ascii=False, indent=2)
def add_knowledge(subject, fact): memory = load_memory()
memory["knowledge"].append({
    "subject": subject,
    "fact": fact
})

save_memory(memory)
def find_knowledge(subject): memory = load_memory()
results = []

for item in memory["knowledge"]:
    if item["subject"].lower() == subject.lower():
        results.append(item)

return results
