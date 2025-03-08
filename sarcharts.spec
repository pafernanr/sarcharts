Name: sarcharts
Version: 0.0.0
Release: py3
Summary: SarCharts gets sysstat files from provided sarfilespaths and generates dynamic HTML Charts.

License: GPLv3
URL:            https://github.com/pafernanr/sarcharts
Source0: https://github.com/pafernanr/%{name}-%{version}.tar.gz
Group: Applications/System
BuildArch: noarch

BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires: python3-jinja2

%description
SarCharts gets sysstat files from provided sarfilespaths and generates dynamic HTML Charts

%prep
%setup -qn %{name}-%{version}

%build

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/tools/sarcharts/bin
install -D -m 755 sarcharts/bin/__init__.py ${RPM_BUILD_ROOT}/usr/lib/tools/sarcharts/bin/__init__.py
cp -rp sarcharts ${RPM_BUILD_ROOT}/usr/lib/tools/

rm -rf ${RPM_BUILD_ROOT}/usr/lib/tools/%{name}/lib/__pycache__
rm -rf ${RPM_BUILD_ROOT}/usr/lib/tools/%{name}/html/images

%post
ln -s -f /usr/lib/tools/sarcharts/bin/__init__.py /usr/bin/sarcharts

%postun
if [ $1 -eq 0 ] ; then
    rm -f /usr/bin/%{name}
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
/usr/lib/tools/sarcharts
