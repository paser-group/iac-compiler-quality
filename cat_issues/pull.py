import json
import subprocess
import os
import pickle

STARTING_NUM = 9424

def request_issue(api_call, token, number, output_file):
    command = "curl -H 'Authorization: token " + token + "' " + api_call + "/issues/" + str(number) + " > " + output_file
    print(command)
    subprocess.check_output(command, shell=True)
    with open(output_file, "r") as fhandle:
        y = json.load(fhandle)
        try:
            temp = y["url"]
            return True
        except KeyError:
            pass
    os.remove(output_file)
    return False

def request_all_issues(api_call, token, directory):
    try:
        os.mkdir(directory)
    except OSError as error:
        pass

    global STARTING_NUM
    output = directory + "/" + str(STARTING_NUM)
    run = True
    while run:
        if not os.path.isfile(output):
            run = request_issue(api_call, token, STARTING_NUM, output)
        STARTING_NUM = STARTING_NUM + 1
        output = directory + "/" + str(STARTING_NUM)

def main():
    api_call = "https://api.github.com/repos/ansible/ansible"
    issue_dir = "./issues"
    f = open('/home/corbin/.gittoken','r')
    token = f.readlines()[0].split()[0]
    f.close()

    request_all_issues(api_call, token, issue_dir)

if __name__ == "__main__":
    main()