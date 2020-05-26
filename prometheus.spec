%define debug_package %{nil}

%define  uid   prometheus
%define  gid   prometheus
%define  nuid  7970
%define  ngid  7970

Name:          prometheus
Summary:       Prometheus systems monitoring and alerting toolkit
Version:       2.18.1
Release:       4%{?dist}
License:       ASL 2.0

Source0:       https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/prometheus.service
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
install -p -D -m 0755 tsdb %{buildroot}%{_bindir}/tsdb

# install unit file
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/%{name}.service

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
      useradd -M -r -u %{nuid} -d %{_sharedstatedir}/minio -g %{gid} %{uid} > /dev/null 2>&1 || :
   else
      useradd -M -r -d %{_sharedstatedir}/minio -g %{gid} %{uid} > /dev/null 2>&1 || :
   fi
fi


%post
%systemd_post minio.service


%preun
%systemd_preun minio.service


%postun
%systemd_postun_with_restart minio.service


%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}
%{_unitdir}/%{name}.service
%attr(755,%{uid},%{gid}) %dir %{_sharedstatedir}/%{name}
%license LICENSE
%doc NOTICE


%changelog
* Tue May 26 2020 Lars Kiesow <lkiesow@uos.de> - 2.18.1-1
- Initial build
