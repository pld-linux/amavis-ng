%include	/usr/lib/rpm/macros.perl
Summary:	New generation amavis
Summary(pl):	Amavis nowej generacji
Name:		amavis-ng
Version:	0.1.4.1.orig
Release:	3
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/amavis/%{name}_%{version}.tar.gz
Patch0:		%{name}.patch
URL:		http://amavis.sourceforge.net/
BuildRequires:	perl-Config-IniFiles
BuildRequires:	perl-File-MMagic
BuildRequires:	perl-devel
BuildRequires:	perl-libnet
BuildRequires:	rpm-perlprov
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Obsoletes:	amavisd
Obsoletes:	amavis
Obsoletes:	AMaViS
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# optionally used
%define	_noautoreq	'perl(Archive::Tar)' 'perl(Archive::Zip)' 'perl(Compress::Zlib)' 'perl(Convert::TNEF)' 'perl(Convert::UUlib)' 'perl(MIME::Parser)' 'perl(File::Scan)'

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

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
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
   /usr/sbin/useradd -u 97 -r -d /var/spool/amavis  -s /bin/false -c "Anti Virus Checker" -g nobody  amavis 1>&2
fi

%postun
if [ "$1" = "0" ]; then
   echo "Removing user amavis"
   /usr/sbin/userdel amavis
   echo "Removing group amavis"
   /usr/sbin/groupdel amavis
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/amavis
%attr(750,amavis,amavis) /var/spool/amavis
%{perl_vendorlib}/AMAVIS.pm
%{perl_vendorlib}/AMAVIS
%{_mandir}/man1/*
