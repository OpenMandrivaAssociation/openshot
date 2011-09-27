%define		major 1.4
%define		minor 0

Name:           openshot
Version:        %{major}.%{minor}
Release:        %mkrel 1
Summary:        GNOME Non-linear video editor 

Group:          Video
License:        GPLv3+
URL:            http://www.openshotvideo.com/

Source0:        http://launchpad.net/openshot/%{major}/%{version}/+download/openshot-%{version}.tar.gz
Patch0:		default_window_size_is_too_big.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch

#BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: python-devel

Requires:      pygoocanvas
Requires:      pygtk2
Requires:      pygtk2.0-libglade
Requires:      python-imaging
Requires:      python-mlt

%description
OpenShot Video Editor is a free, open-source, non-linear video editor, based on
Python, GTK, and MLT. It can edit video and audio files, composite and 
transition video files, and mix multiple layers of video and audio together and 
render the output in many different formats.


%prep
%setup -q -n %{name}-%{version}
#%patch0 -p0

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT 

# Remove unnecessary file
%{__rm} %{buildroot}/%{_usr}/lib/mime/packages/openshot

# We strip bad shebangs (/usr/bin/env) instead of fixing them
# since these files are not executable anyways
find %{buildroot}/%{python_sitelib} -name '*.py' \
  -exec grep -q '^#!' '{}' \; -print | while read F
do
  awk '/^#!/ {if (FNR == 1) next;} {print}' $F >chopped
  touch -r $F chopped
  mv chopped $F
done


desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# modify find-lang.sh to deal with gettext .mo files under
# openshot/locale
%{__sed} -e 's|/share/locale/|/%{name}/locale/|' \
 /usr/lib/rpm/find-lang.sh \
 > find-lang-modified.sh

sh find-lang-modified.sh %{buildroot} OpenShot %{name}.lang
find %{buildroot}%{python_sitelib}/%{name}/locale -type d | while read dir
do
 echo "%%dir ${dir#%{buildroot}}" >> %{name}.lang
done


%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :


%postun
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING AUTHORS 
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/blender/
%{python_sitelib}/%{name}/classes/
%{python_sitelib}/%{name}/effects/
%{python_sitelib}/%{name}/export_presets
%{python_sitelib}/%{name}/images
%{python_sitelib}/%{name}/language
%{python_sitelib}/%{name}/locale
%{python_sitelib}/%{name}/profiles
%{python_sitelib}/%{name}/themes
%{python_sitelib}/%{name}/titles
%{python_sitelib}/%{name}/transitions
%{python_sitelib}/%{name}/uploads
%{python_sitelib}/%{name}/windows
%{python_sitelib}/*egg-info
%{_mandir}/man*/* 


