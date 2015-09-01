%define	__protect	[ "${RPM_BUILD_ROOT}" != "/" ]

%define	_libdir		%{_prefix}/lib
%global	homedir		%{_sharedstatedir}/%{name}
%global	logdir		%{_localstatedir}/log/%{name}
%global	piddir		%{_localstatedir}/run/%{name}
%global plugindir	%{_libdir}/%{name}/lib
%global	ES_HOME		%{_datarootdir}/%{name}

Name:			elasticsearch
Version:		1.7.1
Release:		1%{?dist}.qg
Provides:		elasticsearch
Summary:		Distributed RESTful search engine built for the cloud
Group:			Logstash/ElasticSearch
License:		Apache 2.0
URL:			https://www.elastic.co/products/elasticsearch
Source0:		%{name}-%{version}.tar.gz
Source1:		%{name}.sysctl.d
Source2:		%{name}.tmpfiles.d
Source3:		%{name}.env
Source4:		%{name}.service
Source5:		%{name}.logrotate

Requires:		systemd ruby jruby
%if 0%{?fedora} == 21
Requires:		java-1.8.0-openjdk
%else
Requires:               java-1.7.0-openjdk
%endif

%description
Elasticsearch is a distributed RESTful search engine built for the cloud


%prep

%setup -q

%install

%{__protect} && %{__install} -d %{buildroot}/%{_libdir}/sysctl.d
%{__protect} && %{__install} -m 0644 %{SOURCE1} %{buildroot}/%{_libdir}/sysctl.d/%{name}.conf

%{__protect} && %{__install} -d %{buildroot}/%{_libdir}/tmpfiles.d
%{__protect} && %{__install} -m 0644 %{SOURCE2} %{buildroot}/%{_libdir}/tmpfiles.d/%{name}.conf

%{__protect} && %{__install} -d %{buildroot}%{_sysconfdir}
%{__protect} && %{__install} -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}

%{__protect} && %{__install} -d %{buildroot}%{_unitdir}
%{__protect} && %{__install} -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}

%{__protect} && %{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__protect} && %{__install} -m 0644 config/%{name}.yml %{buildroot}%{_sysconfdir}/%{name}
%{__protect} && %{__install} -m 0644 config/logging.yml %{buildroot}%{_sysconfdir}/%{name}

%{__protect} && %{__install} -d  %{buildroot}%{_localstatedir}/log/%{name}

%{__protect} && %{__install} -d %{buildroot}%{_sysconfdir}/logrotate.d
%{__protect} && %{__install} -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{__protect} && %{__install} -d %{buildroot}/%{ES_HOME}
%{__protect} && for i in LICENSE NOTICE ; do %{__install} -m 0644 $i.txt %{buildroot}/%{ES_HOME} ; done
%{__protect} && %{__install} -m 0644 README.textile %{buildroot}/%{ES_HOME}

%{__protect} && %{__install} -d %{buildroot}/%{ES_HOME}/bin
%{__protect} && %{__install} -m 0755 bin/%{name}{,.in.sh} %{buildroot}/%{ES_HOME}/bin
%{__protect} && %{__install} -m 0755 bin/plugin %{buildroot}/%{ES_HOME}/bin

%{__protect} && %{__install} -d %{buildroot}/%{ES_HOME}/lib
%{__protect} && %{__install} -d %{buildroot}/%{ES_HOME}/lib/sigar
%{__protect} && %{__install} -m 0644 lib/sigar/sigar-1.6.4.jar %{buildroot}/%{ES_HOME}/lib/sigar

%if "%{_arch}" == "i386"
	%{__protect} && %{__install} -m 0755 lib/sigar/libsigar-x86-%{_os}.so %{buildroot}/%{ES_HOME}/lib/sigar
  %else
	%{__protect} && %{__install} -m 0755 lib/sigar/libsigar-amd64-%{_os}.so %{buildroot}/%{ES_HOME}/lib/sigar
%endif

%{__protect} && %{__install} -m 0644 lib/*.jar  %{buildroot}/%{ES_HOME}/lib

%{__protect} && %{__install} -d %{buildroot}/{%{homedir},%{piddir}}

%pre

if ! getent group elasticsearch >/dev/null; then
  /sbin/groupadd -r elasticsearch
fi

if ! getent passwd elasticsearch >/dev/null; then
  /sbin/useradd -r -g elasticsearch -d %{homedir} -s /sbin/nologin -c "ElasticSearch service user" elasticsearch
fi

%post

if [ $1 -eq 1 ]; then
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
%{__protect} && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)

%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/%{name}.yml
%{_sysconfdir}/%{name}/logging.yml
%{_unitdir}/%{name}.service
%{_libdir}/sysctl.d/%{name}.conf
%{_libdir}/tmpfiles.d/%{name}.conf

%dir %{ES_HOME}
%{ES_HOME}/*

%{_sysconfdir}/%{name}.env

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%defattr(-,%{name},%{name},-)
%dir %{logdir}/
%dir %{piddir}/
%dir %{homedir}/

%changelog
* Thu Jul 30 2015 <vitvegl@quintagroup.org> - 1.7.1-1
- version 1.7.1
- Search bugfix: _only_nodes preference parsed incorrectly (issue: #12389)

* Wed Jul 22 2015 <vitvegl@quintagroup.org> - 1.7.0-1
- version 1.7.0

* Fri Jul 3 2015 <vitvegl@quintagroup.org> - 1.6.0-1
- version 1.6.0

* Wed May 13 2015 <vitvegl@quintagroup.org> - 1.5.2-1
- initial build
