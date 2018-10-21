import csv
from github import Github, GithubException

def getIssueNumbers(repo_name):
    numbers = []
    g = Github('username', 'password')
    repo = g.get_repo(repo_name)
    issues = repo.get_issues()
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
    repo_name = 'matplotlib/matplotlib'
    numbers = getIssueNumbers(repo_name)
    
    path = 'filepath'
    writeToCSV(numbers, path)
    
if __name__ == "__main__":
    main()
