Name:       update-motd
Version:    0.1
Release:    1%{?dist}
License:    ASL 2.0
Summary:    Framework for dynamically generating MOTD
Group:      System Environment/Base
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
Requires:   bash coreutils
Requires:   upstart

Source0:    sbin_update-motd
Source1:    cron_update-motd
Source2:    upstart_update-motd.conf

%description
Framework and scripts for producing a dynamically generated Message Of The Day. 
Based on and compatible with the framework implemented Ubuntu.

%install
install -d %{buildroot}/etc/update-motd.d
install -D -m 0755 %{SOURCE0} %{buildroot}/usr/sbin/update-motd
install -D -m 0755 %{SOURCE1} %{buildroot}/etc/cron.daily/update-motd
install -D -m 0444 %{SOURCE2} %{buildroot}/etc/init/update-motd.conf
# for %ghost
install -d %{buildroot}/var/run
touch %{buildroot}/var/run/motd

%clean
rm -rf %{buildroot}

%post
# Only run this on initial install
if [ "$1" = "1" ]; then
    # Backup the current MOTD
    if [ -e /etc/motd ] && [ "$(readlink /etc/motd)" != "/var/run/motd" ]; then
        cp /etc/motd /etc/motd.rpmsave
        # And let it be the MOTD until update-motd gets run
        mv /etc/motd /var/run/motd
    fi
    ln -snf /var/run/motd /etc/motd
fi
# We don't run update-motd on install because the various update-motd.d scripts
# are not installed yet (since their packages will depend on this one).
# This could also be the case in an upgrade situation, so we leave it to cron.

%files
%defattr(-,root,root,-)
%dir /etc/update-motd.d
%config /etc/cron.daily/update-motd
%config /etc/init/update-motd.conf
%ghost /var/run/motd
/usr/sbin/update-motd

%changelog
