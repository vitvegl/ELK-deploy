### %define debug_package %{nil}

Summary:		Packetbeat network agent
Name:			packetbeat
Version:		1.0.0.Beta2
Release:		1%{dist}.qg
Source0:		v1.0.0.Beta2.tar.gz
Source1:		%{name}.service
BuildRoot:		%{_tmppath}/%{name}
Group:			Network
License:		GPLv2
URL:			http://packetbeat.com
Requires:		libpcap >= 1.7.3
Requires(post):		systemd
Requires(preun):	systemd
Requires(preun):	systemd

Patch0:			Makefile.patch

BuildRequires:		git bzr python-virtualenv libpcap-devel
BuildRequires:		golang golang-src golang-vet
%if 0%{__isa_bits} == 32
BuildRequires:		golang-pkg-linux-386
%else
BuildRequires:		golang-pkg-linux-amd64
%endif

%description
Packetbeat agent.

%prep
%setup -n %{name}-1.0.0-beta2
%patch0

%build
export GOPATH="%{_builddir}/go"
make deps && make 

%install
make install DESTDIR=%{buildroot} && \
#mv %{buildroot}/%{name}-%{version} %{buildroot}/%{name}
mkdir -p %{buildroot}%{_unitdir}
install %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service

%clean
make clean && rm -r ${RPM_BUILD_ROOT}

%files
/usr/bin/%{name}
%config %{_sysconfdir}/%{name}/%{name}.yml
%config %{_sysconfdir}/%{name}/%{name}.template.json
%{_unitdir}/%{name}.service
%doc debian/copyright

%post
systemctl enable %{name}.service

%preun
systemctl stop %{name}.service
systemctl disable %{name}.service

%changelog
* Wed Jul 16 2015 <vitvegl@quintagroup.org> - 1.0.0.Beta2
- initial build + Makefile fix
