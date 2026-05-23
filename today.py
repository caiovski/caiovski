import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree
import time
import hashlib

# Configuration for Caiovski GitHub Telemetry
BIRTHDAY = datetime.datetime(2004, 11, 29)
USER_NAME = os.environ.get('USER_NAME', 'caiovski')
ACCESS_TOKEN = os.environ.get('README_STATS') or os.environ.get('ACCESS_TOKEN')

HEADERS = {'authorization': f'token {ACCESS_TOKEN}'} if ACCESS_TOKEN else {}
QUERY_COUNT = {'user_getter': 0, 'follower_getter': 0, 'graph_repos_stars': 0, 'recursive_loc': 0, 'graph_commits': 0, 'loc_query': 0}
OWNER_ID = None


def daily_readme(birthday):
    """
    Returns length of time since birthday:
    e.g. '21 years, 9 months, 11 days'
    """
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    plural_y = 's' if diff.years != 1 else ''
    plural_m = 's' if diff.months != 1 else ''
    plural_d = 's' if diff.days != 1 else ''
    cake = ' 🎂' if (diff.months == 0 and diff.days == 0) else ''
    return f"{diff.years} year{plural_y}, {diff.months} month{plural_m}, {diff.days} day{plural_d}{cake}"


def query_count(funct_id):
    global QUERY_COUNT
    QUERY_COUNT[funct_id] += 1


def simple_request(func_name, query, variables):
    """
    Returns a request, or raises an Exception if the response does not succeed.
    """
    if not ACCESS_TOKEN:
        raise Exception("ACCESS_TOKEN environment variable is not set.")
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=HEADERS)
    if request.status_code == 200:
        return request
    raise Exception(func_name, ' has failed with status', request.status_code, request.text, QUERY_COUNT)


def user_getter(username):
    query_count('user_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            id
            createdAt
        }
    }'''
    variables = {'login': username}
    request = simple_request(user_getter.__name__, query, variables)
    return {'id': request.json()['data']['user']['id']}, request.json()['data']['user']['createdAt']


def follower_getter(username):
    query_count('follower_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            followers {
                totalCount
            }
        }
    }'''
    request = simple_request(follower_getter.__name__, query, {'login': username})
    return int(request.json()['data']['user']['followers']['totalCount'])


def graph_repos_stars(count_type, owner_affiliation, cursor=None):
    query_count('graph_repos_stars')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                totalCount
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            stargazers {
                                totalCount
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': USER_NAME, 'cursor': cursor}
    request = simple_request(graph_repos_stars.__name__, query, variables)
    if request.status_code == 200:
        if count_type == 'repos':
            return request.json()['data']['user']['repositories']['totalCount']
        elif count_type == 'stars':
            total_stars = 0
            for node in request.json()['data']['user']['repositories']['edges']:
                total_stars += node['node']['stargazers']['totalCount']
            return total_stars


def graph_commits(start_date, end_date):
    query_count('graph_commits')
    query = '''
    query($start_date: DateTime!, $end_date: DateTime!, $login: String!) {
        user(login: $login) {
            contributionsCollection(from: $start_date, to: $end_date) {
                contributionCalendar {
                    totalContributions
                }
            }
        }
    }'''
    variables = {'start_date': start_date, 'end_date': end_date, 'login': USER_NAME}
    request = simple_request(graph_commits.__name__, query, variables)
    return int(request.json()['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions'])


def recursive_loc(owner, repo_name, data, cache_comment, addition_total=0, deletion_total=0, my_commits=0, cursor=None):
    query_count('recursive_loc')
    query = '''
    query ($repo_name: String!, $owner: String!, $cursor: String) {
        repository(name: $repo_name, owner: $owner) {
            defaultBranchRef {
                target {
                    ... on Commit {
                        history(first: 100, after: $cursor) {
                            totalCount
                            edges {
                                node {
                                    author {
                                        user {
                                            id
                                        }
                                    }
                                    deletions
                                    additions
                                }
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }
        }
    }'''
    variables = {'repo_name': repo_name, 'owner': owner, 'cursor': cursor}
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=HEADERS)
    if request.status_code == 200:
        repo_data = request.json().get('data', {}).get('repository')
        if repo_data and repo_data.get('defaultBranchRef'):
            history = repo_data['defaultBranchRef']['target']['history']
            for node in history['edges']:
                author_user = node['node']['author'].get('user')
                if author_user and author_user == OWNER_ID:
                    my_commits += 1
                    addition_total += node['node']['additions']
                    deletion_total += node['node']['deletions']
            if not history['pageInfo'].get('hasNextPage'):
                return addition_total, deletion_total, my_commits
            return recursive_loc(owner, repo_name, data, cache_comment, addition_total, deletion_total, my_commits, history['pageInfo']['endCursor'])
        return 0, 0, 0
    return 0, 0, 0


def loc_query(owner_affiliation, comment_size=0, force_cache=False, cursor=None, edges=[]):
    query_count('loc_query')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 60, after: $cursor, ownerAffiliations: $owner_affiliation) {
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            defaultBranchRef {
                                target {
                                    ... on Commit {
                                        history {
                                            totalCount
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': USER_NAME, 'cursor': cursor}
    request = simple_request(loc_query.__name__, query, variables)
    page_info = request.json()['data']['user']['repositories']['pageInfo']
    fetched_edges = request.json()['data']['user']['repositories']['edges']
    if page_info['hasNextPage']:
        return loc_query(owner_affiliation, comment_size, force_cache, page_info['endCursor'], edges + fetched_edges)
    return cache_builder(edges + fetched_edges, comment_size, force_cache)


def cache_builder(edges, comment_size, force_cache, loc_add=0, loc_del=0):
    cached = True
    os.makedirs('cache', exist_ok=True)
    filename = 'cache/' + hashlib.sha256(USER_NAME.encode('utf-8')).hexdigest() + '.txt'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.readlines()
    except FileNotFoundError:
        data = []
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(data)

    if len(data) - comment_size != len(edges) or force_cache:
        cached = False
        with open(filename, 'w', encoding='utf-8') as f:
            for node in edges:
                f.write(hashlib.sha256(node['node']['nameWithOwner'].encode('utf-8')).hexdigest() + ' 0 0 0 0\n')
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.readlines()

    cache_comment = data[:comment_size]
    data = data[comment_size:]
    for index in range(len(edges)):
        parts = data[index].split()
        if len(parts) >= 2:
            repo_hash = parts[0]
            commit_count = parts[1]
            if repo_hash == hashlib.sha256(edges[index]['node']['nameWithOwner'].encode('utf-8')).hexdigest():
                try:
                    default_ref = edges[index]['node'].get('defaultBranchRef')
                    if default_ref:
                        current_total = default_ref['target']['history']['totalCount']
                        if int(commit_count) != current_total:
                            owner, repo_name = edges[index]['node']['nameWithOwner'].split('/')
                            loc = recursive_loc(owner, repo_name, data, cache_comment)
                            data[index] = f"{repo_hash} {current_total} {loc[2]} {loc[0]} {loc[1]}\n"
                except Exception:
                    pass

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(cache_comment)
        f.writelines(data)

    for line in data:
        loc = line.split()
        if len(loc) >= 5:
            loc_add += int(loc[3])
            loc_del += int(loc[4])
    return [loc_add, loc_del, loc_add - loc_del, cached]


def find_and_replace(root, element_id, new_text):
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text


def justify_format(root, element_id, new_text, length=0):
    if isinstance(new_text, int):
        new_text = f"{'{:,}'.format(new_text)}"
    new_text = str(new_text)
    find_and_replace(root, element_id, new_text)
    just_len = max(0, length - len(new_text))
    if just_len <= 2:
        dot_map = {0: '', 1: ' ', 2: '. '}
        dot_string = dot_map.get(just_len, '')
    else:
        dot_string = ' ' + ('.' * just_len) + ' '
    find_and_replace(root, f"{element_id}_dots", dot_string)


def svg_overwrite(filename, age_data, commit_data, star_data, repo_data, contrib_data, follower_data, loc_data):
    """
    Parse SVG file and update dynamic telemetry elements
    """
    if not os.path.exists(filename):
        return
    tree = etree.parse(filename)
    root = tree.getroot()
    find_and_replace(root, 'age_data', age_data)
    justify_format(root, 'commit_data', commit_data, 17)
    justify_format(root, 'star_data', star_data, 11)
    justify_format(root, 'repo_data', repo_data, 6)
    justify_format(root, 'contrib_data', contrib_data)
    justify_format(root, 'follower_data', follower_data, 7)
    justify_format(root, 'loc_data', loc_data[2], 9)
    justify_format(root, 'loc_add', loc_data[0])
    justify_format(root, 'loc_del', loc_data[1], 7)
    tree.write(filename, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    print(f"Caiovski GitHub Profile Update — User: {USER_NAME}")
    age_str = daily_readme(BIRTHDAY)
    print(f"Current calculated Uptime: {age_str}")

    if not ACCESS_TOKEN:
        print("Notice: README_STATS / ACCESS_TOKEN not set in local environment.")
        print("Updating local SVGs with uptime and preserving base telemetry values.")
        for fname in ['dark_mode.svg', 'light_mode.svg']:
            if os.path.exists(fname):
                tree = etree.parse(fname)
                root = tree.getroot()
                find_and_replace(root, 'age_data', age_str)
                tree.write(fname, encoding='utf-8', xml_declaration=True)
        print("SVGs successfully updated with current uptime!")
    else:
        user_data, user_created = user_getter(USER_NAME)
        OWNER_ID = user_data
        print(f"Owner ID: {OWNER_ID}, Account Created: {user_created}")

        star_data = graph_repos_stars('stars', ['OWNER'])
        repo_data = graph_repos_stars('repos', ['OWNER'])
        contrib_data = graph_repos_stars('repos', ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'])
        follower_data = follower_getter(USER_NAME)
        total_loc = loc_query(['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'])

        # Calculate commits across account lifetime
        creation_year = int(user_created[:4])
        current_year = datetime.datetime.now().year
        total_commits = 0
        for y in range(creation_year, current_year + 1):
            s_date = f"{y}-01-01T00:00:00Z"
            e_date = f"{y}-12-31T23:59:59Z"
            total_commits += graph_commits(s_date, e_date)

        for index in range(len(total_loc) - 1):
            total_loc[index] = '{:,}'.format(total_loc[index])

        svg_overwrite('dark_mode.svg', age_str, total_commits, star_data, repo_data, contrib_data, follower_data, total_loc[:-1])
        svg_overwrite('light_mode.svg', age_str, total_commits, star_data, repo_data, contrib_data, follower_data, total_loc[:-1])
        print("GitHub Telemetry successfully updated in dark_mode.svg and light_mode.svg!")
