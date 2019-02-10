Name:      goto-vaisala-server
Version:   2.4.0
Release:   0
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station daemon for GOTO.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python36, python36-Pyro4, python36-pyserial, python36-warwick-observatory-common
Requires:  observatory-log-client, %{?systemd_requires}

%description
Part of the observatory software for GOTO.

vaisalad recieves data from a Vaisala WXT530 weather station attached via a USB-RS232 adaptor and
makes the latest measurement available for other services via Pyro.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/vaisalad %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/goto-vaisalad.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/vaisala-reset-rain.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/vaisala-reset-rain.target %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/vaisala-reset-rain.timer %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/10-goto-vaisala.rules %{buildroot}%{_udevrulesdir}

%post
%systemd_post goto-vaisalad.service

%preun
%systemd_preun goto-vaisalad.service

%postun
%systemd_postun_with_restart goto-vaisalad.service

%files
%defattr(0755,root,root,-)
%{_bindir}/vaisalad
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-goto-vaisala.rules
%{_unitdir}/goto-vaisalad.service
%{_unitdir}/vaisala-reset-rain.service
%{_unitdir}/vaisala-reset-rain.target
%{_unitdir}/vaisala-reset-rain.timer

%changelog
