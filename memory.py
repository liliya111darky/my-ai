import json
import requests
import streamlit as st


GITHUB_REPO = "liliya111darky/my-ai"
FILE_PATH = "memory.json"
BRANCH = "main"


def get_github_url():
    return f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"


def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def load_memory():
    response = requests.get(
        get_github_url(),
        headers=get_headers(),
        params={"ref": BRANCH},
    )

    if response.status_code == 404:
        return {"knowledge": []}

    response.raise_for_status()

    data = response.json()

    content = data["content"]
    content = content.replace("\n", "")

    import base64

    decoded = base64.b64decode(content).decode("utf-8")

    return json.loads(decoded)


def save_memory(memory):
    import base64

    url = get_github_url()

    response = requests.get(
        url,
        headers=get_headers(),
        params={"ref": BRANCH},
    )

    response.raise_for_status()

    file_data = response.json()
    sha = file_data["sha"]

    content = json.dumps(
        memory,
        ensure_ascii=False,
        indent=2
    )

    encoded_content = base64.b64encode(
        content.encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": "Update AI memory",
        "content": encoded_content,
        "branch": BRANCH,
        "sha": sha,
    }

    response = requests.put(
        url,
        headers=get_headers(),
        json=payload,
    )

    response.raise_for_status()


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
        if item["subject"].lower() == subject.lower():
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
