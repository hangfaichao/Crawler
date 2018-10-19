from py2neo import Graph, Node, NodeMatcher, Relationship
from github import Github, GithubException
import re
import socket
import time

def labelFinded(issue, label_names):
    ok = False
    while not ok:
        try:
            labels = issue.labels
        except GithubException:
            ok = False
        except socket.timeout:
            ok = False
        ok = True
    for label in labels:
        for label_name in label_names:
            if label.name == label_name:
                return True
    return False

def titleMatched(title):
    if re.search(r'bug|error|defect|fail|fault|mistake', title, re.IGNORECASE):
        return True
    else:
        return False

def writeBugToNeo(node, graph):
    bug = Node('Bug', id = node['id'], reported_at = node['created_at'], fixed_at = node['closed_at'], title = node['title'], description = node['body'])
    relationship = Relationship(bug, 'issue', node)
    graph.create(bug)
    graph.create(relationship)

def main():
    repo_name = 'numpy/numpy'
    label_names = ['00 - Bug']
    g = Github("username", "password", timeout = 100)
    repo = g.get_repo(repo_name)
    graph = Graph("http://127.0.0.1:7474", username = 'neo4j', password = 'password')
    matcher = NodeMatcher(graph)
    nodes = list(matcher.match('Issue', html_url__contains = repo_name))

    k = 0
    '''
    # when the crawler stopped
    while k < len(nodes):
        if nodes[k]['number'] == '22120':
            break
        k += 1
    k += 1
    '''
    while k < len(nodes):
        node = nodes[k]
        print(repo_name, node['number'])
        time.sleep(0.8)
        try:
            issue = repo.get_issue(int(node['number']))
        except GithubException:
            continue
        except socket.timeout:
            continue
        print('deciding...')
        if titleMatched(node['title']) or labelFinded(issue, label_names):
            print('writing...')
            writeBugToNeo(node, graph)
        else:
            print('Not a Bug')
        k += 1


if __name__ == '__main__':
    main()
