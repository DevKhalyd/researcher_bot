from scrapping import get_results_from_reddit


def main():
    results = get_results_from_reddit("Dulce Soltero")

    if results is None:
        return

    for result in results:
        print(result.title)
        print(result.image)
        print(result.reference)
    pass

main()