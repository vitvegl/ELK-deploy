%define	__protect	[ "${RPM_BUILD_ROOT}" != "/" ]
#%define __autoinstall_contrib 	bin/plugin install contrib
%global plugindir	%{_libdir}/logstash/lib/logstash
%global	LS_home		%{_libdir}/logstash

%define __codecs_dir	%{plugindir}/codecs
%define __inputs_dir	%{plugindir}/inputs
%define __filters_dir	%{plugindir}/filters
%define __outputs_dir	%{plugindir}/outputs
%define __util_dir	%{plugindir}/util

%define __lslibs_dir	%{LS_home}/lib
%define __spec_dir	%{LS_home}/spec
%define __vendor_dir	%{LS_home}/vendor
#%define __gemspecdir	%{__vendor_dir}/bundle/jruby/1.9/specifications

Name:			logstash-contrib
Version:		1.4.2
Release:		2%{?dist}.qg
Provides:		logstash-contrib-plugins
Summary:		Logstash contrib plugins
Group:			Logstash/contrib-plugins
License:		ASL 2.0
URL:			http://logstash.net
Source:			https://download.elasticsearch.org/logstash/logstash/%{name}-%{version}.tar.gz
BuildArch:		noarch
Requires:		logstash

Conflicts:		logstash < 1.4.2
Conflicts:		logstash > 1.4.2

Conflicts:		logstash-contrib < 1.4.2
Conflicts:		logstash-contrib > 1.4.2

#Conflicts:		logstash < %{version}-%{release}.%{_arch}
#Conflicts:		logstash > %{version}-%{release}.%{_arch}

%description
Contrib plugins for logstash-1.4.2

%prep
%setup -q

%install

### Official recommends

#if [ "$PWD" = "%{_builddir}/%{name}-%{version}" ]; then
#	%{__autoinstall_contrib}
#else
#	cd %{_builddir}/%{name}-%{version} && %{__autoinstall_contrib}
#fi

%{__protect} && %{__install} -d %{buildroot}%{__lslibs_dir}
%{__protect} && %{__install} -d %{buildroot}%{__spec_dir}
%{__protect} && %{__install} -d %{buildroot}%{__vendor_dir}

%{__protect} && %{__install} -d %{buildroot}%{__codecs_dir}
%{__protect} && %{__install} -d  %{buildroot}%{__inputs_dir}
%{__protect} && %{__install} -d  %{buildroot}%{__filters_dir}
%{__protect} && %{__install} -d  %{buildroot}%{__outputs_dir}
%{__protect} && %{__install} -d %{buildroot}%{__lslibs_dir}
%{__protect} && %{__install} -d %{buildroot}%{__vendor_dir}

cp -av lib/*  %{buildroot}%{__lslibs_dir}
cp -av spec/* %{buildroot}%{__spec_dir}
cp -av vendor/*  %{buildroot}%{__vendor_dir}

%clean
%{__protect} && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%dir %{LS_home}
%{LS_home}/*
%exclude %{__util_dir}/zeromq.rb
%exclude %{__spec_dir}/filters/json.rb
%exclude %{__vendor_dir}/bundle/jruby/1.9/bin/bundle
%exclude %{__vendor_dir}/bundle/jruby/1.9/bin/bundler
#%exclude %{__gemspecdir}/multipart-post-2.0.0.gemspec
#%exclude %{__gemspecdir}/spoon-0.0.4.gemspec

%changelog

#* Tue Jul 28 2015 <vitvegl@quintagroup.org> - 1.4.4-1
#- v1.4.4
#- excluding specifications of two conflicting gemspecs (multipart-post and spoon)

* Wed May 13 2015 <vitvegl@quintagroup.org> - 1.4.2-2
- initial build
