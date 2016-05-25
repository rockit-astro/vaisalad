Name:      onemetre-vaisala-test
Version:   1.1
Release:   0
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-pyserial, %{?systemd_requires}
BuildRequires: systemd-rpm-macros

%description
Part of the observatory software for the Warwick one-meter telescope.

vaisalad-test simulates the behaviour of vaisalad using previously recorded data.
vaisala is the regular client patched to use the local test server.

%build
mkdir -p %{buildroot}%{_bindir}

%{__install} %{_sourcedir}/vaisalad-test %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/vaisala %{buildroot}%{_bindir}

%files
%defattr(0755,root,root,-)
%{_bindir}/vaisalad-test
%{_bindir}/vaisala

%changelog
