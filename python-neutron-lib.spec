%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library neutron-lib
%global module neutron_lib

Name:       python-%{library}
Version:    0.0.3
Release:    1%{?dist}
Summary:    OpenStack Neutron library
License:    ASL 2.0
URL:        http://launchpad.net/neutron/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{version}%{?milestone}.tar.gz

BuildArch:  noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

Requires:   python-babel >= 1.3
Requires:   python-debtcollector >= 1.2.0
Requires:   python-oslo-config >= 2:3.4.0
Requires:   python-oslo-db >= 4.1.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-log >= 1.14.0
Requires:   python-oslo-messaging >= 4.0.0
Requires:   python-oslo-service >= 1.0.0
Requires:   python-oslo-utils >= 3.4.0


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
BuildRequires: python-oslo-sphinx

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
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

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
%doc html README.rst

%changelog
* Wed Sep 14 2016 Haikel Guemar <hguemar@fedoraproject.org> 0.0.3-1
- Update to 0.0.3

* Thu Mar 24 2016 RDO <rdo-list@redhat.com> 0.0.2-0.1
- RC1 Rebuild for Mitaka .2
