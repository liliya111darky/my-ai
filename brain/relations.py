from storage.database import (
    load_memory,
    save_memory,
)


def add_relation(
    subject,
    relation,
    object,
    confidence=1.0,
    source="user"
):
    memory = load_memory()

    memory["knowledge"].append({
        "subject": subject,
        "relation": relation,
        "object": object,
        "confidence": confidence,
        "source": source
    })

    save_memory(memory)


def find_relations(subject):
    memory = load_memory()

    results = []

    for item in memory["knowledge"]:

        if (
            item.get("subject", "").lower()
            == subject.lower()
            and "relation" in item
            and "object" in item
        ):
            results.append(item)

    return results


def delete_relation(
    subject,
    relation,
    object
):
    memory = load_memory()

    new_knowledge = []

    deleted = False

    for item in memory["knowledge"]:

        if (
            item.get("subject", "").lower()
            == subject.lower()
            and item.get("relation", "").lower()
            == relation.lower()
            and item.get("object", "").lower()
            == object.lower()
        ):
            deleted = True
            continue

        new_knowledge.append(item)

    memory["knowledge"] = new_knowledge

    if deleted:
        save_memory(memory)

    return deleted


def infer_from_relations(subject):
    memory = load_memory()

    inferred = []

    first_relations = []

    for item in memory["knowledge"]:

        if (
            item.get("subject", "").lower()
            == subject.lower()
            and "relation" in item
            and "object" in item
        ):
            first_relations.append(item)

    for first in first_relations:

        middle_object = first["object"]

        for second in memory["knowledge"]:

            if (
                second.get("subject", "").lower()
                == middle_object.lower()
                and "relation" in second
                and "object" in second
            ):

                inferred.append({
                    "subject": subject,
                    "relation": second["relation"],
                    "object": second["object"],
                    "via": middle_object,
                    "confidence": min(
                        first.get(
                            "confidence",
                            1.0
                        ),
                        second.get(
                            "confidence",
                            1.0
                        )
                    )
                })

    return inferred
