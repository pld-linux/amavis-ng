%include	/usr/lib/rpm/macros.perl
Summary:	New generation amavis
Summary(pl):	Amavis nowej generacji
Name:		amavis-ng
Version:	0.1.6.4.orig
Release:	4
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/amavis/%{name}_%{version}.tar.gz
# Source0-md5:	b3559a910bad4a522a466da3a44e62c6
Source1:	%{name}-logrotate
Patch0:		%{name}-quarantine.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-courier.patch
Patch3:		%{name}-mks.patch
URL:		http://amavis.sourceforge.net/
BuildRequires:	perl-Config-IniFiles
BuildRequires:	perl-File-MMagic
BuildRequires:	perl-devel
BuildRequires:	perl-libnet
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.159
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires:       arc
Requires:       bzip2
Requires:       file
Requires:       lha
Requires:       ncompress
Requires:       unarj
Requires:       unrar
Requires:       zoo
Provides:	group(amavis)
Provides:	user(amavis)
Obsoletes:	amavisd
Obsoletes:	amavis
Obsoletes:	AMaViS
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
antywirusowych, ³adnie integruje siê z ró¿nymi serwerami pocztowymi.
W przeciwieñstwie do amavis-perl i amavisd, nie wymaga konfiguracji w
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
    echo type \"info amavis-ng\" to get help
    echo
fi

if [ -n "`getgid amavis`" ]; then
	if [ "`getgid amavis`" != "97" ]; then
		echo "Warning: group amavis doesn't have gid=97. Correct this before installing amavis" 1>&2
		exit 1
	fi
else
	echo "adding group amavis GID=97"
	/usr/sbin/groupadd -g 97 -r -f amavis
fi

if [ -n "`id -u amavis 2>/dev/null`" ]; then
	if [ "`id -u amavis`" != "97" ]; then
		echo "Error: user amavis doesn't have uid=97. Correct this before installing amavis." 1>&2
		exit 1
	fi
else
	echo "adding user amavis UID=97"
	/usr/sbin/useradd -u 97 -r -d /var/spool/amavis -s /bin/false -c "Anti Virus Checker" -g nobody amavis 1>&2
fi

%triggerin -- courier
chown -R daemon /var/{spool,log}/amavis-ng

if [ -e /var/lock/subsys/courier ]; then
	/etc/rc.d/init.d/courier restart
fi

%postun
if [ "$1" = "0" ]; then
	%userremove amavis
	%groupremove amavis
fi

%files
%defattr(644,root,root,755)
%doc doc/old/README* doc/ChangeLog doc/RELEASE-NOTES
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(770,amavis,amavis) /var/log/amavis-ng
%attr(770,amavis,amavis) /var/log/archiv/amavis-ng
%attr(750,amavis,amavis) /var/run/amavis-ng
%attr(770,amavis,amavis) /var/spool/amavis-ng
%attr(644,amavis,amavis) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/amavis.conf
%{_datadir}/amavis-ng
%{_infodir}/amavis-ng.info*
%{perl_vendorlib}/AMAVIS.pm
%{perl_vendorlib}/AMAVIS
%{_mandir}/man1/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/logrotate.d/amavis-ng
