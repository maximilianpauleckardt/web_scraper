import sys
import asyncio
from crawl import crawl_site_async

async def main():
    if len(sys.argv) < 4:
        print("not all arguments provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    print("Script name:", sys.argv[0])
    print("Argument:", sys.argv[1])
    print("max_concurrency:", sys.argv[2])
    print("max_pages:", sys.argv[3])
    print(f"starting crawl of: {sys.argv[1]}")
    results = await crawl_site_async(sys.argv[1])
    for page in results.values():
        print(page)


if __name__ == "__main__":
    asyncio.run(main())
