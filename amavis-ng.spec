%include	/usr/lib/rpm/macros.perl
%define		pdir	AMAVIS
Summary:	New generation amavis
Summary(pl.UTF-8):	Amavis nowej generacji
Name:		amavis-ng
Version:	0.1.6.9
Release:	3
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/amavis/%{name}-%{version}.tar.gz
# Source0-md5:	e9086bfbd3fa2049860d176a0c30549e
Source1:	%{name}-logrotate
Patch0:		%{name}-quarantine.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-courier.patch
Patch3:		%{name}-mks.patch
Patch4:		%{name}-make.patch
URL:		http://amavis.sourceforge.net/
BuildRequires:	perl-devel
BuildRequires:	perl-libnet
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	sendmail-devel
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

%description -l pl.UTF-8
AMaViS-ng to przepisana w sposób modularny wersja projektów amavisd i
amavis-perl. Skanuje pocztę elektroniczną na okoliczność groźnego kodu
wewnątrz załączników i archiwów, nie pozwalając na doręczenie w
przypadku wykrycia. Wspiera integrację różnych zewnętrznych skanerów
antywirusowych, ładnie integruje się z różnymi serwerami pocztowymi. W
przeciwieństwie do amavis-perl i amavisd, nie wymaga konfiguracji w
czasie budowania.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# precompiled x86 binary
rm -f amavis-milter/amavis-milter

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

cd doc
%{__make}

cd ../amavis-milter
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

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
%attr(770,amavis,amavis) /var/log/archive/amavis-ng
%attr(750,amavis,amavis) /var/run/amavis-ng
%attr(770,amavis,amavis) /var/spool/amavis-ng
%attr(644,amavis,amavis) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/amavis.conf
%{_datadir}/amavis-ng
%{_infodir}/amavis-ng.info*
%{perl_vendorlib}/AMAVIS.pm
%{perl_vendorlib}/AMAVIS
%{_mandir}/man1/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/amavis-ng
