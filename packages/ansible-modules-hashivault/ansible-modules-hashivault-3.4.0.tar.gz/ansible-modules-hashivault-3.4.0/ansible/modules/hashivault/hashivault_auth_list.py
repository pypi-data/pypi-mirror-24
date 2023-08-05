#!/usr/bin/env python
DOCUMENTATION = '''
---
module: hashivault_auth_list
version_added: "2.2.0"
short_description: Hashicorp Vault auth list module
description:
    - Module to list authentication backends in Hashicorp Vault.
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
            - "authentication type to use: token, userpass, github, ldap"
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
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_auth_list:
      register: 'hashivault_auth_list'
'''


def main():
    argspec = hashivault_argspec()
    module = hashivault_init(argspec)
    result = hashivault_auth_list(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


from ansible.module_utils.basic import *
from ansible.module_utils.hashivault import *


@hashiwrapper
def hashivault_auth_list(params):
    client = hashivault_auth_client(params)
    return {'changed': True, 'backends': client.list_auth_backends()}


if __name__ == '__main__':
    main()
