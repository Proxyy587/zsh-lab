import random
import webbrowser
import requests


def get_random_problem():
    url = "https://codeforces.com/api/problemset.problems"

    try:
        response = requests.get(url, timeout=20)
        data = response.json()

        if data.get("status") != "OK":
            print("Error please check your internet connection.")
            return

        problems = data["result"]["problems"]
        valid_problems = [
            p for p in problems
            if "contestId" in p and "index" in p
        ]

        if not valid_problems:
            print("No problems found. Please try again later.")
            return

        choice = random.choice(valid_problems)
        contest_id = choice["contestId"]
        index = choice["index"]
        name = choice.get("name", "Unnamed problem")

        problem_url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"

        print(f"Opening: {name} ({contest_id}{index})")
        webbrowser.open(problem_url)

    except Exception as e:
        print(f"An error occurred: {e}")


def handle(args: list[str]) -> None:
    """Usage: cf [random]"""
    if not args:
        get_random_problem()
        return

    if len(args) == 1 and args[0] == "random":
        get_random_problem()
        return

    print("Usage: cf [random]")
