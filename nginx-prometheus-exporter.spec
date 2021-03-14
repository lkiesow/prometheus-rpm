%define debug_package %{nil}

%define  uid   nginxexporter
%define  gid   nginxexporter
%define  nuid  7975
%define  ngid  7975

Name:          nginx-prometheus-exporter
Summary:       NGINX Prometheus Exporter
Version:       0.8.0
Release:       1%{?dist}
License:       ASL 2.0

Source0:       https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v%{version}/nginx-prometheus-exporter-%{version}-linux-amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/nginx-prometheus-exporter.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/nginx-prometheus-exporter.env
Source3:       https://raw.githubusercontent.com/nginxinc/nginx-prometheus-exporter/v%{version}/LICENSE
URL:           https://github.com/nginxinc/nginx-prometheus-exporter
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
NGINX Prometheus exporter makes it possible to monitor NGINX or NGINX Plus
using Prometheus.


%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build

%install
rm -rf %{buildroot}

# install binary
install -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

# install unit file
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/%{name}.service

# install systemd environment file
install -p -D -m 0644 \
   %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/default/%{name}

# license
cp %{SOURCE3} .

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
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_unitdir}/%{name}.service
%license LICENSE


%changelog
* Sun Mar 14 2021 Lars Kiesow <lkiesow@uos.de> - 0.8.0-1
- Initial build
