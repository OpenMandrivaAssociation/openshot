%define		major	1.4
%define		minor	3
#empty debug package
%define debug_package	%{nil}
Name:		openshot
Version:	%{major}.%{minor}
Release:	3
Summary:	Simple and Powerful video editor
Group:		Video
License:	GPLv3+
URL:		http://www.openshot.org/
Source0:	http://launchpad.net/openshot/%{major}/%{version}/+download/openshot-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	frei0r-plugins-devel
BuildRequires:	ladspa-devel
Requires:	python-mlt >= 0.8.8
Requires:	pygoocanvas
Requires:	pygtk2
Requires:	pygtk2.0-libglade
Requires:	python-imaging
Requires:	pyxdg
Requires:	python-httplib2
Requires:	frei0r-plugins
Requires:	ladspa

%description
OpenShot Video Editor is a free, open-source, non-linear video editor, based on
Python, GTK, MLT and frei0r. It can edit video and audio files, composite and 
transition video files, and mix multiple layers of video and audio together and 
render the output in many different formats.

%prep
%setup -q

%build
CFLAGS="%{optflags}" %__python setup.py build

%install
%__python setup.py install -O1 --skip-build --root=%{buildroot}

# Remove unnecessary file
%__rm %{buildroot}/%{_usr}/lib/mime/packages/openshot

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
%doc README COPYING AUTHORS
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%{python_sitelib}/%{name}/
%{python_sitelib}/*egg-info
%{_mandir}/man1/%{name}.1.xz  
%{_mandir}/man1/%{name}-render.1.xz
