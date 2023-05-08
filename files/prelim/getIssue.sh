#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
  echo "----------------------------------------------------------------------------"
  echo $line
  issueNum=`echo $line | tr '/' _`
  echo $issueNum
  curl -H "Accept: application/vnd.github+json" -H "Authorization: Bearer <YOUR_TOKEN_HERE>" https://api.github.com/repos/ansible/ansible/issues/$issueNum > $issueNum.json
  echo "----------------------------------------------------------------------------"
done < "$1" 