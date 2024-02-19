# Ansible Role: BigFix Client

Installs the BigFix Client for various Linux Servers

## Requirements

A BigFix server

## Role Variables

Set the version/development kit of Java to install, along with any other necessary Java packages. Some other options include are included in the distribution-specific files in this role's 'defaults' folder.

    bigfix_client_conf_dir: /etc/opt/BESClient
    bigfix_client_server_name: bigfix.example.com
    bigfix_client_server_port: 52311
    
    bigfix_client_service_name: besclient
    
    # On AIX
    bigfix_client_service_name: SBESClientd

## Overriding a detect OS installer

You can now set `bigfix_client_override_vars` as a mapping from one detect os to another.

```yaml
---
bigfix_client_override_vars:
  Debian-12-x86_64: Debian-11-x86_64
```

## Re-install or update

You may use `bigfix_update: true` to have the client be re-installed. Useful for new versions

## Example Playbook

    - hosts: all
      roles:
        - outsideopen.bigfix_client

## License

MIT / BSD

## Author Information

This role was created in 2016 by [David Lundgren](https://www.github.com/dlundgren/).