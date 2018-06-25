Name:       update-motd
Version:    1.1.1
Release:    1%{?dist}
License:    ASL 2.0
Summary:    Framework for dynamically generating MOTD
Group:      System Environment/Base
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
Requires:   bash coreutils
BuildRequires: systemd-devel
%{?systemd_requires}

Source0:    sbin_update-motd
Source1:    cron_update-motd
Source2:    update-motd.service
Source3:    yum_update-motd.py
Source4:    yum_update-motd.conf

%description
Framework and scripts for producing a dynamically generated Message Of The Day.
Based on and compatible with the framework implemented Ubuntu.

%install
rm -rf %{buildroot}
install -d %{buildroot}/etc/update-motd.d
install -D -m 0755 %{SOURCE0} %{buildroot}/usr/sbin/update-motd
install -D -m 0644 %{SOURCE1} %{buildroot}/etc/cron.d/update-motd
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/update-motd.service
install -D -m 0644 %{SOURCE3} %{buildroot}/usr/lib/yum-plugins/update-motd.py
install -D -m 0644 %{SOURCE4} %{buildroot}/etc/yum/pluginconf.d/update-motd.conf
# for %ghost
install -d %{buildroot}/var/lib/update-motd
touch %{buildroot}/var/lib/update-motd/motd

%clean
rm -rf %{buildroot}

%post
# Only run this on initial install
if [ "$1" = "1" ]; then
    # Backup the current MOTD
    if [ -e /etc/motd ] && [ "$(readlink /etc/motd)" != "/var/lib/update-motd/motd" ]; then
        mv /etc/motd /etc/motd.rpmsave
        # And let it be the MOTD until update-motd gets run
        cp -L /etc/motd.rpmsave /var/lib/update-motd/motd
    fi
    ln -snf /var/lib/update-motd/motd /etc/motd
elif [ "$1" = "2" ]; then
    if [ -e /etc/motd ] && [ "$(readlink /etc/motd)" = "/var/run/motd" ]; then
        # Copy the current motd
        cp -L /etc/motd /var/lib/update-motd/motd
        ln -snf /var/lib/update-motd/motd /etc/motd
    fi
fi
%systemd_post update-motd.service sshd.socket

%preun
%systemd_preun update-motd.service sshd.socket

%postun
systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# 1 = Package upgrade, not uninstall
	systemctl try-restart update-motd.service sshd.socket --no-block >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%dir /etc/update-motd.d
%dir /var/lib/update-motd
%config /etc/cron.d/update-motd
%config %{_unitdir}/update-motd.service
%config /etc/yum/pluginconf.d/update-motd.conf
/usr/sbin/update-motd
/usr/lib/yum-plugins/update-motd.py*
%ghost /var/lib/update-motd/motd

%changelog

