%define __protect [ "${RPM_BUILD_ROOT}" != "/" ]
%define __name awscli
%define debug_package %{nil}

Name:		aws-client
Version:	1.8.12
Release:	1%{?dist}.qg
Summary:	Universal Command Line Environment for AWS

Group:		System/Environment
License:	Apache
URL:		https://pypi.python.org/pypi/awscli
Source0:	https://pypi.python.org/packages/source/a/awscli/awscli-%{version}.tar.gz

BuildRequires:	python-tox = 1.4
BuildRequires:  python-docutils >= 0.10
BuildRequires:  python-sphinx = 1.1.3
BuildRequires:  python-nose = 1.3.0
BuildRequires:  python-colorama >= 0.2.5
BuildRequires:  python-colorama =< 0.3.3
BuildRequires:  python-mock = 1.0.1
BuildRequires:  python-rsa >= 3.1.2
BuildRequires:  python-rsa =< 3.1.4
BuildRequires:  python-wheel = 0.24.0

BuildArch: noarch

%description
This package provides a unified command line interface to Amazon Web Services

%prep
%setup -n %{__name}-%{version}

%build
%{__protect} && %{__python} setup.py build

%install
%{__protect} && %{__python} setup.py install --root=%{buildroot}

%clean
%{__protect} && rm -rf ${RPM_BUILD_ROOT}

%files

%dir /usr/lib/python2.7/site-packages/awscli
%dir /usr/lib/python2.7/site-packages/awscli-1.8.12-py2.7.egg-info

%{_bindir}/aws
%{_bindir}/aws.cmd
%{_bindir}/aws_completer
%{_bindir}/aws_zsh_completer.sh

/usr/lib/python2.7/site-packages/awscli/*

/usr/lib/python2.7/site-packages/awscli-1.8.12-py2.7.egg-info/PKG-INFO
/usr/lib/python2.7/site-packages/awscli-1.8.12-py2.7.egg-info/SOURCES.txt
/usr/lib/python2.7/site-packages/awscli-1.8.12-py2.7.egg-info/dependency_links.txt
/usr/lib/python2.7/site-packages/awscli-1.8.12-py2.7.egg-info/requires.txt
/usr/lib/python2.7/site-packages/awscli-1.8.12-py2.7.egg-info/top_level.txt

%changelog
* Mon Oct 12 2015 - <vitvegl@quintagroup.org>
- initial build
