#!/usr/bin/env -S just --justfile

# Ansible playbook against specific host
run HOST *TAGS:
  ansible-playbook -b playbook.yaml --limit {{HOST}} {{TAGS}}

# docker compose against remote host via Ansible
compose HOST *V:
  ansible-playbook playbook.yaml --limit {{HOST}} --tags compose {{V}}

##########
## repo stuff

# updates submodules
sub-update:
  git submodule sync --recursive
  git submodule update --init --recursive --progress
  git submodule status

# init submodules (first run once in a blank repo)
sub-init:
  git submodule update --init --recursive

# add a submodule under roles/ (explicit name, no auto-commit)
sub-add URL NAME:
  git submodule add {{URL}} "roles/{{NAME}}"
  git submodule update --init --recursive

# optionally use --force to force reinstall all requirements
reqs *FORCE:
	ansible-galaxy install -r requirements.yaml {{FORCE}}

# just vault (encrypt/decrypt/edit)
vault ACTION:
    EDITOR='code --wait' ansible-vault {{ACTION}} group_vars/secrets.yaml
