Name:       update-motd
Version:    1.1.2
Release:    2%{?dist}
License:    ASL 2.0
Summary:    Framework for dynamically generating MOTD
Group:      System Environment/Base
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
Requires:   bash coreutils
Requires:   system-release >= 1:2-4.amzn2
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
    touch /var/lib/update-motd/motd
    # Backup the current MOTD
    if [ -s /etc/motd -o -L /etc/motd ] && [ "$(readlink /etc/motd)" != "/var/lib/update-motd/motd" ]; then
        mv /etc/motd /etc/motd.rpmsave
        # And let it be the MOTD until update-motd gets run
        cp -L /etc/motd.rpmsave /var/lib/update-motd/motd
    fi
    ln -snf /var/lib/update-motd/motd /etc/motd
fi
%systemd_post update-motd.service

%preun
%systemd_preun update-motd.service

%postun
systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# 1 = Package upgrade, not uninstall
	systemctl try-restart update-motd.service --no-block >/dev/null 2>&1 || :
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
* Tue Oct 16 2018 iliana weller <iweller@amazon.com> - 1.1.2-2
- Don't create an empty /etc/motd.rpmsave

* Mon Jul  9 2018 Chad Miller <millchad@amazon.com> - 1.1.2-1
- Avoid deadlock with systemctlreload-thispackage and Wants:
  cloud-final-which-called-us-to-reload

* Mon Jun 25 2018 Chad Miller <millchad@amazon.com> - 1.1.1-2
- Require the system-release that doesn't hang before installing
- Do not touch sshd's service when install/upgrade/remove update-motd
- Give each hook 10 seconds to finish

* Fri Jun 22 2018 Chad Miller <millchad@amazon.com> - 1.1.1-1
- Don't sleep, but add optional dependence ordering with cloud-init

* Mon Jun 18 2018 Chad Miller <millchad@amazon.com> - 1.1.1-1
- Don't start motd yum before cloud-init has a chance to start

* Fri Dec 22 2017 Chad Miller <millchad@amazon.com> - 1.1.0-1
- Systemdify yum plugin

* Thu Dec  7 2017 Jason Green <jasg@amazon.com>
- Update for systemd

* Fri Oct 31 2014 Andrew Jorgensen <ajorgens@amazon.com>
- Fix cron job per cronie requirements

* Wed Aug 06 2014 Andrew Jorgensen <ajorgens@amazon.com>
- Move cron job from cron.daily to cron.d and add a random delay

* Fri Mar 08 2013 Andrew Jorgensen <ajorgens@amazon.com>
- Use --tmpdir when creating temporary files with mktemp

* Thu Mar 15 2012 Andrew Jorgensen <ajorgens@amazon.com>
- Use --quiet when calling start update-motd

* Wed Sep 21 2011 Andrew Jorgensen <ajorgens@amazon.com>
- Copy the current motd on upgrade
- Add an upgrade case to %post
- Use /var/lib/update-motd instead of /var/run

* Fri Sep 16 2011 Andrew Jorgensen <ajorgens@amazon.com>
- Add a yum plugin to call update-motd after an rpm transaction, and support for disabling updates

* Wed Jul 27 2011 Andrew Jorgensen <ajorgens@amazon.com>
- Various improvements

* Thu Jul 21 2011 Andrew Jorgensen <ajorgens@amazon.com>
- Initial version
