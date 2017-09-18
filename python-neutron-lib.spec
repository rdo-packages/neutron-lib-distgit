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
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

%description
%{common_desc}

%package -n  python2-%{library}
Summary:    OpenStack Neutron library
%{?python_provide:%python_provide python2-%{library}}
# Required for tests
BuildRequires: python-os-testr
BuildRequires: python-oslotest
BuildRequires: python-testresources
BuildRequires: python-testscenarios
BuildRequires: python-testtools

Requires:   python-debtcollector >= 1.2.0
Requires:   python-oslo-concurrency >= 3.8.0
Requires:   python-oslo-config >= 2:4.0.0
Requires:   python-oslo-context >= 2.14.0
Requires:   python-oslo-db >= 4.24.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-messaging >= 5.24.2
Requires:   python-oslo-policy >= 1.23.0
Requires:   python-oslo-service >= 1.10.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-sqlalchemy >= 1.0.10
Requires:   python-stevedore

%description -n python2-%{library}
%{common_desc}


%package -n python2-%{library}-tests
Summary:    OpenStack Neutron library tests
%{?python_provide:%python_provide python2-%{library}-tests}
Requires:   python-%{library} = %{version}-%{release}

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
BuildRequires: python3-os-testr
BuildRequires: python3-oslotest
BuildRequires: python3-testresources
BuildRequires: python3-testscenarios
BuildRequires: python3-testtools

Requires:   python3-debtcollector >= 1.2.0
Requires:   python3-oslo-concurrency >= 3.8.0
Requires:   python3-oslo-config >= 2:4.0.0
Requires:   python3-oslo-context >= 2.14.0
Requires:   python3-oslo-db >= 4.24.0
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-oslo-log >= 3.22.0
Requires:   python3-oslo-messaging >= 5.24.2
Requires:   python3-oslo-policy >= 1.23.0
Requires:   python3-oslo-service >= 1.10.0
Requires:   python3-oslo-utils >= 3.20.0
Requires:   python3-sqlalchemy >= 1.0.10
Requires:   python3-stevedore

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

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme
BuildRequires: python-oslo-context
BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-utils
BuildRequires: python-oslo-policy
BuildRequires: python-oslo-service
BuildRequires: python-netaddr
BuildRequires: python-debtcollector
BuildRequires: python-fixtures
BuildRequires: openstack-macros

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
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -fr .testrepository
%{__python3} setup.py test
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
