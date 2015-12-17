%define __protect [ "${RPM_BUILD_ROOT}" != "/" ]
%define __name awscli
%define debug_package %{nil}

Name:           aws-client
Version:        1.9.13
Release:        1%{?dist}.qg
Summary:        Universal Command Line Environment for AWS

Group:          System/Environment
License:        Apache
URL:            https://pypi.python.org/pypi/awscli
#Source0:        https://pypi.python.org/packages/source/a/awscli/awscli-%{version}.tar.gz
Source0:        aws-cli-1.9.13.tar.gz

#BuildRequires:	python-tox = 1.4
#BuildRequires: python-docutils >= 0.10
#BuildRequires: python-sphinx = 1.1.3
#BuildRequires: python-nose = 1.3.0
#BuildRequires: python-colorama >= 0.2.5
#BuildRequires: python-colorama =< 0.3.3
#BuildRequires: python-mock = 1.0.1
#BuildRequires: python-rsa >= 3.1.2
#BuildRequires: python-rsa =< 3.1.4
#BuildRequires: python-wheel = 0.24.0
BuildRequires:  python-tox
BuildRequires:  python-docutils
BuildRequires:  python-sphinx
BuildRequires:  python-nose
BuildRequires:  python-colorama
BuildRequires:  python-mock
BuildRequires:  python-rsa
BuildRequires:  python-wheel

Requires:       botocore
Requires:       python-jmespath
Requires:       python-boto
Requires:       python-tox
Requires:       python-docutils
Requires:       python-sphinx
Requires:       python-nose
Requires:       python-colorama
Requires:       python-mock
Requires:       python-rsa
Requires:       python-wheel

BuildArch:      noarch

%description
This package provides a unified command line interface to Amazon Web Services

%prep
%setup -n aws-cli-%{version}

%build
%{__protect} && %{__python} setup.py build

%install
%{__protect} && %{__python} setup.py install --root=%{buildroot}

%files
%{_bindir}/aws
%{_bindir}/aws.cmd
%{_bindir}/aws_completer
%{_bindir}/aws_zsh_completer.sh

/usr/lib/python2.7/site-packages/awscli
/usr/lib/python2.7/site-packages/awscli-1.9.13-py2.7.egg-info

%changelog
* Thu Dec 17 2015 - <vitvegl@quintagroup.org>
- v1.9.13

* Mon Oct 12 2015 - <vitvegl@quintagroup.org>
- initial build
