#################################################################
# FILE : moogle.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro 2cs ex6 2022-2023
# DESCRIPTION: A program that operates a sophisticated search engine, called moogle.
#################################################################
##############################################################################
#                                   Imports                                  #
##############################################################################
import bs4
import requests
import urllib.parse
import pickle
import sys
##############################################################################
#                                 CONSTANTS                                  #
CRAWL = "crawl"
PAGE_RANK = "page_rank"
WORDS_DICT = "words_dict"
SEARCH = "search"
PICKLE = ".pickle"
PKL = ".pkl"
##############################################################################
arguments = sys.argv
##############################################################################
#                                  Functions                                 #


def create_internl_dict(pre_url, investigated_url, index_file):
    """This function creates the internal dictionary of links occurrences in a specific site"""
    internal_dict = dict()
    full_url_investigated = urllib.parse.urljoin(pre_url, investigated_url)
    response = requests.get(full_url_investigated)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    with open(index_file, "r") as file:
        num_of_lines = file.readlines()
        for line in num_of_lines:
            full_url_inside = urllib.parse.urljoin(pre_url, line.strip("\n"))
            cnt = 0
            for p in soup.find_all("p"):
                for link in p.find_all("a"):
                    target = link.get("href")
                    if target == line.strip("\n") or target == full_url_inside:
                        cnt += 1
            if cnt > 0:
                internal_dict[line.strip("\n")] = cnt
    return internal_dict


def create_dict_traffic(pre_url, index_file):
    """This function creates the external dictionary for each site, using the aforementioned function and giving back
    the searches dictionary"""
    dict_traffic = dict()
    with open(index_file, "r") as file:
        num_of_lines = file.readlines()
        for line in num_of_lines:
            dict_traffic[line.strip("\n")] = create_internl_dict(pre_url, line.strip("\n"), index_file)
    return dict_traffic


def all_links_from_site(dictionary_searches: dict, key):
    """This function calculates total number of links from specific site"""
    cnt = 0
    for value in dictionary_searches[key]:
        cnt += dictionary_searches[key][value]
    return cnt


def page_rank(iterations, dictionary_searches: dict):
    """This function ranks each site, using the searches dictionary and the page rank algorithm"""
    iterations = int(iterations)
    r = dict()
    if iterations > 0:
        for key in dictionary_searches.keys():
            r[key] = 1
        for num in range(iterations):
            new_r = dict()
            for key in dictionary_searches:
                new_r[key] = 0
            for key in dictionary_searches:
                for value in dictionary_searches[key]:
                    a = (dictionary_searches[key][value] / all_links_from_site(dictionary_searches, key))
                    b = r[key]
                    new_r[value] += (a * b)
            r = new_r
    return r


def word_external_dict_count(pre_url, index_file):
    """This function counts each word from all the websites in a specific site, and giving back a words dictionary"""
    external_dict = dict()
    with open(index_file, "r") as file:
        num_of_lines = file.readlines()
        for line in num_of_lines:
            full_url_investigated = urllib.parse.urljoin(pre_url, line)
            response = requests.get(full_url_investigated)
            html = response.text
            soup = bs4.BeautifulSoup(html, "html.parser")
            for p in soup.find_all("p"):
                content = p.text
                newline_split = content.split()
                for word in newline_split:
                    if word in external_dict:
                        if line.strip("\n") in external_dict[word].keys():
                            external_dict[word][line.strip("\n")] += 1
                        else:
                            external_dict[word][line.strip("\n")] = 1
                    else:
                        external_dict[word] = dict()
                        external_dict[word][line.strip("\n")] = 1
    return external_dict


def moogle_engine(query: str, ranking_dict_file: dict, words_dict_file: dict, max_results):
    """This function operates the search engine, receiving a query and giving sites' rate based on the page rank and
    the words dictionary"""
    ranking_results = dict()
    query_split = query.split()
    items = list(ranking_dict_file.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for site, rank in items:
        query_appearances_site = []
        for word in query_split:
            if word in words_dict_file and site in words_dict_file[word]:
                word_formula = words_dict_file.get(word).get(site)
                if word_formula > 0:
                    query_appearances_site.append(word_formula)
            else:
                break
        if len(query_appearances_site) == len(query_split):
            ranking_results[site] = min(query_appearances_site) * rank
        if len(ranking_results) == int(max_results):
            break
    ranking_items = ranking_results.items()
    sorted_ranking_items = sorted(ranking_items, key=lambda x: x[1], reverse=True)
    for tpl in sorted_ranking_items:
        print(tpl[0], tpl[1])


"""Operating each step in the engine, doesn't have to be executed chronologically"""
if __name__ == '__main__':
    if len(arguments) == 5 and arguments[1] == CRAWL:
        searches_dict = create_dict_traffic(arguments[2], arguments[3])
        filename = arguments[4]

        with open(filename, "wb") as f:
            pickle.dump(searches_dict, f)

    elif len(arguments) == 5 and arguments[1] == PAGE_RANK:
        with open(arguments[3], "rb") as f:
            d = pickle.load(f)
        rate_dict = page_rank(arguments[2], d)
        print(rate_dict)
        filename = arguments[4]

        with open(filename, "wb") as f:
            pickle.dump(rate_dict, f)
    elif len(arguments) == 5 and arguments[1] == WORDS_DICT:
        words_dict = word_external_dict_count(arguments[2], arguments[3])

        filename = arguments[4]

        with open(filename, "wb") as f:
            pickle.dump(words_dict, f)
    elif len(arguments) >= 5 and arguments[1] == SEARCH and "pickle" not in arguments[2]:
        i = 2
        my_query = ""
        while PICKLE not in arguments[i] and PKL not in arguments[i]:
            my_query += arguments[i] + " "
            i += 1
        my_query = my_query[:len(my_query) - 1]

        with open(arguments[i], "rb") as f:
            rate = pickle.load(f)
        with open(arguments[i + 1], "rb") as g:
            words = pickle.load(g)
        moogle_engine(my_query, rate, words, arguments[i + 2])
