# TODO: sqlite4 (when released/available in PLD)
# NOTE: it looks for libsqlite.la, libsqlite3.la, libodbcinst.la/libiodbcinst.la in %{_libdir},
#	so these libtool files must be present to build this package without patching
#
# Conditional build:
%bcond_with	iodbc		# use iODBC instead of unixODBC
%bcond_without	sqlite2		# SQLite 2.x driver
%bcond_without	sqlite3		# SQLite 3.x driver
%bcond_with	sqlite4		# SQLite 4.x driver
#
Summary:	ODBC driver for SQLite 2.x
Summary(pl.UTF-8):	Sterownik ODBC dla SQLite 2.x
Name:		sqliteodbc
Version:	0.9993
Release:	2
License:	BSD
Group:		Libraries
Source0:	http://www.ch-werner.de/sqliteodbc/%{name}-%{version}.tar.gz
# Source0-md5:	2a418fa3465d285f75218b619345cd53
Patch0:		%{name}-misc.patch
URL:		http://www.ch-werner.de/sqliteodbc/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_iodbc:BuildRequires:	libiodbc-devel}
%{?with_sqlite3:BuildRequires:	libxml2-devel >= 2}
%{?with_sqlite2:BuildRequires:	sqlite-devel >= 2.8.0}
%{?with_sqlite3:BuildRequires:	sqlite3-devel >= 3}
%{?with_sqlite4:BuildRequires:	sqlite4-devel >= 4}
%{!?with_iodbc:BuildRequires:	unixODBC-devel}
%{?with_sqlite3:BuildRequires:	zlib-devel}
Requires(post):	mktemp
Requires(post):	/usr/bin/odbcinst
Requires:	sqlite >= 2.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# human-readable ODBC variant name
%define ODBCvar	%{?with_iodbc:iODBC}%{!?with_iodbc:unixODBC}

%description
SQLiteODBC is an ODBC driver for SQLite interfacing SQLite 2.x and/or
3.x using unixODBC or iODBC. See <http://www.sqlite.org/> for a
description of SQLite, <http://www.unixodbc.org/> for a description of
unixODBC.

This package contains SQLite 2.x driver for %{ODBCvar}.

%description -l pl.UTF-8
SQLiteODBC to sterownik ODBC dla SQLite współpracujący z SQLite 2.x
i/lub 3.x wykorzystujący unixODBC lub iODBC. Opis SQLite można znaleźć
pod adresem <http://www.sqlite.org/>, a unixODBC pod
<http://www.unixodbc.org/>.

Ten pakiet zawiera sterownik SQLite 2.x dla %{ODBCvar}.

%package -n sqlite3odbc
Summary:	ODBC driver for SQLite 3.x
Summary(pl.UTF-8):	Sterownik ODBC dla SQLite 3.x
Group:		Libraries
Requires(post):	mktemp
Requires(post):	/usr/bin/odbcinst

%description -n sqlite3odbc
SQLiteODBC is an ODBC driver for SQLite interfacing SQLite 2.x and/or
3.x using unixODBC or iODBC. See <http://www.sqlite.org/> for a
description of SQLite, <http://www.unixodbc.org/> for a description of
unixODBC.

This package contains SQLite 3.x driver for %{ODBCvar}.

%description -n sqlite3odbc -l pl.UTF-8
SQLiteODBC to sterownik ODBC dla SQLite współpracujący z SQLite 2.x
i/lub 3.x wykorzystujący unixODBC lub iODBC. Opis SQLite można znaleźć
pod adresem <http://www.sqlite.org/>, a unixODBC pod
<http://www.unixodbc.org/>.

Ten pakiet zawiera sterownik SQLite 3.x dla %{ODBCvar}.

%package -n sqlite4odbc
Summary:	ODBC driver for SQLite 4.x
Summary(pl.UTF-8):	Sterownik ODBC dla SQLite 4.x
Group:		Libraries
Requires(post):	mktemp
Requires(post):	/usr/bin/odbcinst

%description -n sqlite4odbc
SQLiteODBC is an ODBC driver for SQLite interfacing SQLite 2.x, 3.x
and/or 4.x using unixODBC or iODBC. See <http://www.sqlite.org/> for a
description of SQLite, <http://www.unixodbc.org/> for a description of
unixODBC.

This package contains SQLite 4.x driver for %{ODBCvar}.

%description -n sqlite4odbc -l pl.UTF-8
SQLiteODBC to sterownik ODBC dla SQLite współpracujący z SQLite 2.x,
3.x i/lub 4.x wykorzystujący unixODBC lub iODBC. Opis SQLite można
znaleźć pod adresem <http://www.sqlite.org/>, a unixODBC pod
<http://www.unixodbc.org/>.

Ten pakiet zawiera sterownik SQLite 4.x dla %{ODBCvar}.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
INST=`mktemp /tmp/sqliteinstXXXXXX`
cat > $INST << 'EOD'
[SQLITE]
Description=SQLite ODBC 2.X
Driver=%{_libdir}/libsqliteodbc.so
Setup=%{_libdir}/libsqliteodbc.so
FileUsage=1
EOD
/usr/bin/odbcinst -q -d -n SQLITE | grep '^\[SQLITE\]' >/dev/null || {
	/usr/bin/odbcinst -i -d -n SQLITE -f $INST || true
}
cat > $INST << 'EOD'
[SQLite Datasource]
Driver=SQLITE
EOD
/usr/bin/odbcinst -q -s -n "SQLite Datasource" | grep '^\[SQLite Datasource\]' >/dev/null || {
	/usr/bin/odbcinst -i -l -s -n "SQLite Datasource" -f $INST || true
}
rm -f $INST

%preun
if [ "$1" = "0" ] ; then
	test -x /usr/bin/odbcinst && {
		/usr/bin/odbcinst -u -d -n SQLITE || true
		/usr/bin/odbcinst -u -l -s -n "SQLite Datasource" || true
	}
fi

%post	-n sqlite3odbc
cat > $INST << 'EOD'
[SQLITE3]
Description=SQLite ODBC 3.X
Driver=%{_libdir}/libsqlite3odbc.so
Setup=%{_libdir}/libsqlite3odbc.so
FileUsage=1
EOD
/usr/bin/odbcinst -q -d -n SQLITE3 | grep '^\[SQLITE3\]' >/dev/null || {
	/usr/bin/odbcinst -i -d -n SQLITE3 -f $INST || true
}
cat > $INST << 'EOD'
[SQLite3 Datasource]
Driver=SQLITE3
EOD
/usr/bin/odbcinst -q -s -n "SQLite3 Datasource" | grep '^\[SQLite3 Datasource\]' >/dev/null || {
	/usr/bin/odbcinst -i -l -s -n "SQLite3 Datasource" -f $INST || true
}
rm -f $INST

%preun	-n sqlite3odbc
if [ "$1" = "0" ] ; then
	test -x /usr/bin/odbcinst && {
		/usr/bin/odbcinst -u -d -n SQLITE3 || true
		/usr/bin/odbcinst -u -l -s -n "SQLite3 Datasource" || true
	}
fi

%post	-n sqlite4odbc
cat > $INST << 'EOD'
[SQLITE4]
Description=SQLite ODBC 4.X
Driver=%{_libdir}/libsqlite4odbc.so
Setup=%{_libdir}/libsqlite4odbc.so
FileUsage=1
EOD
/usr/bin/odbcinst -q -d -n SQLITE4 | grep '^\[SQLITE4\]' >/dev/null || {
	/usr/bin/odbcinst -i -d -n SQLITE4 -f $INST || true
}
cat > $INST << 'EOD'
[SQLite4 Datasource]
Driver=SQLITE4
EOD
/usr/bin/odbcinst -q -s -n "SQLite4 Datasource" | grep '^\[SQLite4 Datasource\]' >/dev/null || {
	/usr/bin/odbcinst -i -l -s -n "SQLite4 Datasource" -f $INST || true
}
rm -f $INST

%preun	-n sqlite4odbc
if [ "$1" = "0" ] ; then
	test -x /usr/bin/odbcinst && {
		/usr/bin/odbcinst -u -d -n SQLITE4 || true
		/usr/bin/odbcinst -u -l -s -n "SQLite4 Datasource" || true
	}
fi

%if %{with sqlite2}
%files
%defattr(644,root,root,755)
%doc ChangeLog README license.terms
%attr(755,root,root) %{_libdir}/libsqliteodbc-%{version}.so
%attr(755,root,root) %{_libdir}/libsqliteodbc.so
%endif

%if %{with sqlite3}
%files -n sqlite3odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsqlite3odbc-%{version}.so
%attr(755,root,root) %{_libdir}/libsqlite3odbc.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_blobtoxy-%{version}.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_blobtoxy.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_csvtable-%{version}.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_csvtable.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_impexp-%{version}.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_impexp.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_xpath-%{version}.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_xpath.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_zipfile-%{version}.so
%attr(755,root,root) %{_libdir}/libsqlite3_mod_zipfile.so
%endif

%if %{with sqlite4}
%files -n sqlite4odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsqlite4odbc-%{version}.so
%attr(755,root,root) %{_libdir}/libsqlite4odbc.so
%endif
