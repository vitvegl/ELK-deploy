%define __protect [ "${RPM_BUILD_ROOT}" != "/" ]
%define _libdir %{_prefix}/lib
%define debug_package %{nil}

Name:           journal2gelf
Version:        0.0.3
Release:        1%{?dist}.qg
Summary:        Export structured log records from the systemd journal and send them to a Graylog2 server as GELF messages
License:        GPLv3
URL:            https://github.com/systemd/journal2gelf
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.env
BuildArch:      noarch
BuildRequires:  /bin/sh python >= 2.7.5
Requires:       systemd >= 204 python-graypy

%description
Export structured log records from the systemd journal and send them to a Graylog2 server as GELF messages

%prep
%setup -q -n %{name}-%{version}

%build
%{__protect} && %{__python} setup.py build

%install
%{__protect} && %{__python} setup.py install --root=%{buildroot}
%{__protect} && %{__install} -d %{buildroot}/%{_sysconfdir}
%{__protect} && %{__install} -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}
%{__protect} && %{__install} -d %{buildroot}/%{_unitdir}
%{__protect} && %{__install} -m 0644 %{name}.service %{buildroot}/%{_unitdir}

%clean
%{__protect} && rm -rf ${RPM_BUILD_ROOT}

%post
if [ -f %{_sysconfdir}/systemd/system/%{name}.service ]; then
	yes|rm %{_sysconfdir}/systemd/system/%{name}.service
fi

if [ $1 -eq 1 ]; then
  systemctl enable %{name}.service
fi

if [ $1 -eq 2 ]; then
  systemctl stop %{name}.service && \
  systemctl daemon-reload 2>/dev/null
fi

%preun

if [ $1 -eq 0 ]; then
  systemctl disable %{name}.service && \
  systemctl stop %{name}.service
fi

if [ $1 -eq 1 ]; then
  systemctl daemon-reload 2>/dev/null
fi

%postun

if [ $1 -eq 0 ]; then
  systemctl daemon-reload 2>/dev/null
fi

if [ $1 -eq 1 ]; then
  systemctl daemon-reload 2>/dev/null
fi

%files
%{_sysconfdir}/%{name}.env
%{_bindir}/%{name}
%{_libdir}/python2.7/site-packages/%{name}-%{version}-py2.7.egg-info
%{_unitdir}/%{name}.service

%changelog
* Wed May 13 2015 <vitvegl@quintagroup.org> - 0.0.3-1
- initial build
