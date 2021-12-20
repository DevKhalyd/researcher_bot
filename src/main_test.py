from scrapping import get_results_from_reddit


def main():
    results = get_results_from_reddit("Any Topic")

    if results is None:
        return

    print('The results are the following...')

    for result in results:
        print(result.title)
        print(result.image)
        print(result.reference)
    pass

main()