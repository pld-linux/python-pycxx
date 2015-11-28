%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module
#
%global modname pycxx
#
Summary:	Write Python extensions in C++
Name:		python-%{modname}
Version:	6.2.6
Release:	1
License:	BSD
Group:		Development/Libraries
URL:		http://CXX.sourceforge.net/
BuildArch:	noarch
Source0:	http://downloads.sourceforge.net/cxx/%{modname}-%{version}.tar.gz
# Source0-md5:	20bcc50e9529aad3d646c1c48c1502d9
# Patch0:  remove unnecessary 'Src/' directory from include path in sources
Patch0:		%{name}-6.2.4-change-include-paths.patch
# Patch1:  fix several problems with install, esp. omitted files, python
# v2/v3 awareness
Patch1:		%{name}-6.2.4-setup.py.patch
# Patch2:  fix python 3 syntax error (print() is a function)
Patch2:		%{name}-6.2.4-python3-syntax-fix.patch
%{?with_python2:BuildRequires:	python-devel}
%{?with_python3:BuildRequires:	python3-devel}

%description
PyCXX is a set of classes to help create extensions of Python in the
C++ language. The first part encapsulates the Python C API taking care
of exceptions and ref counting. The second part supports the building
of Python extension modules in C++.

%package devel
Summary:	PyCXX header and source files
Group:		Development/Libraries
Requires:	python

%description devel
PyCXX is a set of classes to help create extensions of Python in the
C++ language. The first part encapsulates the Python C API taking care
of exceptions and ref counting. The second part supports the building
of Python extension modules in C++.

The %{name}-devel package provides the header and source files for
Python 2. There is no non-devel package needed.

%package -n python3-%{modname}-devel
Summary:	PyCXX header and source files
Group:		Development/Libraries
Requires:	python3

%description -n python3-%{modname}-devel
PyCXX is a set of classes to help create extensions of Python in the
C++ language. The first part encapsulates the Python C API taking care
of exceptions and ref counting. The second part supports the building
of Python extension modules in C++.

The python3-%{modname}-devel package provides the header and source
files for Python 3. There is no non-devel package needed.

%prep
%setup -q -n %{modname}-%{version}
%patch0 -p1 -b .change-include-paths
%patch1 -p1 -b .setup
%patch2 -p1 -b .python3-syntax-fix


%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install \
	--install-data=%{_datadir}/%{name} \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%py3_install \
	--install-data=%{_datadir}/python3-%{modname} \
	--root=$RPM_BUILD_ROOT
%endif

# Write pkg-config PyCXX.pc file
install -d $RPM_BUILD_ROOT%{_npkgconfigdir}

%if %{with python2}
cat > $RPM_BUILD_ROOT%{_npkgconfigdir}/PyCXX.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
includedir=%{py_incdir}
srcdir=%{_datadir}/%{name}/CXX

Name: PyCXX
Description: Write Python extensions in C++
Version: %{version}
Cflags: -I\${includedir}
EOF
%endif

%if %{with python3}
cat > $RPM_BUILD_ROOT%{_npkgconfigdir}/Py3CXX.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
includedir=%{py3_incdir}
srcdir=%{_datadir}/python3-%{modname}/CXX

Name: Py3CXX
Description: Write Python 3 extensions in C++
Version: %{version}
Cflags: -I\${includedir}
EOF
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files devel
%defattr(644,root,root,755)
%doc README.html COPYRIGHT Doc/Python2/
%{_includedir}/python2*
%{py_sitescriptdir}/CXX*
%{_datadir}/%{name}
%{_npkgconfigdir}/PyCXX.pc
%endif

%if %{with python3}
%files -n python3-%{modname}-devel
%defattr(644,root,root,755)
%doc README.html COPYRIGHT Doc/Python3/
%{_includedir}/python3*/CXX
%{py3_sitescriptdir}/CXX*
%{_datadir}/python3-%{modname}
%{_npkgconfigdir}/Py3CXX.pc
%endif
