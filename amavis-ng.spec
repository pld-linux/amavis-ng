%include	/usr/lib/rpm/macros.perl
%define		pdir	AMAVIS
Summary:	New generation amavis
Summary(pl):	Amavis nowej generacji
Name:		amavis-ng
Version:	0.1.6.9
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/amavis/%{name}-%{version}.tar.gz
# Source0-md5:	e9086bfbd3fa2049860d176a0c30549e
Source1:	%{name}-logrotate
Patch0:		%{name}-quarantine.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-courier.patch
Patch3:		%{name}-mks.patch
URL:		http://amavis.sourceforge.net/
BuildRequires:	perl-devel
BuildRequires:	perl-libnet
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	perl-Config-IniFiles
Requires:	perl-File-MMagic
Provides:	group(amavis)
Provides:	user(amavis)
Obsoletes:	AMaViS
Obsoletes:	amavis
Obsoletes:	amavisd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# optionally used
%define	_noautoreq	'perl(File::Scan)'

%description
AMaViS-ng is a modular rewrite of amavisd and amavis-perl. It scans
email for malicious code inside attachments and archive files,
stopping delivery if malicious code is found. It supports integration
of several third-party virus scanners and integrates nicely into
several MTA setups. Unlike amavis-perl and amavisd, there is no need
for build-time configuration.

%description -l pl
AMaViS-ng to przepisana w sposób modularny wersja projektów amavisd i
amavis-perl. Skanuje pocztê elektroniczn± na okoliczno¶æ gro¼nego kodu
wewn±trz za³±czników i archiwów, nie pozwalaj±c na dorêczenie w
przypadku wykrycia. Wspiera integracjê ró¿nych zewnêtrznych skanerów
antywirusowych, ³adnie integruje siê z ró¿nymi serwerami pocztowymi. W
przeciwieñstwie do amavis-perl i amavisd, nie wymaga konfiguracji w
czasie budowania.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

cd doc
%{__make}

cd ../amavis-milter
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/logrotate.d,%{_infodir},%{_sbindir}}
install -d $RPM_BUILD_ROOT/var/spool/amavis-ng/{problems,quarantine,queue,tmp}
install -d $RPM_BUILD_ROOT/var/{run/amavis-ng,log/{archiv/amavis-ng,amavis-ng}}
install -d $RPM_BUILD_ROOT%{_datadir}/amavis-ng

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/amavis-ng
install etc/amavis.conf $RPM_BUILD_ROOT%{_sysconfdir}
install doc/amavis-ng.info $RPM_BUILD_ROOT%{_infodir}
install amavis-milter/amavis-milter $RPM_BUILD_ROOT%{_sbindir}
install magic.mime $RPM_BUILD_ROOT%{_datadir}/amavis-ng

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "$1" = "1" ]; then
	echo
	echo 'Type "info amavis-ng" to get help'
	echo
fi

%groupadd -g 97 -r -f amavis
%useradd -u 97 -r -d /var/spool/amavis -s /bin/false -c "Anti Virus Checker" -g nobody amavis

%triggerin -- courier
chown -R daemon /var/{spool,log}/amavis-ng
if [ -f /var/lock/subsys/courier ]; then
	%{_sbindir}/filterctl stop perlfilter
	%{_sbindir}/filterctl start perlfilter
fi

%postun
if [ "$1" = "0" ]; then
	%userremove amavis
	%groupremove amavis
fi

%files
%defattr(644,root,root,755)
%doc doc/README* doc/ChangeLog doc/RELEASE-NOTES
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(770,amavis,amavis) /var/log/amavis-ng
%attr(770,amavis,amavis) /var/log/archiv/amavis-ng
%attr(750,amavis,amavis) /var/run/amavis-ng
%attr(770,amavis,amavis) /var/spool/amavis-ng
%attr(644,amavis,amavis) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/amavis.conf
%{_datadir}/amavis-ng
%{_infodir}/amavis-ng.info*
%{perl_vendorlib}/AMAVIS.pm
%{perl_vendorlib}/AMAVIS
%{_mandir}/man1/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/amavis-ng
