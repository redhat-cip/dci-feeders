Name:       dci-feeders
Version:    0.0.VERS
Release:    1%{?dist}
Summary:    DCI Feeders Ansible Playbook
License:    ASL 2.0
URL:        https://github.com/redhat-cip/dci-feeders
Source0:    dci-feeders-%{version}.tar.gz

BuildArch:  noarch
Requires:   ansible
Requires:   dci-ansible
Requires:   python2-dciclient
Requires:   ansible-role-dci-feeders

%description
An Ansible Playbook that feeds components into the DCI Control Server.

%prep
%setup -qc


%build

%install
mkdir -p %{buildroot}%{_datadir}/dci/dci-feeders
chmod 755 %{buildroot}%{_datadir}/dci/dci-feeders

cp -r group_vars %{buildroot}%{_datadir}/dci/dci-feeders
cp ansible.cfg %{buildroot}%{_datadir}/dci/dci-feeders
cp hosts %{buildroot}%{_datadir}/dci/dci-feeders
cp playbook.yml %{buildroot}%{_datadir}/dci/dci-feeders


%files
%doc
%license LICENSE
%{_datadir}/dci/dci-feeders


%changelog
* Tue May 16 2017 Yanis Guenane <yguenane@redhat.com> - 0.0.1-1
- Initial release
