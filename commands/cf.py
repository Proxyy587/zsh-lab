import random
import webbrowser
import requests
from typing import Optional

CODEFORCES_API_URL = "https://codeforces.com/api/problemset.problems"


# fetchiing all the problems from codeforces
def fetch_problems() -> Optional[dict]:
    try:
        response = requests.get(CODEFORCES_API_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "OK":
            print(f"Error: Unexpected API response status: {data.get('status')}")
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"network error: {e}")
        return None
    except ValueError:
        print("error: could not decode JSON response from Codeforces.")
        return None

def get_random_problem_from_list(problem_list: list[dict]) -> Optional[dict]:
    if not problem_list:
        print("no problems found to select from.")
        return None
    try:
        choice = random.choice(problem_list)
        return choice
    except IndexError:
        print("No problems found to select from.")
        return None


# open the shit in browser
def open_browser(problem: dict) -> None:
    contest_id = problem.get("contestId")
    index = problem.get("index")
    name = problem.get("name", "Unnamed problem")
    problem_rating = problem.get("rating", "Unknown")
    if contest_id is None or index is None:
        print("Error: Missing contestId or index for the problem. Cannot open in browser.")
        return
    problem_url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    print(f"Opening: {name} ({contest_id}-{index})" + (f" [rating: {problem_rating}]" if "rating" in problem else ""))
    try:
        webbrowser.open(problem_url)
    except Exception as e:
        print(f"Error opening problem URL: {e}")

def random_rating(rating: int) -> None:
    data = fetch_problems()
    if not data:
        print("could not fetch problems. please try again later.")
        return
    all_problems = data.get("result", {}).get("problems", [])
    if not all_problems:
        print("no problems found in the Codeforces response.")
        return
    valid_problems = [
        p for p in all_problems
        if p.get("contestId") and p.get("index") and p.get("rating") == rating
    ]
    if not valid_problems:
        print(f"no problems found with rating {rating}.")
        return
    choice = get_random_problem_from_list(valid_problems)
    if choice:
        open_browser(choice)

def random_problem() -> None:
    data = fetch_problems()
    if not data:
        print("could not fetch problems. please try again later.")
        return
    all_problems = data.get("result", {}).get("problems", [])
    if not all_problems:
        print("no problems found in the Codeforces response.")
        return
    choice = get_random_problem_from_list(all_problems)
    if choice:
        open_browser(choice)

# userInput = input("enter the command: ")
# if userInput == "random":
#     random_problem()
# elif userInput.isdigit():
#     random_rating(int(userInput))
# else:
#     print("invalid command: cf [random|<rating>]")

def handle(args: list[str]) -> None:
    # cf             # open a random problem
    # cf random      # same thing as cf
    # cf <rating>    # opens a random problem with the given rating
    if not args:
        random_problem()
        return

    if len(args) == 1:
        if args[0].upper() == "RANDOM":
            random_problem()
            return
        try:
            rating = int(args[0])
            if rating <= 0:
                raise ValueError
            random_rating(rating)
            return
        except ValueError:
            print(f"invalid ratings: {args[0]}. either there is no such rating available or it is not a valid integer.")
            return

    print("invalid command: cf [random|<rating>]")
    print("example: cf 800 # open a random problem with the given rating")
