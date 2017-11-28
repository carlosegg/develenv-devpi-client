
%define package_name devpi-client
%{!?python_dependency: %global python_dependency %([[ "$(cat /etc/redhat-release |sed s:'.*release ':'':g|awk '{print $1}'|cut -d '.' -f1)" == "7" ]] && echo python || echo python26)}
%define     modify_package_name true
# disable building of the debug package
%define  debug_package %{nil}
%define _unpackaged_files_terminate_build 0
%{!?sitepackages_path: %global sitepackages_path %(python -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")} 
%define devpi_repository /var/develenv/repositories/devpi

%define cdn_home /opt/ss/develenv/platform/
%define installdir %{cdn_home}/%{package_name}
%define libdir %{installdir}/lib
%define bindir %{installdir}/bin

Summary:    client for devpi-server
Name:       devpi-client
Version:    %{versionModule}
Release:    3.1.0.%{releaseModule}
License:    http://opensource.org/licenses/MIT
Packager:   softwaresano.com
Group:      develenv
BuildArch:  x86_64
BuildRoot:  %{_topdir}/BUILDROOT
Vendor:     softwaresano.com
AutoReq:    no
Requires:   %{python_dependency} ss-develenv-user

%description
%{summary}

%install

mkdir -p $RPM_BUILD_ROOT/%{bindir}
mkdir -p $RPM_BUILD_ROOT/%{libdir}
mkdir -p $RPM_BUILD_ROOT/%{devpi_repository}

cd %{_srcrpmdir}/..
make devclean
make install HOME_DIR=$RPM_BUILD_ROOT/%{installdir} RPM_BUILD_ROOT=$RPM_BUILD_ROOT LIB_DIR=%{libdir} SITEPACKAGES_PATH=%{sitepackages_path}
cp -R %{_sourcedir}/* $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -sf %{bindir}/devpi-upload.sh $RPM_BUILD_ROOT/usr/bin/devpi-upload.sh


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/*
%{installdir}
%{libdir}
%{bindir}
%{sitepackages_path}/%{package_name}.pth
/etc/sysconfig/*
%defattr(-,develenv,develenv)
%dir %{devpi_repository}
%doc ../../../../README.md
