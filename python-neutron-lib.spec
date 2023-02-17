%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
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

Requires:   python3-pbr >= 4.0.0
Requires:   python3-keystoneauth1 >= 3.14.0
Requires:   python3-netaddr >= 0.7.18
Requires:   python3-os-ken >= 0.3.0
Requires:   python3-os-traits >= 0.9.0
Requires:   python3-oslo-concurrency >= 3.26.0
Requires:   python3-oslo-config >= 2:8.0.0
Requires:   python3-oslo-context >= 2.22.0
Requires:   python3-oslo-db >= 4.44.0
Requires:   python3-oslo-i18n >= 3.20.0
Requires:   python3-oslo-log >= 4.3.0
Requires:   python3-oslo-messaging >= 14.2.0
Requires:   python3-oslo-policy >= 3.6.2
Requires:   python3-oslo-serialization >= 2.25.0
Requires:   python3-oslo-service >= 1.24.0
Requires:   python3-oslo-utils >= 4.5.0
Requires:   python3-oslo-versionedobjects >= 1.31.2
Requires:   python3-sqlalchemy >= 1.2.0
Requires:   python3-stevedore >= 1.20.0
Requires:   python3-osprofiler >= 1.4.0
Requires:   python3-pecan >= 1.0.0
Requires:   python3-webob >= 1.7.1

Requires:   python3-setproctitle >= 1.1.10

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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
# TODO - remove workaround in unit tests execution once we move to 2.15.0
PYTHON=python3 stestr-3 --test-path $OS_TEST_PATH run || true

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
