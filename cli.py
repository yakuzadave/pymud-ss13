import argparse


def main():
    parser = argparse.ArgumentParser(description="Simple CLI for MUDpy")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()
    print(f"Using config {args.config}")

    try:
        while True:
            line = input("> ")
            if line.strip().lower() == "quit":
                print("Exiting CLI.")
                break
    except EOFError:
        pass


if __name__ == "__main__":
    main()
