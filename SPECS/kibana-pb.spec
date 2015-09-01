%define _name kibana
%define __protect  [ "${RPM_BUILD_ROOT}" != "/" ]
%define _kh %{_datarootdir}/%{_name}
%define _srcdir %{_name}-%{version}-pb

Name:		kibana-pb
Version:	3.1.2
Release:	1%{?dist}.qg
Summary:	Kibana3 with packetbeat addons

Group:		Logstash/Kibana-packetbeat
License:	Apache	
URL:		https://www.elastic.co/products/kibana
Source0:	v%{version}-pb.tar.gz
BuildArch:	noarch
Requires:	nodejs nodejs-grunt-cli npm rubygem-hashie
Conflicts:	kibana

%description
Kibana is an open source (Apache Licensed), browser based analytics and search dashboard for
ElasticSearch. Kibana is a snap to setup and start using. Written entirely in HTML and Javascript
it requires only a plain webserver, Kibana requires no fancy server side components.
Kibana strives to be easy to get started with, while also being flexible and powerful, just like
Elasticsearch.

%prep
%setup -c %{_name}-%{version}-pb

%install
install -D -m 444 %{_srcdir}/src/index.html %{buildroot}%{_kh}/index.html
install -D -m 444 %{_srcdir}/src/favicon.ico %{buildroot}%{_kh}/favicon.ico

mkdir -p %{buildroot}/%{_kh}/css
install -m 444 %{_srcdir}/src/css/*.* %{buildroot}%{_kh}/css

mkdir -p %{buildroot}/%{_kh}/font
install -m 444 %{_srcdir}/src/font/*.* %{buildroot}%{_kh}/font

mkdir -p %{buildroot}/%{_kh}/img
install -m 444 %{_srcdir}/src/img/*.* %{buildroot}%{_kh}/img

mkdir -p %{buildroot}/%{_kh}/vendor
cp -p -R %{_srcdir}/src/vendor/* %{buildroot}%{_kh}/vendor

mkdir -p %{buildroot}/%{_kh}/app
cp -p -R %{_srcdir}/src/app/* %{buildroot}%{_kh}/app

mkdir -p %{buildroot}/%{_sysconfdir}/%{_name}
install -D -m 444 %{_srcdir}/src/config.js %{buildroot}%{_sysconfdir}/%{_name}/config.js

%files
%dir %{_sysconfdir}/%{_name}

%dir %{_kh}
%{_kh}/index.html
%{_kh}/favicon.ico

%dir %{_kh}/app
%dir %{_kh}/css
%dir %{_kh}/font
%dir %{_kh}/img
%dir %{_kh}/vendor

%{_kh}/app/*
%{_kh}/css/*
%{_kh}/font/*
%{_kh}/img/*
%{_kh}/vendor/*

%config(noreplace) %{_sysconfdir}/%{_name}/config.js

%changelog
* Thu Jul 16 2015 <vitvegl@quintagroup.org> - 3.1.2-1
- initial build
