Summary:	An FTP daemon provided by Washington University
Summary(es):	Deamon FTP de la Universidad de Washington
Summary(pl):	Serwer FTP stworzony przez Uniwersystet Waszyngtona
Summary(pt_BR):	Deamon FTP da Universidade de Washington
Summary(ru):	FTP-сервер разработанный в Washington University
Summary(uk):	FTP-сервер розроблений в Washington University
Name:		wu-ftpd
Version:	2.6.2
Release:	12
License:	BSD
Vendor:		WU-FTPD Development Group <wuftpd-members@wu-ftpd.org>
Group:		Daemons
Source0:	ftp://ftp.wu-ftpd.org/pub/wu-ftpd/%{name}-%{version}.tar.gz
# Source0-md5:	b3c271f02aadf663b8811d1bff9da3f6
Source1:	%{name}.inetd
Source2:	%{name}.logrotate
Source3:	ftp.pamd
Source4:	%{name}-passwd
Source5:	%{name}-group
Source6:	ftpusers.tar.bz2
# Source6-md5:	76c80b6ec9f4d079a1e27316edddbe16
Patch0:		%{name}-ipv6.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-conf.patch
Patch3:		%{name}-release.patch
Patch4:		%{name}-ls.patch
Patch5:		%{name}-2.6.2-realpatch.patch
Patch6:		%{name}-sec_debian.patch
URL:		http://www.wu-ftpd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	ncompress
BuildRequires:	pam-devel
PreReq:		rc-inetd
Requires(post):	awk
Requires(post):	fileutils
Provides:	ftpserver
Requires:	inetdaemon
Requires:	logrotate
Requires:	rc-inetd
Requires:	pam >= 0.77.3
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	ftpserver
Obsoletes:	glftpd
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
Obsoletes:	vsftpd
Conflicts:	man-pages < 1.51
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ftpd
%define		_localstatedir	/var/run
%define		_ftpdir		/home/services/ftp

%description
wu-ftpd is a replacement FTP server for Un*x systems. Besides
supporting the FTP protocol defined in RFC 959, it adds the following
features: logging of transfers, logging of commands, on the fly
compression and archiving, classification of users on type and
location, per class limits, per directory upload permissions,
restricted guest accounts, system wide and per directory messages,
directory alias, cdpath, filename filter, virtual host support.

%description -l es
wu-ftpd es el daemon que ccc archivos FTP para clientes FTP. Es Зtil
si deseas transferir programas entre ordenadores sin ejecutar un
sistema de archivos de red como NFS; o si deseas tener un sitio de FTP
anСnimo (en este caso, necesitas instalar el paquete anonftp).

%description -l pl
wu-ftpd jest bezpo╤rednim zamiennikiem serwera FTP dla systemСw Un*x.
Poza wsparciem dla protokoЁu FTP zdefiniowanego w RFC 959 wu-ftpd
zawiera kilka nowo╤ci takich jak: logowanie transferСw, logowanie
komend, kompresja i archiwizacja w locie, klasyfikacja u©ytkownikСw na
podstawie typu i lokalizacji, limity na podstawie klasy, uprawnienia
do uploadowania dla dowolnego katalogu, restrykcyjne konta dla go╤ci,
ogСlne komunikaty systemowe oraz komunikaty w zale©no╤ci od katalogu,
aliasy dla katalogСw, cdpath, filtr nazw plikСw, wsparcie dla serwerСw
wirtualnych.

%description -l pt_BR
wu-ftpd И o daemon que serve arquivos FTP para clientes FTP. Ele И
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
%patch5 -p1
%patch6 -p1

%build
sed -e 's/dnl.*//' <configure.in >configure.in.new
mv -f configure.in.new configure.in
%{__aclocal}
%{__autoconf}
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
	$RPM_BUILD_ROOT%{_ftpdir}/{etc/msgs,lib,bin,pub/Incoming} \
	$RPM_BUILD_ROOT%{_var}/log

install	/bin/{gzip,tar} $RPM_BUILD_ROOT%{_ftpdir}/bin
install	%{_bindir}/{compress,cksum,md5sum} $RPM_BUILD_ROOT%{_ftpdir}/bin
ln -sf gzip $RPM_BUILD_ROOT%{_ftpdir}/bin/zcat
install	/lib/{libc-*.so,ld-*.so} $RPM_BUILD_ROOT%{_ftpdir}/lib
install	/etc/ld.so.cache $RPM_BUILD_ROOT%{_ftpdir}/etc

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_USER=$(id -u) \
	INSTALL_GROUP=$(id -g)

install doc/examples/ftpaccess.heavy	$RPM_BUILD_ROOT%{_sysconfdir}/ftpaccess
install	doc/examples/ftpservers		$RPM_BUILD_ROOT%{_sysconfdir}/ftpservers
install doc/examples/ftpgroups		$RPM_BUILD_ROOT%{_sysconfdir}/ftpgroups
install doc/examples/ftphosts		$RPM_BUILD_ROOT%{_sysconfdir}/ftphosts
install	doc/examples/ftpconversions	$RPM_BUILD_ROOT%{_sysconfdir}/ftpconversions
install %{SOURCE1}			$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpd
install %{SOURCE2}			$RPM_BUILD_ROOT/etc/logrotate.d/ftpd
install %{SOURCE3}			$RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE4}			$RPM_BUILD_ROOT%{_ftpdir}/etc/passwd
install %{SOURCE5}			$RPM_BUILD_ROOT%{_ftpdir}/etc/group
install util/xferstats			$RPM_BUILD_ROOT%{_bindir}/xferstat

touch $RPM_BUILD_ROOT%{_sysconfdir}/ftpusers.default
touch $RPM_BUILD_ROOT%{_sysconfdir}/ftpusers
touch $RPM_BUILD_ROOT/var/log/xferlog
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

echo "Too many users. Try again later." > $RPM_BUILD_ROOT%{_ftpdir}/etc/msgs/toomany
echo "Server shutdown."			> $RPM_BUILD_ROOT%{_ftpdir}/etc/msgs/shutdown
echo "Wrong file path."			> $RPM_BUILD_ROOT%{_ftpdir}/etc/msgs/path

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.ftpd $RPM_BUILD_ROOT%{_sbindir}/wu-ftpd
ln -sf wu-ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd

bzip2 -dc %{SOURCE6} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 027
touch /var/log/xferlog
umask 022
awk 'BEGIN { FS = ":" }; { if (($3 < 500) && ($1 != "ftp")) print $1; }' < /etc/passwd >> %{_sysconfdir}/ftpusers.default
if [ ! -f %{_sysconfdir}/ftpusers ]; then
	cp -f %{_sysconfdir}/ftpusers.default %{_sysconfdir}/ftpusers
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
%doc CHANGES CONTRIBUTORS ERRATA LICENSE README doc/{HOWTO/*,misc/opie,TODO}
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/*
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
%lang(ja) %{_mandir}/ja/man5/ftpusers*
%lang(pl) %{_mandir}/pl/man5/ftpusers*
%lang(pt_BR) %{_mandir}/pt_BR/man5/ftpusers*
%lang(ru) %{_mandir}/ru/man5/ftpusers*
