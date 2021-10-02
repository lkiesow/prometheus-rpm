%define debug_package %{nil}

%define  uid   prometheus
%define  gid   prometheus
%define  nuid  7970
%define  ngid  7970

Name:          prometheus
Summary:       Prometheus systems monitoring and alerting toolkit
Version:       2.30.2
Release:       3%{?dist}
License:       ASL 2.0

Source0:       https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/prometheus.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/prometheus.env
URL:           https://prometheus.io/
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
An open-source monitoring system with a dimensional data model, flexible query
language, efficient time series database and modern alerting approach.


%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build

%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

# Maybe for console templates?
#install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

# install binary
install -p -D -m 0755 prometheus %{buildroot}%{_bindir}/prometheus
install -p -D -m 0755 promtool %{buildroot}%{_bindir}/promtool

# install unit file
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/%{name}.service

# install systemd environment file
install -p -D -m 0644 \
   %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/default/%{name}

# install configuration
install -p -D -m 0644 \
   prometheus.yml \
   %{buildroot}%{_sysconfdir}/%{name}/prometheus.yml
cp -r consoles console_libraries \
   %{buildroot}%{_sysconfdir}/%{name}/

%clean
rm -rf %{buildroot}


%pre
# Create user and group if nonexistent
# Try using a common numeric uid/gid if possible
if [ ! $(getent group %{gid}) ]; then
   if [ ! $(getent group %{ngid}) ]; then
      groupadd -r -g %{ngid} %{gid} > /dev/null 2>&1 || :
   else
      groupadd -r %{gid} > /dev/null 2>&1 || :
   fi
fi
if [ ! $(getent passwd %{uid}) ]; then
   if [ ! $(getent passwd %{nuid}) ]; then
      useradd -M -r -u %{nuid} -g %{gid} %{uid} > /dev/null 2>&1 || :
   else
      useradd -M -r -g %{gid} %{uid} > /dev/null 2>&1 || :
   fi
fi


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_unitdir}/%{name}.service
%attr(755,%{uid},%{gid}) %dir %{_sharedstatedir}/%{name}
%license LICENSE
%doc NOTICE


%changelog
* Sat Oct 02 2021 Lars Kiesow <lkiesow@uos.de> - 2.30.2-3
- Update to 2.30.2

* Wed Sep 29 2021 Lars Kiesow <lkiesow@uos.de> - 2.30.1-3
- Update to 2.30.1

* Wed Sep 15 2021 Lars Kiesow <lkiesow@uos.de> - 2.30.0-3
- Update to 2.30.0

* Sat Aug 28 2021 Lars Kiesow <lkiesow@uos.de> - 2.29.2-3
- Update to 2.29.2

* Thu Aug 12 2021 Lars Kiesow <lkiesow@uos.de> - 2.29.1-3
- Update to 2.29.1

* Fri Jul 02 2021 Lars Kiesow <lkiesow@uos.de> - 2.28.1-3
- Update to 2.28.1

* Tue Jun 22 2021 Lars Kiesow <lkiesow@uos.de> - 2.28.0-3
- Update to 2.28.0

* Wed May 19 2021 Lars Kiesow <lkiesow@uos.de> - 2.27.1-3
- Update to 2.27.1

* Thu May 13 2021 Lars Kiesow <lkiesow@uos.de> - 2.27.0-3
- Update to 2.27.0

* Thu Apr 01 2021 Lars Kiesow <lkiesow@uos.de> - 2.26.0-3
- Update to 2.26.0

* Wed Mar 17 2021 Lars Kiesow <lkiesow@uos.de> - 2.25.2-3
- Update to 2.25.2

* Mon Mar 15 2021 Lars Kiesow <lkiesow@uos.de> - 2.25.1-3
- Update to 2.25.1

* Thu Feb 18 2021 Lars Kiesow <lkiesow@uos.de> - 2.25.0-3
- Update to 2.25.0

* Thu Jan 21 2021 Lars Kiesow <lkiesow@uos.de> - 2.24.1-3
- Update to 2.24.1

* Thu Jan 07 2021 Lars Kiesow <lkiesow@uos.de> - 2.24.0-3
- Update to 2.24.0

* Fri Nov 27 2020 Lars Kiesow <lkiesow@uos.de> - 2.23.0-3
- Update to 2.23.0

* Tue Nov 17 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.2-3
- Update to 2.22.2

* Fri Nov 06 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.1-3
- Update to 2.22.1

* Sun Nov 01 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.0-3
- Allow setting additional parameters

* Sun Oct 25 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.0-2
- Fix systemd actions

* Mon Oct 19 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.0-1
- Update to 2.22.0

* Mon Oct 12 2020 Lars Kiesow <lkiesow@uos.de> - 2.21.0-3
- By default, listen to 127.0.0.1 only

* Mon Oct 12 2020 Lars Kiesow <lkiesow@uos.de> - 2.21.0-2
- Removed tsdb binary

* Mon Oct 12 2020 Lars Kiesow <lkiesow@uos.de> - 2.21.0-1
- Update to 2.21.0

* Tue May 26 2020 Lars Kiesow <lkiesow@uos.de> - 2.18.1-1
- Initial build
