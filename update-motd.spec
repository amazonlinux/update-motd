Name:       update-motd
Version:    2.3
Release:    1%{?dist}
License:    ASL 2.0
Summary:    Framework for dynamically generating MOTD
URL:        https://github.com/amazonlinux/update-motd
Group:      System Environment/Base
BuildArch:  noarch
Requires:   bash coreutils
Requires:   system-release >= 2022
BuildRequires: systemd-devel
%{?systemd_requires}

Source0:    sbin_update-motd
Source1:    update-motd.timer
Source2:    update-motd.service

%description
Framework and scripts for producing a dynamically generated Message Of The Day.
Based on and compatible with the framework implemented Ubuntu.

%install
rm -rf %{buildroot}
install -d %{buildroot}/etc/update-motd.d
install -D -m 0755 %{SOURCE0} %{buildroot}/usr/sbin/update-motd
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/update-motd.timer
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/update-motd.service
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
%config %{_unitdir}/update-motd.{service,timer}
/usr/sbin/update-motd
%ghost /var/lib/update-motd/motd

%changelog
* Thu Mar 14 2024 Keith Gable <gablk@amazon.com> - 2.3-1
- Make update-motd.service depend on network-online.target and cloud-final.service
  if available.
* Mon Feb 05 2024 Stewart Smith <trawets@amazon.com> - 2.2-1
- Restrict startup and runtime CPU and IO usage

* Fri Aug 11 2023 Stephen A. Zarkos <szarkos@amazon.com> - 2.1-1.amzn2023.0.1
- Copy the final $TMPFILE using 'mv -Z' to ensure the motd file inherits
  the selinux context of the destination directory.
- Lock down the update-motd.service file to remove unneeded permissions
  and capabilities.

* Wed Mar 15 2023 Stewart Smith <trawets@amazon.com> 2.1
- Replace update-motd motd part even when it's zero sized
- This fixes https://github.com/amazonlinux/amazon-linux-2023/issues/286

* Thu Mar 09 2023 Nikhil Dikshit <nikhildi@amazon.com> 2.0-1.amzn2023.0.3
- Migrated Cron job to Systemd timer
- Trigger update-motd.service after cloud-final.service
- Set RemainAfterExit=no on update-motd so that timer can restart it after exit

* Thu Feb 02 2023 Stewart Smith <trawets@amazon.com> - 2.0-1.amzn2023.0.2
- Mass rebuild for AL2023

* Tue Oct 04 2022 Stewart Smith <trawets@amazon.com> - 2.0-1.amzn2022.0.1
- AL2022 pre-GA mass rebuild

* Mon Oct 18 2021 Stewart Smith <trawets@amazon.com> - 2.0-1
- Initial build for AL2022

* Mon Jun 07 2021 Sonia Xu <sonix@amazon.com> - 1.1.2-2.amzn2.0.2
- Changed the timeout to 30 from 10 seconds in update-motd script

* Tue Apr 20 2021 Sonia Xu <sonix@amazon.com> - 1.1.2-2.amzn2.0.1
- Changed the random delay to 24 hours from 6 hours

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
