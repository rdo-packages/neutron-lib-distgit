%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library neutron-lib
%global module neutron_lib

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

Requires:   python-debtcollector >= 1.2.0
Requires:   python-oslo-concurrency >= 3.8.0
Requires:   python-oslo-config >= 2:4.0.0
Requires:   python-oslo-context >= 2.14.0
Requires:   python-oslo-db >= 4.24.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-messaging >= 5.24.0
Requires:   python-oslo-policy >= 1.23.0
Requires:   python-oslo-service >= 1.10.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-sqlalchemy >= 1.0.10


%description
OpenStack Neutron library shared by all Neutron sub-projects.


%package tests
Summary:    OpenStack Neutron library tests
Requires:   python-%{library} = %{version}-%{release}

%description tests
OpenStack Neutron library shared by all Neutron sub-projects.

This package contains the Neutron library test files.


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

%description doc
OpenStack Neutron library shared by all Neutron sub-projects.

This package contains the documentation.

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install

%files
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files doc
%license LICENSE
%doc doc/build/html README.rst

%changelog
