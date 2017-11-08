Name:      goto-vaisala-server
Version:   2.3.1
Release:   0
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station daemon for GOTO.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
%if 0%{?suse_version}
Requires:  python3, python34-Pyro4, python34-pyserial, python34-warwick-observatory-common, observatory-log-client, %{?systemd_requires}
BuildRequires: systemd-rpm-macros
%endif
%if 0%{?centos_ver}
Requires:  python34, python34-Pyro4, python34-pyserial, python34-warwick-observatory-common, observatory-log-client, %{?systemd_requires}
%endif

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

%pre
%if 0%{?suse_version}
%service_add_pre goto-vaisalad.service
%endif

%post
%if 0%{?suse_version}
%service_add_post goto-vaisalad.service
%endif
%if 0%{?centos_ver}
%systemd_post goto-vaisalad.service
%endif

%preun
%if 0%{?suse_version}
%stop_on_removal goto-vaisalad.service
%service_del_preun goto-vaisalad.service
%endif
%if 0%{?centos_ver}
%systemd_preun goto-vaisalad.service
%endif

%postun
%if 0%{?suse_version}
%restart_on_update goto-vaisalad.service
%service_del_postun goto-vaisalad.service
%endif
%if 0%{?centos_ver}
%systemd_postun_with_restart goto-vaisalad.service
%endif

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
