#!/usr/bin/env python3
#
# Builds the BigFix vars files for the given version and patch level
#
# @author David Lundgren <dlundgren@outsideopen.com>
#

import sys
import os
import yaml
import codecs
import requests
from bs4 import BeautifulSoup

if len(sys.argv) != 3:
    print "Missing an argument"
    print "Usage: generate.py <version> <patch_level>"
    print "\tversion\tThe BigFix Version"
    print "\tpatch  \tThe BigFix Version Patch level"
    sys.exit()

# Maps the names from their full BigFix name to their download name
os_map = {
    "Oracle Enterprise Linux" : "OracleLinux",
    "Red Hat Enterprise Linux": "RedHat",
    # this could be problematic..
    "SUSE Linux Enterprise": "Suse",
}

# Maps the versions from their full BigFix name to their download name
ver_map = {
    "Vista / 2008 (or greater)" : '8',
    "6.1 (TL4 or greater)" : "6",
    "7.x" : "7",
    "5 (Update 5 or greater)" : "5",
}

version   = sys.argv[1]
patch     = sys.argv[2]
path      = os.path.dirname(os.path.abspath(__file__))
info_path = "%s/data/%s.%s" % (path, version, patch)

base_url = "http://support.bigfix.com/bes/release/%s/patch%s/" % (version, patch)
if not os.path.exists(info_path):
    os.makedirs(info_path, 0o755, exist_ok=True)

def download_file(url, target):
    if not os.path.exists(target):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file = open(target, 'wb')
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)

# download the SUMS
sums = {}
sums_file = "%s/SHA256SUMS" % info_path
download_file("%s/SHA256SUMS" % base_url, sums_file)
with open(sums_file) as f:
    for line in f:
        (sum, file) = line.rstrip("\n").split('  ')
        sums[file] = sum

# download the HTML file so that we can parse the info
index_file = "%s/index.html" % info_path
download_file("%s/index.html" % base_url, index_file)
with open(index_file) as f:
    data = f.readlines()

# not sure why the have double headers - dlundgren
data = "\n".join(data[10:-2])

vars_path = "%s/vars" % (path)
if not os.path.exists(vars_path):
    os.mkdir(vars_path, 0o755)

# retrieve the table row data
html = BeautifulSoup(data, "html.parser")
h3_agent = html.body.find('h3', attrs={"id":"agent"})
info = {}
for tr in h3_agent.find_next_sibling().tbody.findAll('tr'):
    obj = {}
    tds = tr.findAll('td')
    file = os.path.basename(tds[4].a.attrs['href'])
    if file in sums:
        _os = tds[0].text
        if _os == "Mac OSX (.pkg)" or _os == "Windows":
            continue
        if _os in os_map:
            _os = os_map[_os]

        _major = tds[1].text
        if ',' in _major:
            _major = _major.split(", ")
        else:
            _major = [_major]

        _arch = tds[2].text.replace(" (little-endian)", "").replace(" (big-endian)", "")
        for m in _major:
            if m in ver_map:
                m = ver_map[m]

            out_file = "%s/%s-%s-%s.yml" % (vars_path, _os, m, _arch)
            data ={
                "bigfix_client_file_dest": file,
                "bigfix_client_file_url": tds[4].a.attrs['href'],
                "bigfix_client_file_sum": sums[file]
            }
            with codecs.open(out_file, 'w', encoding="utf-8") as f:
                f.write("---\n")
                yaml.safe_dump(data, f, default_flow_style=False, default_style='')
    else:
        print "Missing: %s" % file
