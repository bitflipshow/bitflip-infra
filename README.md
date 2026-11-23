# bitflipshow/bitflip-infra

This repo deploys the BitFlip podcast infrastructure.

There are a set of self-hosted services that use a combination of Tailscale, Cloudflare, and local AI to bring the show to life every 2 weeks.

## Add or change a service

This repo uses [`ironicbadger/ansible-role-docker-compose-generator`](https://github.com/ironicbadger/ansible-role-docker-compose-generator) to ingest configuration files and output a fully formatted `compose.yaml` file.

- To add a service, create a numbered directory under [`services/infra-svcs/`](services/infra-svcs/) with a `compose.yaml`. Use an existing directory as a template.
- To change a service, edit its `compose.yaml` and any config files in the same directory.
- Put shared settings in [`group_vars/infra-svcs.yaml`](group_vars/infra-svcs.yaml) and keep secrets in Ansible Vault.

## Deploy

Commit your changes on a branch, push it, and open a pull request. Merging into `main` automatically deploys to production. A direct push to `main` also triggers a deploy.

The [deploy workflow](.github/workflows/deploy-infra-svcs.yaml) joins the tailnet and runs Ansible over Tailscale SSH to assemble and apply the Docker Compose stack on the production VM. Check the `Deploy infra-svcs` job in GitHub Actions for the result.
