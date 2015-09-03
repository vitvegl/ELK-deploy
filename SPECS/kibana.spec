%define __protect [ "${RPM_BUILD_ROOT}" != "/" ]
%define __prefix /usr/share

%define __config config.js

%define __bindir bin
%define __confdir config
%define __nodedir node
%define __plugins plugins
%define __modules node_modules
%define __public public
%define __routes routes
%define __views views
%define __srcdir src

%define __mainconf kibana.yml

Name:           kibana
Summary:        Browser based analytics and search dashboard for Elasticsearch
Version:        4.1.1
Release:        2%{?dist}.qg
License:        Apache Software License 2.0
Group:          Logstash/Kibana
Prefix:         %{__prefix}
Url:            https://www.elastic.co/products/%{name}

Source0:	%{name}-%{version}-%{_os}-x86.tar.gz
Source1:	%{name}-%{version}-%{_os}-x64.tar.gz

Source2:	%{name}.service

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}.tmp
BuildRequires:	/bin/sh

Conflicts: 	kibana-pb

%description
Kibana is an open source browser based analytics and search dashboard for Elasticsearch.
Kibana is a snap to setup and start using. Kibana strives to be easy to get started with, 
while also being flexible and powerful, just like Elasticsearch.

%prep

%if 0%{__isa_bits} == 32
[ -d %{_builddir}/%{name}-%{version}-%{_os}-x86 ] && rm -rf %{_builddir}/%{name}-%{version}-%{_os}-x86
mkdir %{_builddir}/%{name}-%{version}-%{_os}-x86
tar -xvpf %{SOURCE0} -C %{_builddir}/
%else
[ -d %{_builddir}/%{name}-%{version}-%{_os}-x64 ] && rm -rf %{_builddir}/%{name}-%{version}-%{_os}-x64
mkdir %{_builddir}/%{name}-%{version}-%{_os}-x64
tar -xvpf %{SOURCE1} -C %{_builddir}/
%endif

%install

%{__protect} && rm -rf ${RPM_BUILD_ROOT}

%{__install} -d %{buildroot}%{__prefix}/%{name}
%{__install} -d %{buildroot}%{__prefix}/%{name}/{%{__bindir},%{__confdir},%{__nodedir},%{__plugins},%{__srcdir}}

%if 0%{__isa_bits} == 32
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x86/%{__bindir}/* %{buildroot}%{__prefix}/%{name}/%{__bindir}
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x86/%{__confdir}/* %{buildroot}%{__prefix}/%{name}/%{__confdir}
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x86/%{__nodedir}/* %{buildroot}%{__prefix}/%{name}/%{__nodedir}
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x86/%{__plugins}/* %{buildroot}%{__prefix}/%{name}/%{__plugins}
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x86/%{__srcdir}/* %{buildroot}%{__prefix}/%{name}/%{__srcdir}

%{__install} -d %{buildroot}/%{_sysconfdir}/{,%{name}}
install -m 0644 %{_builddir}/%{name}-%{version}-%{_os}-x86/config/%{__mainconf} %{buildroot}/%{_sysconfdir}/%{name}

%{__install} -d %{buildroot}/%{_unitdir}
%{__install} -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}

%else
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x64/%{__bindir}/* %{buildroot}%{__prefix}/%{name}/%{__bindir}
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x64/%{__confdir}/* %{buildroot}%{__prefix}/%{name}/%{__confdir}
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x64/%{__nodedir}/* %{buildroot}%{__prefix}/%{name}/%{__nodedir}
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x64/%{__plugins}/* %{buildroot}%{__prefix}/%{name}/%{__plugins}
cp -r %{_builddir}/%{name}-%{version}-%{_os}-x64/%{__srcdir}/* %{buildroot}%{__prefix}/%{name}/%{__srcdir}

%{__install} -d %{buildroot}/%{_sysconfdir}/{,%{name}}
install -m 0644 %{_builddir}/%{name}-%{version}-%{_os}-x64/config/%{__mainconf} %{buildroot}/%{_sysconfdir}/%{name}

%{__install} -d %{buildroot}/%{_unitdir}
%{__install} -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}
%endif

%clean
%if 0%{__isa_bits} == 32
%{__protect} && rm -rf %{_builddir}/%{name}-%{version}-%{_os}-x86 && \
%{__protect} && rm -rf %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}
%else
%{__protect} && rm -rf %{_builddir}/%{name}-%{version}-%{_os}-x64 && \
%{__protect} && rm -rf %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}
%endif

%files
%defattr(-,root,root,-)
%config(noreplace)%{_sysconfdir}/%{name}/%{__mainconf}
%{_unitdir}/%{name}.service
%{__prefix}/%{name}/*

%changelog
* Thu Sep 3 2015 <vitvegl@quintagroup.org> - 4.1.1-2

- bug in %setup macro ( unpack only first tarball ):

- %if 0%{__isa_bits} == 32
- %setup -a0 -n %{name}-%{version}-%{_os}-x86
- %else
- %setup -a1 -n %{name}-%{version}-%{_os}-x64
- %endif

* Wed Jul 22 2015 <vitvegl@quintagroup.org> - 4.1.1-1

* Fri Jul 3 2015 <vitvegl@quintagroup.org> - 4.1.0-1

* Wed May 13 2015 <vitvegl@quintagroup.org> - 4.0.2-1
- initial build
