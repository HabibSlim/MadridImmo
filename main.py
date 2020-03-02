import argparse
import pandas as pd
import operator

from functools import reduce
from multiprocessing import Pool
from models import PisosScraper, HabitacliaScraper, TucasaScraper
from shared import PropType


def parse_params():
    """Parsing input parameters"""

    parser = argparse.ArgumentParser(description='Web scraping real estate prices in Madrid.')
    parser.add_argument('site', metavar='name', type=str, nargs=1,
                        help='website to scrape (pisos, tucasa or habitaclia).',
                        choices={"pisos", "habitaclia", "tucasa"})
    parser.add_argument('target', metavar='type', type=str, nargs=1,
                        help='type of dwellings to target (houses or flats).',
                        choices={"houses", "flats"})
    
    params = parser.parse_args()

    return (params.site[0], params.target[0])


def main():
    """Main procedure."""

    scrapers = {"pisos":PisosScraper, "habitaclia":HabitacliaScraper, "tucasa":TucasaScraper}
    targets = {"houses":PropType.HOUSE, "flats":PropType.FLAT}

    # Parsing parameters
    site, target = parse_params()
    target = targets[target]
    scp = scrapers[site]()

    # Generating URL list
    url_list = scp.gen_urls(target)

    # Assigning jobs
    with Pool(8) as p:
        entries = p.map(scp.parse_page, url_list)

    # Flattening output list
    entries = reduce(operator.concat, entries)

    # Writing output file
    of = scp.of_name(target)
    df = pd.DataFrame(entries)
    df.to_csv(of)

main()