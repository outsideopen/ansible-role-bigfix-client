# Version vars builder

## Pre-Requisites

  - `pip install pyyaml bs4 requests`

## Usage

`generate.py <version> <patch>`

  - *version*: This is the BigFix version number
  - *patch*: This is the BigFix version patch number

## OS Aliases

BigFix may identify differently from Ansible. In these cases we configure the `os_map` variable in the generator.

## Other Notes
For the AIX systems, be sure to set this in your group_vars or host_vars

`bigfix_client_service_name: SBESClientd`