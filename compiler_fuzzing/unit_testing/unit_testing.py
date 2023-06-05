from compiler_fuzzing.github_scraper import GithubScraper

from .test_groups import (
    test_github_scraper,
)

from compiler_fuzzing.utils import (
    strings,
    display,
    validate,
)

def unit_test(cfg):
    # start routine
    print_review_data = cfg['unit_testing']['print_review_data']
    display.title('BEGIN UNIT TESTING')

    """ unit testing starts """

    # test github scraper
    test_github_scraper(cfg)

    """ unit testing ends """

    # exit routine
    display.title('END UNIT TESTING')
