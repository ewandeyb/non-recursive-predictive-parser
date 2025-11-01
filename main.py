from parsers import production_rules


def main():
    parsed = production_rules.load_prod_rules("rules.prod")
    print(parsed)


if __name__ == "__main__":
    main()
