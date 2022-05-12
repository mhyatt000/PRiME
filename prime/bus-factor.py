from args import main_args
from version import version
from dev_count import get_devs

def main() -> None:

    args: Namespace = main_args()

    if not args.alpha:
        print(f'bus_factor calculation requires alpha value')
        quit()

    df = pd.read_json(args.input) #.T
    bf = get_devs(df, bin=args.bin, alpha=args.alpha)
