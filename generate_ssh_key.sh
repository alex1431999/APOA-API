#!/bin/bash

python --version
# install ssh-agent
'which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )'
# run ssh-agent
eval $(ssh-agent -s)
# add ssh key stored in SSH_PRIVATE_KEY variable to the agent store
ssh-add <(echo "$SSH_PRIVATE_KEY")
# disable host key checking (NOTE: makes you susceptible to man-in-the-middle attacks)
# WARNING: use only in docker container, if you use it with shell you will overwrite your user's ssh config
mkdir -p ~/.ssh
echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
# Install requirements
python3 -m pip install -r requirements.txt
