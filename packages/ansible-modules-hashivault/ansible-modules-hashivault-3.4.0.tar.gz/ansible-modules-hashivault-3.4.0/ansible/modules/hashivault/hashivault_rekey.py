#!/usr/bin/env python
DOCUMENTATION = '''
---
module: hashivault_rekey
version_added: "3.3.0"
short_description: Hashicorp Vault rekey module
description:
    - Module to (update) rekey Hashicorp Vault. Requires that a rekey
      be started with hashivault_rekey_init.
options:
    url:
        description:
            - url for vault
        default: to environment variable VAULT_ADDR
    verify:
        description:
            - verify TLS certificate
        default: to environment variable VAULT_SKIP_VERIFY
    authtype:
        description:
            - authentication type to use: token, userpass, github, ldap
        default: token
    token:
        description:
            - token for vault
        default: to environment variable VAULT_TOKEN
    username:
        description:
            - username to login to vault.
    password:
        description:
            - password to login to vault.
    key:
        description:
            - vault key shard (aka unseal key).
    nonce:
        description:
            - rekey nonce.
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_rekey:
      key: '{{vault_key}}'
      nonce: '{{nonce}}'
'''


def main():
    argspec = hashivault_argspec()
    argspec['key'] = dict(required=True, type='str')
    argspec['nonce'] = dict(required=True, type='str')
    module = hashivault_init(argspec)
    result = hashivault_rekey(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


from ansible.module_utils.basic import *
from ansible.module_utils.hashivault import *


@hashiwrapper
def hashivault_rekey(params):
    key = params.get('key')
    nonce = params.get('nonce')
    client = hashivault_client(params)
    return {'status': client.rekey(key, nonce), 'changed': True}


if __name__ == '__main__':
    main()
