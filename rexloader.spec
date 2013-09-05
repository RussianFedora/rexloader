%global svn     334

Name:           rexloader
Version:        0.1.svn%{svn}
Release:        1%{?dist}
Summary:        A cross-platform download manager
Summary(ru):    Кросс-платформенный менеджер закачек

License:        GPLv3
Url:            http://code.google.com/p/rexloader/
Source0:        %{name}-%{version}.tar.xz

BuildRequires:  pkgconfig(QtWebKit)
BuildRequires:  qt-devel
BuildRequires:  desktop-file-utils

Requires:       %{name}-hashcalculator%{?_isa} = %{version}-%{release}
Requires:       %{name}-notifications%{?_isa} = %{version}-%{release}

%description
An advanced Qt/C++ download manager over http(s) with configurable
multithreaded downloading, proxy support, logging and hash calculating
(md5, sha1). We also plan to implement support for ftp and p2p (torrent,
dc++ etc).

%description -l ru
кросс-платформенный менеджер закачек, поддерживающий настраиваемую
многопоточную загрузку файлов по протоколу http(s), прокси, ведение журнала, и
расчёт контрольных сумм (md5, sha1).

%package hashcalculator
Summary:        Rexloader Hash Calculator
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description hashcalculator
This package provides a Hash Calculator plugin for Rexloader.
It allows to calculate downloaded files hash sums.

%package nixnotify
Summary:        Rexloader D-Bus Notifications
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-notifications%{?_isa} = %{version}-%{release}

%description nixnotify
This package provides a D-Bus implementation plugin for Rexloader.

It allows to show notifications via implementations supporting FreeDesktop's
notifications standard, like KDE 4.4 (or higher), Gnome, XFCE and others.

%package noticewindow
Summary:        Rexloader Qt Notifications
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-notifications%{?_isa} = %{version}-%{release}

%description noticewindow
This package provides a simple Qt Notifications plugin for Rexloader.

%prep
%setup -q
mkdir build
chmod -x plugins/HttpLoader/*.cpp
chmod -x plugins/HttpLoader/*.h


%build
pushd build
    %{qmake_qt4} ../REXLoader.pro
    make %{?_smp_mflags}

    pushd ../plugins/NoticeWindow
        %{qmake_qt4} NoticeWindow.pro
        make %{?_smp_mflags}
    popd
popd

%install
pushd build
    mkdir -p %{buildroot}%{_bindir}
    install ./usr/bin/%{name} %{buildroot}%{_bindir}
    cp -R ./usr/share %{buildroot}/usr

    mkdir -p %{buildroot}%{_libdir}
    cp -R ./usr/lib/%{name} %{buildroot}%{_libdir}

    install ../plugins/NoticeWindow/NoticeWindow %{buildroot}%{_libdir}/%{name}/plugins/libNoticeWindow.so

    mkdir -p %{buildroot}%{_datadir}/pixmaps
    install ../REXLoader/images/RExLoader_64x64.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

    mkdir -p %{buildroot}%{_datadir}/applications/
    desktop-file-install ../REXLoader/%{name}.desktop

    chmod 644 %{buildroot}%{_datadir}/applications/%{name}.desktop
    chmod 755 %{buildroot}%{_bindir}/%{name}
popd

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files
%doc COPYING
%{_bindir}/rexloader
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}
%{_libdir}/%{name}

%files hashcalculator
%{_libdir}/%{name}/plugins/libhashcalculator.so

%files nixnotify
%{_libdir}/%{name}/plugins/libNixNotifyPlugin.so

%files noticewindow
%{_libdir}/%{name}/plugins/libNoticeWindow.so

%changelog
* Thu Sep 05 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.1.svn334-1
- Update
- Correct spec

* Mon Jun 03 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.1a.svn.313-1
- Initial release
