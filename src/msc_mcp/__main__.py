import argparse
from .server import serve

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="MSC MCP Server")
    parser.parse_args(argv)

    # serve() is synchronous; FastMCP manages its own event loop.
    serve()

if __name__ == "__main__":
    main()
