from storage.database import load_memory


def find_direct_relations(subject):
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


def find_next_relations(subject):
    return find_direct_relations(subject)


def build_reasoning_chain(
    subject,
    max_depth=5
):
    chain_results = []

    visited = set()

    def explore(
        current_subject,
        path,
        confidence
    ):

        if len(path) >= max_depth:
            return

        relations = find_next_relations(
            current_subject
        )

        for relation in relations:

            object_name = relation["object"]

            step = (
                current_subject,
                relation["relation"],
                object_name
            )

            if step in visited:
                continue

            visited.add(step)

            new_confidence = min(
                confidence,
                relation.get(
                    "confidence",
                    1.0
                )
            )

            new_path = path + [
                {
                    "subject": current_subject,
                    "relation": relation["relation"],
                    "object": object_name,
                    "confidence": relation.get(
                        "confidence",
                        1.0
                    )
                }
            ]

            chain_results.append({
                "result": object_name,
                "path": new_path,
                "confidence": new_confidence
            })

            explore(
                object_name,
                new_path,
                new_confidence
            )

    explore(
        subject,
        [],
        1.0
    )

    return chain_results


def explain_reasoning(
    subject,
    result
):
    chains = build_reasoning_chain(
        subject
    )

    explanations = []

    for chain in chains:

        if chain["result"].lower() != result.lower():
            continue

        steps = []

        for step in chain["path"]:

            steps.append(
                f"{step['subject']} → "
                f"{step['relation']} → "
                f"{step['object']}"
            )

        explanations.append({
            "subject": subject,
            "result": result,
            "steps": steps,
            "confidence": chain["confidence"]
        })

    return explanations
