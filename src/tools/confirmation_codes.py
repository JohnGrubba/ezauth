import random
from tools import SignupConfig


all_ids = []


def regenerate_ids():
    global all_ids
    # Generate and shuffle 10000 unique IDs for confirmation email (Depending on complexity)
    match (SignupConfig.conf_code_complexity):
        case 2:
            # Random 6 Digit Numbers
            all_ids = [str(random.randint(100000, 999999)) for _ in range(10000)]
            random.shuffle(all_ids)
        case 3:
            # Random 4 Character Strings
            all_ids = [
                "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=4))
                for _ in range(10000)
            ]
            random.shuffle(all_ids)
        case 4:
            # Random 6 Character Strings
            all_ids = [
                "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=6))
                for _ in range(10000)
            ]
            random.shuffle(all_ids)
        case _:
            # Default Case (1)
            all_ids = [str(i) for i in range(10000)]
            random.shuffle(all_ids)


regenerate_ids()
