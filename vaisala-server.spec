Name:      onemetre-vaisala-server
Version:   1.13
Release:   1
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-pyserial, python3-warwickobservatory, onemetre-obslog-client, %{?systemd_requires}
BuildRequires: systemd-rpm-macros

%description
Part of the observatory software for the Warwick one-meter telescope.

vaisalad recieves data from a Vaisala WXT520 weather station attached via a USB-RS232 adaptor and
makes the latest measurement available for other services via Pyro.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/vaisalad %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/vaisalad.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/vaisala-reset-rain.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/vaisala-reset-rain.target %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/vaisala-reset-rain.timer %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/10-onemetre-vaisala.rules %{buildroot}%{_udevrulesdir}

%pre
%service_add_pre vaisalad.service

%post
%service_add_post vaisalad.service

%preun
%stop_on_removal vaisalad.service
%service_del_preun vaisalad.service

%postun
%restart_on_update vaisalad.service
%service_del_postun vaisalad.service

%files
%defattr(0755,root,root,-)
%{_bindir}/vaisalad
%{_udevrulesdir}/10-onemetre-vaisala.rules
%defattr(-,root,root,-)
%{_unitdir}/vaisalad.service
%{_unitdir}/vaisala-reset-rain.service
%{_unitdir}/vaisala-reset-rain.target
%{_unitdir}/vaisala-reset-rain.timer
%changelog
