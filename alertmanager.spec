%define debug_package %{nil}

%define  uid   alertmanager
%define  gid   alertmanager
%define  nuid  7972
%define  ngid  7972

Name:          alertmanager
Summary:        Prometheus Alertmanager
Version:       0.21.0
Release:       1%{?dist}
License:       ASL 2.0

Source0:       https://github.com/prometheus/alertmanager/releases/download/v%{version}/alertmanager-%{version}.linux-amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/prometheus.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/prometheus.env
URL:           https://prometheus.io/
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
The Alertmanager handles alerts sent by client applications such as the
Prometheus server. It takes care of deduplicating, grouping, and routing them
to the correct receiver integrations such as email, PagerDuty, or OpsGenie. It
also takes care of silencing and inhibition of alerts.


%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build

%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

# install binary
install -p -D -m 0755 alertmanager %{buildroot}%{_bindir}/alertmanager
install -p -D -m 0755 amtool %{buildroot}%{_bindir}/amtool

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
   alertmanager.yml \
   %{buildroot}%{_sysconfdir}/%{name}/alertmanager.yml

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
* Sun Oct 25 2020 Lars Kiesow <lkiesow@uos.de> - 0.21.0-1
- Initial build
