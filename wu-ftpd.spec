Summary:	An FTP daemon provided by Washington University.
Name: 		wu-ftpd
Version:	2.4.2vr17
Release:	3
Copyright:	BSD
Group:		System Environment/Daemons
Source: 	ftp://ftp.vr.net/pub/wu-ftpd/wu-ftpd-2.4.2-vr17.tar.gz
Source1:	ftpd.logrotate
Source2:	ftp.pamd
Patch0:		wu-ftpd-2.4.2-vr17-redhat.patch
Patch1:		wu-ftpd-2.4.2-vr17-glob.patch
Patch2:		wu-ftpd-2.4.2-vr17-pathname.patch
Requires:	pam >= 0.59
Provides:	ftpserver
Prereq:		fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The wu-ftpd package contains the wu-ftpd FTP (File Transfer Protocol)
server daemon.  The FTP protocol is a method of transferring files
between machines on a network and/or over the Internet.  Wu-ftpd's
features include logging of transfers, logging of commands, on the fly
compression and archiving, classification of users' type and location,
per class limits, per directory upload permissions, restricted guest
accounts, system wide and per directory messages, directory alias,
cdpath, filename filter and virtual host support.

Install the wu-ftpd package if you need to provide FTP service to remote
users.

%prep
%setup -q -n wu-ftpd-2.4.2-vr17
mkdir rhsconfig
%patch0 -p1
%patch1 -p1 -b .glob
%patch2 -p1 -b .pathname

%build
RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ./build lnx USE_PAM=1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
%{__make} install DESTDIR=$RPM_BUILD_ROOT
install -m755 util/xferstats $RPM_BUILD_ROOT/usr/sbin
cd rhsconfig
install -m 600 ftpaccess ftpusers  ftphosts ftpgroups ftpconversions $RPM_BUILD_ROOT/etc
strip $RPM_BUILD_ROOT/usr/sbin/* || :
mkdir -p $RPM_BUILD_ROOT/etc/{pam,logrotate}.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/ftpd
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/ftp
ln -sf in.ftpd $RPM_BUILD_ROOT/usr/sbin/wu.ftpd
ln -sf in.ftpd $RPM_BUILD_ROOT/usr/sbin/in.wuftpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /var/log/xferlog ]; then
    touch /var/log/xferlog
    chmod 600 /var/log/xferlog
fi

%files
%defattr(-,root,root)
%doc README ANNOUNCE-RELEASE ERRATA VIRTUAL.FTP.SUPPORT
%doc doc/FIXES doc/examples
/usr/sbin/*
/usr/bin/*
/usr/man/*/*
%config /etc/ftp*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/ftp
%config /etc/logrotate.d/ftpd
