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

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n  python3-%{library}
Summary:    OpenStack Neutron library
%{?python_provide:%python_provide python3-%{library}}
# Required for tests
BuildRequires: python3-keystoneauth1
BuildRequires: python3-oslotest
BuildRequires: python3-stestr
BuildRequires: python3-testtools
BuildRequires: python3-osprofiler
BuildRequires: python3-pecan
BuildRequires: python3-six
BuildRequires: python3-testscenarios
BuildRequires: python3-testresources
BuildRequires: python3-os-ken
BuildRequires: python3-os-traits
BuildRequires: python3-oslo-context
BuildRequires: python3-oslo-concurrency
BuildRequires: python3-oslo-db
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-log
BuildRequires: python3-oslo-utils
BuildRequires: python3-oslo-versionedobjects
BuildRequires: python3-oslo-policy
BuildRequires: python3-oslo-service
BuildRequires: python3-fixtures
BuildRequires: python3-netaddr

BuildRequires: python3-setproctitle

Requires:   python3-pbr
Requires:   python3-keystoneauth1 >= 3.4.0
Requires:   python3-netaddr >= 0.7.18
Requires:   python3-os-ken >= 0.3.0
Requires:   python3-os-traits >= 0.9.0
Requires:   python3-oslo-concurrency >= 3.26.0
Requires:   python3-oslo-config >= 2:5.2.0
Requires:   python3-oslo-context >= 2.19.2
Requires:   python3-oslo-db >= 4.37.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-oslo-messaging >= 5.29.0
Requires:   python3-oslo-policy >= 1.30.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-oslo-service >= 1.24.0
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-oslo-versionedobjects >= 1.31.2
Requires:   python3-sqlalchemy >= 1.2.0
Requires:   python3-stevedore
Requires:   python3-osprofiler >= 1.4.0
Requires:   python3-pecan >= 1.0.0
Requires:   python3-webob >= 1.7.1

Requires:   python3-setproctitle

%description -n python3-%{library}
%{common_desc}


%package -n python3-%{library}-tests
Summary:    OpenStack Neutron library tests
%{?python_provide:%python_provide python3-%{library}-tests}
Requires:   python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
%{common_desc}

This package contains the Neutron library test files.

%if 0%{?with_doc}
%package doc
Summary:    OpenStack Neutron library documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
rm -f ./neutron_lib/tests/unit/hacking/test_checks.py
export OS_TEST_PATH='./neutron_lib/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
PYTHON=python3 stestr-3 --test-path $OS_TEST_PATH run

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/neutron-lib/commit/?id=245e005d1bbb9af5e57ff600fb97b2a13c85c83b
