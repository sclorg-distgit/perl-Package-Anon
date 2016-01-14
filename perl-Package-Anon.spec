%{?scl:%scl_package perl-Package-Anon}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}perl-Package-Anon
Version:	0.05
Release:	6%{?dist}
Summary:	Anonymous packages
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Package-Anons/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AU/AUGGY/Package-Anon-%{version}.tar.gz
# Build
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	%{?scl_prefix}perl >= 4:5.14
BuildRequires:	%{?scl_prefix}perl(Scalar::Util)
BuildRequires:	%{?scl_prefix}perl(XSLoader)
# Test suite
BuildRequires:	%{?scl_prefix}perl(lib)
BuildRequires:	%{?scl_prefix}perl(Sub::Exporter)
BuildRequires:	%{?scl_prefix}perl(Test::More)
# Release tests
%if ! 0%{?scl:1}
BuildRequires:	%{?scl_prefix}perl(Pod::Coverage::TrustPod)
BuildRequires:	%{?scl_prefix}perl(Test::EOL)
BuildRequires:	%{?scl_prefix}perl(Test::NoTabs)
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	%{?scl_prefix}perl(Test::Pod) >= 1.41
%endif
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})

# Avoid private object provides
%{?perl_default_filter}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_from_provides /\.so()/d
%filter_setup
%endif

%description
This module allows for anonymous packages that are independent of the main
namespace and only available through an object instance, not by name.

%prep
%setup -q -n Package-Anon-%{version}

%build
%{?scl:scl enable %{scl} '}
perl Makefile.PL INSTALLDIRS=vendor OPTMIZE="%{optflags}"
%{?scl:'}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} "}
make test %{!?scl:RELEASE_TESTING=1}
%{?scl:"}

%files
%doc Changes LICENSE README
%{perl_vendorarch}/auto/Package/
%{perl_vendorarch}/Package/
%{_mandir}/man3/Package::Anon.3pm*

%changelog
* Thu Nov 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-6
- Rebuilt for SCL

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.05-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Paul Howarth <paul@city-fan.org> - 0.05-2
- Sanitize for Fedora submission (#892651)

* Fri Jan  4 2013 Paul Howarth <paul@city-fan.org> - 0.05-1
- Initial RPM build
