Summary:	An FTP daemon provided by Washington University
Summary(es):	Deamon FTP de la Universidad de Washington
Summary(pl):	Serwer FTP stworzony przez Uniwersystet Waszyngtona
Summary(pt_BR):	Deamon FTP da Universidade de Washington
Summary(ru):	FTP-сервер разработанный в Washington University
Summary(uk):	FTP-сервер розроблений в Washington University
Name:		wu-ftpd
Version:	2.6.2
Release:	6
License:	BSD
Group:		Daemons
Source0:	ftp://ftp.wu-ftpd.org/pub/wu-ftpd/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.logrotate
Source3:	ftp.pamd
Source4:	%{name}-passwd
Source5:	%{name}-group
Patch0:		%{name}-ipv6.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-conf.patch
Patch3:		%{name}-release.patch
Patch4:		%{name}-ls.patch
URL:		http://www.wu-ftpd.org/
Vendor:		WU-FTPD Development Group <wuftpd-members@wu-ftpd.org>
BuildRequires:	autoconf
BuildRequires:	automake
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
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
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

%description -l es
wu-ftpd es el daemon que ccc archivos FTP para clientes ftp. Es Зtil
si deseas transferir programas entre ordenadores sin ejecutar un
sistema de archivos de red como NFS; o si deseas tener un sitio de FTP
anСnimo (en este caso, necesitas instalar el paquete anonftp).

%description -l pl
wu-ftpd jest bezpo╤rednim zamiennikiem serwera ftp dla systemСw Un*x.
Poza wsparciem dla protokoЁu ftp zdefiniowanego w RFC 959 wu-ftpd
zawiera kilka nowo╤ci takich jak: logowanie transferСw, logowanie
komend, kompresja i archiwizacja w locie, klasyfikacja u©ytkownikСw na
podstawie typu i lokalizacji, limity na podstawie klasy, uprawnienia
do uploadowania dla dowolnego katalogu, restrykcyjne konta dla go╤ci,
ogСlne komunikaty systemowe oraz komunikaty w zale©no╤ci od katalogu,
aliasy dla katalogСw, cdpath, filtr nazw plikСw, wsparcie dla serwerСw
wirtualnych.

%description -l pt_BR
wu-ftpd И o daemon que serve arquivos FTP para clientes ftp. Ele И
Зtil se vocЙ deseja transferir programas entre computadores sem rodar
um sistema de arquivos de rede como NFS; ou se vocЙ deseja ter um site
de FTP anТnimo (neste caso, vocЙ necessita instalar o pacote anonftp).

%description -l ru
Этот пакет содержит сервер wu-ftpd протокола FTP (File Transfer
Protocol). Возможности wu-ftpd включают протоколирование пересылок
файлов, протоколирование команд, компрессию и архивирование "на лету",
классификация пользователей по типам и "локальности", разные лимиты
для разных классов, разрешения на загрузку файлов по каждому каталогу
отдельно, ограниченные гостевые входы, общесистемные и индивидуальные
для каталогов сообщения, синонимы каталогов, cdpath, фильтр имен
файлов и поддержка виртуальных серверов.

%description -l uk
Цей пакет м╕стить сервер wu-ftpd протоколу FTP (File Transfer
Protocol). Можливост╕ wu-ftpd включають протоколювання пересилок
файл╕в, протоколювання команд, компрес╕я та арх╕вац╕я "на льоту",
класиф╕кац╕я користувач╕в по типу та та "локальност╕", р╕зн╕ обмеження
для р╕зних клас╕в, покаталоговий дозв╕л на завантаження файл╕в,
обмежен╕ гостьов╕ входи, загальн╕ та окрем╕ для каталог╕в
пов╕домлення, синон╕ми каталог╕в, cdpath, ф╕льтр ╕мен файл╕в та
п╕дтримка в╕ртуальних сервер╕в.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
sed -e 's/dnl.*//' <configure.in >configure.in.new
mv -f configure.in.new configure.in
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
ln -sf wu-ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd

gzip -9nf CHANGES CONTRIBUTORS ERRATA LICENSE README doc/{HOWTO/*,misc/opie,TODO}

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/log/xferlog
awk 'BEGIN { FS = ":" }; { if (($3 < 1000) && ($1 != "ftp")) print $1; }' < /etc/passwd >> %{_sysconfdir}/ftpusers.default
if [ ! -f %{_sysconfdir}/ftpusers ]; then
	( cd %{_sysconfdir}; cp -f ftpusers.default ftpusers )
fi

if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.gz doc/{HOWTO,misc}/*.gz

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
