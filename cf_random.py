# import requests
# import random
# import webbrowser
# import sys

# def get_random_problem():
#     url = "https://codeforces.com/api/problemset.problems"
#     try:
#         response = requests.get(url)
#         data = response.json()
        
#         if data['status'] != 'OK':
#             print("Error fetching problems from Codeforces.")
#             return

#         problems = data['result']['problems']
#         # Filter mostly for actual contest problems (optional)
#         valid_problems = [p for p in problems if 'contestId' in p and 'index' in p]
        
#         if not valid_problems:
#             print("No problems found.")
#             return

#         choice = random.choice(valid_problems)
#         contest_id = choice['contestId']
#         index = choice['index']
#         name = choice['name']

#         problem_url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
        
#         print(f"Opening: {name} ({contest_id}{index})")
#         webbrowser.open(problem_url)

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     get_random_problem()