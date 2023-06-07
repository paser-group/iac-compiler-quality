# external imports
import json
import sys
from pprint import pprint

# local imports
from compiler_fuzzing.github_scraper import GithubScraper
from compiler_fuzzing.utils import (
    display,
    validate,
    menus,
)

def test_github_scraper(cfg):
    print_review_data = cfg['unit_testing']['print_review_data']
    end = '\n\n' if print_review_data else ' '

    display.title('Testing compiler_fuzzing.github_scraper.GithubScraper', fill_char='.')

    display.note(
        'GithubScraper tests only test for non-empty responses. '
        + 'for further data inspection set cfg["unit_testing"][print_review_data"] to False'
    )

    # define scraper object
    gs = GithubScraper(cfg)

    # test get_issue_data function
    test_case = 'testing GithubScraper.get_issue_data(58813) ...'
    display.testing(test_case, end=end)
    try:
        data = gs.get_issue_data(58813)

        if data is not None:

            if print_review_data:
                display.review('--- contents from output of get_issue_data(58813) ---')
                pprint(data)
        
            display.test_passed(end='\n\n')
        else:
            print()
            display.fail(test_case, end='\n\n')

    except Exception as e:
        display.fail('GithubScraper.get_issue_data(58813) crashed during execution')
        display.exception(str(e), end='\n\n')


    # test list_branches()
    test_case = 'testing GithubScarper.list_branches() ...'
    display.testing(test_case, end=end)
    try:
        data = gs.list_branches()
        if data is not None:

            if print_review_data:
                display.review('--- contents from output of list_branches() ---')
                pprint(data)

            display.test_passed(end='\n\n')
        else:
            display.fail(test_case, end='\n\n')

    except Exception as e:
        print()
        display.fail('GithubScraper.list_branches() crashed during execution')
        display.exception(str(e), end='\n\n')

    # test commit_collector
    test_case = 'testing GithubScraper.collect_commits(n_samples=100, progbar=False) ...'
    display.testing(test_case, end=end)
    try:
        data = gs.collect_commits(n_samples=100, progbar=False)
        if data is not None:

            if print_review_data:
                display.review('--- contents from output of collect_commits() ---')
                pprint(data)
            breakpoint()
            display.test_passed()
        else:
            display.fail(test_case)
    except Exception as e:
        display.fail('GithubScraper.collect_commits() crashed during execution')
        display.exception(str(e), end='\n\n')
    
    display.title('Finished Testing compiler_fuzzing.github_scraper.GithubScraper', fill_char='.')
