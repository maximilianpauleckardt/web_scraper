import sys
from crawl import get_html

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    print("Script name:", sys.argv[0])
    print("Argument:", sys.argv[1])
    print(f"starting crawl of: {sys.argv[1]}")
    results = get_html(sys.argv[1])
    print(results)


if __name__ == "__main__":
    main()
