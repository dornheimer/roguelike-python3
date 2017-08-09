from random import randint


def random_choice_index(chances):
    """Get a random index from a list of spawn chances (weights)."""
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1

def random_choice_from_dict(choice_dict):
    """
    Uses random_choice_index().
    Select a random key from a dictionary that has spawn chances as values.
    """
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]
