# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global library neutron-lib
%global module neutron_lib

%global common_desc OpenStack Neutron library shared by all Neutron sub-projects.

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Neutron library
License:    ASL 2.0
URL:        http://launchpad.net/neutron/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n  python%{pyver}-%{library}
Summary:    OpenStack Neutron library
%{?python_provide:%python_provide python%{pyver}-%{library}}
# Required for tests
BuildRequires: python%{pyver}-keystoneauth1
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-stestr
BuildRequires: python%{pyver}-testtools
BuildRequires: python%{pyver}-osprofiler
BuildRequires: python%{pyver}-pecan
BuildRequires: python%{pyver}-six
BuildRequires: python%{pyver}-testscenarios
BuildRequires: python%{pyver}-testresources
BuildRequires: python%{pyver}-os-traits
BuildRequires: python%{pyver}-oslo-context
BuildRequires: python%{pyver}-oslo-concurrency
BuildRequires: python%{pyver}-oslo-db
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-oslo-log
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-oslo-policy
BuildRequires: python%{pyver}-oslo-service
BuildRequires: python%{pyver}-fixtures
BuildRequires: python%{pyver}-netaddr

# Handle python2 exception
%if %{pyver} == 2
BuildRequires: python-weakrefmethod
BuildRequires: python-setproctitle
%else
BuildRequires: python%{pyver}-setproctitle
%endif

Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-keystoneauth1 >= 3.4.0
Requires:   python%{pyver}-os-traits >= 0.9.0
Requires:   python%{pyver}-oslo-concurrency >= 3.26.0
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-oslo-context >= 2.19.2
Requires:   python%{pyver}-oslo-db >= 4.37.0
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-oslo-messaging >= 5.29.0
Requires:   python%{pyver}-oslo-policy >= 1.30.0
Requires:   python%{pyver}-oslo-serialization >= 2.18.0
Requires:   python%{pyver}-oslo-service >= 1.24.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-oslo-versionedobjects >= 1.31.2
Requires:   python%{pyver}-sqlalchemy >= 1.2.0
Requires:   python%{pyver}-stevedore
Requires:   python%{pyver}-osprofiler >= 1.4.0
Requires:   python%{pyver}-pecan >= 1.0.0
Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-webob >= 1.7.1

# Handle python2 exception
%if %{pyver} == 2
Requires:   python-weakrefmethod  >= 1.0.2
Requires:   python-setproctitle
%else
Requires:   python%{pyver}-setproctitle
%endif

%description -n python%{pyver}-%{library}
%{common_desc}


%package -n python%{pyver}-%{library}-tests
Summary:    OpenStack Neutron library tests
%{?python_provide:%python_provide python%{pyver}-%{library}-tests}
Requires:   python%{pyver}-%{library} = %{version}-%{release}

%description -n python%{pyver}-%{library}-tests
%{common_desc}

This package contains the Neutron library test files.

%if 0%{?with_doc}
%package doc
Summary:    OpenStack Neutron library documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
export OS_TEST_PATH='./neutron_lib/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
