import json
import base64
import requests
import streamlit as st


GITHUB_REPO = "liliya111darky/my-ai"
FILE_PATH = "memory.json"
BRANCH = "main"


def get_github_url():
    return (
        f"https://api.github.com/repos/"
        f"{GITHUB_REPO}/contents/{FILE_PATH}"
    )


def get_headers():
    return {
        "Authorization": (
            f"Bearer {st.secrets['GITHUB_TOKEN']}"
        ),
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
        return {
            "knowledge": [],
            "reasoning": []
        }

    response.raise_for_status()

    data = response.json()

    content = data["content"].replace("\n", "")

    decoded = base64.b64decode(
        content
    ).decode("utf-8")

    memory = json.loads(decoded)

    # Если старый файл ещё не содержит
    # раздел reasoning — создаём его.
    if "knowledge" not in memory:
        memory["knowledge"] = []

    if "reasoning" not in memory:
        memory["reasoning"] = []

    return memory


def save_memory(memory):
    url = get_github_url()

    response = requests.get(
        url,
        headers=get_headers(),
        params={"ref": BRANCH},
    )

    response.raise_for_status()

    file_data = response.json()

    sha = file_data["sha"]

    # Гарантируем наличие двух основных
    # разделов памяти.
    if "knowledge" not in memory:
        memory["knowledge"] = []

    if "reasoning" not in memory:
        memory["reasoning"] = []

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
