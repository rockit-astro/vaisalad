Name:      onemetre-vaisala-client
Version:   1.11
Release:   0
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station client for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4

%description
Part of the observatory software for the Warwick one-meter telescope.

vaisala is a commandline utility that prints the latest measurement in a human-readable form.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/vaisala %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/vaisala %{buildroot}/etc/bash_completion.d/vaisala

%files
%defattr(0755,root,root,-)
%{_bindir}/vaisala
/etc/bash_completion.d/vaisala

%changelog
