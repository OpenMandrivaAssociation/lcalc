# mpfr patch not complete. Could be done by changing most places a
# template wants a mpfr_t to a double, or calling the proper mpfr_foo
# function. But due to large amount of patches required (and only a
# few done in patch0), better to just disable it to avoid breaking
# the package.

%define with_mpfr	0
%define name		lcalc

Name:		%{name}
Group:		Sciences/Mathematics
License:	LGPL
Summary:	C++ L-function class library and command line interface
Version:	1.21
Release:	%mkrel 1
Source:		http://pmmac03.math.uwaterloo.ca/~mrubinst/L_function_public/CODE/L-%{version}.tar.gz
# From sage tarball, lcalc spkg, debian directory
Source1:	lcalc.1
URL:		http://pmmac03.math.uwaterloo.ca/~mrubinst/L_function_public/L.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	gcc-c++
%if %{with_mpfr}
BuildRequires:	mpfr-devel
%endif
BuildRequires:	gmpxx-devel
BuildRequires:	libpari-devel

Patch0:		L-1.21.g++4.3.2-mpfr.patch

%description
C++ L-function class library and command line interface.

%package	devel
Group:		Development/C++
Summary:	Development files for %{name}

%description	devel
Development files for %{name}.

%prep
%setup -q -n L-%{version}

%if %{with_mpfr}
%patch0	-p1
%endif

# Make it actually link with the generated library
perl -pi							\
	-e 's|/lib/|/%{_lib}/|g;'				\
	-e 's|libLfunction.so|libLfunction.so.%{version}|g;'	\
	-e 's|(\$\(CC\).*cc )lib(Lfunction).so.%{version}|$1-L. -l$2|g;'\
	src/Makefile
rm -f src/libLfunction.a

%build
pushd src
# Create link before library is created
    ln -sf libLfunction.so.%{version} libLfunction.so
    %make							\
%if %{with_mpfr}
	PREPROCESSOR_DEFINE="-DUSE_MPFR"			\
%endif
	PARI_DEFINE="-DINCLUDE_PARI"				\
	LOCATION_PARI_H="%{_includedir}/pari"			\
	LOCATION_PARI_LIBRARY="%{_libdir}"			\
	all
popd

%install
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
pushd src
    %make							\
	INSTALL_DIR="%{buildroot}%{_prefix}"			\
	install
    rm -f %{buildroot}%{_includedir}/Lfunction/*.back
    rm -f %{buildroot}%{_includedir}/Lfunction/.??*
    mkdir -p %{buildroot}%{_datadir}/%{name}
    cp -fa example_data_files/* %{buildroot}%{_datadir}/%{name}
popd
cp %{SOURCE1} %{buildroot}%{_mandir}/man1
lzma -f -z %{buildroot}%{_mandir}/man1/`basename %{SOURCE1}`
ln -sf %{_libdir}/libLfunction.so-%{version}  %{buildroot}%{_libdir}/libLfunction.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_libdir}/libLfunction.so.%{version}
%{_datadir}/%{name}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/Lfunction
%{_includedir}/Lfunction/*
%{_libdir}/libLfunction.so
