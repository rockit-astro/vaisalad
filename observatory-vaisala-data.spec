Name:      observatory-vaisala-data
Version:   20230629
Release:   0
Url:       https://github.com/warwick-one-metre/vaisalad
Summary:   Weather station data for La Palma
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch

%description

%build
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_sysconfdir}/vaisalad/

%{__install} %{_sourcedir}/10-lapalma-vaisala.rules %{buildroot}%{_udevrulesdir}
%{__install} %{_sourcedir}/onemetre.json %{buildroot}%{_sysconfdir}/vaisalad/
%{__install} %{_sourcedir}/goto.json %{buildroot}%{_sysconfdir}/vaisalad/
%{__install} %{_sourcedir}/halfmetre.json %{buildroot}%{_sysconfdir}/vaisalad/

%files
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-lapalma-vaisala.rules
%{_sysconfdir}/vaisalad/onemetre.json
%{_sysconfdir}/vaisalad/goto.json
%{_sysconfdir}/vaisalad/halfmetre.json

%changelog
