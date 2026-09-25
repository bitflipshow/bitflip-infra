"""Merge staged metrics credentials into the vault without writing plaintext files."""
import json
import os
from pathlib import Path
import subprocess
import yaml

required = {'vault_metrics_admin_password', 'vault_metrics_hash_secret',
            'vault_metrics_r2_account_id', 'vault_metrics_r2_access_key_id',
            'vault_metrics_r2_secret_access_key'}
values = json.loads(os.environ['METRICS_BOOTSTRAP_JSON'])
if set(values) != required or any(not isinstance(v, str) or not v for v in values.values()):
    raise SystemExit('Invalid staged metrics credential fields')

def vault(args, data=None):
    result = subprocess.run(['ansible-vault', *args], input=data, capture_output=True)
    if result.returncode:
        raise SystemExit('Ansible vault operation failed; output withheld to protect credentials')
    return result.stdout

source = 'group_vars/secrets.yaml'
plaintext = vault(['view', source]).decode()
existing = yaml.safe_load(plaintext)
if not isinstance(existing, dict):
    raise SystemExit('Vault must contain a YAML mapping')
for key, value in values.items():
    if key in existing and existing[key] != value:
        raise SystemExit('An existing metrics value differs; refusing implicit credential rotation')
missing = {key: value for key, value in values.items() if key not in existing}
if missing:
    plaintext = plaintext.rstrip() + '\n\n# Podcast metrics\n' + yaml.safe_dump(missing, sort_keys=True)
    encrypted = vault(['encrypt', '--output', '-'], plaintext.encode())
else:
    encrypted = Path(source).read_bytes()
# Verify the encrypted artifact round-trips before exporting it.
output = Path('metrics-vault.yaml')
output.write_bytes(encrypted)
verified = yaml.safe_load(vault(['view', str(output)]))
if any(verified.get(k) != v for k, v in {**existing, **values}.items()):
    output.unlink()
    raise SystemExit('Vault verification failed')
print('Verified encrypted vault contains all previous values and the five metrics fields.')
