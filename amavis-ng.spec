Summary:	New generation amavis
Summary(pl):	Amavis nowej generacji
Name:		amavis-ng
Version:	0.1.3.1
Release:	0
License:	GPL
Group:		Applications/Mail
Source0:	http://prdownloads.sourceforge.net/amavis/%{name}-%{version}.tar.gz
URL:		http://amavis.sourceforge.net/
BuildRequires:	perl
BuildRequires:	perl-devel
Obsoletes:	amavisd
Obsoletes:	amavis
Obsoletes:	AMaViS
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
blah

%description -l pl
blah blah

%prep
%setup -q

%build
perl Makefile.PL

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

#%pre

#%preun

#%post

#%postun

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
