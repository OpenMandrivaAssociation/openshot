%define		major	2.6
%define		minor	1
#empty debug package
%define debug_package	%{nil}
Name:		openshot
Version:	4.1.0
Release:	1
Summary:	Simple and Powerful video editor
Group:		Video
License:	GPLv3+
URL:		https://www.openshot.org/
Source0:	https://github.com/OpenShot/openshot-qt/archive/v%{version}/%{name}-qt-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(defusedxml)
BuildRequires:	python-qt6
BuildRequires:	python-qt6-devel
BuildRequires:	python-qt6-statemachine
Requires:	python-qt6
# PyQt6.uic.loadUi lives in the -devel package.
Requires:	python-qt6-devel
Requires:	python-qt6-statemachine
Requires:	python%{pyver}dist(defusedxml)
Requires:	python%{pyver}dist(requests)
Requires:	python-libopenshot >= 1.1.0

%description
OpenShot Video Editor is a free, open-source, non-linear video editor, based on
Python, Qt, and libopenshot. It can edit video and audio files, composite and
transition video files, and mix multiple layers of video and audio together and
render the output in many different formats.

%prep
%autosetup -p1 -n %{name}-qt-%{version}

%build
CFLAGS="%{optflags}" %__python setup.py build

%install
%__python setup.py install -O1 --skip-build --root=%{buildroot} --record=%{name}.filelist

# We strip bad shebangs (/usr/bin/env) instead of fixing them
# since these files are not executable anyways
find %{buildroot}/%{python_sitelib} -name '*.py' \
  -exec grep -q '^#!' '{}' \; -print | while read F
do
  awk '/^#!/ {if (FNR == 1) next;} {print}' $F >chopped
  touch -r $F chopped
  mv chopped $F
done


%files
%doc COPYING
%{_bindir}/openshot-qt
%{_bindir}/openshot-cli
%{_prefix}/lib/mime/packages/openshot-qt
%{python_sitelib}/openshot_qt-%{version}*
%{python_sitelib}/openshot_qt/
%{_datadir}/applications/org.openshot.OpenShot.desktop
%{_datadir}/metainfo/org.openshot.OpenShot.appdata.xml
%{_datadir}/mime/packages/org.openshot.OpenShot.xml
%{_datadir}/pixmaps/openshot-qt.svg
%{_iconsdir}/hicolor/*x*/apps/openshot-qt.png
%{_iconsdir}/hicolor/scalable/apps/openshot-qt.svg
%{_iconsdir}/hicolor/scalable/mimetypes/openshot-qt-doc.svg
