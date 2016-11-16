#!/bin/bash
set -eux
PROJ_NAME=dci-feeders
DATE=$(date +%Y%m%d%H%M)
SHA=$(git rev-parse HEAD | cut -c1-8)

# Configure rpmmacros to enable signing packages
#
echo '%_signature gpg' >> ~/.rpmmacros
echo '%_gpg_name Distributed-CI' >> ~/.rpmmacros

# Create the proper filesystem hierarchy to proceed with srpm creatioon
#
rm -rf ${HOME}/rpmbuild
mock --clean
rpmdev-setuptree
cp ${PROJ_NAME}.spec ${HOME}/rpmbuild/SPECS/
sed -i "s/version='.*'/version='0.0.${DATE}git${SHA}'/" setup.py
python setup.py sdist
cp -v dist/* ${HOME}/rpmbuild/SOURCES/
cp -v systemd/* ${HOME}/rpmbuild/SOURCES/
sed -i "s/VERS/${DATE}git${SHA}/g" ${HOME}/rpmbuild/SPECS/${PROJ_NAME}.spec
rpmbuild -bs ${HOME}/rpmbuild/SPECS/${PROJ_NAME}.spec

for arch in fedora-23-x86_64 fedora-24-x86_64 epel-7-x86_64; do
    rpath=$(echo ${arch}|sed s,-,/,g|sed 's,epel,el,')

    mkdir -p ${HOME}/.mock
    head -n -1 /etc/mock/${arch}.cfg > ${HOME}/.mock/${arch}-with-extras.cfg
    cat <<EOF >> ${HOME}/.mock/${arch}-with-extras.cfg
"""
# NOTE(spredzy) Add signing options
#
config_opts['plugin_conf']['sign_enable'] = True
config_opts['plugin_conf']['sign_opts'] = {}
config_opts['plugin_conf']['sign_opts']['cmd'] = 'rpmsign'
config_opts['plugin_conf']['sign_opts']['opts'] = '--addsign %(rpms)s'
config_opts['use_host_resolv'] = False
config_opts['files']['etc/hosts'] = """
127.0.0.1 pypi.python.org
"""
config_opts['nosync'] = True
EOF

    # Build the RPMs in a clean chroot environment with mock to detect missing
    # BuildRequires lines.
    mkdir -p development
    mock -r ${HOME}/.mock/${arch}-with-extras.cfg rebuild --resultdir=development/${rpath} ${HOME}/rpmbuild/SRPMS/${PROJ_NAME}*
done
