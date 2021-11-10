# Pleaase ONLY UNCOMMENT ONE line to simplify the output.

# See the rate limit for the provided user:
curl -u USER:TOKEN -H "Accept: application/vnd.github.v3+json" https://api.github.com/rate_limit

# See information for a certain user (if you provide creds, you get more info)
#curl -u USER:TOKEN -H "Accept: application/vnd.github.v3+json" https://api.github.com/users/USER

# Pull a certain issue number using a token.
#curl -H 'Authorization: TOKEN' https://api.github.com/repos/ansible/ansible/issues/ISSUE_NUM
