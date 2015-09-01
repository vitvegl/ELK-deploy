%define	_protect	[ "${RPM_BUILD_ROOT}" != "/" ]
%global	homedir		%{_sharedstatedir}/%{name}
%global	logdir		%{_localstatedir}/log/%{name}
%global	piddir		%{_localstatedir}/run/%{name}
%global plugindir	%{_libdir}/%{name}/lib
%global	LS_home		%{_libdir}/%{name}

Name:			logstash
Version:		1.4.4
Release:		1%{?dist}.qg
Provides:		logstash-server
Summary:		A tool for managing events and logs
Group:			System Environment/Daemons
License:		ASL 2.0
URL:			http://logstash.net
Source0:		https://download.elasticsearch.org/logstash/logstash/%{name}-%{version}.tar.gz
Source1:		logstash.wrapper
Source2:		logstash.logrotate
Source3:		logstash.init
Source4:		logstash.env
Source5:		logstash.service
BuildArch:		noarch

AutoReqProv:		no
Requires:		systemd
%if 0%{?fedora} == 21
Requires:		java-1.8.0-openjdk
%else
Requires:               java-1.7.0-openjdk
%endif
Requires:		ruby
Requires:		jruby
Requires(post):		openssl

Conflicts:		logstash < 1.4.4
Conflicts:		logstash > 1.4.4

#Conflicts:		%{name} < %{version}-%{release}
#Conflicts:		%{name} > %{version}-%{release}
#Conflicts:		logstash-contrib < %{version}-%{release}
#Conflicts:		%{name}-contrib > %{version}-%{release}

%description
A tool for managing events and logs.

%prep
%setup -q

%install
%{_protect} && %{__install} -d %{buildroot}%{_sysconfdir}
%{_protect} && %{__install} -m 644 %{_sourcedir}/%{name}.env %{buildroot}%{_sysconfdir}

%{__sed} -i \
  -e "s|@@@NAME@@@|%{name}|g" \
  -e "s|@@@CONFDIR@@@|%{_sysconfdir}/%{name}/conf.d|g" \
  -e "s|@@@LOGDIR@@@|%{logdir}|g" \
  -e "s|@@@PLUGINDIR@@@|%{plugindir}|g" \
  -e "s|@@@JAVA_IO_TMPDIR@@@|%{piddir}/java_io|g" \
  %{buildroot}%{_sysconfdir}/%{name}.env

%{_protect} && %{__install} -d %{buildroot}%{_unitdir}
%{_protect} && %{__install} -m 644 %{_sourcedir}/%{name}.service %{buildroot}%{_unitdir}
%{__sed} -i \
  -e "s|@@@LS_HOME@@@|%{LS_home}|g" \
  -e "s|@@@CONFDIR@@@|%{_sysconfdir}/%{name}.d|g" \
  -e "s|@@@USRSHARE@@@|%{plugindir}|g" \
  -e "s|@@@ENVFILE@@@|%{_sysconfdir}/%{name}.env|g" \
  %{buildroot}/%{_unitdir}/%{name}.service

%{_protect} && %{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{_protect} && %{__install} -d %{buildroot}%{_sysconfdir}/%{name}/conf.d
%{_protect} && %{__install} -d  %{buildroot}%{_localstatedir}/log/%{name}
%{_protect} && %{__install} -D -m 644 %{_sourcedir}/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{_protect} && %{__install} -d %{buildroot}%{piddir}
%{_protect} && %{__install} -d %{buildroot}%{piddir}/java_io

%{_protect} && %{__install} -d %{buildroot}%{LS_home}/lib
%{_protect} && %{__install} -d %{buildroot}%{LS_home}/patterns
%{_protect} && %{__install} -d %{buildroot}%{LS_home}/locales
%{_protect} && %{__install} -d %{buildroot}%{LS_home}/vendor
%{_protect} && %{__install} -d %{buildroot}%{LS_home}/bin
%{_protect} && %{__install} -d %{buildroot}%{LS_home}/spec

cp -ar patterns/*  %{buildroot}%{LS_home}/patterns/
cp -ar lib/*  %{buildroot}%{LS_home}/lib/
cp -ar locales/*  %{buildroot}%{LS_home}/locales/
cp -ar vendor/*  %{buildroot}%{LS_home}/vendor/
cp -ar bin/*  %{buildroot}%{LS_home}/bin/
cp -ar spec/* %{buildroot}%{LS_home}/spec/

%{_protect} && %{__install} -d  %{buildroot}%{homedir}

%pre
if ! getent group logstash >/dev/null; then
  /sbin/groupadd -r logstash
fi

if ! getent passwd logstash >/dev/null; then
  /sbin/useradd -r -g logstash -d %{homedir} -s /sbin/nologin -c "Logstash service user" logstash
fi

%post
if [ $1 -eq 1 ]; then
#%{__post_job} && \
systemctl enable %{name}.service
fi

%preun
systemctl stop %{name}.service
systemctl disable %{name}.service

%postun
if [ $1 -eq 0 ]; then
systemctl daemon-reload
fi

%clean
%{_protect} && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_unitdir}/*

%dir %{LS_home}
%{LS_home}/*

%{_sysconfdir}/%{name}.env

%dir %{_sysconfdir}/%{name}/conf.d

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%defattr(-,%{name},%{name},-)
%dir %{logdir}/
%dir %{piddir}/
%dir %{homedir}/

%changelog
* Tue Jul 28 2015 vitvegl@quintagroup.org 1.4.4-1
- Update logstash to version 1.4.4

* Wed May 13 2015 vitvegl@quintagroup.org 1.4.2-2
- rebuild

* Tue Mar 10 2015 vitvegl@quintagroup.org 1.4.2-2
- fc21 fix (openjdk-1.8.0 as required dependency)
- fc21 fix (package jpackage-utils was renamed)

* Wed Jan 28 2015 vgologuz@redhat.com 1.4.2-1
- Updated to new upstream distribution format. Replaced sysv init script with
  systemd unit. Current RPM target: Fedora 20+.

* Mon Jan 26 2015 BogusDateBot
- Eliminated rpmbuild "bogus date" warnings due to inconsistent weekday,
  by assuming the date is correct and changing the weekday.
  Tue Jan 11 2013 --> Tue Jan 08 2013 or Fri Jan 11 2013 or Tue Jan 15 2013 or ....
  Mon Feb 06 2014 --> Mon Feb 03 2014 or Thu Feb 06 2014 or Mon Feb 10 2014 or ....

* Thu Feb 06 2014 lars.francke@gmail.com 1.3.3-2
- Start script now allows multiple server types (web & agent) at the same time (Thanks to Brad Quellhorst)
- Logging can be configured via LOGSTASH_LOGLEVEL flag in /etc/sysconfig/logstash
- Default log level changed from INFO TO WARN

* Mon Jan 20 2014 dmaher@mozilla.com 1.3.3-1
- Update logstash to version 1.3.3

* Fri Jan 10 2014 lars.francke@gmail.com 1.3.2-1
- Update logstash to version 1.3.2 (Thanks to Brad Quellhorst)

* Thu Dec 12 2013 lars.francke@gmail.com 1.3.1-1
- Update logstash to version 1.3.1
- Fixed Java version to 1.7 as 1.5 does not work

* Wed Dec 11 2013 lars.francke@gmail.com 1.2.2-2
- Fixed reference to removed jre7 package
- Fixed rpmlint warning about empty dummy.rb file
- Fixes stderr output not being captured in logfile
- Fixed home directory location (now in /var/lib/logstash)

* Mon Oct 28 2013 lars.francke@gmail.com 1.2.2-1
- Update logstash version to 1.2.2
- Change default log level from WARN to INFO

* Wed Jun 12 2013 lars.francke@gmail.com 1.1.13-1
- Update logstash version to 1.1.13

* Thu May 09 2013 dmaher@mozilla.com 1.1.12-1
- Update logstash version to 1.1.12

* Thu Apr 25 2013 dmaher@mozilla.com 1.1.10-1
- Use flatjar instead of monolithic
- Update logstash version to 1.1.10

* Tue Jan 22 2013 dmaher@mozilla.com 1.1.9-1
- Add chkconfig block to init
- Update logstash version to 1.1.9

* Fri Jan 11 2013 lars.francke@gmail.com 1.1.5-1
- Initial version
