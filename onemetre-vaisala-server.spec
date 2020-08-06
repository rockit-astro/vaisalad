Name:      onemetre-vaisala-server
Version:   3.0.1
Release:   0
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-pyserial, python3-warwick-observatory-common, python3-warwick-observatory-vaisala
Requires:  observatory-log-client, %{?systemd_requires}

%description
Part of the observatory software for the Warwick one-meter telescope.

vaisalad recieves data from a Vaisala WXT520 weather station attached via a USB-RS232 adaptor and
makes the latest measurement available for other services via Pyro.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_sysconfdir}/vaisalad/

%{__install} %{_sourcedir}/vaisalad %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/vaisalad.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/10-onemetre-vaisala.rules %{buildroot}%{_udevrulesdir}
%{__install} %{_sourcedir}/onemetre.json %{buildroot}%{_sysconfdir}/vaisalad/

%post
%systemd_post vaisalad.service

%preun
%systemd_preun vaisalad.service

%postun
%systemd_postun_with_restart vaisalad.service

%files
%defattr(0755,root,root,-)
%{_bindir}/vaisalad
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-onemetre-vaisala.rules
%{_unitdir}/vaisalad.service
%{_sysconfdir}/vaisalad/onemetre.json

%changelog
