%define		major	2.5
%define		minor	1
#empty debug package
%define debug_package	%{nil}
Name:		openshot
Version:	%{major}.%{minor}
Release:	2
Summary:	Simple and Powerful video editor
Group:		Video
License:	GPLv3+
URL:		http://www.openshot.org/
Source0:	https://github.com/OpenShot/openshot-qt/archive/v%{version}/%{name}-qt-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pyqt5-sip)
BuildRequires:  PyQt5
BuildRequires:	frei0r-plugins-devel
BuildRequires:	ladspa-devel
Requires:	python-mlt >= 0.8.8
Requires:	python-qt5
Requires:	python-imaging
Requires:	python-zmq
Requires:	python-libopenshot
Requires:	pyxdg
#Requires:	python-httplib2
Requires:	frei0r-plugins
Requires:	ladspa
# FIXME this is not a typo -- openshot does require uic bits.
# Probably parts of python uic need to move out of -devel.
Requires:	python-qt5-devel

%description
OpenShot Video Editor is a free, open-source, non-linear video editor, based on
Python, Qt, MLT and frei0r. It can edit video and audio files, composite and 
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


%files -f %{name}.filelist
%doc COPYING AUTHORS
