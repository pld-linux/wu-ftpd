Summary:	An FTP daemon provided by Washington University
Summary(pl):	Serwer FTP stworzony przez Uniwersystet Waszyngtona
Name:		wu-ftpd
Version:	2.6.1
Release:	10
License:	BSD
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	ftp://ftp.wu-ftpd.org/pub/wu-ftpd/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.logrotate
Source3:	ftp.pamd
Source4:	%{name}-passwd
Source5:	%{name}-group
Patch0:		ftp://ftp.wu-ftpd.org/pub/dist/patches/apply_to_2.6.1/missing_format_strings.patch
Patch1:		ftp://ftp.wu-ftpd.org/pub/dist/patches/apply_to_2.6.1/nlst-shows-dirs.patch
Patch2:		ftp://ftp.wu-ftpd.org/pub/dist/patches/apply_to_2.6.1/pasv-port-allow-correction.patch
Patch3:		%{name}-install.patch
Patch4:		%{name}-conf.patch
Patch5:		%{name}-release.patch
Patch6:		http://www.t17.ds.pwr.wroc.pl/~misiek/ipv6/%{name}-%{version}-ipv6-20000914.patch.gz
URL:		http://www.wu-ftpd.org/
Vendor:		WU-FTPD Development Group <wuftpd-members@wu-ftpd.org>
BuildRequires:	pam-devel
BuildRequires:	bison
BuildRequires:	ncompress
BuildRequires:	pam-devel
Prereq:		rc-inetd
Prereq:		awk
Requires:	rc-inetd
Requires:	logrotate
Requires:	inetdaemon
Provides:	ftpserver
Obsoletes:	ftpserver
Obsoletes:	wu-ftpd
Obsoletes:	ftpd-BSD
Obsoletes:	linux-ftpd
Obsoletes:	anonftp
Obsoletes:	bftpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ftpd
%define		_localstatedir	/var/run

%description
wu-ftpd is a replacement ftp server for Un*x systems. Besides
supporting the ftp protocol defined in RFC 959, it adds the following
features: logging of transfers, logging of commands, on the fly
compression and archiving, classification of users on type and
location, per class limits, per directory upload permissions,
restricted guest accounts, system wide and per directory messages,
directory alias, cdpath, filename filter, virtual host support.

%description -l pl
wu-ftpd jest bezpo¶rednim zamiennikiem serwera ftp dla systemów Un*x.
Poza wsparciem dla protoko³u ftp zdefiniowanego w RFC 959 wu-ftpd
zawiera kilka nowo¶ci takich jak: logowanie transferów, logowanie
koment, kompresja i archiwizacja w locie, klasyfikacja u¿ytkowników na
podstawie typu i lokalizacji, limity na podstawie klasy, uprawnienia
do uploadowania dla dowolnego katalogu, restrykcyjne konta dla go¶ci,
ogólne komunikaty systemowe oraz komunikaty w zale¿no¶ci od katalogu,
aliasy dla katalogów, cdpath, filtr nazw plików, wsparcie dla serwerów
wirtualnych.

%prep
%setup -q 
%patch6 -p1
#%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
sed -e 's/dnl.*//' <configure.in >configure.in.new
mv configure.in.new configure.in
aclocal
autoconf
%configure \
	--with-etc-dir=%{_sysconfdir} \
	--with-pid-dir=%{_localstatedir} \
	--with-log-dir=%{_var}/log \
	--enable-pam \
	--enable-quota \
	--enable-ratios \
	--enable-passwd \
	--enable-ls \
	--disable-numericuid \
	--enable-rfc931 \
	--enable-ipv6
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,pam.d,sysconfig/rc-inetd,security} \
	$RPM_BUILD_ROOT/home/ftp/{etc/msgs,lib,bin,pub/Incoming} \
	$RPM_BUILD_ROOT%{_var}/log

install	/bin/{gzip,tar} $RPM_BUILD_ROOT/home/ftp/bin
install	%{_bindir}/{compress,cksum,md5sum} $RPM_BUILD_ROOT/home/ftp/bin
ln -sf gzip $RPM_BUILD_ROOT/home/ftp/bin/zcat
install	/lib/{libc-*.so,ld-*.so} $RPM_BUILD_ROOT/home/ftp/lib
install	/etc/ld.so.cache $RPM_BUILD_ROOT/home/ftp/etc

%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL_USER=$(id -u) INSTALL_GROUP=$(id -g)

install doc/examples/ftpaccess.heavy	$RPM_BUILD_ROOT%{_sysconfdir}/ftpaccess
install	doc/examples/ftpservers		$RPM_BUILD_ROOT%{_sysconfdir}/ftpservers
install doc/examples/ftpgroups		$RPM_BUILD_ROOT%{_sysconfdir}/ftpgroups
install doc/examples/ftphosts		$RPM_BUILD_ROOT%{_sysconfdir}/ftphosts
install	doc/examples/ftpconversions	$RPM_BUILD_ROOT%{_sysconfdir}/ftpconversions
install %{SOURCE1}			$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpd
install %{SOURCE2}			$RPM_BUILD_ROOT/etc/logrotate.d/ftpd
install %{SOURCE3}			$RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE4}			$RPM_BUILD_ROOT/home/ftp/etc/passwd
install %{SOURCE5}			$RPM_BUILD_ROOT/home/ftp/etc/group
install util/xferstats			$RPM_BUILD_ROOT%{_bindir}/xferstat

touch $RPM_BUILD_ROOT%{_sysconfdir}/ftpusers.default
touch $RPM_BUILD_ROOT%{_sysconfdir}/ftpusers
touch $RPM_BUILD_ROOT/var/log/xferlog
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

echo "Too many users. Try again later." > $RPM_BUILD_ROOT/home/ftp/etc/msgs/toomany
echo "Server shutdown."			> $RPM_BUILD_ROOT/home/ftp/etc/msgs/shutdown
echo "Wrong file path."			> $RPM_BUILD_ROOT/home/ftp/etc/msgs/path

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.ftpd $RPM_BUILD_ROOT%{_sbindir}/wu-ftpd
ln -s wu-ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd

gzip -9nf CHANGES CONTRIBUTORS README doc/{HOWTO/*,misc/opie,TODO}

%post 
touch /var/log/xferlog
awk 'BEGIN { FS = ":" }; { if (($3 < 1000) && ($1 != "ftp")) print $1; }' < /etc/passwd >> %{_sysconfdir}/ftpusers.default
if [ ! -f %{_sysconfdir}/ftpusers ]; then
	( cd %{_sysconfdir}; cp ftpusers.default ftpusers )
fi

if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.gz CONTRIBUTORS.gz README.gz doc/{HOWTO/*,misc/opie,TODO}.gz

%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) /etc/logrotate.d/*
%attr(640,root,root) %ghost /var/log/*
%attr(640,root,root) /etc/sysconfig/rc-inetd/ftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/security/blacklist.ftp

%attr(640,root,root) %{_sysconfdir}/ftpusers.default
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpaccess
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpconversions
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpgroups
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftphosts
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpservers
%attr(640,root,root) %ghost %{_sysconfdir}/ftpusers

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man[158]/*
