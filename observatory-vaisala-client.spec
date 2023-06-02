Name:      observatory-vaisala-client
Version:   20230602
Release:   0
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station client for the Warwick telescopes.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3 python3-Pyro4 python3-warwick-observatory-common python3-warwick-observatory-vaisala

%description

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
