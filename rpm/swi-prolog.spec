%undefine __cmake_in_source_build

%define swiplversion 10.0.0

Name:       swi-prolog

Summary:    Prolog Interpreter
Version:    %{swiplversion}
Release:    1
License:    BSD
URL:        https://github.com/sailfishos/swi-prolog
Source0:    %{name}-%{version}.tar.gz
Provides:   pl
BuildRequires: cmake
BuildRequires: fdupes
BuildRequires: pkgconfig(zlib)

%description
ISO/Edinburgh-style Prolog compiler.  Compliant with Part 1 of the ISO standard
for Prolog.  Covers all traditional Edinburgh Prolog features and shares many
features with Quintus and SICStus Prolog, including a compatible module system.
Very fast compiler, garbage collection (also on atoms), fast and powerful C/C++
interface, autoloading, GNU-readline interface.
 
SWI-Prolog has been designed and implemented such that it can easily be
modified for experiments with logic programming and the relation
between logic programming and other programming paradigms (such as the
object oriented XPCE environment).  SWI-Prolog has a rich set of
built-in predicates and reasonable performance, which makes it possible
to develop substantial applications in it.  The current version offers
a module system, garbage collection and an interface to the C language.

%package runtime-lib
Summary:    SWI-Prolog runtime environment dynamic lib
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description runtime-lib
SWI-Prolog runtime environment dynamic lib.

%package doc
Summary:    Documentation for SWI-Prolog
Requires:   %{name} = %{version}-%{release}

%description doc
This package contains SWI-Prolog documentation (manual pages, README, etc.).

%package library-core
Summary:    Minimal library of SWI-Prolog predicates
Requires(preun): /bin/rm
Requires(post): %{name} = %{version}
Requires(post): /bin/rm

%description library-core
This package contains a minimal collection of prolog predicates, just enough
to load foreign libraries.

%package library
Summary:    Library of SWI-Prolog predicates
Requires:   %{name}-library-core = %{version}
Requires(post): %{name} = %{version}
Requires(post): /bin/rm
Requires(postun): %{name} = %{version}
Requires(postun): /bin/rm

%description library
This package contains a collection of commonly used prolog predicates. You
need this is you are running non-precompiled prolog code.

%package nox
Summary:        ISO/Edinburgh-style Prolog interpreter - without X support
Requires:       %{name}-library = %{version}

%description nox
This package contains a SWI-Prolog installation without GUI components.

%package devel
Summary:    Headers files and libraries for SWI-Prolog C-interface
Requires:   %{name}-runtime-lib = %{version}
Provides:   pl-devel

%description devel
This package contains headers files, etc. necessary for developing software
that uses the C-interface to SWI-Prolog.


%prep
%autosetup -p1 -n %{name}-%{version}/swi-prolog

%build

%cmake -DSWIPL_ARCH=%{_arch} -DSWIPL_PACKAGES=OFF -DINSTALL_QLF=OFF
%cmake_build

%install
%cmake_install

# Scripts with shebang should be executable
chmod 0755 \
  %{buildroot}%{_libdir}/swipl/customize/edit

# Remove stuff we do not want to package
rm %{buildroot}%{_libdir}/swipl/{LICENSE,README.md}

# remove .qlf files which don't seem to be reproducible
find %{buildroot} -name '*.qlf' -exec rm -f {} ';'

# Link duplicates
%fdupes %{buildroot}%{_libdir}/swipl

%post runtime-lib -p /sbin/ldconfig

%postun runtime-lib -p /sbin/ldconfig

%preun library-core
if [ $1 -eq 0 ]; then
/bin/rm -f -- %{_libdir}/swipl/library/INDEX.pl
fi

%post library-core
/bin/rm -f -- %{_libdir}/swipl/library/INDEX.pl
cd %{_libdir}/swipl/library || :
%{_libdir}/bin/%{_arch}/swipl --quiet -f none -F none -g "make_library_index('.')" -t halt || :

%post library
/bin/rm -f -- %{_libdir}/swipl/library/INDEX.pl
cd %{_libdir}/swipl/library || :
%{_libdir}/bin/%{_arch}/swipl --quiet -f none -F none -g "make_library_index('.')" -t halt || :

%postun library
/bin/rm -f -- %{_libdir}/swipl/library/INDEX.pl
cd %{_libdir}/swipl/library || :
%{_libdir}/bin/%{_arch}/swipl --quiet -f none -F none -g "make_library_index('.')" -t halt || :

%files
%license LICENSE
%dir %{_libdir}/swipl
%dir %{_libdir}/swipl/bin
%dir %{_libdir}/swipl/bin/%{_arch}
%{_libdir}/swipl/bin/%{_arch}/swipl
%{_libdir}/swipl/bin/%{_arch}/swipl-win
%{_bindir}/swipl
%{_bindir}/swipl-win
%{_libdir}/swipl/ABI
%{_libdir}/swipl/boot*.prc

%files runtime-lib
%dir %{_libdir}/swipl/lib
%dir %{_libdir}/swipl/lib/%{_arch}
%{_libdir}/swipl/lib/%{_arch}/libswipl.so.*
%{_libdir}/swipl/swipl.home
%{_libdir}/swipl/bin/swipl.home

%files doc
%doc %{_mandir}/man1/*.1.gz
%dir %{_libdir}/swipl/customize
%{_libdir}/swipl/customize/README.md
%{_libdir}/swipl/customize/edit
%{_libdir}/swipl/customize/init.pl
%dir %{_libdir}/swipl/demo
%{_libdir}/swipl/demo/README.md
%{_libdir}/swipl/demo/likes.pl

%files library-core
%dir %{_libdir}/swipl/library
%{_libdir}/swipl/library/shlib.pl
%{_libdir}/swipl/library/error.pl
%{_libdir}/swipl/library/lists.pl
%exclude %{_libdir}/swipl/library/INDEX.pl

%files library
%dir %{_libdir}/swipl/boot
%{_libdir}/swipl/boot/*.pl
%{_libdir}/swipl/library/*
%exclude %{_libdir}/swipl/library/shlib.pl
%exclude %{_libdir}/swipl/library/error.pl
%exclude %{_libdir}/swipl/library/lists.pl

%files nox
%{_libdir}/swipl/app/

%files devel
%dir %{_libdir}/swipl/include
%{_libdir}/swipl/include/SWI-Prolog.h
%dir %{_libdir}/swipl/include/Yap
%{_libdir}/swipl/include/Yap/YapInterface.h
%{_libdir}/swipl/include/SWI-Stream.h
%dir %{_libdir}/swipl/include/sicstus
%{_libdir}/swipl/include/sicstus/sicstus.h
%{_libdir}/swipl/bin/%{_arch}/swipl-ld
%{_bindir}/swipl-ld
%{_datadir}/pkgconfig/swipl.pc
%{_libdir}/swipl/lib/%{_arch}/libswipl.so
%{_libdir}/swipl/cmake/
%{_libdir}/cmake/swipl/
