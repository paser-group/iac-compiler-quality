import json
import subprocess
import os
import pickle

def read_issues_from_file(file):
    with open(file, 'rb') as filehandle:
        return pickle.load(filehandle)

def seperate_by_status(issues):
    open, closed = [], []
    for i in issues:
        if i["state"] == "closed":
            closed.append(int(i["number"]))
        else:
            open.append(int(i["number"]))
    return (open, closed)

def label_in_issue(label, issue):
    try:
        if label in issue["title"].lower():
            return True
    except:
        pass
    try:
        if label in issue["body"].lower():
            return True
    except:
        pass
    try:
        for i in issue["labels"]:
            if label in i["name"].lower():
                return True
    except:
        pass
    return False

def label_in_issues(label, issues):
    open, closed = [], []
    within = False
    for i in issues:
        if i["state"] == "closed":
            within = label_in_issue(label, i)
            if within:
                closed.append(int(i["number"]))
        else:
            within = label_in_issue(label, i)
            if within:
                open.append(int(i["number"]))
    return (open, closed)

def print_all_stats(cats, labels):
    print("-"*95)
    total_issues = len(cats['closed']['all']) + len(cats['open']['all'])
    print(f"total issues: {total_issues}")
    print(f"closed:{len(cats['closed']['all'])} ({((len(cats['closed']['all']) / total_issues) * 100):.2f}%) | ",end='')
    print(f"open:{len(cats['open']['all'])} ({((len(cats['open']['all']) / total_issues) * 100):.2f}%)")
    print("-"*95)
    for i in labels:
        print('{0: <22}'.format("["+i+"]"), end='')
        print('{0: <22}'.format(f"total:{len(cats['closed'][i]) + len(cats['open'][i])} ({(((len(cats['closed'][i])+len(cats['open'][i])) / total_issues) * 100):.2f}%)"), end='')
        print(" |     ", end='')
        print('{0: <22}'.format(f"closed:{len(cats['closed'][i])} ({((len(cats['closed'][i]) / total_issues) * 100):.2f}%)"),end='')
        print(" |     ", end='')
        print(f"open:{len(cats['open'][i])} ({((len(cats['open'][i]) / total_issues) * 100):.2f}%)")
    print("-"*95)

def main():
    repository = "https://api.github.com/repos/ansible/ansible"
    issues_file = "./issues.data"
    temp_issue_file = "./issue"
    issues = read_issues_from_file(issues_file)
    labels = ["error","bug","fix","issue","mistake","incorrect","fault","defect","flaw",
            "solve","race","racy","buffer","overflow","stack","integer","signedness","widthness",
            "underflow","improper","unauthenticated","gain access","permission","crosssite",
            "css","xss","htmlspecialchar","denial service","dos","crash","deadlock","sql",
            "sqli","injection","format","string","printf","scanf","request forgery","csrf",
            "xsrf","forged","security","vulnerability","vulnerable","hole","exploit","attack",
            "bypass","backdoor","threat","expose","breach","violate","fatal","blacklist",
            "overrun","insecure"]

    cats = {}
    cats["closed"] = {}
    cats["open"] = {}
    cats["open"]["all"], cats["closed"]["all"] = seperate_by_status(issues)
    for label in labels:
        cats["open"][label], cats["closed"][label] = label_in_issues(label, issues)

    print_all_stats(cats, labels)

if __name__ == "__main__":
    main()