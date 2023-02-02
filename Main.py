import random


def generate_random_ref_num_list(prefix: str, iterations: int) -> list[int]:
    start: int = 1000
    end: int = 9999

    ref_num_list: list[int] = []
    rand_num_list: list[int] = []
    rand_num: int = random.randint(start, end)

    for num in range(iterations):
        while rand_num in rand_num_list:
            rand_num = random.randint(start, end)

        rand_num_list.append(rand_num)

        ref_str: str = prefix + str(rand_num)
        ref_num: int = int(ref_str)
        ref_num_list.append(ref_num)

    ref_num_list.sort()

    return ref_num_list


def print_ref_num_list():
    ref_nums: list[int] = generate_random_ref_num_list('24', 10)
    for ref in ref_nums:
        print(ref)


def main():
    print_ref_num_list()


if __name__ == '__main__':
    main()