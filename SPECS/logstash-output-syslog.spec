%define ES_HOME /usr/lib/logstash

Name:		logstash-output-syslog
Version:	1.4.4
Release:	1%{?dist}.qg
Summary:	Logstash output plugins, which send events to a syslog server

Group:		Logstash
License:	Apache
URL:		https://www.elastic.co/products/logstash
Source0:	%{name}_quinta.rb
Requires:	logstash = 1.4.4
Conflicts:	logstash < 1.4.4 logstash > 1.4.4 logstash >= 1.5.0

BuildArch:	noarch

%description
Logstash output plugins, which send events to a syslog server (RFC 5424)

%install

install -d  %{buildroot}/%{ES_HOME}/lib/logstash/outputs

install -m 755 %{SOURCE0} %{buildroot}/%{ES_HOME}/lib/logstash/outputs/syslog_quinta.rb


%files
%{ES_HOME}/lib/logstash/outputs/syslog_quinta.rb

%changelog
* Wed Jul 29 2015 <vitvegl@quintagroup.org> - 1.4.4-1
* Wed Jul 22 2015 <vitvegl@quintagroup.org> - 1.4.2-1
- initial build
