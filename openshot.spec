%define		major	1.4
%define		minor	2

Name:		openshot
Version:	%{major}.%{minor}
Release:	2
Summary:	Simple and Powerful video editor
Group:		Video
License:	GPLv3+
URL:		http://www.openshot.org/
Source0:	http://launchpad.net/openshot/%{major}/%{version}/+download/openshot-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	frei0r-plugins-devel
Requires:	python-mlt
Requires:	pygoocanvas
Requires:	pygtk2
Requires:	pygtk2.0-libglade
Requires:	python-imaging
Requires:	pyxdg
Requires:	python-httplib2
Suggests:	frei0r-plugins

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
%{python_sitelib}/%{name}
%{python_sitelib}/*egg-info
%{_mandir}/man*/*



%changelog
* Wed Feb 08 2012 Andrey Bondrov <abondrov@mandriva.org> 1.4.2-2
+ Revision: 771749
- Require pyxdg instead of python-pyxdg

* Wed Feb 08 2012 Andrey Bondrov <abondrov@mandriva.org> 1.4.2-1
+ Revision: 771728
- New version 1.4.2, update summary and description, spec cleanup

  + Александр Казанцев <kazancas@mandriva.org>
    - only suggests frei0r-plugins

* Sat Nov 19 2011 Александр Казанцев <kazancas@mandriva.org> 1.4.0-2
+ Revision: 731806
- add frei0r-plugins to BR and R

* Tue Sep 27 2011 Stéphane Téletchéa <steletch@mandriva.org> 1.4.0-1
+ Revision: 701411
- Update to latest 1.4.0
- Add major and minor conventions so the url can be parsed automatically by mdvsys

* Mon May 09 2011 Stéphane Téletchéa <steletch@mandriva.org> 1.3.1-1
+ Revision: 672778
- Update to 1.3.1

* Wed Mar 09 2011 Stéphane Téletchéa <steletch@mandriva.org> 1.3.0-2
+ Revision: 643044
- Add missing BR on python-imaging preventing openshot launch

* Mon Feb 14 2011 Lev Givon <lev@mandriva.org> 1.3.0-1
+ Revision: 637764
- Update to 1.3.0.

* Fri Nov 19 2010 Funda Wang <fwang@mandriva.org> 1.2.2-2mdv2011.0
+ Revision: 598903
- rebuild for py2.7

* Thu Sep 23 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.2.2-1mdv2011.0
+ Revision: 580803
- Update to 1.2.2
- It seems that our patch is not needed anymore, just disabling it for now, to revive it in case it is still needed

* Fri Jun 11 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.1.3-6mdv2010.1
+ Revision: 547865
- add missing requires

* Mon Jun 07 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.3-5mdv2010.1
+ Revision: 547196
- Re-introduce our patch to have the main window in a reasonable size, fixes bug #59251

* Fri Apr 16 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.3-4mdv2010.1
+ Revision: 535421
- Removing patch, upstream cairo has been fixed

* Wed Apr 14 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.3-2mdv2010.1
+ Revision: 534892
- Add patch to fix segfault in openshot, should fix #57815

* Tue Apr 13 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.3-1mdv2010.1
+ Revision: 534182
- New version 1.1.3

* Tue Apr 06 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.2-1mdv2010.1
+ Revision: 532061
- Update to 1.1.2, pygoocanvas still needs to be fixed

* Wed Mar 17 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.1-1mdv2010.1
+ Revision: 523549
- Update to 1.1.1

* Mon Mar 08 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.0-1mdv2010.1
+ Revision: 516023
- Update to 1.1.0 final

* Tue Feb 23 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.0-0.alpha2mdv2010.1
+ Revision: 510350
- Alpha2 release

* Tue Feb 16 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.1.0-0.alpha1mdv2010.1
+ Revision: 506692
- New upstream release
- Some cleanup needed in the spec file

  + Pascal Terjan <pterjan@mandriva.org>
    - test

* Wed Jan 13 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.0.0-2mdv2010.1
+ Revision: 490838
- Update Requires for the upcoming python-melt package

* Tue Jan 12 2010 Stéphane Téletchéa <steletch@mandriva.org> 1.0.0-1mdv2010.1
+ Revision: 490320
- Update lib dir for mime defintions
- Enumerate explicitly subdirs to the warning concerning the duplication of locale files
- Remove explicit python macro
- import openshot


* Tue Jan 12 2010 Stephane Teletchea <steletch@mandriva.org> 1.0.0-1mdv2010.1
- Initial Mandriva release, imported from the fedora rpm

* Tue Jan 12 2010 Zarko <zarko.pintar@gmail.com> - 1.0.0-1
- Release 1.0.0

* Thu Dec 04 2009 Zarko <zarko.pintar@gmail.com> - 0.9.54-1
- initial release
