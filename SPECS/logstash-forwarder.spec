#%define debug_package %{nil}
%define __protect [ "${RPM_BUILD_ROOT}" != "/" ]
%define homedir	%{_sharedstatedir}/%{name}
%define __prefix /usr/bin
%define __clonedate 20150312

Summary:	An experiment to cut logs in preparation for processing elsewhere
Name:		logstash-forwarder
Version:	0.4.0
Release:	1git%{__clonedate}%{?dist}.qg
License:	Apache Software License 2.0
Group:		Logstash/forwarder-agent
Prefix:		%{_prefix}
Url:		https://github.com/elasticsearch/%{name}
Source0:	%{name}-%{version}-%{__clonedate}git.tar.xz
Source1:	%{name}-sysconfig

%if %{?fedora} >= 15

Source2:	%{name}.service
Source3:	%{name}.conf.template
Requires(pre):  systemd initscripts
Requires(post): systemd initscripts

%else

Source2:	%{name}.sh
Source3:	%{name}.init
Requires(pre):	initscripts
Requires(post):	initscripts

%endif

BuildRequires:  golang make ruby ruby-devel
Requires(pre):  shadow-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A tool to collect logs locally in preparation for processing elsewhere; using lumberjack protocol

%prep
%setup -q -n %{name}-%{version}

%build
go build

%install

%{__protect} && rm -rf ${RPM_BUILD_ROOT}

%{__install} -d %{buildroot}%{_sharedstatedir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig

%{__protect} && %{__install} -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -d %{buildroot}%{__prefix}
%{__protect} && %{__install} -m 0755 %{_builddir}/%{name}-%{version}/%{name}-%{version} %{buildroot}%{__prefix}/%{name}

%{__protect} && %{__install} -d %{buildroot}%{_sysconfdir}/%{name}

%if %{?fedora} >= 15

%{__install} -d %{buildroot}%{_unitdir}
%{__protect} && %{__install} -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}
%{__protect} && %{__install} -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%else

%{__install} -d %{buildroot}/%{_initdir}
%{__protect} && %{__install} -m 0755 %{SOURCE2} %{buildroot}%{_initdir}/%{name}
%{__protect} && %{__install} -m 0755 %{SOURCE3} %{buildroot}%{__prefix}

%endif


%clean

%{__protect} && rm -r ${RPM_BUILD_ROOT}

%pre

if ! getent group lumberjack >/dev/null; then
/sbin/groupadd -r lumberjack
fi

if ! getent passwd lumberjack >/dev/null; then
/sbin/useradd -r -g lumberjack -d %{homedir} -s /sbin/nologin -c "logstash-forwarder service user" lumberjack
fi

%post

%if %{?fedora} >= 15

if [ $1 -eq 1 ]; then
  systemctl enable %{name}.service
fi

if [ $1 -eq 2 ]; then
  systemctl daemon-reload 2>/dev/null && \
  systemctl restart %{name}.service 2>/dev/null
fi

%else

if [ $1 -eq 1 ]; then
/sbin/chkconfig %{name} on
fi

if [ $1 -eq 2 ]; then
/sbin/service %{name} stop 2>/dev/null && \
/sbin/service %{name} start 2>/dev/null
fi

%endif

%preun

%if %{?fedora} >= 15

if [ $1 -eq 1 ]; then
  systemctl stop %{name}.service && \
  systemctl disable %{name}.service 2>/dev/null
fi

%else

if [ $1 -eq 1 ]; then
  /sbin/chkconfig %{name} off 2>/dev/null
fi

%endif


%postun

%if %{?fedora} >= 15

if [ $1 -eq 0 ]; then
  systemctl daemon-reload
fi

%endif


%files

%defattr(-,root,root,-)
%{__prefix}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%if %{?fedora} >= 15
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/%{name}.conf
%{_unitdir}/%{name}.service

%else

%{__prefix}/%{name}.sh
%{_initddir}/%{name}

%endif

%{_sharedstatedir}/%{name}
%defattr(-,lumberjack,lumberjack,-)

%changelog
* Wed May 13 2015 <vitvegl@quintagroup.org> - 0.4.0-1git20150312
- initial build
