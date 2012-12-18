%define libLfunction		%mklibname    Lfunction 1
%define libLfunction_devel	%mklibname -d Lfunction

Name:		lcalc
Group:		Sciences/Mathematics
License:	GPLv2+
Summary:	C++ L-function class library and command line interface
Version:	1.23
Release:	7
Source0:	http://oto.math.uwaterloo.ca/~mrubinst/L_function_public/CODE/L-1.23.tar.gz
# From sage tarball, lcalc spkg, debian directory
Source1:	lcalc.1
URL:		http://oto.math.uwaterloo.ca/~mrubinst/L_function_public/L.html
BuildRequires:	gcc-c++
BuildRequires:	gmpxx-devel
BuildRequires:	gomp-devel
BuildRequires:	libpari-devel
Patch0:		L-fix-broken-include-of-libc++.diff
# Build with newer pari
Patch1:		L-1.23-pari.patch
# Correct problem with inline functions casting to double with gcc 4.6 or newer
Patch2:		L-1.23-lcalc_to_double.patch

%description
C++ L-function class library and command line interface.

%package	-n %{libLfunction}
Group:		Sciences/Mathematics
Summary:	Runtime library for %{name}

%description	-n %{libLfunction}
Runtime library for %{name}.

%package	-n %{libLfunction_devel}
Group:		Development/C++
Summary:	Development files for %{name}
%rename		%{name}-devel
Requires:	%{libLfunction} = %{EVRD}

%description	-n %{libLfunction_devel}
Development files for %{name}.

%prep
%setup -q -n L-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
rm -f .*DS_Store
rm -f include/.*{DS_Store,.swp,.swap.crap,.back}
rm -f src/.*{DS_Store,.swp}
find . | xargs chmod a+r

# Make it actually link with the generated library
sed -e 's|/lib/|/%{_lib}/|g' \
 -e "s|^[^#]*LDFLAGS2.*LDFLAGS1.*\$|LDFLAGS2 = \$(LDFLAGS1) $RPM_LD_FLAGS|" \
 -e 's|libLfunction.so|libLfunction.so.%{version}|g' \
 -e 's|\($(CC).*cc\) libLfunction.so.%{version}|\1 -L. -lLfunction|g' \
 -e 's|-Xlinker -rpath .*||;' \
 -e "s|\(DYN_OPTION=shared\)|\1 -Wl,-soname=libLfunction.so.%{version} -lgomp $RPM_LD_FLAGS|" \
 -e 's|#\(OPENMP_FLAG = -fopenmp\)|\1|' \
 -i src/Makefile
sed -i -e 's/\r//' src/example_programs/example.cc
# Upstream tarball comes with a prebuilt library
rm -f src/libLfunction.a

%build
pushd src
# Create link before library is created
    ln -sf libLfunction.so.%{version} libLfunction.so
    %make							\
	EXTRA="$RPM_OPT_FLAGS"					\
	PARI_DEFINE="-DINCLUDE_PARI"				\
	LOCATION_PARI_H="%{_includedir}/pari"			\
	LOCATION_PARI_LIBRARY="%{_libdir}"			\
	all
popd
rm -f src/example_programs/example

%install
mkdir -p $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_bindir},%{_mandir}/man1}
pushd src
    make INSTALL_DIR="$RPM_BUILD_ROOT%{_prefix}" install
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
    pushd example_data_files
	for sample in *; do
	    install -p -m644 $sample $RPM_BUILD_ROOT%{_datadir}/%{name}/$sample
	done
    popd
    install -m644 example_programs/example.cc \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/example.cc
popd
install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf libLfunction.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libLfunction.so
# Correct permissions
chmod 644 $RPM_BUILD_ROOT%{_includedir}/Lfunction/*.h
# Make install creates include/Lfunction but sagemath wants include/lcalc
pushd $RPM_BUILD_ROOT%{_includedir}
    ln -sf Lfunction lcalc
popd

%files
%doc CONTRIBUTORS
%doc COPYING
%doc README
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man1/*

%files		-n %{libLfunction}
%{_libdir}/libLfunction.so.%{version}

%files		-n %{libLfunction_devel}
%{_includedir}/Lfunction
%{_includedir}/lcalc
%{_libdir}/libLfunction.so

%changelog
* Mon Dec 17 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.23-7
- Drop unfinished mpfr support patch.
- Update URL for source and home page.
- Generate library with a proper soname.
- Drop BuildRoot, mkrel, defattr and clean.
- Create library subpackage with proper major in name.
- Rename lcalc-devel subpackage to libLfunction_devel.

* Tue Jan 24 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.23-6mdv2012.0
+ Revision: 767481
- Rebuild with newer pari.

* Sat Apr 09 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.23-5
+ Revision: 652002
- Correct build with gcc 4.6.0

* Thu Nov 11 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.23-4mdv2011.0
+ Revision: 595921
- Rebuild with newer pari

* Tue Aug 17 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.23-3mdv2011.0
+ Revision: 571049
+ rebuild (emptylog)

* Tue Aug 17 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.23-2mdv2011.0
+ Revision: 571038
+ rebuild (emptylog)

* Wed Jul 14 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.23-1mdv2011.0
+ Revision: 552977
- Update to version 1.23.

* Sat May 09 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.21-2mdv2010.0
+ Revision: 373565
+ rebuild (emptylog)

* Thu Mar 26 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.21-1mdv2009.1
+ Revision: 361222
- Initial import of lcalc version 1.21.
  C++ L-function class library and command line interface
  http://pmmac03.math.uwaterloo.ca/~mrubinst/L_function_public/L.html
- lcalc

