%define tname QtSpell
%define oname %(echo %{tname} | tr [:upper:] [:lower:])

Summary:	A spell checking for Qt text widgets
Name:		%{oname}
Version:	0.8.1
Release:	0
License:	GPLv3+
Group:		Development/KDE and Qt
URL:		https://github.com/manisandro/%{name}
Source0:	https://github.com/manisandro/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	qt5-linguist-tools
BuildRequires:	pkgconfig(enchant)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(Qt5Core)

Requires:	iso-codes

%description
QtSpell adds spell-checking functionality to Qt's text widgets, using the
enchant spell-checking library.

#----------------------------------------------------------------------------

%package	qt4
Summary:	Spell checking for Qt4 text widgets
Group:		System/Libraries

%description qt4
QtSpell adds spell-checking functionality to Qt4's text widgets, using the
enchant spell-checking library.

%files qt4
%{_libdir}/libqtspell-qt4.so.*
%{_qt_translationdir}/QtSpell_*.qm
%doc build-qt4/COPYING

#----------------------------------------------------------------------------

%package qt4-devel
Summary:	Development files for %{name}-qt4
Group:		Development/KDE and Qt

Requires:	%{name}-qt4 = %{version}-%{release}

%description qt4-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files qt4-devel
%{_includedir}/QtSpell-qt4/
%{_libdir}/libqtspell-qt4.so
%{_libdir}/pkgconfig/QtSpell-qt4.pc
%doc build-qt4/README.md
%doc build-qt4/NEWS
%doc build-qt4/AUTHORS
%doc build-qt4/ChangeLog
%doc build-qt4/COPYING

#----------------------------------------------------------------------------

%package qt5
Summary:	Spell checking for Qt5 text widgets
Group:		System/Libraries

%description qt5
QtSpell adds spell-checking functionality to Qt5's text widgets, using the
enchant spell-checking library.

%files qt5
%{_libdir}/libqtspell-qt5.so.*
%doc build-qt5/COPYING

#----------------------------------------------------------------------------

%package qt5-devel
Summary:	Development files for %{name}-qt5
Group:		Development/KDE and Qt

Requires:	%{name}-qt5 = %{version}-%{release}

%description qt5-devel
The %{name}-qt5-devel package contains libraries and header files for
developing applications that use %{name}-qt5.

%files qt5-devel
%{_includedir}/QtSpell-qt5/
%{_libdir}/libqtspell-qt5.so
%{_libdir}/pkgconfig/QtSpell-qt5.pc
%doc build-qt5/README.md
%doc build-qt5/NEWS
%doc build-qt5/AUTHORS
%doc build-qt5/ChangeLog
%doc build-qt5/COPYING

#----------------------------------------------------------------------------

%package qt5-translations
Summary:	Translations for %{name}-qt5
BuildArch:	noarch

Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	qt5-qttranslations

%description qt5-translations
The %{name}-qt5-translations contains translations for %{name}-qt5.

%files qt5-translations
%{_qt5_translationsdir}/QtSpell_*.qm

#----------------------------------------------------------------------------

%package doc
Summary:	Developer documentation for %{name}
BuildArch:	noarch

%description doc
The %{name}-doc package contains the documentation for developing applications
that use %{name}.

%files doc
%doc build-qt5/build/doc/html
%doc build-qt5/COPYING

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}

# set qt4 and qt5 branch
mkdir build-qt4
find .	-maxdepth 1 -mindepth 1 -not -name ./build-qt4 -exec mv -t ./build-qt4 '{}' \;
cp -a build-qt4 build-qt5

# fix qt4 translations path
sed -i -e 's|DESTINATION share/${QT_VER}/translations|DESTINATION lib/${QT_VER}/translations|' build-qt4/CMakeLists.txt

%build

# build qt4
pushd build-qt4
%cmake -DUSE_QT5:BOOL=OFF
%make
popd

# build qt5 and docs
pushd build-qt5
%cmake -DUSE_QT5:BOOL=ON
%make
%make doc
popd


%install
# install qt4
%make_install -C build-qt4/build

# install qt5 and docs
%make_install -C build-qt5/build

