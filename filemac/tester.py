import re

input_string = "The number is 12345"

if (match := re.search(r'\s+', input_string)):
    print(f"The first number in the string is= {match.group()}")
else:
    print("No numbers found in the string")
