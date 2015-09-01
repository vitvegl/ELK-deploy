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
Release:        1%{?dist}.qg
License:        Apache Software License 2.0
Group:          Logstash/Kibana
Prefix:         %{__prefix}
Url:            https://www.elastic.co/products/%{name}

#Source0:        https://download.elasticsearch.co/kibana/kibana/%{name}-%{version}-%{_os}-x86.tar.gz
#Source1:	https://download.elasticsearch.co/kibana/kibana/%{name}-%{version}-%{_os}-x64.tar.gz

#%if "%{_arch}" == "i386"
#Source0:	%{name}-%{version}-%{_os}-x86.tar.gz
#%else
#Source0:	%{name}-%{version}-%{_os}-x64.tar.gz
#%endif

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

%if "%{_arch}" == "i386"
%setup -a0 -n %{name}-%{version}-%{_os}-x86
%else
%setup -a1 -n %{name}-%{version}-%{_os}-x64
%endif

%install

%{__protect} && rm -rf ${RPM_BUILD_ROOT}

%{__install} -d %{buildroot}%{__prefix}/%{name}
%{__install} -d %{buildroot}%{__prefix}/%{name}/{%{__bindir},%{__confdir},%{__nodedir},%{__plugins},%{__srcdir}}

%{__cp} -r %{__bindir}/* %{buildroot}%{__prefix}/%{name}/%{__bindir}
%{__cp} -r %{__confdir}/* %{buildroot}%{__prefix}/%{name}/%{__confdir}
%{__cp} -r %{__nodedir}/* %{buildroot}%{__prefix}/%{name}/%{__nodedir}
%{__cp} -r %{__plugins}/* %{buildroot}%{__prefix}/%{name}/%{__plugins}
%{__cp} -r %{__srcdir}/* %{buildroot}%{__prefix}/%{name}/%{__srcdir}

%{__install} -d %{buildroot}/%{_sysconfdir}/{,%{name}}
%{__install} -m 0644 config/%{__mainconf} %{buildroot}/%{_sysconfdir}/%{name}

%{__install} -d %{buildroot}/%{_unitdir}
%{__install} -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}

%clean
%{__protect} && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%config(noreplace)%{_sysconfdir}/%{name}/%{__mainconf}
%{_unitdir}/%{name}.service
%{__prefix}/%{name}/*

%changelog
* Wed Jul 22 2015 <vitvegl@quintagroup.org> - 4.1.1-1

* Fri Jul 3 2015 <vitvegl@quintagroup.org> - 4.1.0-1

* Wed May 13 2015 <vitvegl@quintagroup.org> - 4.0.2-1
- initial build
