%define rel_ver 3.8.0
%define pkg_ver 1
%define _prefix /opt/zookeeper
%global debug_package %{nil}

Summary: High-performance coordination service for distributed applications.
Name: zookeeper
Version: %{rel_ver}
Release: %{pkg_ver}
License: Apache-2.0 and OpenSSL and SSLeay and MIT and BSD
Group: Applications/Databases
URL: https://www.apache.org/dist/zookeeper/
Source0: https://github.com/apache/zookeeper/archive/refs/tags/release-3.8.0-1.tar.gz
Source1: zoo.cfg
Source2: zookeeper.service
Source3: zookeeper.sysconfig
Source4: log4j.properties 
Source5: xmvn-reactor
BuildRoot: %{_tmppath}/%{name}-%{rel_ver}-%{release}-root
BuildRequires: java-1.8.0-openjdk-devel,maven,hostname,maven-local,systemd
Requires: java-1.8.0-openjdk,systemd
Provides: apache-zookeeper
Provides: mvn(org.apche.zookeeper:zookeeper)

%description
ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.

%prep
%setup -q -n zookeeper-release-%{version}-1
cp %{SOURCE5} ./.xmvn-reactor
echo `pwd` > absolute_prefix.log
sed -i 's/\//\\\//g' absolute_prefix.log
absolute_prefix=`head -n 1 absolute_prefix.log`
sed -i 's/absolute-prefix/'"$absolute_prefix"'/g' .xmvn-reactor

%build
mvn -DskipTests package
tar xvf zookeeper-assembly/target/apache-%{name}-%{rel_ver}-bin.tar.gz -C .
cp -r apache-%{name}-%{rel_ver}-bin/lib .

%install
%mvn_install

mkdir -p %{buildroot}%{_prefix}/bin
mkdir -p %{buildroot}%{_prefix}/lib
mkdir -p %{buildroot}%{_prefix}/conf
mkdir -p %{buildroot}%{_localstatedir}/log/zookeeper
mkdir -p %{buildroot}%{_localstatedir}/lib/zookeeper/data

install -p -D -m 755 bin/*.sh %{buildroot}%{_prefix}/bin
install -p -D -m 644 lib/*.jar %{buildroot}%{_prefix}/lib
install -p -D -m 644 conf/* %{buildroot}%{_prefix}/conf
install -p -D -m 644 %{S:1} %{buildroot}%{_prefix}/conf/zoo.cfg
install -p -D -m 644 %{S:2} %{buildroot}%{_unitdir}/zookeeper.service
install -p -D -m 644 %{S:3} %{buildroot}%{_sysconfdir}/sysconfig/zookeeper
install -p -D -m 644 %{S:4} %{buildroot}%{_prefix}/conf/log4j.properties 

%clean
rm -rf %{buildroot}

%files -f .mfiles
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
* Thu May 5 2022 xiexing <xiexing4@hisilicon.com> - 3.8.0-1
- update version

* Tue Oct 24 2021 wangyue <wangyue92@huawei.com> - 2.4
- Add systemd to buildrequire because %{_unitdir} can't recognize

* Thu Jun 24 2021 Ge Wang <wangge20@huawei.com> - 2.3
- Add provides item apache-zookeeper and add packages to system default java package directory

* Fri Jun 18 2021 lingsheng <lingsheng@huawei.com> - 2.2
- Fix reload service failure

* Thu Apr 1 2021 zhangshaoning <zhangshaoning@uniontech.com> - 2.1
- Repair status failure after stopping service

* Thu Mar 25 2021 baizhonggui <baizhonggui@huawei.com> - 2.0
- Delete %{dist} in Release

* Sun Jun 28 2020 hao zhang <unioah@isrc.iscas.ac.cn> - 1.0
- Add zookeeper.service
