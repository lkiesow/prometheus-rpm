%define debug_package %{nil}

%define  uid   sslexporter
%define  gid   sslexporter
%define  nuid  7973
%define  ngid  7973

Name:          ssl_exporter
Summary:       SSL Certificate Exporter
Version:       2.1.1
Release:       1%{?dist}
License:       ASL 2.0

Source0:       https://github.com/ribbybibby/ssl_exporter/releases/download/v%{version}/%{name}_%{version}_linux_amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.env
URL:           https://github.com/ribbybibby/ssl_exporter
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
Exports Prometheus metrics for SSL certificates


%prep
%setup -q

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
%doc NOTICE


%changelog
* Sun Oct 25 2020 Lars Kiesow <lkiesow@uos.de> - 2.1.1-1
- Initial build
