import random
from tools import SignupConfig


all_ids = []

# Has to stay below 9000
amount = 100


def regenerate_ids(complexity_test: int = None):
    global all_ids
    # Generate and shuffle 10000 unique IDs for confirmation email (Depending on complexity)
    match (complexity_test if complexity_test else SignupConfig.conf_code_complexity):
        case 2:
            # Random 6 Digit Numbers
            all_ids = random.sample(range(100000, 999999), amount)
        case 3:
            # Random 4 Character Strings
            all_ids = list(
                set(
                    [
                        "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=4))
                        for _ in range(amount)
                    ]
                )
            )
            random.shuffle(all_ids)
        case 4:
            # Random 6 Character Strings
            all_ids = list(
                set(
                    [
                        "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=6))
                        for _ in range(amount)
                    ]
                )
            )
            random.shuffle(all_ids)
        case _:
            # Default Case (1)
            all_ids = random.sample(range(1000, 10000), amount)


regenerate_ids()

if __name__ == "__main__":
    regenerate_ids(4)
    print(all_ids)
