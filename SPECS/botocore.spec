%define   debug_package %{nil}

Name:           botocore
Version:        1.3.13
Release:        1%{?dist}.qg
Summary:        A low-level interface to a growing number of Amazon Web Services

Group:          System/Environment
License:        Apache 2.0
URL:            https://github.com/boto/botocore
Source0:        %{name}-%{version}.tar.gz

#BuildRequires:  python-tox == 1.4
#BuildRequires:  python-dateutil >= 2.1
#BuildRequires:  python-dateutil < 3.0.0
#BuildRequires:  python-nose == 1.3.0
#BuildRequires:  python-mock == 1.0.1
#BuildRequires:  python-wheel == 0.24.0
#BuildRequires:  python-docutils >= 0.10
#BuildRequires:  python-behave == 1.2.5

BuildRequires:  python-tox
BuildRequires:  python-dateutil
BuildRequires:  python-dateutil
BuildRequires:  python-nose
BuildRequires:  python-mock
BuildRequires:  python-wheel
BuildRequires:  python-docutils
BuildRequires:  python-behave

Requires:       python-tox
Requires:       python-dateutil
Requires:       python-nose
Requires:       python-mock
Requires:       python-wheel
Requires:       python-docutils
Requires:       python-behave

%description
A low-level interface to a growing number of Amazon Web Services

%prep
%setup -q

%build
%{__python} setup.py build


%install
%{__python} setup.py install --root=%{buildroot}

%files
%doc

%dir /usr/lib/python2.7/site-packages/botocore/
/usr/lib/python2.7/site-packages/botocore/*

%dir /usr/lib/python2.7/site-packages/botocore-%{version}-py2.7.egg-info
/usr/lib/python2.7/site-packages/botocore-%{version}-py2.7.egg-info/*

%changelog

* Thu Dec 17 2015 <vitvegl@quintagroup.org> - 1.3.13-1
- initial build
