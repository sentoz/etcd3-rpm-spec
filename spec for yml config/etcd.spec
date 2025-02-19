# https://github.com/etcd-io/etcd
%define debug_package %{nil}

Name:    etcd
Version: 3.5.18
Release: 1%{?dist}
Summary: A highly-available key value store for shared configuration
License: ASL 2.0
URL:     https://github.com/etcd-io/etcd/
Source0: https://github.com/etcd-io/%{name}/releases/download/v%{version}/%{name}-v%{version}-linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.yml

%description
A highly-available key value store for shared configuration.

%prep

%build
/bin/true

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_bindir}
tar --strip-components=1 -C %{buildroot}%{_bindir} -xvf %{SOURCE0}
rm -f %{buildroot}%{_bindir}/README*.md
rm -rf %{buildroot}%{_bindir}/Documentation
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} %{SOURCE2}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "etcd user" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
case "$1" in
  0)
    # This is an uninstallation.
    getent passwd %{name} >/dev/null && userdel %{name}
    getent group %{name} >/dev/null && groupdel %{name}
  ;;
  1)
    # This is an upgrade.
  ;;
esac
%systemd_postun_with_restart %{name}.service

%files
%dir %attr(-, %{name}, %{name}) %{_sharedstatedir}/%{name}
%attr(755, root, root) %{_bindir}/%{name}
%attr(755, root, root) %{_bindir}/%{name}ctl
%attr(755, root, root) %{_bindir}/%{name}utl
%attr(644, root, root) %{_unitdir}/%{name}.service
%dir %attr(-, root, root) %{_sysconfdir}/%{name}
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/%{name}/%{name}.yml

%changelog
* Wed Feb 19 2025 Dmitriy Okladin <sentoz66@gmail.com> - 3.5.18
- update to 3.5.18

* Sat Mar 13 2022 Dmitriy Okladin <sentoz66@gmail.com> - 3.5.1
- update to 3.5.1
- added etcdutl util

* Mon Nov 08 2021 Dmitriy Okladin <sentoz66@gmail.com> - 3.4.18
- fix config(noreplace) with binary

* Thu Oct 23 2021 Dmitriy Okladin <sentoz66@gmail.com> - 3.4.18
- initial build 3.4.18