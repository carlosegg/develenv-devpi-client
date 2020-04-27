
%define package_name devpi-client
%{!?python_dependency: %global python_dependency %([[ "$(cat /etc/redhat-release |sed s:'.*release ':'':g|awk '{print $1}'|cut -d '.' -f1)" == "8" ]] && echo python3 || echo python26)}
%define     modify_package_name true
# disable building of the debug package
%define  debug_package %{nil}
%define _unpackaged_files_terminate_build 0
%{!?sitepackages_path: %global sitepackages_path %(python3 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")} 
%define devpi_repository /var/develenv/repositories/devpi

%define cdn_home /opt/ss/develenv/platform/
%define installdir %{cdn_home}/%{package_name}
%define libdir %{installdir}/lib
%define bindir %{installdir}/bin

Summary:    client for devpi-server
Name:       devpi-client
Version:    %{versionModule}
Release:    5.4.1.%{releaseModule}
License:    http://opensource.org/licenses/MIT
Packager:   softwaresano.com
Group:      develenv
BuildArch:  x86_64
BuildRoot:  %{_topdir}/BUILDROOT
Vendor:     softwaresano.com
AutoReq:    no
Requires:   %{python_dependency}
%description
%{summary}

%pre
#Create develenv user if not exists
if [ "$(id -u develenv 2>/dev/null)" == "" ]; then
   default_id=600
   id_user=$(grep "^.*:.*:$default_id:" /etc/passwd)
   id_group=$(grep "^.*:.*:$default_id:" /etc/group)
   if [ "$id_user" == "" -a "$id_group" == "" ]; then
      groupadd -g $default_id develenv
      useradd -s /bin/bash -g $default_id -u $default_id develenv
   else
      useradd -s /bin/bash develenv
   fi
fi

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
sed -i /\'\'\'/d $RPM_BUILD_ROOT/%{bindir}/devpi
sed -i s:"bin/sh":"bin/python3":g  $RPM_BUILD_ROOT/%{bindir}/devpi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/*
%{installdir}
%{libdir}
%{bindir}
/etc/sysconfig/*
%defattr(-,develenv,develenv)
%dir %{devpi_repository}
%doc ../../../../README.md
