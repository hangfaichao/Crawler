import csv
from github import Github, GithubException
import socket

def getIssueNumbers(repo_name):
    numbers = []
    g = Github('username', 'password', timeout = 100)
    repo = g.get_repo(repo_name)
    ok = False
    while not ok:
        try:
            issues = repo.get_issues()
            ok = True
        except socket.timeout:
            ok = False
    
    for issue in issues:
        numbers.append(issue.number)
        print(issue.number)
    return numbers

def writeToCSV(numbers, path):
    w = csv.writer(open(path, 'w', encoding = 'utf-8', newline = ''))
    w.writerow(['number'])
    for number in numbers:
        w.writerow([number])
        
def main():
    repo_name = 'tensorflow/tensorflow'
    numbers = getIssueNumbers(repo_name)
    
    path = 'file path'
    writeToCSV(numbers, path)

if __name__ == "__main__":
    main()
