from py2neo import Graph, Node ,NodeMatcher
from github import Github, GithubException
import csv
import time
import requests
import socket

def getIssueNumbers(path):
	with open(path, 'r') as f:
		reader = csv.DictReader(f)
		return [int(row['number']) for row in reader]

def fromGithub(issue, flag):
    if flag == "pull":
        pull = issue
        data = [pull.id, pull.number, pull.html_url, pull.title, pull.body, pull.state, pull.merged, 
            pull.created_at, pull.updated_at, pull.closed_at ,pull.merged_at, pull.comments, 
            pull.review_comments, pull.commits, pull.additions, pull.deletions, pull.changed_files]
    elif flag == "issue":
        data = [issue.id, issue.number, issue.html_url, issue.title, issue.body, issue.state, 
            issue.created_at, issue.updated_at, issue.closed_at, issue.comments]
    return [str(item) for item in data]

def toNeo(data, graph, flag):
    #matcher = NodeMatcher(graph)
    #print(matcher.match("Issue", number = '1').first())
    if flag == "pull":
        node = Node("Pull", id = data[0], number = data[1], html_url = data[2], title = data[3], body = data[4], state = data[5], merged = data[6], 
            created_at = data[7], updated_at = data[8], closed_at = data[9] ,merged_at = data[10], comments = data[11], 
            review_comments = data[12], commits = data[13], additions = data[14], deletions = data[15], changed_files = data[16])
    elif flag == "issue":
        node = Node("Issue", id = data[0], number = data[1], html_url = data[2], title = data[3], body = data[4], state = data[5], 
            created_at = data[6], updated_at = data[7], closed_at = data[8] ,comments = data[9])
    graph.create(node)


def main():
    numbers = getIssueNumbers('path of csvfile stored issue numbers')
    g = Github("username", "password", timeout = 100)
    repo = g.get_repo('numpy/numpy')
    graph = Graph("http://127.0.0.1:7474",username="neo4j",password="password")
    k = 0
    '''
    # when crawler stopped
    while k < len(numbers):
        if numbers[k] == 617:
            break
        k += 1
    k += 1
    '''
    while k < len(numbers):
        number = numbers[k]
        try:
            issue = repo.get_issue(number)
        except requests.exceptions.ConnectionError:
            continue
        except socket.timeout:
            continue
        print('numpy', number)
        try:
            issue = issue.as_pull_request()
            flag = "pull"
        except GithubException:
            flag = "issue"
        except requests.exceptions.ConnectionError:
            continue
        except socket.timeout:
            continue
        print("data crawling...")
        time.sleep(0.6)
        data = fromGithub(issue, flag)
        print("data inputing...")
        toNeo(data, graph, flag)
        print("successed")
        k += 1
    

if __name__ == "__main__":
    main()
