%define swiplversion 7.6.4

Name:       swi-prolog

Summary:    Prolog Interpreter
Version:    %{swiplversion}
Release:    1
Group:      Development/Languages
License:    BSD
URL:        http://www.swi-prolog.org
Source0:    %{name}-%{version}.tar.gz
Provides:   pl

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
Group:      System/Resource Policy
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description runtime-lib
SWI-Prolog runtime environment dynamic lib.

%package doc
Summary:    Documentation for SWI-Prolog
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description doc
This package contains SWI-Prolog documentation (manual pages, README, etc.).

%package library-core
Summary:    Minimal library of SWI-Prolog predicates
Group:      System/Resource Policy
Requires(preun): /bin/rm
Requires(post): %{name} = %{version}
Requires(post): /bin/rm
Obsoletes:  %{name}-lib-core

%description library-core
This package contains a minimal collection of prolog predicates, just enough
to load foreign libraries.


%package library
Summary:    Library of SWI-Prolog predicates
Group:      Development/Languages
Requires:   %{name}-library-core = %{version}
Requires(post): %{name} = %{version}
Requires(post): /bin/rm
Requires(postun): %{name} = %{version}
Requires(postun): /bin/rm
Obsoletes:  %{name}-lib

%description library
This package contains a collection of commonly used prolog predicates. You
need this is you are running non-precompiled prolog code.


%package devel
Summary:    Headers files and libraries for SWI-Prolog C-interface
Group:      Development/Libraries
Requires:   %{name}-runtime-lib = %{version}
Provides:   pl-devel

%description devel
This package contains headers files, etc. necessary for developing software
that uses the C-interface to SWI-Prolog.


%prep
%setup -q -n %{name}-%{version}/swi-prolog

%build
pushd src
autoheader
autoconf
popd

%configure \
    --with-world            \
    --disable-static        \
    --enable-shared         \
    --without-bench         \
    --without-chr           \
    --without-clpqr         \
    --without-inclpr        \
    --without-jpl           \
    --without-xpce          \
    --without-odbc          \
    --without-protobufs     \
    --without-sgml          \
    --without-clib          \
    --without-http          \
    --without-plunit        \
    --without-pldoc         \
    --without-RDF           \
    --without-semweb        \
    --without-ssl           \
    --without-zlib          \
    --without-tipc          \
    --without-table         \
    --without-nlp           \
    --without-cpp           \
    --without-windows       \
    --without-PDT           \
    --without-utf8proc      \
    --without-archive       \
    --without-swipl-win     \
    --without-pengines      \
    --without-cql           \
    --without-bdb           \
    --without-readline      \
    --without-libedit       \
    --without-pcre          \
    PLARCH=%{_arch}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} ARCH=%{_arch} install-lite

%post runtime-lib -p /sbin/ldconfig

%postun runtime-lib -p /sbin/ldconfig

%preun library-core
if [ $1 -eq 0 ]; then
/bin/rm -f -- %{_libdir}/swipl-%{swiplversion}/library/INDEX.pl
fi

%post library-core
/bin/rm -f -- %{_libdir}/swipl-%{swiplversion}/library/INDEX.pl
cd %{_libdir}/swipl-%{swiplversion}/library || :
%{_libdir}/swipl-%{swiplversion}/bin/%{_arch}/swipl --quiet -f none -F none -g "make_library_index('.')" -t halt || :

%post library
/bin/rm -f -- %{_libdir}/swipl-%{swiplversion}/library/INDEX.pl
cd %{_libdir}/swipl-%{swiplversion}/library || :
%{_libdir}/swipl-%{swiplversion}/bin/%{_arch}/swipl --quiet -f none -F none -g "make_library_index('.')" -t halt || :

%postun library
/bin/rm -f -- %{_libdir}/swipl-%{swiplversion}/library/INDEX.pl
cd %{_libdir}/swipl-%{swiplversion}/library || :
%{_libdir}/swipl-%{swiplversion}/bin/%{_arch}/swipl --quiet -f none -F none -g "make_library_index('.')" -t halt || :

%files
%defattr(-,root,root,-)
%dir %{_libdir}/swipl-%{swiplversion}
%dir %{_libdir}/swipl-%{swiplversion}/bin
%dir %{_libdir}/swipl-%{swiplversion}/bin/%{_arch}
%{_libdir}/swipl-%{swiplversion}/bin/%{_arch}/swipl
%{_bindir}/swipl
%{_libdir}/swipl-%{swiplversion}/boot*.prc

%files runtime-lib
%defattr(-,root,root,-)
%dir %{_libdir}/swipl-%{swiplversion}/lib
%dir %{_libdir}/swipl-%{swiplversion}/lib/%{_arch}
%{_libdir}/swipl-%{swiplversion}/lib/%{_arch}/libswipl.so.*
%{_libdir}/swipl-%{swiplversion}/swipl.home
%{_libdir}/swipl-%{swiplversion}/bin/swipl.home

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man1/*.1.gz
%dir %{_libdir}/swipl-%{swiplversion}/customize
%{_libdir}/swipl-%{swiplversion}/customize/README
%{_libdir}/swipl-%{swiplversion}/customize/dotswiplrc
%{_libdir}/swipl-%{swiplversion}/customize/dotxpcerc
%{_libdir}/swipl-%{swiplversion}/customize/edit
%dir %{_libdir}/swipl-%{swiplversion}/demo
%{_libdir}/swipl-%{swiplversion}/demo/README
%{_libdir}/swipl-%{swiplversion}/demo/likes.pl

%files library-core
%defattr(-,root,root,-)
%dir %{_libdir}/swipl-%{swiplversion}/library
%{_libdir}/swipl-%{swiplversion}/library/shlib.pl
%{_libdir}/swipl-%{swiplversion}/library/error.pl
%{_libdir}/swipl-%{swiplversion}/library/lists.pl
%exclude %{_libdir}/swipl-%{swiplversion}/library/INDEX.pl

%files library
%defattr(-,root,root,-)
%dir %{_libdir}/swipl-%{swiplversion}/boot
%{_libdir}/swipl-%{swiplversion}/boot/apply.pl
%{_libdir}/swipl-%{swiplversion}/boot/attvar.pl
%{_libdir}/swipl-%{swiplversion}/boot/autoload.pl
%{_libdir}/swipl-%{swiplversion}/boot/bags.pl
%{_libdir}/swipl-%{swiplversion}/boot/dcg.pl
%{_libdir}/swipl-%{swiplversion}/boot/dicts.pl
%{_libdir}/swipl-%{swiplversion}/boot/dwim.pl
%{_libdir}/swipl-%{swiplversion}/boot/engines.pl
%{_libdir}/swipl-%{swiplversion}/boot/expand.pl
%{_libdir}/swipl-%{swiplversion}/boot/history.pl
%{_libdir}/swipl-%{swiplversion}/boot/init.pl
%{_libdir}/swipl-%{swiplversion}/boot/license.pl
%{_libdir}/swipl-%{swiplversion}/boot/load.pl
%{_libdir}/swipl-%{swiplversion}/boot/messages.pl
%{_libdir}/swipl-%{swiplversion}/boot/packs.pl
%{_libdir}/swipl-%{swiplversion}/boot/parms.pl
%{_libdir}/swipl-%{swiplversion}/boot/predopts.pl
%{_libdir}/swipl-%{swiplversion}/boot/qlf.pl
%{_libdir}/swipl-%{swiplversion}/boot/rc.pl
%{_libdir}/swipl-%{swiplversion}/boot/syspred.pl
%{_libdir}/swipl-%{swiplversion}/boot/toplevel.pl
%{_libdir}/swipl-%{swiplversion}/boot/topvars.pl
%{_libdir}/swipl-%{swiplversion}/library/aggregate.pl
%{_libdir}/swipl-%{swiplversion}/library/ansi_term.pl
%{_libdir}/swipl-%{swiplversion}/library/apply_macros.pl
%{_libdir}/swipl-%{swiplversion}/library/apply.pl
%{_libdir}/swipl-%{swiplversion}/library/arithmetic.pl
%{_libdir}/swipl-%{swiplversion}/library/assoc.pl
%{_libdir}/swipl-%{swiplversion}/library/backcomp.pl
%{_libdir}/swipl-%{swiplversion}/library/base32.pl
%{_libdir}/swipl-%{swiplversion}/library/base64.pl
%{_libdir}/swipl-%{swiplversion}/library/broadcast.pl
%{_libdir}/swipl-%{swiplversion}/library/charsio.pl
%{_libdir}/swipl-%{swiplversion}/library/check_installation.pl
%{_libdir}/swipl-%{swiplversion}/library/checklast.pl
%{_libdir}/swipl-%{swiplversion}/library/check.pl
%{_libdir}/swipl-%{swiplversion}/library/checkselect.pl
%{_libdir}/swipl-%{swiplversion}/library/clp/
%{_libdir}/swipl-%{swiplversion}/library/codesio.pl
%{_libdir}/swipl-%{swiplversion}/library/coinduction.pl
%{_libdir}/swipl-%{swiplversion}/library/console_input.pl
%{_libdir}/swipl-%{swiplversion}/library/csv.pl
%{_libdir}/swipl-%{swiplversion}/library/ctypes.pl
%{_libdir}/swipl-%{swiplversion}/library/date.pl
%{_libdir}/swipl-%{swiplversion}/library/dcg/
%{_libdir}/swipl-%{swiplversion}/library/debug.pl
%dir %{_libdir}/swipl-%{swiplversion}/library/dialect/
%dir %{_libdir}/swipl-%{swiplversion}/library/dialect/yap
%{_libdir}/swipl-%{swiplversion}/library/dialect/yap/README.TXT
%dir %{_libdir}/swipl-%{swiplversion}/library/dialect/ifprolog
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/ifprolog.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/yap.pl
%dir %{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus/terms.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus/lists.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus/system.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus/swipl-lfr.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus/arrays.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus/block.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus/timeout.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/sicstus/sockets.pl
%dir %{_libdir}/swipl-%{swiplversion}/library/dialect/hprolog
%{_libdir}/swipl-%{swiplversion}/library/dialect/hprolog/format.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/commons.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/hprolog.pl
%dir %{_libdir}/swipl-%{swiplversion}/library/dialect/swi
%{_libdir}/swipl-%{swiplversion}/library/dialect/swi/syspred_options.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect/bim.pl
%dir %{_libdir}/swipl-%{swiplversion}/library/dialect/iso
%{_libdir}/swipl-%{swiplversion}/library/dialect/iso/iso_predicates.pl
%dir %{_libdir}/swipl-%{swiplversion}/library/dialect/eclipse
%{_libdir}/swipl-%{swiplversion}/library/dialect/eclipse/test_util_iso.pl
%{_libdir}/swipl-%{swiplversion}/library/dialect.pl
%{_libdir}/swipl-%{swiplversion}/library/dicts.pl
%{_libdir}/swipl-%{swiplversion}/library/dif.pl
%{_libdir}/swipl-%{swiplversion}/library/edinburgh.pl
%{_libdir}/swipl-%{swiplversion}/library/edit.pl
%{_libdir}/swipl-%{swiplversion}/library/explain.pl
%{_libdir}/swipl-%{swiplversion}/library/fastrw.pl
%{_libdir}/swipl-%{swiplversion}/library/files.pl
%{_libdir}/swipl-%{swiplversion}/library/gensym.pl
%{_libdir}/swipl-%{swiplversion}/library/git.pl
%{_libdir}/swipl-%{swiplversion}/library/heaps.pl
%{_libdir}/swipl-%{swiplversion}/library/help.pl
%{_libdir}/swipl-%{swiplversion}/library/hotfix.pl
%{_libdir}/swipl-%{swiplversion}/library/iostream.pl
%{_libdir}/swipl-%{swiplversion}/library/lazy_lists.pl
%{_libdir}/swipl-%{swiplversion}/library/listing.pl
%{_libdir}/swipl-%{swiplversion}/library/main.pl
%{_libdir}/swipl-%{swiplversion}/library/make.pl
%{_libdir}/swipl-%{swiplversion}/library/modules.pl
%{_libdir}/swipl-%{swiplversion}/library/nb_rbtrees.pl
%{_libdir}/swipl-%{swiplversion}/library/nb_set.pl
%{_libdir}/swipl-%{swiplversion}/library/occurs.pl
%{_libdir}/swipl-%{swiplversion}/library/operators.pl
%{_libdir}/swipl-%{swiplversion}/library/option.pl
%{_libdir}/swipl-%{swiplversion}/library/optparse.pl
%{_libdir}/swipl-%{swiplversion}/library/ordsets.pl
%{_libdir}/swipl-%{swiplversion}/library/oset.pl
%{_libdir}/swipl-%{swiplversion}/library/pairs.pl
%{_libdir}/swipl-%{swiplversion}/library/persistency.pl
%{_libdir}/swipl-%{swiplversion}/library/pio.pl
%{_libdir}/swipl-%{swiplversion}/library/portray_text.pl
%{_libdir}/swipl-%{swiplversion}/library/pprint.pl
%{_libdir}/swipl-%{swiplversion}/library/predicate_options.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_autoload.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_breakpoints.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_clause.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_codewalk.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_colour.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_format.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_history.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_install.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_jiti.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_metainference.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_pack.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_source.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_stack.pl
%{_libdir}/swipl-%{swiplversion}/library/prolog_xref.pl
%{_libdir}/swipl-%{swiplversion}/library/pure_input.pl
%{_libdir}/swipl-%{swiplversion}/library/qpforeign.pl
%{_libdir}/swipl-%{swiplversion}/library/qsave.pl
%{_libdir}/swipl-%{swiplversion}/library/quasi_quotations.pl
%{_libdir}/swipl-%{swiplversion}/library/quintus.pl
%{_libdir}/swipl-%{swiplversion}/library/random.pl
%{_libdir}/swipl-%{swiplversion}/library/rbtrees.pl
%{_libdir}/swipl-%{swiplversion}/library/readln.pl
%{_libdir}/swipl-%{swiplversion}/library/readutil.pl
%{_libdir}/swipl-%{swiplversion}/library/record.pl
%{_libdir}/swipl-%{swiplversion}/library/sandbox.pl
%{_libdir}/swipl-%{swiplversion}/library/settings.pl
%{_libdir}/swipl-%{swiplversion}/library/shell.pl
%{_libdir}/swipl-%{swiplversion}/library/solution_sequences.pl
%{_libdir}/swipl-%{swiplversion}/library/sort.pl
%{_libdir}/swipl-%{swiplversion}/library/statistics.pl
%{_libdir}/swipl-%{swiplversion}/library/system.pl
%{_libdir}/swipl-%{swiplversion}/library/tabling.pl
%{_libdir}/swipl-%{swiplversion}/library/terms.pl
%{_libdir}/swipl-%{swiplversion}/library/thread.pl
%{_libdir}/swipl-%{swiplversion}/library/thread_pool.pl
%{_libdir}/swipl-%{swiplversion}/library/threadutil.pl
%{_libdir}/swipl-%{swiplversion}/library/tty.pl
%{_libdir}/swipl-%{swiplversion}/library/ugraphs.pl
%dir %{_libdir}/swipl-%{swiplversion}/library/unicode
%{_libdir}/swipl-%{swiplversion}/library/unicode/blocks.pl
%{_libdir}/swipl-%{swiplversion}/library/unicode/unicode_data.pl
%{_libdir}/swipl-%{swiplversion}/library/url.pl
%{_libdir}/swipl-%{swiplversion}/library/utf8.pl
%{_libdir}/swipl-%{swiplversion}/library/varnumbers.pl
%{_libdir}/swipl-%{swiplversion}/library/vm.pl
%{_libdir}/swipl-%{swiplversion}/library/when.pl
%{_libdir}/swipl-%{swiplversion}/library/win_menu.pl
%{_libdir}/swipl-%{swiplversion}/library/writef.pl
%{_libdir}/swipl-%{swiplversion}/library/www_browser.pl
%{_libdir}/swipl-%{swiplversion}/library/yall.pl

%files devel
%defattr(-,root,root,-)
%dir %{_libdir}/swipl-%{swiplversion}/include
%{_libdir}/swipl-%{swiplversion}/include/SWI-Prolog.h
%dir %{_libdir}/swipl-%{swiplversion}/include/Yap
%{_libdir}/swipl-%{swiplversion}/include/Yap/YapInterface.h
%{_libdir}/swipl-%{swiplversion}/include/SWI-Stream.h
%dir %{_libdir}/swipl-%{swiplversion}/include/sicstus
%{_libdir}/swipl-%{swiplversion}/include/sicstus/sicstus.h
%{_libdir}/swipl-%{swiplversion}/bin/%{_arch}/swipl-ld
%{_libdir}/swipl-%{swiplversion}/bin/%{_arch}/swipl-rc
%{_bindir}/swipl-ld
%{_bindir}/swipl-rc
%{_libdir}/pkgconfig/swipl.pc
%{_libdir}/swipl-%{swiplversion}/lib/%{_arch}/libswipl.so
