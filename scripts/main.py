def compare_two_dicts(old: dict, new: dict):

    old_set = set(old.items())
    new_set = set(new.items())

    diffs: set = old_set ^ new_set

    data: dict = {}

    for diff in diffs:
        key = data.get(diff[0])
        if key:
            data[diff[0]] = [data.get(diff[0]), diff[1]]
        else:
            data[diff[0]] = diff[1]

    print(data)


def run() -> None:
    old = {
        'name': 'abdullah',
        'age': 16,
    }
    new = {
        'name': 'abdullah',
        'age': 17,
    }
    compare_two_dicts(old, new)