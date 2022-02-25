%define rel_ver 3.6.1
%define pkg_ver 2.4
%define _prefix /opt/zookeeper

Summary: High-performance coordination service for distributed applications.
Name: apache-zookeeper
Version: %{rel_ver}
Release: %{pkg_ver}
License: Apache-2.0 and OpenSSL and SSLeay and MIT and BSD
Group: Applications/Databases
URL: https://www.apache.org/dist/zookeeper/
BuildArch: noarch
Source0: https://www.apache.org/dist/zookeeper/zookeeper-%{rel_ver}/apache-zookeeper-%{rel_ver}.tar.gz
Source1: zoo.cfg
Source2: zookeeper.service
Source3: zookeeper.sysconfig
Source4: log4j.properties 
BuildRoot: %{_tmppath}/%{name}-%{rel_ver}-%{release}-root
BuildRequires: java-1.8.0-openjdk-devel,maven,hostname
Requires: java-1.8.0-openjdk,systemd

%description
ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.

%prep
%setup -q

%build
mvn -DskipTests package
tar xvf zookeeper-assembly/target/%{name}-%{rel_ver}-bin.tar.gz -C .

%install
mkdir -p %{buildroot}%{_prefix}/bin
mkdir -p %{buildroot}%{_prefix}/lib
mkdir -p %{buildroot}%{_prefix}/conf
mkdir -p %{buildroot}%{_localstatedir}/log/zookeeper
mkdir -p %{buildroot}%{_localstatedir}/lib/zookeeper/data

install -p -D -m 755 %{name}-%{rel_ver}-bin/bin/*.sh %{buildroot}%{_prefix}/bin
install -p -D -m 644 %{name}-%{rel_ver}-bin/lib/*.jar %{buildroot}%{_prefix}/lib
install -p -D -m 644 %{name}-%{rel_ver}-bin/conf/* %{buildroot}%{_prefix}/conf
install -p -D -m 644 %{S:1} %{buildroot}%{_prefix}/conf/zoo.cfg
install -p -D -m 644 %{S:2} %{buildroot}%{_unitdir}/zookeeper.service
install -p -D -m 644 %{S:3} %{buildroot}%{_sysconfdir}/sysconfig/zookeeper
install -p -D -m 644 %{S:4} %{buildroot}%{_prefix}/conf/log4j.properties 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(-,zookeeper,zookeeper) %{_prefix}
%dir %attr(744, zookeeper, zookeeper) %{_localstatedir}/log/zookeeper
%dir %attr(755, zookeeper, zookeeper) %{_localstatedir}/lib/zookeeper
%doc LICENSE.txt NOTICE.txt README.md
%{_unitdir}/zookeeper.service
%config(noreplace) %{_sysconfdir}/sysconfig/zookeeper

%pre
getent group zookeeper >/dev/null || groupadd -r zookeeper
getent passwd zookeeper >/dev/null || useradd -r -g zookeeper -d / -s /sbin/nologin zookeeper
exit 0

%post
%systemd_post zookeeper.service

%preun
%systemd_preun zookeeper.service

%postun
%systemd_postun_with_restart zookeeper.service

%changelog
* Fri Feb 25 2022 wangkai <wangkai385@huawei.com> - 2.4
- Rebuild for fix log4j1.x cves

* Thu Dec 16 2021 wangkai <wangkai385@huawei.com> - 2.3
- This package depends on log4j.After the log4j vulnerability CVE-2021-44228 is fixed,the version needs to be rebuild.

* Fri Jun 18 2021 lingsheng <lingsheng@huawei.com> - 2.2
- Fix reload service failure

* Thu Apr 1 2021 zhangshaoning <zhangshaoning@uniontech.com> - 2.1
- Repair status failure after stopping service

* Thu Mar 25 2021 baizhonggui <baizhonggui@huawei.com> - 2.0
- Delete %{dist} in Release

* Sun Jun 28 2020 hao zhang <unioah@isrc.iscas.ac.cn> - 1.0
- Add zookeeper.service
