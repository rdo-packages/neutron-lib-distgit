%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library neutron-lib
%global module neutron_lib

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global common_desc OpenStack Neutron library shared by all Neutron sub-projects.

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Neutron library
License:    ASL 2.0
URL:        http://launchpad.net/neutron/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git

%description
%{common_desc}

%package -n  python2-%{library}
Summary:    OpenStack Neutron library
%{?python_provide:%python_provide python2-%{library}}
# Required for tests
BuildRequires: python2-keystoneauth1
BuildRequires: python2-os-testr
BuildRequires: python2-oslotest
BuildRequires: python2-testtools
%if 0%{?fedora} > 0
BuildRequires: python2-osprofiler
BuildRequires: python2-pecan
BuildRequires: python2-six
BuildRequires: python2-testscenarios
BuildRequires: python2-testresources
BuildRequires: python2-weakrefmethod
%else
BuildRequires: python-osprofiler
BuildRequires: python-pecan
BuildRequires: python-six
BuildRequires: python-testscenarios
BuildRequires: python-testresources
BuildRequires: python-weakrefmethod
%endif

Requires:   python2-pbr
Requires:   python2-debtcollector >= 1.2.0
Requires:   python2-keystoneauth1 >= 3.3.0
Requires:   python2-oslo-concurrency >= 3.25.0
Requires:   python2-oslo-config >= 2:5.1.0
Requires:   python2-oslo-context >= 2.19.2
Requires:   python2-oslo-db >= 4.27.0
Requires:   python2-oslo-i18n >= 3.15.3
Requires:   python2-oslo-log >= 3.36.0
Requires:   python2-oslo-messaging >= 5.29.0
Requires:   python2-oslo-policy >= 1.30.0
Requires:   python2-oslo-serialization >= 2.18.0
Requires:   python2-oslo-service >= 1.24.0
Requires:   python2-oslo-utils >= 3.33.0
Requires:   python2-sqlalchemy >= 1.0.10
Requires:   python2-stevedore
%if 0%{?fedora} > 0
Requires:   python2-osprofiler >= 1.4.0
Requires:   python2-pecan >= 1.0.0
Requires:   python2-six >= 1.10.0
Requires:   python2-weakrefmethod >= 1.0.2
Requires:   python2-webob >= 1.7.1
%else
Requires:   python-osprofiler >= 1.4.0
Requires:   python-pecan >= 1.0.0
Requires:   python-six >= 1.10.0
Requires:   python-weakrefmethod >= 1.0.2
Requires:   python-webob >= 1.7.1
%endif

%description -n python2-%{library}
%{common_desc}


%package -n python2-%{library}-tests
Summary:    OpenStack Neutron library tests
%{?python_provide:%python_provide python2-%{library}-tests}
Requires:   python2-%{library} = %{version}-%{release}

%description -n python2-%{library}-tests
%{common_desc}

This package contains the Neutron library test files.

%if 0%{?with_python3}
%package -n  python3-%{library}
Summary:    OpenStack Neutron library
%{?python_provide:%python_provide python3-%{library}}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
# Required for tests
BuildRequires: python3-keystoneauth1
BuildRequires: python3-os-testr
BuildRequires: python3-oslo-db
BuildRequires: python3-oslo-policy
BuildRequires: python3-oslotest
BuildRequires: python3-osprofiler
BuildRequires: python3-pecan
BuildRequires: python3-six
BuildRequires: python3-testresources
BuildRequires: python3-testscenarios
BuildRequires: python3-testtools

Requires:   python3-pbr
Requires:   python3-debtcollector >= 1.2.0
Requires:   python3-keystoneauth1 >= 3.3.0
Requires:   python3-oslo-concurrency >= 3.25.0
Requires:   python3-oslo-config >= 2:5.1.0
Requires:   python3-oslo-context >= 2.19.2
Requires:   python3-oslo-db >= 4.27.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-oslo-messaging >= 5.29.0
Requires:   python3-oslo-policy >= 1.30.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-oslo-service >= 1.24.0
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-osprofiler >= 1.4.0
Requires:   python3-pecan >= 1.0.0
Requires:   python3-six >= 1.10.0
Requires:   python3-sqlalchemy >= 1.0.10
Requires:   python3-stevedore
Requires:   python3-webob >= 1.7.1

%description -n python3-%{library}
%{common_desc}

%package -n python3-%{library}-tests
Summary:    OpenStack Neutron library tests
%{?python_provide:%python_provide python3-%{library}-tests}
Requires:   python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
%{common_desc}

This package contains the Neutron library test files.
%endif


%package doc
Summary:    OpenStack Neutron library documentation

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-oslo-context
BuildRequires: python2-oslo-concurrency
BuildRequires: python2-oslo-db
BuildRequires: python2-oslo-i18n
BuildRequires: python2-oslo-log
BuildRequires: python2-oslo-utils
BuildRequires: python2-oslo-policy
BuildRequires: python2-oslo-service
BuildRequires: python2-debtcollector
BuildRequires: python2-fixtures
BuildRequires: openstack-macros
%if 0%{?fedora} > 0
BuildRequires: python2-netaddr
%else
BuildRequires: python-netaddr
%endif

%description doc
%{common_desc}

This package contains the documentation.

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
export OS_TEST_PATH='./neutron_lib/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr --test-path $OS_TEST_PATH run
%if 0%{?with_python3}
rm -rf .stestr
stestr-3 --test-path $OS_TEST_PATH run
%endif

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif

%files doc
%license LICENSE
%doc doc/build/html README.rst

%changelog
