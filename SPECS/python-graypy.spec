%define __protect [ "${RPM_BUILD_ROOT}" != "/" ]
%define debug_package %{nil}
%define	_libdir	%{_prefix}/lib

Summary:	Python logging handler that sends messages in GELF
Name:		python-graypy
Provides:	graypy
Version:	0.2.11
Release:	1%{?dist}.qg
Source:		graypy-%{version}.tar.gz
Url:		https://pypi.python.org/pypi/graypy
License:	BSD
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	/bin/sh
BuildRequires:	python >= 2.7.5-5
Requires:	python >= 2.7.5-5 python-amqplib
Conflicts:	python >= 2.8

%description
This package can be used to sent messages to Graylog2 using a custom handler
for the builtin logging library in the Graylog Extended Log Format (GELF).
Alternately, GELFRabbitHandler can be used to send messages to RabbitMQ. Your
Graylog2 server needs to be configured to consume messages via AMQP then. This
prevents log messages from being lost due to dropped UDP packets (GELFHandler
sends messages to Graylog2 using UDP). You will need to configure RabbitMQ
with a 'gelf_log' queue and bind it to the 'logging.gelf' exchange so messages
are properly routed to a queue that can be consumed by Graylog2 (the queue and
exchange names may be customized to your liking).
Graypy can be easily integrated into Django's logging settings.

%prep
%setup -q -n graypy-%{version}

%build
%{__python} setup.py build

%install

%{__python} setup.py install --root=%{buildroot}

%files -n python-graypy

%defattr(-,root,root,-)

%dir %{_libdir}/python2.7/site-packages/graypy
%{_libdir}/python2.7/site-packages/graypy/__init__.py
%{_libdir}/python2.7/site-packages/graypy/__init__.py[co]
%{_libdir}/python2.7/site-packages/graypy/handler.py
%{_libdir}/python2.7/site-packages/graypy/handler.py[co]
%{_libdir}/python2.7/site-packages/graypy/rabbitmq.py
%{_libdir}/python2.7/site-packages/graypy/rabbitmq.py[co]

%dir %{_libdir}/python2.7/site-packages/graypy-%{version}-py2.7.egg-info
%{_libdir}/python2.7/site-packages/graypy-%{version}-py2.7.egg-info/dependency_links.txt
%{_libdir}/python2.7/site-packages/graypy-%{version}-py2.7.egg-info/not-zip-safe
%{_libdir}/python2.7/site-packages/graypy-%{version}-py2.7.egg-info/PKG-INFO
%{_libdir}/python2.7/site-packages/graypy-%{version}-py2.7.egg-info/requires.txt
%{_libdir}/python2.7/site-packages/graypy-%{version}-py2.7.egg-info/SOURCES.txt
%{_libdir}/python2.7/site-packages/graypy-%{version}-py2.7.egg-info/top_level.txt

%changelog
* Wed May 13 2015 <vitvegl@quintagroup.org> - 0.2.11-1
- initial build
