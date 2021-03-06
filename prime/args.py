from argparse import ArgumentParser, Namespace

from version import version

name: str = "PRIME"
authors: list = [
    "Nicholas M. Synovic",
    "Matthew Hyatt",
    "George K. Thiruvathukal",
]

def main_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Bus Factor Calculator",
        description="A tool to calculate the bus factor of a Git repository",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Commits JSON file. DEFAULT: ./commits_loc.json",
        default="commits_loc.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output JSON file. DEFAULT: ./bus_factor.json",
        type=str,
        default="bus_factor.json",
    )
    parser.add_argument(
        "-b",
        "--bin",
        help="Bin containing the number of days between computed bus factor values. DEFAULT: 1",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display version of the tool",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    if args.version:
        print(f"{name} version {version()}")
        quit(0)

    if args.bin < 1:
        print(f"Bin argument must be an integer greater than 0: {args.bin}")
        quit(1)

    return args


def graph_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Bus Factor Grapher",
        description="A tool to graph the bus factor of a repository",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        help=f"JSON export from {name}-git-bus-factor-compute. DEFAULT: ./bus_factor.json",
        type=str,
        required=False,
        default="bus_factor.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Filename of the graph. DEFAULT: ./bus_factor.pdf",
        type=str,
        required=False,
        default="bus_factor.pdf",
    )
    parser.add_argument(
        "--type",
        help="Type of figure to plot. DEFAULT: line",
        type=str,
        required=False,
        default="line",
    )
    parser.add_argument(
        "--title",
        help='Title of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--x-label",
        help='X axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--y-label",
        help='Y axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--stylesheet",
        help='Filepath of matplotlib stylesheet to use. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display version of the tool",
        action="store_true",
        default=False,
    )

    return parser.parse_args()
