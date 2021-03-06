import pandas as pd
from pandas import Categorical, DataFrame, Interval, Series

from args import main_args
from version import version

def get_devs(df: DataFrame, *, bin: int, alpha=0.0) -> DataFrame:
    '''if alpha compute bus factor else num devs'''

    '''pseudocode
    find average DLOC per day
    find number of devs who contribute alpha% of avg DLOC each day

    rationale:
        if someone commits 1 line and he is the only contributor that day,
        that does not make him a key contributor

    or

    find find avg DLOC per commit
    find number of devs who are in alpha percentile of contributors each day
    ** choice rn ... easier and more important imo
    '''

    # # global percentile DLOC
    # if alpha:
    #     dloc = df["delta_loc"].tolist()
    #     dloc.sort()
    #
    #     # significance is the highest DLOC committed in the lowest alpha% of commits
    #     # any value higher than "significance" is considered a a key contribution
    #     # TODO is it ok that some people may be key contributors one day but not the next
    #
    #     threshold = int(alpha*len(dloc))
    #     significance = dloc[threshold]

    day_key = "day_since_0"
    # keeps swiching between day_since days_since and author_days_since 0

    lastday = df[day_key].max() + bin
    bins = list(range(0,lastday,bin))

    # original implementation:
    # bins = [day for day in range(lastday) if day % bin == 0]

    df["commitBin"] = pd.cut(df[day_key], bins=bins, include_lowest=True)
    bins = df["commitBin"].unique().tolist()

    '''pseudocode ... this is slow
    for bin in bins:
        iterate through all commits to find the commits that are in the bin
        ... find commits with unique authors
        count them up

        todo seperate by bin initially
        or just once
    '''

    data = []
    for bin in bins:

        item = {"days_since_0" : int(bin.left) if bin.left > 0 else 0}

        if alpha:
            temp = df[df["commitBin"] == bin]
            abs_list = lambda l : [abs(item) for item in l]
            significance = alpha * sum(abs_list(temp["delta_loc"].tolist()))

            bf = 0
            authors = set(temp["author_email"].tolist())
            for author in authors:
                author_dloc = sum(abs_list(temp[temp["author_email"] == author]["delta_loc"].tolist()))
                if author_dloc > significance:
                    bf += 1

            temp = temp[temp["delta_loc"] > significance]

            item["bus_factor"] = bf
        else:
            item["devs"] = len( df[df["commitBin"] == bin]["author_email"].unique() )

        data.append(item)

    return DataFrame(data)


def main() -> None:

    args: Namespace = main_args()

    df = pd.read_json(args.input) #.T
    bf = get_devs(df, bin=args.bin, alpha=0.15)
    devs = get_devs(df, bin=args.bin)

    # import matplotlib.pyplot as plt
    # devs = devs["devs"].tolist()
    # plt.bar([i for i in range(len(devs))], devs, width=4)
    #
    # bf = bf["bus_factor"]
    # plt.bar([i for i in range(len(bf))], bf, width=4)
    #
    # plt.show()
    #
    # quit()
    bf.to_json(args.output, indent=4)


if __name__ == "__main__":
    main()
