import json
import subprocess
import os
import pickle

def read_git_token(file):
    with open(file, 'r') as filehandle:
        return filehandle.readlines()[0].split()[0]
def read_issues_from_file(file):
    with open(file, 'rb') as filehandle:
        return pickle.load(filehandle)
def write_issues_to_file(data, file):
    with open(file, 'wb') as filehandle:
        pickle.dump(data, filehandle)
def check_issues(issues):
    num = 1
    for i in issues:
        if ("url" in i.keys()) and int(i["number"]) == num:
            num = num + 1
            continue
        else:
            return False
    return True
def clean_up_before_exit(issues, temp_file):
    try:
        os.remove(temp_file)
    except:
        pass
    if "url" not in issues[-1].keys():
        issues = issues[:-1]

def request_issue(repository, token, issue_number, tempfile):
    command = "curl -H 'Authorization: token " + token + "' " + repository + "/issues/" + str(issue_number) + " > " + tempfile
    output = subprocess.check_output(command, shell=True)
    fhandle = open(tempfile, "r")
    result = json.load(fhandle)
    fhandle.close()
    os.remove(tempfile)
    return result

def request_all_issues(repository, token, issues, tempfile):
    number = len(issues) + 1
    run = True
    while run:
        data = request_issue(repository, token, number, tempfile)
        if "url" not in data.keys():
            print(data)
            run = False
        else:
            issues.append(data)
        number = number + 1

def main():
    repository = "https://api.github.com/repos/ansible/ansible"
    issues_file = "./issues.data"
    temp_issue_file = "./issue"
    token = read_git_token("./Token.txt")
    issues = read_issues_from_file(issues_file)

    try:
        request_all_issues(repository, token, issues, temp_issue_file)
    except:
        clean_up_before_exit(issues, temp_issue_file)
    finally:
        status = check_issues(issues)
        print(f"\n# Issues: {len(issues)}, Status: {status}")
        write_issues_to_file(issues, issues_file)

if __name__ == "__main__":
    main()
