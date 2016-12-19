Name:           dci-feeders
Version:        0.0.VERS
Release:        1%{?dist}
Summary:        DCI Feeders
License:        ASL 2.0
URL:            https://github.com/redhat-cip/dcifeeder
Source0:        dci-feeders-%{version}.tar.gz
Source1:        dci-feeder@.service
Source2:        dci-feeder@.timer

BuildArch:      noarch

BuildRequires:  systemd
BuildRequires:  systemd-units

Requires:       createrepo
Requires:       python-dciclient
Requires:       python-six
Requires:       python-click
Requires:       python-requests

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Set of feeders for the DCI Control Server


%prep -a
%autosetup -n %{name}-%{version}

%build


%install
install -p -D -m 755 osp.py %{buildroot}/%{_datadir}/%{name}/osp.py
install -p -D -m 755 osp.py %{buildroot}/%{_datadir}/%{name}/rdo.py
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/dci-feeder@.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/dci-feeder@.timer

%post
%systemd_post dci-feeder@.service

%preun
%systemd_preun dci-feeder@.service

%postun
%systemd_postun_with_restart dci-feeder@.service

%files
%doc README.rst
%license LICENSE
%{_datadir}/%{name}/osp.py
%{_datadir}/%{name}/rdo.py
%{_unitdir}


%changelog
* Mon Nov 16 2015 Yanis Guenane <yguenane@redhat.com> 0.1-1
- Initial commit
