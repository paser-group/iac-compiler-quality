import json
import subprocess
import os
import pickle

def read_issues_from_file(ifile):
    with open(ifile, 'rb') as filehandle:
        return pickle.load(filehandle)

def add_left_overs(l, dir):
    with

def main():
    api_call = "https://api.github.com/repos/ansible/ansible"
    issues_file = "./issues.data"
    issues_dir = "./issues"
    f = open('/home/corbin/.gittoken','r')
    token = f.readlines()[0].split()[0]
    f.close()

    issues = read_issues_from_file(issues_file)
    add_left_overs(issues, issues_dir)

if __name__ == "__main__":
    main()