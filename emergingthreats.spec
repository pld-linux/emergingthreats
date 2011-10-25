
Summary:	Emerging Threats open rules for Snort IDS/IPS
Name:		emergingthreats
Version:	6947
Release:	1
License:	GNU GPLv2 and BSD
Group:		Networking
Source0:	http://rules.emergingthreats.net/open/snort-2.9.0/emerging.rules.tar.gz
# Source0-md5:	38db422a5b87375c25b8714f42dc8670
URL:		http://emergingthreats.net/
Requires:	snort >= 2.9.0
Requires:	perl-base
Provides:	snort-rules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emerging Threats open rules for Snort IDS/IPS.

%prep
%setup -qn rules

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/snort/rules
install emerging.conf		$RPM_BUILD_ROOT%{_sysconfdir}/snort
install emerging-*.rules	$RPM_BUILD_ROOT%{_sysconfdir}/snort/rules
install classification.config	$RPM_BUILD_ROOT%{_sysconfdir}/snort/rules
install reference.config	$RPM_BUILD_ROOT%{_sysconfdir}/snort/rules

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post
[ -f /etc/snort/snort.conf ] \
	&& /bin/echo "include emerging.conf" >> /etc/snort/snort.conf
%service snortd start

%preun
/usr/bin/perl -i.et_orig -pe 's/^\s*include\s+emerging.conf.*$//' /etc/snort/snort.conf

%postun
%service snortd start

%files
%defattr(644,root,root,755)
%doc LICENSE BSD-License.txt snort-2.9.0-open.txt gpl-2.0.txt compromised-ips.txt rbn-ips.txt rbn-malvertisers-ips.txt
%attr(640,root,snort) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/snort/emerging.conf
%attr(640,root,snort) %{_sysconfdir}/snort/rules/*
