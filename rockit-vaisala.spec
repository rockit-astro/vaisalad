Name:      rockit-vaisala
Version:   %{_version}
Release:   1
Summary:   Weather station
Url:       https://github.com/rockit-astro/vaisalad
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/vaisalad/
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/vaisala %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/vaisalad %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/vaisalad@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/completion/vaisala %{buildroot}/etc/bash_completion.d/vaisala

%{__install} %{_sourcedir}/config/onemetre.json %{buildroot}%{_sysconfdir}/vaisalad/
%{__install} %{_sourcedir}/config/goto.json %{buildroot}%{_sysconfdir}/vaisalad/
%{__install} %{_sourcedir}/config/halfmetre.json %{buildroot}%{_sysconfdir}/vaisalad/
%{__install} %{_sourcedir}/config/warwick.json %{buildroot}%{_sysconfdir}/vaisalad/
%{__install} %{_sourcedir}/config/10-lapalma-vaisala.rules %{buildroot}%{_udevrulesdir}

%package server
Summary:  Weather station server
Group:    Unspecified
Requires: python3-rockit-vaisala
%description server

%package client
Summary:  Weather station client
Group:    Unspecified
Requires: python3-rockit-vaisala
%description client

%files server
%defattr(0755,root,root,-)
%{_bindir}/vaisalad
%defattr(0644,root,root,-)
%{_unitdir}/vaisalad@.service

%files client
%defattr(0755,root,root,-)
%{_bindir}/vaisala
/etc/bash_completion.d/vaisala

%package data-lapalma
Summary: Weather station data for La Palma telescopes
Group:   Unspecified
%description data-lapalma

%files data-lapalma
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-lapalma-vaisala.rules
%{_sysconfdir}/vaisalad/onemetre.json
%{_sysconfdir}/vaisalad/goto.json
%{_sysconfdir}/vaisalad/halfmetre.json

%package data-warwick
Summary: Weather station data for Windmill Hill observatory
Group:   Unspecified
%description data-warwick

%files data-warwick
%defattr(0644,root,root,-)
%{_sysconfdir}/vaisalad/warwick.json

%changelog
