Summary:	Emerging Threats open rules for Snort IDS/IPS
Name:		emergingthreats
Version:	6947
Release:	1
License:	GNU GPLv2 and BSD
Group:		Networking
Source0:	http://rules.emergingthreats.net/open/snort-2.9.0/emerging.rules.tar.gz
# Source0-md5:	38db422a5b87375c25b8714f42dc8670
URL:		http://emergingthreats.net/
Requires:	sed >= 4.0
Requires:	snort >= 2.9.0
Provides:	snort-rules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/snort

%description
Emerging Threats open rules for Snort IDS/IPS.

%prep
%setup -qn rules

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rules
cp -p emerging.conf		$RPM_BUILD_ROOT%{_sysconfdir}
cp -p emerging-*.rules	$RPM_BUILD_ROOT%{_sysconfdir}/rules
cp -p classification.config	$RPM_BUILD_ROOT%{_sysconfdir}/rules
cp -p reference.config	$RPM_BUILD_ROOT%{_sysconfdir}/rules

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	if [ -f %{_sysconfdir}/snort.conf ]; then
		echo "include emerging.conf" >> %{_sysconfdir}/snort.conf
	fi
fi
%service -q snortd restart

%postun
if [ "$1" = "0" ]; then
	%{__sed} -i -re 's/^\s*include\s+emerging.conf.*$//' %{_sysconfdir}/snort.conf
	%service -q snortd restart
fi

%files
%defattr(644,root,root,755)
%doc LICENSE BSD-License.txt snort-2.9.0-open.txt gpl-2.0.txt compromised-ips.txt rbn-ips.txt rbn-malvertisers-ips.txt
%attr(640,root,snort) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/emerging.conf
%attr(640,root,snort) %{_sysconfdir}/rules/*
