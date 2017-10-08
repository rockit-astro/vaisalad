Name:      onemetre-vaisala-server
Version:   2.0
Release:   0
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
%if 0%{?suse_version}
Requires:  python3, python3-Pyro4, python3-pyserial, python3-warwick-observatory-common, observatory-log-client, %{?systemd_requires}
BuildRequires: systemd-rpm-macros
%endif
%if 0%{?centos_ver}
Requires:  python34, python34-Pyro4, python34-pyserial, python34-warwick-observatory-common, observatory-log-client, %{?systemd_requires}
%endif

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
%if 0%{?suse_version}
%service_add_pre vaisalad.service
%endif

%post
%if 0%{?suse_version}
%service_add_post vaisalad.service
%endif
%if 0%{?centos_ver}
%systemd_post vaisalad.service
%endif

%preun
%if 0%{?suse_version}
%stop_on_removal vaisalad.service
%service_del_preun vaisalad.service
%endif
%if 0%{?centos_ver}
%systemd_preun vaisalad.service
%endif

%postun
%if 0%{?suse_version}
%restart_on_update vaisalad.service
%service_del_postun vaisalad.service
%endif
%if 0%{?centos_ver}
%systemd_postun_with_restart vaisalad.service
%endif

%files
%defattr(0755,root,root,-)
%{_bindir}/vaisalad
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-onemetre-vaisala.rules
%{_unitdir}/vaisalad.service
%{_unitdir}/vaisala-reset-rain.service
%{_unitdir}/vaisala-reset-rain.target
%{_unitdir}/vaisala-reset-rain.timer
%changelog
