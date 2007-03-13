Summary:	ODBC driver for SQLite
Summary(pl.UTF-8):	Sterownik ODBC dla SQLite
Name:		sqliteodbc
Version:	0.64
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://www.ch-werner.de/sqliteodbc/%{name}-%{version}.tar.gz
# Source0-md5:	f2ebdac541838e6db0e897fd98c5f34e
Patch0:		%{name}-misc.patch
URL:		http://www.ch-werner.de/sqliteodbc/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	sqlite-devel
BuildRequires:	sqlite3-devel
Requires(post):	mktemp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ODBC driver for SQLite interfacing SQLite 2.x and/or 3.x using
unixODBC or iODBC. See http://www.sqlite.org/ for a description of
SQLite, http://www.unixodbc.org/ for a description of unixODBC.

%description -l pl.UTF-8
Sterownik ODBC dla SQLite współpracujący z SQLite 2.x i/lub 3.x przy
użyciu unixODBC lub iODBC. Opis SQLite można znaleźć pod adresem
<http://www.sqlite.org/, a unixODBC pod http://www.unixodbc.org/>.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#rm -f $RPM_BUILD_ROOT%{_libdir}/libsqliteodbc*.{a,la}
#rm -f $RPM_BUILD_ROOT%{_libdir}/libsqlite3odbc*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /usr/bin/odbcinst ] ; then
	INST=`mktemp /tmp/sqliteinstXXXXXX`
	if [ -r %{_libdir}/libsqliteodbc.so ] ; then
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
		/usr/bin/odbcinst -q -s -n "SQLite Datasource" | \
			grep '^\[SQLite Datasource\]' >/dev/null || {
			/usr/bin/odbcinst -i -l -s -n "SQLite Datasource" -f $INST || true
		}
	fi
	if [ -r %{_libdir}/libsqlite3odbc.so ] ; then
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
		/usr/bin/odbcinst -q -s -n "SQLite3 Datasource" | \
			grep '^\[SQLite3 Datasource\]' >/dev/null || {
			/usr/bin/odbcinst -i -l -s -n "SQLite3 Datasource" -f $INST || true
		}
	fi
	rm -f $INST
fi

%preun
if [ "$1" = "0" ] ; then
	test -x /usr/bin/odbcinst && {
		/usr/bin/odbcinst -u -d -n SQLITE || true
		/usr/bin/odbcinst -u -l -s -n "SQLite Datasource" || true
		/usr/bin/odbcinst -u -d -n SQLITE3 || true
		/usr/bin/odbcinst -u -l -s -n "SQLite3 Datasource" || true
	}
fi

%files
%defattr(644,root,root,755)
%doc README license.terms ChangeLog
%attr(755,root,root) %{_libdir}/libsqlite*.so*
