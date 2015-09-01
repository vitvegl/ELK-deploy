%define debug_package %{nil}
%define __protect [ "{RPM_BUILD_ROOT}" != "/" ]
%define ES_HOME	%{_datarootdir}/elasticsearch

Name:		marvel
Version:	1.3.1
Release:	1%{?dist}
Summary:	Monitor and Optimize Elasticsearch
Group:		Logstash/Marvel
License:	Apache2
URL:		https://www.elastic.co/products/marvel
Source0:	https://download.elasticsearch.org/elasticsearch/%{name}/%{name}-%{version}.zip

BuildArch:	noarch
BuildRequires:	/bin/sh
Requires:	elasticsearch >= 1.5.2

%description
Monitor and Optimize Elasticsearch

%prep
%setup -c %{name}-%{version}

%install

%{__protect} && install -d %{buildroot}/%{ES_HOME}/plugins/%{name}
%{__protect} && install -m 0644 %{name}-%{version}.jar %{buildroot}/%{ES_HOME}/plugins/%{name}/%{name}-%{version}.jar
%{__protect} && install -m 0644 LICENSE.txt %{buildroot}/%{ES_HOME}/plugins/%{name}/LICENSE.txt

%{__protect} && install -d %{buildroot}/%{ES_HOME}/plugins/%{name}/_site

%{__protect} && cp -rv _site/* %{buildroot}/%{ES_HOME}/plugins/%{name}/_site

%files

%dir %{ES_HOME}/plugins/%{name}
%{ES_HOME}/plugins/%{name}/%{name}-%{version}.jar
%{ES_HOME}/plugins/%{name}/LICENSE.txt

%dir %{ES_HOME}/plugins/%{name}/_site
%{ES_HOME}/plugins/%{name}/_site/*

%changelog
* Fri May 22 2015 <vitvegl@quintagroup.org> - 1.3.1-1
- initial build
