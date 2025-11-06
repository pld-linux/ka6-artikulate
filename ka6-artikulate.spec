#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		artikulate
Summary:	Artikulate
Name:		ka6-%{kaname}
Version:	25.08.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	7ba3b27ee127637e8e44214dc95bae06
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Multimedia-devel
BuildRequires:	Qt6Network-devel >= 5.11.1
BuildRequires:	Qt6Qml-devel
BuildRequires:	Qt6Quick-devel
BuildRequires:	Qt6Sql-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Artikulate is a language learning application that helps improving
pronunciation skills for various languages. This repository maintains
the application and language specifications. All course files are
maintained in a separate repository named "artikulate-data" and hosted
on the KDE infrastructure.

%description -l pl.UTF-8
Artikulate jest programem wspomagającym naukę języków, który pomaga
poprawić umiejętności wymowy dla wielu z nich. To repozytorium zawiera
program i specyfikacje języków. Wszystkie plików kursów są utrzymywane
w oddzielnym repozytorum nazwanym "artikulate-data" i hostowanym przez
infrastrukturę KDE.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/artikulate
%attr(755,root,root) %{_bindir}/artikulate_editor
%{_libdir}/libartikulatecore.so.0
%{_libdir}/libartikulatelearnerprofile.so.0
%{_desktopdir}/org.kde.artikulate.desktop
%{_datadir}/config.kcfg/artikulate.kcfg
%{_iconsdir}/hicolor/*x*/apps/artikulate.png
%{_iconsdir}/hicolor/scalable/apps/artikulate.svg
%{_datadir}/knsrcfiles/artikulate.knsrc
%{_datadir}/metainfo/org.kde.artikulate.appdata.xml
