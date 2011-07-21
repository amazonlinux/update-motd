Name:       update-motd
Version:    0.1
Release:    1%{?dist}
License:    Apache License, Version 2.0
Summary:    Framework for dynamically generating MOTD
Group:      System Environment/Base
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

Source0:    sbin_update-motd
Source1:    upstart_update-motd.conf
Source2:    cron_update-motd

%description
Framework and scripts for producing a dynamically generated Message Of The Day. 
Based on and compatible with the framework implemented Ubuntu.

%install
install -d %{buildroot}/etc/update-motd.d
install -D -m 0755 %{SOURCE0} %{buildroot}/usr/sbin/update-motd
install -D -m 0755 %{SOURCE1} %{buildroot}/etc/cron.daily/update-motd
install -D -m 0444 %{SOURCE2} %{buildroot}/etc/init/update-motd.conf
ln -s /var/run/motd %{buildroot}/etc/motd


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir /etc/update-motd.d
%config /etc/cron.daily/update-motd
%config /etc/init/update-motd.conf
%config /etc/motd
%ghost /var/run/motd
%ghost /var/run/motd.tmp
/usr/sbin/update-motd

%changelog
