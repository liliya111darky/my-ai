from memory import (
    load_memory,
    save_memory,
)


def add_knowledge(subject, fact):
    memory = load_memory()

    memory["knowledge"].append({
        "subject": subject,
        "fact": fact
    })

    save_memory(memory)


def find_knowledge(subject):
    memory = load_memory()

    results = []

    for item in memory["knowledge"]:
        if item.get("subject", "").lower() == subject.lower():
            if "fact" in item:
                results.append(item)

    return results


def add_structured_knowledge(
    subject,
    property,
    value,
    confidence=1.0,
    source="user"
):
    memory = load_memory()

    memory["knowledge"].append({
        "subject": subject,
        "property": property,
        "value": value,
        "confidence": confidence,
        "source": source
    })

    save_memory(memory)


def find_structured_knowledge(subject):
    memory = load_memory()

    results = []

    for item in memory["knowledge"]:
        if (
            item.get("subject", "").lower() == subject.lower()
            and "property" in item
            and "value" in item
        ):
            results.append(item)

    return results


def find_contradictions(subject, property, value):
    memory = load_memory()

    contradictions = []

    for item in memory["knowledge"]:
        if (
            item.get("subject", "").lower() == subject.lower()
            and item.get("property", "").lower() == property.lower()
            and "value" in item
        ):
            if item["value"].lower() != value.lower():
                contradictions.append(item)

    return contradictions


def find_duplicate(subject, property, value):
    memory = load_memory()

    for item in memory["knowledge"]:
        if (
            item.get("subject", "").lower() == subject.lower()
            and item.get("property", "").lower() == property.lower()
            and item.get("value", "").lower() == value.lower()
        ):
            return item

    return None
