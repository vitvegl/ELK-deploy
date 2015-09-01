%define debug_package %{nil}
%define __protect [ "{RPM_BUILD_ROOT}" != "/" ]
%define ES_HOME	%{_datarootdir}/elasticsearch

Name:		shield
Version:	1.2.1
Release:	1%{?dist}.qg
Summary:	Security mechanism for Elasticsearch

Group:		Logstash/Shield
License:	Apache2
URL:		https://www.elastic.co/products/shield
Source0:	https://download.elasticsearch.org/elasticsearch/%{name}/%{name}-%{version}.zip

BuildArch:	noarch
BuildRequires:	/bin/sh
Requires:	elasticsearch >= 1.5.2

%description
Security mechanism for Elasticsearch

%prep
%setup -c %{name}-%{version}

%install

%{__protect} && install -d %{buildroot}/%{ES_HOME}/bin/%{name}
%{__protect} && install -m 0755 bin/esusers %{buildroot}/%{ES_HOME}/bin/%{name}
%{__protect} && install -m 0755 bin/syskeygen %{buildroot}/%{ES_HOME}/bin/%{name}

%{__protect} && install -d %{buildroot}/%{ES_HOME}/config/%{name}
%{__protect} && install -m 0644 config/logging.yml %{buildroot}/%{ES_HOME}/config/%{name}/logging.yml
%{__protect} && install -m 0644 config/role_mapping.yml %{buildroot}/%{ES_HOME}/config/%{name}/role_mapping.yml
%{__protect} && install -m 0644 config/roles.yml %{buildroot}/%{ES_HOME}/config/%{name}/roles.yml
%{__protect} && install -m 0644 config/users %{buildroot}/%{ES_HOME}/config/%{name}/users
%{__protect} && install -m 0644 config/users_roles %{buildroot}/%{ES_HOME}/config/%{name}/users_roles

%{__protect} && install -d %{buildroot}/%{ES_HOME}/plugins/%{name}

%{__protect} && install -m 0644 automaton-1.11-8.jar %{buildroot}/%{ES_HOME}/plugins/%{name}/automaton-1.11-8.jar
%{__protect} && install -m 0644 commons-codec-1.10.jar %{buildroot}/%{ES_HOME}/plugins/%{name}/commons-codec-1.10.jar
%{__protect} && install -m 0644 elasticsearch-%{name}-%{version}.jar %{buildroot}/%{ES_HOME}/plugins/%{name}/elasticsearch-%{name}-%{version}.jar
%{__protect} && install -m 0644 unboundid-ldapsdk-2.3.8.jar %{buildroot}/%{ES_HOME}/plugins/%{name}/unboundid-ldapsdk-2.3.8.jar

%{__protect} && install -m 0644 LICENSE.txt %{buildroot}/%{ES_HOME}/plugins/%{name}/LICENSE.txt
%{__protect} && install -m 0644 NOTICE.txt %{buildroot}/%{ES_HOME}/plugins/%{name}/NOTICE.txt

%files

%defattr(-,elasticsearch,elasticsearch,-)

%dir %{ES_HOME}/bin/%{name}

%{ES_HOME}/bin/%{name}/esusers
%{ES_HOME}/bin/%{name}/syskeygen

%defattr(-,elasticsearch,elasticsearch,-)

%dir %{ES_HOME}/config/%{name}

%{ES_HOME}/config/%{name}/logging.yml
%{ES_HOME}/config/%{name}/role_mapping.yml
%{ES_HOME}/config/%{name}/roles.yml
%{ES_HOME}/config/%{name}/users
%{ES_HOME}/config/%{name}/users_roles

%defattr(-,root,root,-)

%dir %{ES_HOME}/plugins/%{name}

%{ES_HOME}/plugins/%{name}/automaton-1.11-8.jar
%{ES_HOME}/plugins/%{name}/commons-codec-1.10.jar
%{ES_HOME}/plugins/%{name}/elasticsearch-%{name}-%{version}.jar
%{ES_HOME}/plugins/%{name}/unboundid-ldapsdk-2.3.8.jar

%{ES_HOME}/plugins/%{name}/LICENSE.txt
%{ES_HOME}/plugins/%{name}/NOTICE.txt

%changelog
* Fri May 22 2015 <vitvegl@quintagroup.org> - 1.2.1-1
- initial build
