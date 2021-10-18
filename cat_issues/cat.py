import json
import subprocess
import os
import pickle

def read_issues_from_file(ifile):
    with open(ifile, 'rb') as filehandle:
        return pickle.load(filehandle)

def main():
    api_call = "https://api.github.com/repos/ansible/ansible"
    issues_file = "./issues.data"
    issues_dir = "./issues"
    f = open('/home/corbin/.gittoken','r')
    token = f.readlines()[0].split()[0]
    f.close()

    issues = read_issues_from_file(issues_file)
    #open_issues, closed_issues = seperate_by_status(issues)



if __name__ == "__main__":
    main()