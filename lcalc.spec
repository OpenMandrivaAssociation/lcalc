%define major	1
%define libname	%mklibname	Lfunction
%define devname	%mklibname	Lfunction -d

Summary:	C++ L-function class library and command line interface
Name:		lcalc
License:	GPLv2+
Version:	2.0.5
Release:	1
URL:		https://gitlab.com/sagemath/lcalc
Source0:	https://gitlab.com/sagemath/lcalc/-/archive/%{version}/%{name}-%{version}.tar.bz2
# From sage tarball, lcalc spkg, debian directory
#Source1:	lcalc.1
#Source2:	%{name}.rpmlintrc

BuildRequires:	gcc-c++
BuildRequires:	gengetopt
#BuildRequires:	gomp-devel
#BuildRequires:	pkgconfig(gmpxx)
BuildRequires:	libpari-devel

%description
C++ L-function class library and command line interface.

%files
%license doc/COPYING
%doc doc/{ChangeLog,CONTRIBUTORS,README.md}
%{_bindir}/%{name}
%{_mandir}/man1/lcalc.1*

#---------------------------------------------------------------------------

%package	-n %{libname}
Summary:	Runtime library for %{name}

%description	-n %{libname}
Runtime library for %{name}.

%files		-n %{libname}
%{_libdir}/libLfunction.so.%{major}*

#---------------------------------------------------------------------------

%package	-n %{devname}
Summary:	Development files for %{name}
%rename		%{name}-devel

Requires:	%{libname} = %{EVRD}

%description	-n %{devname}
Development files for %{name}.

%files		-n %{devname}
%doc doc/examples
%{_includedir}/%{name}/
%{_libdir}/libLfunction.so
%{_libdir}/pkgconfig/%{name}.pc

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure \
	--with-pari

# (fedora)
# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build

%install
%make_install

# data dir
install -pm 0755 -d %{buildroot}%{_datadir}/%{name}

# manually select docs
rm -fr %{buildroot}%{_docdir}/lcalc

%check
%make check

