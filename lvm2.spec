%global device_mapper_version 1.02.175

%global enable_cache 1
%global enable_cluster 1
%global enable_cmirror 1
%global enable_lvmdbusd 1
%global enable_lvmlockd 1
%global enable_lvmpolld 1
%global enable_thin 1
%global enable_dmfilemapd 1
%global enable_testsuite 1
%global enable_vdo 1
%global enable_writecache 1
%global enable_integrity 1

%global system_release_version 23
%global systemd_version 189-3
%global dracut_version 002-18
%global util_linux_version 2.24
%global bash_version 4.0
%global corosync_version 1.99.9-1
%global resource_agents_version 3.9.5-12
%global dlm_version 4.0.6-1
%global libselinux_version 1.30.19-4
%global persistent_data_version 0.7.0-0.1.rc6
%global sanlock_version 3.3.0-2

%global enable_lockd_sanlock %{enable_lvmlockd}
%global enable_lockd_dlm %{enable_lvmlockd}

%if 0%{?rhel} && 0%{?rhel} <= 8
  %ifnarch i686 x86_64 ppc64le s390x
    %global enable_cluster 0
    %global enable_cmirror 0
    %global enable_lockd_dlm 0
  %endif

  %ifnarch x86_64 ppc64 aarch64
    %global enable_lockd_sanlock 0
  %endif
%endif

# Do not reset Release to 1 unless both lvm2 and device-mapper
# versions are increased together.

Summary: Userland logical volume management tools
Name: lvm2
%if 0%{?rhel}
Epoch: %{rhel}
%endif
Version: 2.03.11
Release: 9%{?dist}
License: GPLv2
URL: https://sourceware.org/lvm2/
Source0: https://sourceware.org/pub/lvm2/releases/LVM2.%{version}.tgz
Patch0: lvm2-set-default-preferred_names.patch
Patch3: lvm2-2_03_12-lvmlockd-sscanf-buffer-size-warnings.patch
# BZ 1915497:
Patch4: lvm2-2_03_12-alloc-enhance-estimation-of-sufficient_pes_free.patch
Patch5: lvm2-2_03_12-tests-check-thin-pool-corner-case-allocs.patch
Patch6: lvm2-2_03_12-tests-check-full-zeroing-of-thin-pool-metadata.patch
# BZ 1915580:
Patch7: lvm2-2_03_12-integrity-fix-segfault-on-error-path-when-replacing-.patch
# BZ 1872695:
Patch8: lvm2-2_03_12-devs-remove-invalid-path-name-aliases.patch
Patch9: lvm2-2_03_12-make-generate.patch
Patch10: lvm2-2_03_12-label_scan-fix-missing-free-of-filtered_devs.patch
# BZ 1917920:
Patch11: lvm2-2_03_12-pvck-fix-warning-and-exit-code-for-non-4k-mda1-offse.patch
Patch12: lvm2-2_03_12-WHATS_NEW-update.patch
# BZ 1921214:
Patch13: lvm2-2_03_12-writecache-use-cleaner-message-instead-of-table-relo.patch
# BZ 1909699:
Patch14: lvm2-2_03_12-man-update-lvmthin.patch
Patch15: lvm2-2_03_12-thin-improve-16g-support-for-thin-pool-metadata.patch
Patch16: lvm2-2_03_12-pool-limit-pmspare-to-16GiB.patch
Patch17: lvm2-2_03_12-cache-reuse-code-for-metadata-min_max.patch
Patch18: lvm2-2_03_12-tests-check-16G-thin-pool-metadata-size.patch
Patch19: lvm2-2_03_12-tests-update-thin-and-cache-checked-messages.patch
# BZ 1914389:
Patch20: lvm2-2_03_12-lvcreate-use-lv_passes_readonly_filter.patch
Patch21: lvm2-2_03_12-test-check-read_only_volume_list-tagging-works.patch
# BZ 1859659:
Patch22: lvm2-2_03_12-filter-mpath-work-with-nvme-devices.patch
# BZ 1925871:
Patch23: lvm2-2_03_12-dev_get_primary_dev-fix-invalid-path-check.patch
# Fix editline compilation:
Patch24: lvm2-2_03_12-lvm-Fix-editline-compilation.patch

BuildRequires: make
BuildRequires: gcc
%if %{enable_testsuite}
BuildRequires: gcc-c++
%endif
BuildRequires: libselinux-devel >= %{libselinux_version}, libsepol-devel
BuildRequires: libblkid-devel >= %{util_linux_version}
BuildRequires: ncurses-devel
BuildRequires: libedit-devel
BuildRequires: libaio-devel
%if %{enable_cluster}
BuildRequires: corosynclib-devel >= %{corosync_version}
%endif
%if %{enable_cluster} || %{enable_lockd_dlm}
BuildRequires: dlm-devel >= %{dlm_version}
%endif
BuildRequires: module-init-tools
BuildRequires: pkgconfig
BuildRequires: systemd-devel
BuildRequires: systemd-units
%if %{enable_lvmdbusd}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-dbus
BuildRequires: python3-pyudev
%endif
%if %{enable_thin} || %{enable_cache}
BuildRequires: device-mapper-persistent-data >= %{persistent_data_version}
%endif
%if %{enable_lockd_sanlock}
BuildRequires: sanlock-devel >= %{sanlock_version}
%endif
Requires: %{name}-libs = %{?epoch}:%{version}-%{release}
%if 0%{?fedora}
Requires(post): (system-release >= %{system_release_version} if system-release)
%endif
Requires: bash >= %{bash_version}
Requires(post): systemd-units >= %{systemd_version}, systemd-sysv
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}
Requires: module-init-tools
%if %{enable_thin} || %{enable_cache}
Requires: device-mapper-persistent-data >= %{persistent_data_version}
%endif

%description
LVM2 includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadm(8) or even loop devices, see
losetup(8)), creating volume groups (kind of virtual disks) from one
or more physical volumes and creating one or more logical volumes
(kind of logical partitions) in volume groups.

%prep
%setup -q -n LVM2.%{version}
%patch0 -p1 -b .backup0
%patch3 -p1 -b .backup3
%patch4 -p1 -b .backup4
%patch5 -p1 -b .backup5
%patch6 -p1 -b .backup6
%patch7 -p1 -b .backup7
%patch8 -p1 -b .backup8
%patch9 -p1 -b .backup9
%patch10 -p1 -b .backup10
%patch11 -p1 -b .backup11
%patch12 -p1 -b .backup12
%patch13 -p1 -b .backup13
%patch14 -p1 -b .backup14
%patch15 -p1 -b .backup15
%patch16 -p1 -b .backup16
%patch17 -p1 -b .backup17
%patch18 -p1 -b .backup18
%patch19 -p1 -b .backup19
%patch20 -p1 -b .backup20
%patch21 -p1 -b .backup21
%patch22 -p1 -b .backup22
%patch23 -p1 -b .backup23
%patch24 -p1 -b .backup24

%build
%global _default_pid_dir /run
%global _default_dm_run_dir /run
%global _default_run_dir /run/lvm
%global _default_locking_dir /run/lock/lvm

%global _udevdir %{_prefix}/lib/udev/rules.d

%configure \
  --with-default-dm-run-dir=%{_default_dm_run_dir} \
  --with-default-run-dir=%{_default_run_dir} \
  --with-default-pid-dir=%{_default_pid_dir} \
  --with-default-locking-dir=%{_default_locking_dir} \
  --with-usrlibdir=%{_libdir} \
  --enable-fsadm \
  --enable-write_install \
  --with-user= \
  --with-group= \
  --with-device-uid=0 \
  --with-device-gid=6 \
  --with-device-mode=0660 \
  --enable-pkgconfig \
  --enable-cmdlib \
  --enable-dmeventd \
  --enable-blkid_wiping \
  --disable-readline \
  --enable-editline \
%if %{enable_cluster}
  --with-cluster=internal \
  %if %{enable_cmirror}
  --enable-cmirrord \
  %endif
%else
  --with-cluster=internal \
%endif
  --with-udevdir=%{_udevdir} --enable-udev_sync \
%if %{enable_thin}
  --with-thin=internal \
%endif
%if %{enable_cache}
  --with-cache=internal \
%endif
%if %{enable_lvmpolld}
  --enable-lvmpolld \
%endif
%if %{enable_lockd_dlm}
  --enable-lvmlockd-dlm --enable-lvmlockd-dlmcontrol \
%endif
%if %{enable_lockd_sanlock}
  --enable-lvmlockd-sanlock \
%endif
%if %{enable_lvmdbusd}
  --enable-dbus-service --enable-notify-dbus \
%endif
%if %{enable_dmfilemapd}
  --enable-dmfilemapd \
%endif
%if %{enable_writecache}
  --with-writecache=internal \
%endif
%if %{enable_vdo}
  --with-vdo=internal --with-vdo-format=%{_bindir}/vdoformat \
%endif
%if %{enable_integrity}
  --with-integrity=internal \
%endif
  --disable-silent-rules

%make_build

%install
%make_install
make install_system_dirs DESTDIR=$RPM_BUILD_ROOT
make install_systemd_units DESTDIR=$RPM_BUILD_ROOT
make install_systemd_generators DESTDIR=$RPM_BUILD_ROOT
make install_tmpfiles_configuration DESTDIR=$RPM_BUILD_ROOT
%if %{enable_testsuite}
%make_install -C test
%endif

%post
%systemd_post blk-availability.service lvm2-monitor.service
if [ "$1" = "1" ] ; then
	# FIXME: what to do with this? We do not want to start it in a container/chroot
	# enable and start lvm2-monitor.service on completely new installation only, not on upgrades
	systemctl enable lvm2-monitor.service
	systemctl start lvm2-monitor.service >/dev/null 2>&1 || :
fi

%if %{enable_lvmpolld}
%systemd_post lvm2-lvmpolld.socket
# lvm2-lvmpolld socket is always enabled and started and ready to serve if lvmpolld is used
# replace direct systemctl calls with systemd rpm macro once this is provided in the macro:
# http://cgit.freedesktop.org/systemd/systemd/commit/?id=57ab2eabb8f92fad5239c7d4492e9c6e23ee0678
systemctl enable lvm2-lvmpolld.socket
systemctl start lvm2-lvmpolld.socket >/dev/null 2>&1 || :
%endif

%preun
%systemd_preun blk-availability.service lvm2-monitor.service

%if %{enable_lvmpolld}
%systemd_preun lvm2-lvmpolld.service lvm2-lvmpolld.socket
%endif

%postun
%systemd_postun lvm2-monitor.service

%if %{enable_lvmpolld}
%systemd_postun_with_restart lvm2-lvmpolld.service
%endif

%triggerun -- %{name} < 2.02.86-2
%{_bindir}/systemd-sysv-convert --save lvm2-monitor >/dev/null 2>&1 || :
/bin/systemctl --no-reload enable lvm2-monitor.service > /dev/null 2>&1 || :
/sbin/chkconfig --del lvm2-monitor > /dev/null 2>&1 || :
/bin/systemctl try-restart lvm2-monitor.service > /dev/null 2>&1 || :

%files
%license COPYING COPYING.LIB
%doc README VERSION WHATS_NEW
%doc doc/lvm_fault_handling.txt

# Main binaries
%{_sbindir}/fsadm
%{_sbindir}/lvm
%{_sbindir}/lvmconfig
%{_sbindir}/lvmdump
%if %{enable_lvmpolld}
%{_sbindir}/lvmpolld
%endif

# Other files
%{_sbindir}/lvchange
%{_sbindir}/lvconvert
%{_sbindir}/lvcreate
%{_sbindir}/lvdisplay
%{_sbindir}/lvextend
%{_sbindir}/lvmdiskscan
%{_sbindir}/lvmsadc
%{_sbindir}/lvmsar
%{_sbindir}/lvreduce
%{_sbindir}/lvremove
%{_sbindir}/lvrename
%{_sbindir}/lvresize
%{_sbindir}/lvs
%{_sbindir}/lvscan
%{_sbindir}/pvchange
%{_sbindir}/pvck
%{_sbindir}/pvcreate
%{_sbindir}/pvdisplay
%{_sbindir}/pvmove
%{_sbindir}/pvremove
%{_sbindir}/pvresize
%{_sbindir}/pvs
%{_sbindir}/pvscan
%{_sbindir}/vgcfgbackup
%{_sbindir}/vgcfgrestore
%{_sbindir}/vgchange
%{_sbindir}/vgck
%{_sbindir}/vgconvert
%{_sbindir}/vgcreate
%{_sbindir}/vgdisplay
%{_sbindir}/vgexport
%{_sbindir}/vgextend
%{_sbindir}/vgimport
%{_sbindir}/vgimportclone
%{_sbindir}/vgmerge
%{_sbindir}/vgmknodes
%{_sbindir}/vgreduce
%{_sbindir}/vgremove
%{_sbindir}/vgrename
%{_sbindir}/vgs
%{_sbindir}/vgscan
%{_sbindir}/vgsplit
%{_mandir}/man5/lvm.conf.5.gz
%{_mandir}/man7/lvmcache.7.gz
%{_mandir}/man7/lvmraid.7.gz
%{_mandir}/man7/lvmreport.7.gz
%{_mandir}/man7/lvmthin.7.gz
%{_mandir}/man7/lvmvdo.7.gz
%{_mandir}/man7/lvmsystemid.7.gz
%{_mandir}/man8/fsadm.8.gz
%{_mandir}/man8/lvchange.8.gz
%{_mandir}/man8/lvconvert.8.gz
%{_mandir}/man8/lvcreate.8.gz
%{_mandir}/man8/lvdisplay.8.gz
%{_mandir}/man8/lvextend.8.gz
%{_mandir}/man8/lvm.8.gz
%{_mandir}/man8/lvm2-activation-generator.8.gz
%{_mandir}/man8/lvm-config.8.gz
%{_mandir}/man8/lvmconfig.8.gz
%{_mandir}/man8/lvm-dumpconfig.8.gz
%{_mandir}/man8/lvmdiskscan.8.gz
%{_mandir}/man8/lvmdump.8.gz
%{_mandir}/man8/lvm-fullreport.8.gz
%{_mandir}/man8/lvmsadc.8.gz
%{_mandir}/man8/lvmsar.8.gz
%{_mandir}/man8/lvreduce.8.gz
%{_mandir}/man8/lvremove.8.gz
%{_mandir}/man8/lvrename.8.gz
%{_mandir}/man8/lvresize.8.gz
%{_mandir}/man8/lvs.8.gz
%{_mandir}/man8/lvscan.8.gz
%{_mandir}/man8/pvchange.8.gz
%{_mandir}/man8/pvck.8.gz
%{_mandir}/man8/pvcreate.8.gz
%{_mandir}/man8/pvdisplay.8.gz
%{_mandir}/man8/pvmove.8.gz
%{_mandir}/man8/pvremove.8.gz
%{_mandir}/man8/pvresize.8.gz
%{_mandir}/man8/pvs.8.gz
%{_mandir}/man8/pvscan.8.gz
%{_mandir}/man8/vgcfgbackup.8.gz
%{_mandir}/man8/vgcfgrestore.8.gz
%{_mandir}/man8/vgchange.8.gz
%{_mandir}/man8/vgck.8.gz
%{_mandir}/man8/vgconvert.8.gz
%{_mandir}/man8/vgcreate.8.gz
%{_mandir}/man8/vgdisplay.8.gz
%{_mandir}/man8/vgexport.8.gz
%{_mandir}/man8/vgextend.8.gz
%{_mandir}/man8/vgimport.8.gz
%{_mandir}/man8/vgimportclone.8.gz
%{_mandir}/man8/vgmerge.8.gz
%{_mandir}/man8/vgmknodes.8.gz
%{_mandir}/man8/vgreduce.8.gz
%{_mandir}/man8/vgremove.8.gz
%{_mandir}/man8/vgrename.8.gz
%{_mandir}/man8/vgs.8.gz
%{_mandir}/man8/vgscan.8.gz
%{_mandir}/man8/vgsplit.8.gz
%{_udevdir}/11-dm-lvm.rules
%{_udevdir}/69-dm-lvm-metad.rules
%if %{enable_lvmpolld}
%{_mandir}/man8/lvmpolld.8.gz
%{_mandir}/man8/lvm-lvpoll.8.gz
%endif
%dir %{_sysconfdir}/lvm
%ghost %{_sysconfdir}/lvm/cache/.cache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvm.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvmlocal.conf
%dir %{_sysconfdir}/lvm/profile
%{_sysconfdir}/lvm/profile/command_profile_template.profile
%{_sysconfdir}/lvm/profile/metadata_profile_template.profile
%{_sysconfdir}/lvm/profile/thin-generic.profile
%{_sysconfdir}/lvm/profile/thin-performance.profile
%{_sysconfdir}/lvm/profile/cache-mq.profile
%{_sysconfdir}/lvm/profile/cache-smq.profile
%{_sysconfdir}/lvm/profile/lvmdbusd.profile
%if %{enable_vdo}
%{_sysconfdir}/lvm/profile/vdo-small.profile
%endif
%dir %{_sysconfdir}/lvm/backup
%dir %{_sysconfdir}/lvm/cache
%dir %{_sysconfdir}/lvm/archive
%dir %{_default_locking_dir}
%dir %{_default_run_dir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-monitor.service
%{_unitdir}/lvm2-pvscan@.service
%{_prefix}/lib/systemd/system-generators/lvm2-activation-generator
%if %{enable_lvmpolld}
%{_unitdir}/lvm2-lvmpolld.socket
%{_unitdir}/lvm2-lvmpolld.service
%endif

##############################################################################
# Library and Development subpackages
##############################################################################
%package devel
Summary: Development libraries and headers
License: LGPLv2
Requires: %{name} = %{?epoch}:%{version}-%{release}
Requires: device-mapper-devel = %{?epoch}:%{device_mapper_version}-%{release}
Requires: device-mapper-event-devel = %{?epoch}:%{device_mapper_version}-%{release}
Requires: pkgconfig

%description devel
This package contains files needed to develop applications that use
the lvm2 libraries.

%files devel
%{_libdir}/liblvm2cmd.so
%{_libdir}/libdevmapper-event-lvm2.so
%{_includedir}/lvm2cmd.h

%package libs
Summary: Shared libraries for lvm2
License: LGPLv2
Requires: device-mapper-event = %{?epoch}:%{device_mapper_version}-%{release}

%description libs
This package contains shared lvm2 libraries for applications.

%ldconfig_scriptlets libs

%files libs
%license COPYING.LIB
%{_libdir}/liblvm2cmd.so.*
%{_libdir}/libdevmapper-event-lvm2.so.*
%dir %{_libdir}/device-mapper
%{_libdir}/device-mapper/libdevmapper-event-lvm2mirror.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2snapshot.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2raid.so
%{_libdir}/libdevmapper-event-lvm2mirror.so
%{_libdir}/libdevmapper-event-lvm2snapshot.so
%{_libdir}/libdevmapper-event-lvm2raid.so

%if %{enable_thin}
%{_libdir}/libdevmapper-event-lvm2thin.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2thin.so
%endif

%{_libdir}/libdevmapper-event-lvm2vdo.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2vdo.so

##############################################################################
# LVM locking daemon
##############################################################################
%if %{enable_lockd_dlm} || %{enable_lockd_sanlock}
%package lockd
Summary: LVM locking daemon
Requires: lvm2 = %{?epoch}:%{version}-%{release}
%if %{enable_lockd_sanlock}
Requires: sanlock-lib >= %{sanlock_version}
%endif
%if %{enable_lockd_dlm}
Requires: dlm-lib >= %{dlm_version}
%endif
Requires(post): systemd-units >= %{systemd_version}
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

%description lockd

LVM commands use lvmlockd to coordinate access to shared storage.

%post lockd
%systemd_post lvmlockd.service lvmlocks.service

%preun lockd
%systemd_preun lvmlockd.service lvmlocks.service

%postun lockd
%systemd_postun lvmlockd.service lvmlocks.service

%files lockd
%{_sbindir}/lvmlockd
%{_sbindir}/lvmlockctl
%{_mandir}/man8/lvmlockd.8.gz
%{_mandir}/man8/lvmlockctl.8.gz
%{_unitdir}/lvmlockd.service
%{_unitdir}/lvmlocks.service

%endif

###############################################################################
# Cluster mirror subpackage
# The 'clvm' OCF script to manage cmirrord instance is part of resource-agents.
###############################################################################
%if %{enable_cluster}
%if %{enable_cmirror}

%package -n cmirror
Summary: Daemon for device-mapper-based clustered mirrors
Requires: corosync >= %{corosync_version}
Requires: device-mapper = %{?epoch}:%{device_mapper_version}-%{release}
Requires: resource-agents >= %{resource_agents_version}

%description -n cmirror
Daemon providing device-mapper-based mirrors in a shared-storage cluster.

%files -n cmirror
%{_sbindir}/cmirrord
%{_mandir}/man8/cmirrord.8.gz

##############################################################################
# Cmirror-standalone subpackage
##############################################################################
%package -n cmirror-standalone
Summary: Additional files to support device-mapper-based clustered mirrors in standalone mode
License: GPLv2
Requires: cmirror >= %{?epoch}:%{version}-%{release}

%description -n cmirror-standalone

Additional files needed to run daemon for device-mapper-based clustered
mirrors in standalone mode as a service without cluster resource manager
involvement (e.g. pacemaker).

%post -n cmirror-standalone
%systemd_post lvm2-cmirrord.service

%preun -n cmirror-standalone
%systemd_preun lvm2-cmirrord.service

%postun -n cmirror-standalone
%systemd_postun lvm2-cmirrord.service

%files -n cmirror-standalone
%{_unitdir}/lvm2-cmirrord.service

%endif
%endif

##############################################################################
# LVM D-Bus daemon
##############################################################################
%if %{enable_lvmdbusd}

%package dbusd
Summary: LVM2 D-Bus daemon
License: GPLv2
BuildArch: noarch
Requires: lvm2 >= %{?epoch}:%{version}-%{release}
Requires: dbus
Requires: python3-dbus
Requires: python3-pyudev
Requires: python3-gobject-base
Requires(post): systemd-units >= %{systemd_version}
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

%description dbusd

Daemon for access to LVM2 functionality through a D-Bus interface.

%post dbusd
%systemd_post lvm2-lvmdbusd.service

%preun dbusd
%systemd_preun lvm2-lvmdbusd.service

%postun dbusd
%systemd_postun lvm2-lvmdbusd.service

%files dbusd
%{_sbindir}/lvmdbusd
%{_sysconfdir}/dbus-1/system.d/com.redhat.lvmdbus1.conf
%{_datadir}/dbus-1/system-services/com.redhat.lvmdbus1.service
%{_mandir}/man8/lvmdbusd.8.gz
%{_unitdir}/lvm2-lvmdbusd.service
%{python3_sitelib}/lvmdbusd/*

%endif

##############################################################################
# Device-mapper subpackages
##############################################################################
%package -n device-mapper
Summary: Device mapper utility
Version: %{device_mapper_version}
License: GPLv2
URL: https://www.sourceware.org/dm/
Requires: device-mapper-libs = %{?epoch}:%{device_mapper_version}-%{release}
Requires: util-linux-core >= %{util_linux_version}
Requires: systemd >= %{systemd_version}
# We need dracut to install required udev rules if udev_sync
# feature is turned on so we don't lose required notifications.
Conflicts: dracut < %{dracut_version}

%description -n device-mapper
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%files -n device-mapper
%license COPYING COPYING.LIB
%doc WHATS_NEW_DM VERSION_DM README
%doc udev/12-dm-permissions.rules
%{_sbindir}/dmsetup
%{_sbindir}/blkdeactivate
%{_sbindir}/dmstats
%{_mandir}/man8/dmsetup.8.gz
%{_mandir}/man8/dmstats.8.gz
%{_mandir}/man8/blkdeactivate.8.gz
%if %{enable_dmfilemapd}
%{_sbindir}/dmfilemapd
%{_mandir}/man8/dmfilemapd.8.gz
%endif
%{_udevdir}/10-dm.rules
%{_udevdir}/13-dm-disk.rules
%{_udevdir}/95-dm-notify.rules

%package -n device-mapper-devel
Summary: Development libraries and headers for device-mapper
Version: %{device_mapper_version}
License: LGPLv2
Requires: device-mapper = %{?epoch}:%{device_mapper_version}-%{release}
Requires: pkgconfig

%description -n device-mapper-devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%files -n device-mapper-devel
%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%package -n device-mapper-libs
Summary: Device-mapper shared library
Version: %{device_mapper_version}
License: LGPLv2
Requires: device-mapper = %{?epoch}:%{device_mapper_version}-%{release}

%description -n device-mapper-libs
This package contains the device-mapper shared library, libdevmapper.

%ldconfig_scriptlets -n device-mapper-libs

%files -n device-mapper-libs
%license COPYING COPYING.LIB
%{_libdir}/libdevmapper.so.*

%package -n device-mapper-event
Summary: Device-mapper event daemon
Version: %{device_mapper_version}
Requires: device-mapper = %{?epoch}:%{device_mapper_version}-%{release}
Requires: device-mapper-event-libs = %{?epoch}:%{device_mapper_version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n device-mapper-event
This package contains the dmeventd daemon for monitoring the state
of device-mapper devices.

%post -n device-mapper-event
%systemd_post dm-event.socket
# dm-event.socket is always enabled and started and ready to serve if dmeventd is used
# replace direct systemctl calls with systemd rpm macro once this is provided in the macro:
# http://cgit.freedesktop.org/systemd/systemd/commit/?id=57ab2eabb8f92fad5239c7d4492e9c6e23ee0678
systemctl enable dm-event.socket
systemctl start dm-event.socket >/dev/null 2>&1 || :
if [ -e %{_default_pid_dir}/dmeventd.pid ]; then
	%{_sbindir}/dmeventd -R || echo "Failed to restart dmeventd daemon. Please, try manual restart."
fi

%preun -n device-mapper-event
%systemd_preun dm-event.service dm-event.socket

%files -n device-mapper-event
%{_sbindir}/dmeventd
%{_mandir}/man8/dmeventd.8.gz
%{_unitdir}/dm-event.socket
%{_unitdir}/dm-event.service

%package -n device-mapper-event-libs
Summary: Device-mapper event daemon shared library
Version: %{device_mapper_version}
License: LGPLv2

%description -n device-mapper-event-libs
This package contains the device-mapper event daemon shared library,
libdevmapper-event.

%ldconfig_scriptlets -n device-mapper-event-libs

%files -n device-mapper-event-libs
%license COPYING.LIB
%{_libdir}/libdevmapper-event.so.*

%package -n device-mapper-event-devel
Summary: Development libraries and headers for the device-mapper event daemon
Version: %{device_mapper_version}
License: LGPLv2
Requires: device-mapper-event = %{?epoch}:%{device_mapper_version}-%{release}
Requires: pkgconfig

%description -n device-mapper-event-devel
This package contains files needed to develop applications that use
the device-mapper event library.

%files -n device-mapper-event-devel
%{_libdir}/libdevmapper-event.so
%{_includedir}/libdevmapper-event.h
%{_libdir}/pkgconfig/devmapper-event.pc

##############################################################################
# Testsuite
##############################################################################
%if %{enable_testsuite}
%package testsuite
Summary: LVM2 Testsuite
# Most of the code is GPLv2, the harness in test/lib/{brick-shelltest.h,runner.cpp} is BSD, and C files in test/api are LGPLv2...
License: LGPLv2 and GPLv2 and BSD-2-Clause

%description testsuite
An extensive functional testsuite for LVM2.

%files testsuite
%license COPYING COPYING.LIB COPYING.BSD
%{_datadir}/lvm2-testsuite/
%{_libexecdir}/lvm2-testsuite/
%{_bindir}/lvm2-testsuite
%endif

%changelog
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.03.11-8
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.03.11-5
- Rebuilt for Python 3.10

* Mon Mar 22 2021 Marian Csontos <mcsontos@redhat.com> - 2.03.11-4
- Fix editline compilation.

* Tue Mar 16 2021 Marian Csontos <mcsontos@redhat.com> - 2.03.11-3
- Replace readline library with editline.

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.03.11-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 22 2021 Marian Csontos <mcsontos@redhat.com> - 2.03.11-1
- Fix mpath filtering of NVMe devices.
- Check if lvcreate passes read_only_volume_list with tags and skips zeroing.
- Limit pool metadata spare to 16GiB.
- Improves conversion and allocation of pool metadata.
- Fix different limits used for metadata by lvm2 and thin-tools.
- Fix interrupting lvconvert --splitcache command with striped origin volumes.
- Fix problem with wiping of converted LVs.
- Fix memleak in scanning.
- Fix corner case allocation for thin-pools.
- Fix pvck handling MDA at offset different from 4096.
- Partial or degraded activation of writecache is not allowed.
- Enhance error handling in fsadm and handle correct fsck result.
- Dmeventd lvm plugin ignores higher reserved_stack lvm.conf values.
- Support using BLKZEROOUT for clearing devices.
- Fixed interrup handling.
- Fix block cache when device has too many failing writes.
- Fix block cache waiting for IO completion with failing disks.
- Add configure --enable-editline support as an alternative to readline.
- Enhance reporting and error handling when creating thin volumes.
- Enable vgsplit for VDO volumes.
- Lvextend of vdo pool volumes ensure at least 1 new VDO slab is added.
- Restore lost signal blocking while VG lock is held.
- Improve estimation of needed extents when creating thin-pool.
- Use extra 1% when resizing thin-pool metadata LV with --use-policy.
- Enhance --use-policy percentage rounding.
- Allow pvmove of writecache origin.
- Report integrity fields.
- Integrity volumes defaults to journal mode.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Aug 09 2020 Marian Csontos <mcsontos@redhat.com> - 2.03.10-1
- Add integrity with raid capability.
- Add writecache and integrity support to lvmdbusd.
- Zero pool metadata on allocation (disable with allocation/zero_metadata=0).
- Failure in zeroing or wiping will fail command (bypass with -Zn, -Wn).
- Add lvcreate of new cache or writecache lv with single command.
- Generate unique cachevol name when default required from lvcreate.
- Converting RAID1 volume to one with same number of legs now succeeds with a
  warning.
- Fix conversion to raid from striped lagging type.
- Fix conversion to 'mirrored' mirror log with larger regionsize.
- Fix running out of free buffers for async writing for larger writes.
- Fix support for lvconvert --repair used by foreign apps (i.e. Docker).
- Add support for VDO in blkdeactivate script.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.03.09-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.03.09-2
- Rebuilt for Python 3.9

* Thu Mar 26 2020 Marian Csontos <mcsontos@redhat.com> - 2.03.09-1
- Fix showing of a dm kernel error when uncaching a volume with cachevol.
- Fix memleak in syncing of internal cache.
- Fix pvck dump_current_text memleak.
- Fix lvmlockd result code on error path for _query_lock_lv().
- Update pvck man page and help output.
- Accept more output lines from vdo_format.
- Prevent raid reshaping of stacked volumes.
- Writecache and VDO volume handling improvements.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.07-1
- Ensure minimum required region size on striped RaidLV creation.
- Fix resize of thin-pool with data and metadata of different segtype.
- Improve mirror type leg splitting.
- Fix activation order when removing merged snapshot.
- Experimental VDO support for lvmdbusd.

* Wed Oct 23 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.06-1
- IMPORTANT: Prevent creating VGs with PVs with different logical block sizes.
- Fix metadata writes from corrupting with large physical block size.
- Correctly set read_ahead for LVs when pvmove is finished.
- Add support for DM_DEVICE_GET_TARGET_VERSION into device_mapper.
- Activate thin-pool layered volume as 'read-only' device.
- Ignore crypto devices with UUID signature CRYPT-SUBDEV.
- Synchronize with udev when dropping snapshot.
- Add missing device synchronization point before removing pvmove node.
- See WHATS_NEW for more.

* Wed Sep 18 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.05-4
- Remove unsupported OPTIONS+="event_timeout" from udev rule (#1749857)

* Tue Aug 27 2019 Adam Williamson <awilliam@redhat.com> - 2.03.05-3
- Backport fix for converting dbus.UInt to string in Python 3.8 (#1745597)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.03.05-2
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.05-1
- IMPORTANT: Prohibit mirrored 'mirror' log via lvcreate and lvconvert. Use RAID1.
- IMPORTANT: Dropped deprecated liblvm2app.
- IMPORTANT: clvmd dropped. Use lvmlockd for cluster locking.
- Dropped lvmetad.
- Deduplication and compression - support for VDO volumes.
- Add device hints to reduce scanning.
- See WHATS_NEW and WHATS_NEW_DM in the documentation directory for more.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.185-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Marian Csontos <mcsontos@redhat.com> - 2.02.185-1
- Fix change of monitoring in clustered volumes.
- Improve -lXXX%%VG modifier which improves cache segment estimation.
- Add synchronization with udev before removing cached devices.
- Fix missing growth of _pmspare volume when extending _tmeta volume.
- Automatically grow thin metadata, when thin data gets too big.
- Add cached devices support to vgsplit.
- Fix signal delivery checking race in libdaemon (lvmetad).
- Add missing Before=shutdown.target to LVM2 services to fix shutdown ordering.

* Mon Apr 01 2019 Marian Csontos <mcsontos@redhat.com> - 2.02.184-1
- IMPORTANT: Change scan_lvs default to 0 so LVs are not scanned for PVs.
- Fix (de)activation of RaidLVs with visible SubLVs.
- Add scan_lvs config setting to control if lvm scans LVs for PVs.
- Fix missing proper initialization of pv_list struct when adding PV.
- Ensure migration_threshold for cache is at least 8 chunks.
- Enhance ioctl flattening and add parameters only when needed.
- Add DM_DEVICE_ARM_POLL for API completness matching kernel.

* Thu Mar 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-4
- Remove obsolete scriptlets

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-3
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.183-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.183-1
- Bug fix release addressing issus with MD RAID version 1.0 and 0.90.

* Wed Oct 31 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.182-1
- Important bugfix release fixing possible data corruption.

* Thu Aug 02 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.181-1
- Reject conversions on raid1 LVs with split tracked SubLVs.
- Reject conversions on raid1 split tracked SubLVs.
- Fix dmstats list failing when no regions exist.
- Reject conversions of LVs under snapshot.
- Limit suggested options on incorrect option for lvconvert subcommand.
- Add vdo plugin for monitoring VDO devices.

* Thu Jul 19 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.180-1
- Never send any discard ioctl with test mode.
- Fix thin-pool alloc which needs same PV for data and metadata.
- Enhance vgcfgrestore to check for active LVs in restored VG.
- Provide possible layouts when converting between linear and striped/raid.
- Fix unmonitoring of merging snapshots.
- Cache can uses metadata format 2 with cleaner policy.
- Avoid showing internal error in lvs output or pvmoved LVs.
- Fix check if resized PV can also fit metadata area.
- Reopen devices RDWR only before writing to avoid udev issues.
- Change pvresize output confusing when no resize took place.
- Fix lvmetad hanging on shutdown.
- Fix mem leak in clvmd and more coverity issues.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.179-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-3
- Remove deprecated python bindings.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.02.179-2
- Rebuilt for Python 3.7.

* Mon Jun 18 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-1
- Bugfix release mainly fixing known cache and lvmlockd issues.

* Wed Jun 13 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-1
- Remove the rc1 from release.

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-0.1.rc1
- Remove lvm1 and pool format handling and add filter to ignore them.
- Rework disk scanning and when it is used.
- Add new io layer using libaio for faster scanning.
- Support activation of component LVs in read-only mode.
- Avoid non-exclusive activation of exclusive segment types.
- Restore pvmove support for clusterwide active volumes (2.02.177).
- Add prioritized_section() to restore cookie boundaries (2.02.177).
- Again accept striped LV as COW LV with lvconvert -s (2.02.169).
- Restore usability of thin LV to be again external origin for another thin (2.02.169).
- See WHATS_NEW and WHATS_NEW_DM in the documentation directory for more.

* Wed Apr 04 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.177-5
- Disable python2 bindings.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.177-4
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.177-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.02.177-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Dec 19 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.177-1
- When writing text metadata content, use complete 4096 byte blocks.
- Change text format metadata alignment from 512 to 4096 bytes.
- When writing metadata, consistently skip mdas marked as failed.
- Refactor and adjust text format metadata alignment calculation.
- Fix python3 path in lvmdbusd to use value detected by configure.
- Reduce checks for active LVs in vgchange before background polling.
- Ensure _node_send_message always uses clean status of thin pool.
- Fix lvmlockd to use pool lock when accessing _tmeta volume.
- Report expected sanlock_convert errors only when retries fail.
- Avoid blocking in sanlock_convert on SH to EX lock conversion.
- Deactivate missing raid LV legs (_rimage_X-missing_Y_Z) on decativation.
- Skip read-modify-write when entire block is replaced.
- Categorise I/O with reason annotations in debug messages.
- Allow extending of raid LVs created with --nosync after a failed repair.
- Command will lock memory only when suspending volumes.
- Merge segments when pvmove is finished.
- Remove label_verify that has never been used.
- Ensure very large numbers used as arguments are not casted to lower values.
- Enhance reading and validation of options stripes and stripes_size.
- Fix printing of default stripe size when user is not using stripes.
- Activation code for pvmove automatically discovers holding LVs for resume.
- Make a pvmove LV locking holder.
- Do not change critical section counter on resume path without real resume.
- Enhance activation code to automatically suspend pvmove participants.
- Prevent conversion of thin volumes to snapshot origin when lvmlockd is used.
- Correct the steps to change lock type in lvmlockd man page.
- Retry lock acquisition on recognized sanlock errors.
- Fix lock manager error codes in lvmlockd.
- Remove unnecessary single read from lvmdiskscan.
- Check raid reshape flags in vg_validate().
- Add support for pvmove of cache and snapshot origins.
- Avoid using precommitted metadata for suspending pvmove tree.
- Ehnance pvmove locking.
- Deactivate activated LVs on error path when pvmove activation fails.
- Add "io" to log/debug_classes for logging low-level I/O.
- Avoid importing persistent filter in vgscan/pvscan/vgrename.
- Fix memleak of string buffer when vgcfgbackup runs in secure mode.
- Do not print error when clvmd cannot find running clvmd.
- Prevent start of new merge of snapshot if origin is already being merged.
- Fix offered type for raid6_n_6 to raid5 conversion (raid5_n).
- Deactivate sub LVs when removing unused cache-pool.
- Do not take backup with suspended devices.
- Avoid RAID4 activation on incompatible kernels under all circumstances.
- Reject conversion request to striped/raid0 on 2-legged raid4/5.
- Activation tree of thin pool skips duplicated check of pool status.
- Remove code supporting replicator target.
- Do not ignore failure of _info_by_dev().
- Propagate delayed resume for pvmove subvolumes.
- Suppress integrity encryption keys in 'table' output unless --showkeys supplied.

* Thu Dec 14 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.176-2
- Add testsuite subpackage.

* Fri Nov 03 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.176-1
- Fix segfault in lvm_pv_remove in liblvm. (2.02.173)
- Do not allow storing VG metadata with LV without any segment.
- Fix printed message when thin snapshot was already merged.
- Remove created spare LV when creation of thin-pool failed.
- Avoid reading ignored metadata when MDA gets used again.
- Fix detection of moved PVs in vgsplit. (2.02.175)
- Ignore --stripes/--stripesize on RAID takeover
- Disallow creation of snapshot of mirror/raid subLV (was never supported).
- Keep Install section only in *.socket systemd units.
- Improve used paths for generated systemd units and init shells.
- Fix regression in more advanced vgname extraction in lvconvert (2.02.169).
- Allow lvcreate to be used for caching of _tdata LV.
- Avoid internal error when resizing cache type _tdata LV (not yet supported).
- Show original converted names when lvconverting LV to pool volume.
- Move lib code used only by liblvm into metadata-liblvm.c.
- Distinguish between device not found and excluded by filter.
- Monitor external origin LVs.
- Allow lvcreate --type mirror to work with 100%%FREE.
- Improve selection of resource name for complex volume activation lock.
- Avoid cutting first character of resource name for activation lock.
- Support for encrypted devices in fsadm.
- Improve thin pool overprovisioning and repair warning messages.
- Fix incorrect adjustment of region size on striped RaidLVs.
- Issue a specific error with dmsetup status if device is unknown.
- Fix RT_LIBS reference in generated libdevmapper.pc for pkg-config.

* Mon Oct 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.175-1
- Use --help with blockdev when checking for --getsize64 support in fsadm.
- Dump lvmdbusd debug information with SIGUSR1.
- Fix metadata corruption in vgsplit and vgmerge intermediate states.
- Add PV_MOVED_VG PV status flag to mark PVs moving between VGs.
- Fix lvmdbus hang and recognise unknown VG correctly.
- Improve error messages when command rules fail.
- Require LV name with pvmove in a shared VG.
- Allow shared active mirror LVs with lvmlockd, dlm, and cmirrord.
- Support lvconvert --repair with cache and cachepool volumes.
- lvconvert --repair respects --poolmetadataspare option.
- Fix thin pool creation in a shared VG. (2.02.173)
- Schedule exit when received SIGTERM in dmeventd.
- Fix blkdeactivate regression with failing DM/MD devs deactivation (1.02.142).
- Add blkdeactivate -r wait option to wait for MD resync/recovery/reshape.
- Use blkdeactivate -r wait in blk-availability systemd service/initscript.
- Also try to unmount /boot on blkdeactivate -u if on top of supported device.
- Fix typo in blkdeactivate's '--{dm,lvm,mpath}options' option name.
- Correct return value testing when get reserved values for reporting.
- Take -S with dmsetup suspend/resume/clear/wipe_table/remove/deps/status/table.
- Fix mistakenly commented out %%python_provide line for python3-lvm.

* Mon Oct 02 2017 Troy Dawson <tdawson@redhat.com> - 2.02.174-2
- Bump to rebuild on rebuilt corosync
- Cleanup spec file conditionals

* Wed Sep 20 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.174-1.f28
- NOTE: Deprecating python bindings and liblvm2app.
- Prevent raid1 split with trackchanges in a shared VG.
- Avoid double unlocking of client & lockspace mutexes in lvmlockd.
- Fix leaking of file descriptor for non-blocking filebased locking.
- Fix check for 2nd mda at end of disk fits if using pvcreate --restorefile.
- Use maximum metadataarea size that fits with pvcreate --restorefile.
- Always clear cached bootloaderarea when wiping label e.g. in pvcreate.
- Disallow --bootloaderareasize with pvcreate --restorefile.
- Fix lvmlockd check for running lock managers during lock adoption.
- Add --withgeneralpreamble and --withlocalpreamble to lvmconfig.
- Add warning when creating thin-pool with zeroing and chunk size >= 512KiB.
- Introduce exit code 4 EINIT_FAILED to replace -1 when initialisation fails.
- Add synchronization points with udev during reshape of raid LVs.
- Restore umask when creation of node fails.
- Add --concise to dmsetup create for many devices with tables in one command.
- Accept minor number without major in library when it knows dm major number.
- Introduce single-line concise table output format: dmsetup table --concise.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.173-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.02.173-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.173-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.173-1
- Create /dev/disk/by-part{uuid,label} and gpt-auto-root symlinks with udev.
- Add synchronization points with udev during conversion of raid LVs.
- Improve --size args validation and report more detailed error message.
- Initialize debugging mutex before any debug message in clvmd.
- Log error instead of warn when noticing connection problem with lvmetad.
- Fix memory leak in lvmetad when working with duplicates.
- Remove restrictions on reshaping open and clustered raid devices.
- Add incompatible data_offset to raid metadata to fix reshape activation.
- Accept 'lvm -h' and 'lvm --help' as well as 'lvm help' for help.
- Suppress error message from accept() on clean lvmetad shutdown.
- Tidy clvmd client list processing and fix segfaults.
- Protect clvmd debug log messages with mutex and add client id.
- Fix shellcheck reported issues for script files.

* Thu Jun 29 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.172-1
- Do not lvdisplay --maps unset settings of cache pool.
- Fix lvdisplay --maps for cache pool without policy settings.
- Support aborting of flushing cache LV.
- Improve lvcreate --cachepool arg validation.
- Cache format2 flag is now using segment name type field.
- Disallow cachepool creation with policy cleaner and mode writeback.
- Lvconvert --repair handles failing raid legs (present but marked 'D'ead).
- Add display_percent helper function for printing percent values.
- Add dm_percent_to_round_float for adjusted percentage rounding.
- Fix lvcreate extent percentage calculation for mirrors.
- Reenable conversion of data and metadata thin-pool volumes to raid.
- Linear to RAID1 upconverts now use "recover" sync action, not "resync".
- No longer necessary to '--force' a repair for RAID1.
- Improve raid status reporting with lvs.
- dm_get_status_raid() handle better some incosistent md statuses.
- Limit maximal size of thin-pool for specific chunk size.
- Print a warning about in-use PVs with no VG using them.
- Disable automatic clearing of PVs that look like in-use orphans.
- Extend validation of filesystems resized by fsadm.
- Properly handle subshell return codes in fsadm.
- Stop using '--yes' mode when fsadm runs without terminal.
- Support storing status flags via segtype name field.
- Enhance lvconvert automatic settings of possible (raid) LV types.
- Add missing NULL to argv array when spliting cmdline arguments.
- Don't reinstate still-missing devices when correcting inconsistent metadata.
- Allow lvchange to change properties on a thin pool data sub LV.
- Fix reusing of dm_task structure for status reading (used by dmeventd).
- Drop unneeded --config option from raid dmeventd plugin.
- Accept truncated files in calls to dm_stats_update_regions_from_fd().
- Restore Warning by 5% increment when thin-pool is over 80% (1.02.138).
- Reset array with dead rimage devices once raid gets in sync.

* Fri Jun 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-3
- Fix lvmdbusd not passing --all with vgreduce --removemissing.

* Wed May 17 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-2
- Fix lvmdbusd mangling config options.

* Tue May 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-1
- Add RAID takeover and reshaping.
- Add pvcreate prompt when device size doesn't match setphysicalvolumesize.
- Remove obsolete lvmchange binary - convert to built-in command.
- Support cache segment with configurable metadata format.
- Add option for lvcreate/lvconvert --cachemetadataformat auto|1|2.
- Add allocation/cache_metadata_format profilable settings.
- Command line options, help and man pages using common definitions.
- Add build-time configuration command line to 'lvm version' output.
- Disable lvmetad when lvconvert --repair is run.
- Raise mirror/raid default regionsize to 2MiB.
- Support shrinking of RaidLVs.
- Introduce global/fsadm_executable to make fsadm path configurable.
- Look for limited thin pool metadata size when using 16G metadata.
- Add lvconvert pool creation rule disallowing options with poolmetadata.
- Fix missing lvmlockd LV locks in lvchange and lvconvert.
- Fix dmeventd setup for lvchange --poll.
- Fix use of --poll and --monitor with lvchange and vgchange.
- Disallow lvconvert of hidden LV to a pool.
- Ignore --partial option when not used for activation.
- Allow --activationmode option with lvchange --refresh.
- Allow valid lvconvert --regionsize change
- Fix SIGINT blocking to prevent corrupted metadata
- Fix systemd unit existence check for lvmconf --services --startstopservices.
- Check and use PATH_MAX buffers when creating vgrename device paths.
- Handle known table line parameter order change in specific raid target vsns.
- Show more information for cached volumes in lvdisplay [-m].
- Use function cache_set_params() for both lvcreate and lvconvert.
- Skip rounding on cache chunk size boudary when create cache LV.
- Improve cache_set_params support for chunk_size selection.
- Fix metadata profile allocation/cache_[mode|policy] setting.
- Fix missing support for using allocation/cache_pool_chunk_size setting.
- Support conversion of raid type, stripesize and number of disks
- Reject writemostly/writebehind in lvchange during resynchronization.
- Deactivate active origin first before removal for improved workflow.
- Fix regression of accepting both --type and -m with lvresize. (2.02.158)
- Add extra memory page when limiting pthread stack size in clvmd.
- Support striped/raid0* <-> raid10_near conversions.
- Support region size changes on existing RaidLVs.
- Avoid parallel usage of cpg_mcast_joined() in clvmd with corosync.
- Support raid6_{ls,rs,la,ra}_6 segment types and conversions from/to it.
- Support raid6_n_6 segment type and conversions from/to it.
- Support raid5_n segment type and conversions from/to it.
- Support new internal command _dmeventd_thin_command.
- Introduce new dmeventd/thin_command configurable setting.
- Use new default units 'r' for displaying sizes.
- Also unmount mount point on top of MD device if using blkdeactivate -u.
- Restore check preventing resize of cache type volumes (2.02.158).
- Add missing udev sync when flushing dirty cache content.
- vgchange -p accepts only uint32 numbers.
- Report thin LV date for merged LV when the merge is in progress.
- Detect if snapshot merge really started before polling for progress.
- Checking LV for merging origin requires also it has merged snapshot.
- Extend validation of metadata processing.
- Enable usage of cached volumes as snapshot origin LV.
- Fix displayed lv name when splitting snapshot (2.02.146).
- Warn about command not making metadata backup just once per command.
- Enable usage of cached volume as thin volume's external origin.
- Support cache volume activation with -real layer.
- Improve search of lock-holder for external origin and thin-pool.
- Support status checking of cache volume used in layer.
- Avoid shifting by one number of blocks when clearing dirty cache volume.
- Extend metadata validation of external origin LV use count.
- Fix dm table when the last user of active external origin is removed.
- Improve reported lvs status for active external origin volume.
- Fix table load for splitted RAID LV and require explicit activation.
- Always active splitted RAID LV exclusively locally.
- Do not use LV RAID status bit for segment status.
- Check segtype directly instead of checking RAID in segment status.
- Reusing exiting code for raid image removal.
- Fix pvmove leaving -pvmove0 error device in clustered VG.
- Avoid adding extra '_' at end of raid extracted images or metadata.
- Optimize another _rmeta clearing code.
- Fix deactivation of raid orphan devices for clustered VG.
- Fix lvconvert raid1 to mirror table reload order.
- Add internal function for separate mirror log preparation.
- Fix segfault in lvmetad from missing NULL in daemon_reply_simple.
- Simplify internal _info_run() and use _setup_task_run() for mknod.
- Better API for internal function _setup_task_run.
- Avoid using lv_has_target_type() call within lv_info_with_seg_status.
- Simplify internal lv_info_with_seg_status API.
- Decide which status is needed in one place for lv_info_with_seg_status.
- Fix matching of LV segment when checking for it info status.
- Report log_warn when status cannot be parsed.
- Test segment type before accessing segment members when checking status.
- Implement compatible target function for stripe segment.
- Use status info to report merge failed and snapshot invalid lvs fields.
- See WHATS_NEW and WHATS_NEW_DM in the documentation directory for more.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.168-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.02.168-3
- Rebuild for readline 7.x

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.02.168-2
- Rebuild for Python 3.6

* Thu Dec 01 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.168-1
- Display correct sync_percent on large RaidLVs
- lvmdbusd --blackboxsize <n> added, used to override default size of 16
- Allow a transiently failed RaidLV to be refreshed
- Use lv_update_and_reload() inside mirror code where it applies.
- Preserve mirrored status for temporary layered mirrors.
- Use transient raid check before repairing raid volume.
- Implement transient status check for raid volumes.
- Only log msg as debug if lvm2-lvmdbusd unit missing for D-Bus notification.
- Avoid duplicated underscore in name of extracted LV image.
- Missing stripe filler now could be also 'zero'.
- lvconvert --repair accepts --interval and --background option.
- More efficiently prepare _rmeta devices when creating a new raid LV.
- Document raid status values.
- Always exit dmsetup with success when asked to display help/version.

* Tue Nov 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-2
- Only log msg as debug if lvm2-lvmdbusd unit missing for D-Bus notification.

* Mon Nov 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-1
- Use log_error in regex and sysfs filter to describe reason of failure.
- Fix blkdeactivate to deactivate dev stack if dev on top already unmounted.
- Prevent non-synced raid1 repair unless --force
- Prevent raid4 creation/conversion on non-supporting kernels
- Add direct striped -> raid4 conversion
- Fix raid4 parity image pair position on conversions from striped/raid0*
- Fix a few unconverted return code values for some lvconvert error path.
- Disable lvconvert of thin pool to raid while active.
- Disable systemd service start rate limiting for lvm2-pvscan@.service.
- Log failure of raid device with log_error level.
- Use dm_log_with_errno and translate runtime to dm_log only when needed.
- Make log messages from dm and lvm library different from dmeventd.
- Notice and Info messages are again logged from dmeventd and its plugins.
- Dmeventd now also respects DM_ABORT_ON_INTERNAL_ERRORS as libdm based tool.
- Report as non default dm logging also when logging with errno was changed.
- Use log_level() macro to consistently decode message log level in dmeventd.
- Still produce output when dmsetup dependency tree building finds dev missing.
- Check and report pthread_sigmask() failure in dmeventd.
- Check mem alloc fail in _canonicalize_field_ids().
- Use unsigned math when checking more then 31 legs of raid.
- Fix 'dmstats delete' with dmsetup older than v1.02.129
- Fix stats walk segfault with dmsetup older than v1.02.129

* Thu Oct 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.166-2
- Add various fixes for lvmdbusd from upcoming lvm2 version 2.02.167.

* Mon Sep 26 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.166-1
- Fix lvm2-activation-generator to read all LVM2 config sources. (2.02.155)
- Fix lvchange-rebuild-raid.sh to cope with older target versions.
- Use dm_config_parse_without_dup_node_check() to speedup metadata reading.
- Fix lvconvert --repair regression
- Fix reported origin lv field for cache volumes. (2.02.133)
- Always specify snapshot cow LV for monitoring not internal LV. (2.02.165)
- Fix lvchange --discard|--zero for active thin-pool.
- Enforce 4MiB or 25% metadata free space for thin pool operations.
- Fix lock-holder device for thin pool with inactive thin volumes.
- Use --alloc normal for mirror logs even if the mimages were stricter.
- Use O_DIRECT to gather metadata in lvmdump.
- Ignore creation_time when checking for matching metadata for lvmetad.
- Fix possible NULL pointer derefence when checking for monitoring.
- Add lvmreport(7) man page.
- Don't install lvmraid(7) man page when raid excluded. (2.02.165)
- Report 0% as dirty (copy%%) for cache without any used block.
- Fix lvm2api reporting of cache data and metadata percent.
- Restore reporting of metadata usage for cache volumes (2.02.155).
- Support raid scrubbing on cache origin LV.
- Fix man entry for dmsetup status.
- Introduce new dm_config_parse_without_dup_node_check().
- Don't omit last entry in dmstats list --group.

* Wed Sep 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.165-1
- Add lvmraid(7) man page.
- Use udev db to check for mpath components before running pvscan for lvmetad.
- Use lsblk -s and lsblk -O in lvmdump only if these options are supported.
- Fix number of stripes shown in lvcreate raid10 message when too many.
- Change lvmdbusd to use new lvm shell facilities.
- Do not monitor cache-pool metadata when LV is just being cleared.
- Add allocation/cache_pool_max_chunks to prevent misuse of cache target.
- Give error not segfault in lvconvert --splitmirrors when PV lies outside LV.
- Fix typo in report/columns_as_rows config option name recognition (2.02.99).
- Avoid PV tags when checking allocation against parallel PVs. 
- Disallow mirror conversions of raid10 volumes.
- Fix dmeventd unmonitoring when segment type (and dso) changes.
- Don't allow lvconvert --repair on raid0 devices or attempt to monitor them.
- No longer adjust incorrect number of raid stripes supplied to lvcreate.
- Move lcm and gcd to lib/misc.
- Fix vgsplit of external origins. (2.02.162)
- Prohibit creation of RAID LVs unless VG extent size is at least the page size.
- Suppress some unnecessary --stripesize parameter warnings.
- Fix 'pvmove -n name ...' to prohibit collocation of RAID SubLVs
- Improve explanation of udev fallback in libdevmapper.h.

* Mon Aug 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.164-2
- Fix selection of PVs when allocating raid0_meta.
- Fix sdbus socket leak leading to hang in lvmnotify.
- Specify max stripes for raid LV types: raid0:64; 1:10; 4,5:63; 6:62; 10:32.
- Avoid double suffix when naming _rmeta LV paired with _rimage LV.

* Wed Aug 10 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.163-1
- Add profile for lvmdbusd which uses lvm shell json report output.
- Restrict in-command modification of some parms in lvm shell.
- Apply LVM_COMMAND_PROFILE early for lvm shell.
- Refactor reporting so lvm shell log report collects whole of cmd execution.
- Support LVM_*_FD envvars to redirect output to file descriptors.
- Limit use of --corelog and --mirrorlog to mirrors in lvconvert.
- Reject --nosync option for RAID6 LVs in lvcreate.
- Do not refresh whole cmd context if profile dropped after processing LVM cmd. 
- Support straightforward lvconvert between striped and raid4 LVs. 
- Support straightforward lvconvert between raid1 and mirror LVs. 
- Report supported conversions when asked for unsupported raid lvconvert.
- Add "--rebuild PV" option to lvchange to allow for PV selective rebuilds.
- Preserve existing mirror region size when using --repair.
- Forbid stripe parameters with lvconvert --repair.
- Unify stripe size validation into get_stripe_params to catch missing cases.
- Further lvconvert validation logic refactoring.
- Add "lvm fullreport" man page.
- Add dm_report_destroy_rows/dm_report_group_output_and_pop_all for lvm shell.
- Adjust group handling and json production for lvm shell.

* Fri Jul 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.162-1
- Support lvconvert -Zn also when doing full cache pool conversion.
- Suppress not zeroing warn when converting to thin LV for non-zeroing tpool.
- Fix automatic updates of PV extension headers to newest version.
- Improve lvconvert --trackchanges validation to require --splitmirrors 1.
- Add note about lastlog built-in command to lvm man page.
- Fix unrecognised segtype flag message.
- lvconvert not clears cache pool metadata ONLY with -Zn. 
- Enabled lvconvert --uncache to work with partial VG.
- Fix json reporting to escape '"' character that may appear in reported string.

* Thu Jul 21 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.161-3
- Enable LVM notifications over dbus for lvmdbusd.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.161-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.161-1
- Prohibit some lvchange/lvresize that were failing on raid0 volumes.
- Fix segfaults in complex vgsplits. (2.02.159)
- Reformat unwieldy lvconvert man page.
- Allow --force to be passed through to pvcreate from vgcreate. (2.02.144)
- Fix lvresize of filesystem when LV has already right size (2.02.141)
- New LVM_LOG_FILE_MAX_LINES env var to limit max size of created logs.
- Disable queueing on mpath devs in blk-availability systemd service/initscript.
- Add new -m|--mpathoption disablequeueing to blkdeactivate.
- Automatically group regions with 'create --segments' unless --nogroup.
- Fix resource leak when deleting the first member of a group.
- Allow --bounds with 'create --filemap' for dmstats.
- Enable creation of filemap regions with histograms.
- Enable histogram aggregation for regions with more than one area.
- Enable histogram aggregation for groups of regions.
- Add a --filemap option to 'dmstats create' to allow mapping of files.
- Add dm_stats_create_regions_from_fd() to map file extents to regions.

* Thu Jul 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.160-1
- Minor fixes from coverity.

* Thu Jul 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.159-1
- Add raid0_meta segment type that provides metadata space for raid conversions.
- Fix created link for a used pool for vgmknode.
- Introduce and use is_power_of_2 macro.
- Support conversions between striped and raid0 segment types.
- Add infrastructure for raid takeover lvconvert options.
- Update default dmstats field selections for groups.
- Add 'obj_type', 'group_id', and 'statsname' fields to dmstats reports.
- Add --area, --region, and --group to dmstats to control object selection.
- Add --alias, --groupid, --regions to dmstats for group creation and deletion.
- Add 'group' and 'ungroup' commands to dmstats.
- Allow dm_stats_delete_group() to optionally delete all group members.
- Add dm_stats_get_object_type() to return the type of object present.
- Add dm_stats_walk_init() allowing control of objects visited by walks.
- Add dm_stats_get_group_descriptor() to return the member list as a string.
- Introduce dm_stats_get_nr_groups() and dm_stats_group_present().
- Add dm_stats_{get,set}_alias() to set and retrieve alias names for groups.
- Add dm_stats_get_group_id() to return the group ID for a given region.
- Add dm_stats_{create,delete}_group() to allow grouping of stats regions.
- Add enum-driven dm_stats_get_{metric,counter}() interfaces.
- Add dm_bitset_parse_list() to parse a string representation of a bitset.
- Thin dmeventd plugin umounts lvm2 volume only when pool is 95% or more.

* Tue Jun 28 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.158-1
- Add a more efficient native vgimportclone command to replace the script.
- Make lvmlockd always attempt to connect to lvmetad if no connection exists.
- Let lvmetad handle new connections after shutdown signal.
- Disable lvmetad when vgcfgrestore begins and enable it again after.
- Make pvscan do activation if lvmetad is configured but not running.
- Fix rescanning the PVs for a single VG when using lvmetad.
- Pool metadata lvresize uses now same code as resize of normal volume.
- Preserve monitoring status when updating thin-pool metadata.
- Return 0 (inactive) when status cannot be queried in _lv_active().
- Switch to log_warn() for failing activation status query.
- Replace vgimportclone script with binary.
- While lvmetad is shutting down, continue handling all connections cleanly.
- Refactor lvconvert argument handling code.
- Notify lvmetad when vgcfgrestore changes VG metadata.
- Add --logonly option to report only cmd log for a command, not other reports.
- Add log/command_log_selection to configure default selection used on cmd log. 
- Use 'orphan' object type in cmd log for groups to collect PVs not yet in VGs. 
- Add lvm lastlog command for query and display of last cmd's log in lvm shell.
- Report per-object return codes via cmd log while processing multiple objects.
- Annotate processing code with log report hooks for per-object command log. 
- Also pass common printed messages (besides warnings and errors) to log report.
- Log warnings and errors via report during cmd processing if this is enabled.
- Make it possible to iterate over internal 'orphan' VGs in process_each_vg fn.
- Make -S|--select option groupable that allows this option to be repeated.
- Make -O|--sort option groupable that allows this option to be repeated.
- Add --configreport option to select report for which next options are applied.
- Add support for priorities on grouping command arguments.
- Add report/{pvs,vgs,lvs,pvsegs,segs}_{cols,sort}_full to lvm.conf.
- Add lvm fullreport command for joined PV, VG, LV and segment report per VG.
- Integrate report group handling and cmd log report into cmd processing code.
- Add log/report_command_log to lvm.conf to enable or disable cmd log report.
- Add log/report_output_format to lvm.conf for default report output format.
- Recognize --reportformat {basic|json} option to select report output format.
- Add log/command_log_{sort,cols} to lvm.conf to configure command log report.
- Add log_object_{type,name,id,group,group_id} fields to cmd log. 
- Add log_{seq_num,type,context,message,errno,ret_code} fields to cmd log. 
- Add CMDLOG report type - a separate report type for command logging.
- Recognize 'all' keyword used in selection as synonym for "" (no selection).
- Add dm_report_set_selection to set selection for multiple output of report.
- Add DM_REPORT_OUTPUT_MULTIPLE_TIMES flag for multiple output of same report.
- Move field width handling/sort init from dm_report_object to dm_report_output.
- Add _LOG_BYPASS_REPORT flag for bypassing any log report currently set. 
- Introduce DM_REPORT_GROUP_JSON for report group with JSON output format.
- Introduce DM_REPORT_GROUP_BASIC for report group with basic report output.
- Introduce DM_REPORT_GROUP_SINGLE for report group having single report only.
- Add dm_report_group_{create,push,pop,destroy} to support report grouping.

* Fri Jun 17 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.157-2
- Change pvscan --cache -aay to scan locally if lvmetad fails.

* Mon Jun 13 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.156-1
- Don't allow duplicate orphan PVs to be used with vgcreate/vgextend/pvcreate.
- Improve handling of lvmetad update failures.
- Yes/No prompt accepts '^[ ^t]*([Yy]([Ee]([Ss]|)|)|[Nn]([Oo]|))[ ^t]*$'.
- If available, also collect output from lsblk command when running lvmdump -s.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-2
- Fix regression in blkdeactivate causing dm and md devices to be skipped. (2.02.155)

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-1
- Reject PV tags on pvmove cmdline because only 1 PV is supported. (2.02.141)
- Fix compilation error when building with configure --disable-devmapper.
- Fix lvmconfig --type diff to display complete diff if config cascade used.
- Automatically filter out partitioned loop devices with partscan (losetup -P).
- Fix lvm devtypes internal error if -S used with field name from pvs/vgs/lvs.
- When reporting Data%%,Snap%%,Meta%%,Cpy%%Sync use single ioctl per LV.
- Add lvseg_percent_with_info_and_seg_status() for percent retrieval.
- Enhance internal seg_status handling to understand snapshots better.
- When refresh failed in suspend, call resume upon error path.
- Support passthrough cache mode when waiting for clean cache.
- Check cache status only for 'in-use' cache pools.
- Extend setup_task() to preset flushing for dm_task object.
- When checking LV is a merging COW, validate its a COW LV first.
- Correcting value in copy_percent() for 100%%.
- Update vgreduce to use process_each_vg.
- Update lvconvert to use process_each_lv.
- Update pvscan to use process_each_vg for autoactivation.
- Add basic support for --type raid0 using md.
- Add support for lvchange --cachemode for cached LV.
- Fix liblvm2app error handling when setting up context.
- Delay liblvm2app init in python code until it is needed.
- Simplify thread locking in lvmetad to fix locking problems.
- Allow pvremove -ff to remove a duplicate PV.
- Fix lvm2-activation-generator to read lvm.conf without full command setup.
- Allow a minimal context to be used in lvm2app for reading lvm.conf.
- Report passthrough caching mode when parsing cache mode.

* Mon May 16 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.154-1
- Fix liblvm segfault after failure initialising lvmetad connection.
- Retry open without O_NOATIME if it fails (not file owner/CAP_FOWNER).
- Split _report into one fn for options and arguments and one for processing.
- Show library version in message even if dm driver version is unavailable.

* Tue May 10 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.153-2
- Change warning messages related to duplicate PVs.
- A named device is always processed itself, not switched for a duplicate.
- Add PV attr "d" and report field "duplicate" for duplicate PVs.
- Add config setting to disallow VG changes when duplicate PVs exist.
- Use device size and active LVs to choose the preferred duplicate PV.
- Disable lvmetad when duplicate PVs are seen.
- Support --chunksize option also when caching LV when possible.
- Add function to check for target presence and version via 1 ioctl.

* Mon May 02 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.152-1
- Use any inherited tags when wiping metadata sub LVs to ensure activation.
- Add str_list_wipe.
- Improve support for interrupting procesing of volumes during lvchange.
- Use failed command return code when lvchanging read-only volume.
- Show creation transaction_id and zeroing state of pool with thin volume.
- Stop checking for dm_cache_mq policy with cache target 1.9 (alias to smq).
- Check first /sys/module/dm_* dir existance before using modprobe.
- Remove mpath from 10-dm.rules, superseded by 11-dm-mpath.rules (mpath>=0.6.0).
- Add dm_udev_wait_immediate to libdevmapper for waiting outside the library.

* Mon Apr 25 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.151-1
- Fix error path after reusing of _setup_task (2.02.150).
- Fix memory access for empty sysfs values (2.02.149).
- Disable lvmetad when lvm1 metadata is seen, so commands revert to scanning.
- Suppress errors when snapshot merge gets delayed because volume is in use.
- Avoid internal snapshot LV names in messages.
- Autodetect and use /run/lock dir when available instead of /var/lock.
- lvchange --refresh for merging thin origin will retry to deactivate snapshot.
- Recognize in-progress snapshot merge for thin volumes from dm table.
- Avoid deciding to initiate a pending snapshot merge during resume.
- Improve retrying lvmetad requests while lvmetad is being updated.
- Read devices instead of using the lvmetad cache if rescan fails.
- Move lvmetad token/filter check and device rescan to the start of commands.
- Don't try deactivating fictional internal LV before snapshot merge. (2.02.105)
- When not obtaining devs from udev, check they exist before caching them.
- Detect device mismatch also when compiling without udev support.
- Do not strip LVM- when debug reporting not found uuid.

* Mon Apr 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.150-1
- Avoid using flushing dm status ioctl when checking for usable DM device.
- Check for devices without LVM- uuid prefix only with kernels < 3.X.
- Reuse %%FREE size aproximation with lvcreate -l%%PVS thin-pool.
- Allow the lvmdump directory to exist already provided it is empty.
- Show lvconverted percentage with 2 decimal digits.
- Fix regression in suspend when repairing --type mirror (2.02.133).
- Change log_debug ioctl flags from single characters into words.

* Mon Apr 04 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.149-2
- Do not flush thin-pool when checking metadata fullness.
- Remove spurious error about no value in /sys/dev/block/major:minor/dm/uuid.
- Fix device mismatch detection for LV if persistent .cache file is used.
- Fix holder device not being found in /dev while sysfs has it during dev scan.

* Tue Mar 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.148-1
- Introduce TARGET_NAME and MODULE NAME macros.
- Replace hard-coded module and target names with macros.
- Add pv_major and pv_minor report fields.
- Detect and warn about mismatch between devices used and assumed for an LV.
- Adjust raid status function.

* Mon Mar 21 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.147-5
- If available, use /proc/self/mountinfo to detect mounted volume in fsadm.
- Fix resize of stacked raid thin data volume (2.02.141).
- Fix test for lvremove failure in lvconvert --uncache (2.02.146).

* Fri Mar 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.146-4
- More man page cleanups in lvconvert.
- Fix makefile vpath in /udev when generating udev rules files.
- Another attempt to improve VG name parsing for lvconvert (2.02.144).
- Use new cache status info and skip flushing for failed cache.
- Support --uncache with missing PVs.
- Improve parsing of cache status and report Fail, Error, needs_check, ro.

* Fri Mar 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.146-3
- Tidy report field names, headings and widths.
- Add vgscan --notifydbus to send a dbus notification.
- Add dbus notification from commands after a PV/VG/LV changes state.

* Wed Mar 09 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.145-2
- Require python3-gobject-base insetad of python3-gobject.

* Mon Mar 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.145-1
- Make it possible to use lvremove and lvrename on historical LVs.
- For historical LVs, report 'none' for lv_layout and 'history' for lv_role.
- Add full_{ancestors,descendants} fields to report LV ancestry with history.
- Report (h)istorical state within 5th bit (State) of the lv_attr field.
- Add lv_historical reporting field to report if LV is historical or not.
- Add lv_time_removed reporting field to display removal time for hist. LVs.
- Report lv_name, lv_uuid, vg_name, lv_time for historical LVs.
- Add --nohistory switch to lvremove to disable history recording on demand.
- Add -H|--history switch to lvs and lvdisplay to include historical LVs.
- Create historical LVs out of removed thin snapshot LVs and record in history.
- Add metadata/lvs_history_retention_time for automatic removal of hist. LVs.
- Add metadata/record_lvs_history config for switching LV history recording.
- Add support and infrastructure for tracking historical LVs.
- Improve lvconvert man page.
- Add kernel_cache_policy lvs field.
- Display [unknown] instead of 'unknown device' in pvs output.
- Fix error path when pvcreate allocation fails (2.02.144).
- Display [unknown] instead of blank for unknown VG names in pvs output.
- Fix dm_config_write_node and variants to return error on subsection failures.
- Remove 4096 char limit due to buffer size if writing dm_config_node.

* Mon Feb 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.144-1
- Only show (u)sed pv_attr char when PV is not (a)llocatable. (2.02.143)
- Update makefile to generate lcov output also for lvmpolld and lvmlockd.
- Fix SystemdService lvm2-lvmdbusd.service name.
- Improve support for env LVM_VG_NAME for reference VG name in lvconvert.
- Fix regression when lvresize accepted zero sizes. (2.02.141)
- Always warn user about PV in use even when pvremove uses --force --force.
- Use uninitialized pool header detection in all cases.
- Fix read error detection when checking for uninitialized thin-pool header.
- Fix error path for internal error in lvmetad VG lookup code.
- Fix string boundary check in _get_canonical_field_name().
- Always initialized hist struct in _stats_parse_histogram().

* Wed Feb 24 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-4
- Reinstate lvm2-lockd on all architectures as sanlock package is fixed now.

* Tue Feb 23 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-3
- Remove Requires: sanlock-lib for lvm2-lockd subpackage if sanlock not compiled.

* Tue Feb 23 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-2
- Add Requires: python3-gobject dependency for lvm2-dbusd subpackage.
- Build lvm2-lockd with sanlock support only on x86_64, arch64 and power64 arch.

* Mon Feb 22 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-1
- Introduce new lvm2-dbusd package providing LVM D-Bus daemon and service.
- Fix error path when sending thin-pool message fails in update_pool_lv().
- Support reporting CheckNeeded and Fail state for thin-pool and thin LV.
- For failing thin-pool and thin volume correctly report percentage as INVALID.
- Report -1, not 'unkown' for lv_{snapshot_invalid,merge_failed} with --binary.
- Add configure --enable-dbus-service for an LVM D-Bus service.
- Replace configure --enable-python_bindings with python2 and python3 versions.
- If PV belongs to some VG and metadata missing, skip it if system ID is used.
- Automatically change PV header extension to latest version if writing PV/VG.
- Identify used PVs in pv_attr field by new 'u' character.
- Add pv_in_use reporting field to report if PV is used or not.
- Add pv_ext_vsn reporting field to report PV header extension version.
- Add protective flag marking PVs as used even if no metadata available.
- Improve status parsing for thin-pool and thin devices.

* Mon Feb 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.142-1
- Fix memory pool corruption in pvmove (2.02.141).
- Support control of spare metadata creation when repairing thin-pool.
- Fix config type of 'log/verbose' from bool to int (2.02.99).
- Fix inverted data LV thinp watermark calc for dmeventd response (2.02.133).
- Use use_blkid_wiping=0 if not defined in lvm.conf and support not compiled in.
- Do not check for suspended devices if scanning for lvmetad update.
- Clear cached bootloader areas when PV format changed.
- Fix partn table filter with external_device_info_source="udev" and blkid<2.20.
- Use fully aligned allocations for dm_pool_strdup/strndup() (1.02.64).
- Fix thin-pool table parameter feature order to match kernel output.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.141-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.141-1
- Add metadata/check_pv_device_sizes switch to lvm.conf for device size checks.
- Warn if device size is less than corresponding PV size in metadata.
- Cache device sizes internally.
- Restore support for command breaking in process_each_lv_in_vg() (2.02.118).
- Use correct mempool when process_each_lv_in_vg() (2.02.118).
- Fix lvm.8 man to show again prohibited suffixes.
- Fix configure to set proper use_blkid_wiping if autodetected as disabled.
- Initialise udev in clvmd for use in device scanning. (2.02.116)
- Add seg_le_ranges report field for common format when displaying seg devices.
- Honour report/list_item_separator for seg_metadata_le_ranges report field.
- Don't mark hidden devs in -o devices,metadata_devices,seg_pe_ranges.(2.02.140)
- Change LV sizes in seg_pe_ranges report field to match underlying devices.
- Add kernel_cache_settings report field for cache LV settings used in kernel.
- Fix man page for dmsetup udevcreatecookie.

* Mon Jan 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.140-3
- Fix lvm2app to return either 0 or 1 for lvm_vg_is_{clustered,exported}.
- Add kernel_discards report field to display thin pool discard used in kernel.
- Correct checking of target presence when driver access is disabled.
- Eval poolmetadatasize arg earlier in lvresize.
- Fix vgcfgrestore to respect allocatable attribute of PVs.
- Add report/mark_hidden_devices to lvm.conf.
- Use brackets consistently in report fields to mark hidden devices.
- Restore background polling processing during auto-activation (2.02.119).
- Fix invalid memory read when reporting cache LV policy_name (2.02.126).

* Mon Jan 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.139-2
- Update lvmlockd with the new VG seqno before devices are suspended.
- Rework vgrename to use the common processing code in toollib.
- Make pvs show new devices on the system since the last .cache update.
- Document F,D and M thin pool health status chars for lv_attr in lvs man page.
- Also add lvm2-activation{-early,-net}.service systemd status for lvmdump -s.

* Mon Jan 04 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.138-1
- Support lvrename for hidden (used) cache pools.
- Fix lvrename for stacked cache pools
- Better support for dmsetup static linkage.
- Extend validity checks on dmeventd client socket.

* Mon Dec 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.137-1
- Restore archiving before changing metadata in vgextend (2.02.117).
- Dropped internal usage of log_suppress(2).
- Cleaned logging code for buffer size usage.
- Added internal id_read_format_try() function to check and read valid UUID.
- Change lvcreate, lvrename, lvresize to use process_each_vg.
- Change process_each_vg to handle single VG as separate arg.
- Issue error if ambiguous VG name is supplied in most commands.
- Make process_each fns always work through full list of known VG names.
- Use dm_get_status_mirror() instead of individual parsers.
- Add mem pool arg for check_transient_status() target function.
- Avoid misleading error with -m is omitted with lvconvert to raid types.
- Add system_id to vginfo cache.
- Mirror plugin in dmeventd uses dm_get_status_mirror().
- Add dm_get_status_mirror() for parsing mirror status line.

* Wed Dec 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.136-1
- Add new --sinceversion option for lvmconfig --type new.
- Fix inactive table loaded for wrapping thin-pool when resizing it.
- Extend the list of ignored libraries when locking memory.
- Show error message when trying to create unsupported raid type.
- Improve preloading sequence of an active thin-pool target.
- Drop extra space from cache target line to fix unneded table reloads.

* Mon Nov 23 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.135-1
- Add a model file for Coverity.
- Show correct error message for unsupported yet cache pool repair.
- Allow lvconvert cache pools' data and metadata LV to raid.
- Fix reading of old metadata with missing cache policy or mode settings.
- Issue error if external_device_info_source=udev and udev db record incomplete.
- Update lvmetad duplicate VG name handling to use hash function extensions.
- Detect invalid vgrenames by vgid where the name is unchanged.
- Fix passing of 32bit values through daemons (mostly lvmlockd).
- Use local memory pool for whole alloc_handle manipulation.
- Add missing pointer validation after dm_get_next_target().
- Do not deref NULL pointer in debug message for _match_pv_tags().
- Drop unneeded stat() call when checking for sysfs file.
- Fix memory leak on error path of failing thin-pool percentage check.
- Add missing test for failing node allocation in lvmetad.
- Correct configure messages when enabling/disabling lvmlockd.
- Extend dm_hash to support multiple values with the same key.
- Add missing check for allocation inside dm_split_lvm_name().
- Test dm_task_get_message_response for !NULL in dm_stats_print_region().
- Add checks for failing dm_stats_create() in dmsetup.
- Add missing fifo close when failed to initialize client connection.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-4
- Refactor some lvmetad code and adjust some duplicate PV messages.
- No longer repair/wipe VG/PVs if inaccessible because foreign or shared.
- Pass correct data size to mirror log calc so log can be bigger than 1 extent.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.133-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.133-2
- Shutdown lvmetad automatically after one hour of inactivity.

* Fri Oct 30 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.133-1
- Support repeated -o|--options for reporting commands.
- Support -o- and -o# for reporting commands to remove and compact fields.
- Fix missing PVs from pvs output if vgremove is run concurrently.
- Remove unwanted error message when running pvs/vgs/lvs and vgremove at once.
- Check newly created VG's metadata do not overlap in metadata ring buffer.
- Check metadata area size is at least the minimum size defined for the format.
- Thin pool targets uses low_water_mark from profile.
- Dropping 'yet' from error of unsupported thick snapshot of snapshots.
- Do not support unpartitioned DASD devices with CDL formatted with pvcreate.
- For thins use flush for suspend only when volume size is reduced.
- Enable code which detects the need of flush during suspend.
- Ensure --use-policy will resize volume to fit below threshold.
- Correct percentage evaluation when checking thin-pool over threshold.
- Fix lvmcache to move PV from VG to orphans if VG is removed and lvmetad used.
- Fix lvmcache to not cache even invalid info about PV which got removed.
- Support checking of memlock daemon counter.
- Allow all log levels to be used with the lvmetad -l option.
- Add optional shutdown when idle support for lvmetad.
- Fix missing in-sync progress info while lvconvert used with lvmpolld.
- Add report/compact_output_cols to lvm.conf to define report cols to compact.
- Do not change logging in lvm2 library when it's already set.
- Check for enough space in thin-pool in command before creating new thin.
- Make libblkid detect all copies of the same signature if use_blkid_wiping=1.
- Fix vgimportclone with -n to not add number unnecessarily to base VG name.
- Cleanup vgimportclone script and remove dependency on awk, grep, cut and tr.
- Add vg_missing_pv_count report field to report number of missing PVs in a VG.
- Properly identify internal LV holding sanlock locks within lv_role field.
- Add metadata_devices and seg_metadata_le_ranges report fields for raid vols.
- Fix lvm2-{activation,clvmd,cmirrord,monitor} service to exec before mounting.
- Disable thin monitoring plugin when it fails too often (>10 times).
- Fix/restore parsing of empty field '-' when processing dmeventd event.
- Enhance dm_tree_node_size_changed() to recognize size reduction.
- Support exit on idle for dmenventd (1 hour).
- Add support to allow unmonitor device from plugin itself.
- New design for thread co-operation in dmeventd.
- Dmeventd read device status with 'noflush'.
- Dmeventd closes control device when no device is monitored.
- Thin plugin for dmeventd improved percentage usage.
- Snapshot plugin for dmeventd improved percentage usage.
- Add dm_hold_control_dev to allow holding of control device open.
- Add dm_report_compact_given_fields to remove given empty fields from report.
- Use libdm status parsing and local mem raid dmeventd plugin.
- Use local mem pool and lock only lvm2 execution for mirror dmeventd plugin.
- Lock protect only lvm2 execution for snapshot and thin dmeventd plugin.
- Use local mempool for raid and mirror plugins.
- Reworked thread initialization for dmeventd plugins.
- Dmeventd handles snapshot overflow for now equally as invalid.
- Convert dmeventd to use common logging macro system from libdm.
- Return -ENOMEM when device registration fails instead of 0 (=success).
- Enforce writethrough mode for cleaner policy.
- Add support for recognition and deactivation of MD devices to blkdeactivate.
- Move target status functions out of libdm-deptree.
- Correct use of max_write_behind parameter when generating raid target line.
- Fix dm-event systemd service to make sure it is executed before mounting.

* Mon Oct 26 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.132-2
- Remove %%{epoch} from cmirror requires.

* Wed Sep 23 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.132-1
- Fix lvmconf to set locking_type=2 if external locking library is requested.
- Remove verbose message when rescanning an unchanged device. (2.02.119)
- Add origin_uuid, mirror_log_uuid, move_pv_uuid, convert_lv_uuid report fields.
- Add pool_lv_uuid, metadata_lv_uuid, data_lv_uuid reporting fields.
- Fix PV label processing failure after pvcreate in lvm shell with lvmetad.
- Update man pages for dmsetup and dmstats.
- Improve help text for dmsetup.
- Use --noflush and --nolockfs when removing device with --force.
- Parse new Overflow status string for snapshot target.
- Check dir path components are valid if using dm_create_dir, error out if not.
- Fix /dev/mapper handling to remove dangling entries if symlinks are found.
- Make it possible to use blank value as selection for string list report field.

* Wed Sep 16 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.131-1
- Fix PV label processing failure after pvcreate in lvm shell with lvmetad.
- Rename 'make install_full_man' to install_all_man and add all_man target.
- Fix vgimportclone cache_dir path name (2.02.115).
- Swapping of LV identifiers handles more complex LVs.
- Use passed list of PVS when allocating space in lvconvert --thinpool.
- Disallow usage of --stripe and --stripesize when creating cache pool.
- Warn user when caching raid or thin pool data LV.
- When layering LV, move LV flags with segments.
- Ignore persistent cache if configuration changed. (2.02.127)
- Fix devices/filter to be applied before disk-accessing filters. (2.02.112)
- Make tags only when requested via 'make tags'.
- Configure supports --disable-dependency-tracking for one-time builds.
- Fix usage of configure.h when building in srcdir != builddir.
- Do not check for full thin pool when activating without messages (1.02.107).

* Mon Sep 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.130-1
- Fix use of uninitialized device status if reading outdated .cache record.
- Restore support for --monitor option in lvcreate (2.02.112).
- Read thin-pool data and metadata percent without flush.
- Detect blocked thin-pool and avoid scanning their thin volumes.
- Check if dm device is usable before checking its size (2.02.116).
- Extend parsing of cache_check version in configure.
- Make lvpoll error messages visible in lvmpolld's stderr and in syslog.
- Add 'make install_full_man' to install all man pages regardless of config.
- Parse thin-pool status with one single routine internally.
- Add --histogram to select default histogram fields for list and report.
- Add report fields for displaying latency histogram configuration and data.
- Add dmstats --bounds to specify histogram boundaries for a new region.
- Add dm_histogram_to_string() to format histogram data in string form.
- Add public methods to libdm to access numerical histogram config and data.
- Parse and store histogram data in dm_stats_list() and dm_stats_populate().
- Add an argument to specify histogram bounds to dm_stats_create_region().
- Add dm_histogram_bounds_from_{string,uint64_t}() to parse histogram bounds.
- Add dm_histogram handle type to represent a latency histogram and its bounds.

* Wed Sep 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.129-2
- Reinstate dm_task_get_info@Base to libdevmapper exports. (1.02.106)

* Thu Aug 27 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.129-1
- Drop error message when vgdisplay encounters an exported VG. (2.02.27)
- Fix shared library generation to stop exporting internal functions.(2.02.120)
- Accept --cachemode with lvconvert.
- Fix and improve reporting properties of cache-pool.
- Enable usage of --cachepolicy and --cachesetting with lvconvert.
- Don't allow to reduce size of thin-pool metadata.
- Fix debug buffer overflows in cmirrord logging.
- Add --foreground and --help to cmirrord.
- Add 'precise' column to statistics reports.
- Add --precise switch to 'dmstats create' to request nanosecond counters.
- Add precise argument to dm_stats_create_region().
- Add support to libdm-stats for precise_timestamps
- Fix devmapper.pc pkgconfig file to declare -lrt dependency properly.

* Tue Aug 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.128-1
- Allocation setting cache_pool_cachemode is replaced by cache_mode.
- Don't attempt to close config file that couldn't be opened.
- Check for valid cache mode in validation of cache segment.
- Change internal interface handling cache mode and policy.
- When no cache policy specified, prefer smq (if available) over mq.
- Add demo cache-mq and cache-smq profiles.
- Add cmd profilable allocation/cache_policy,cache_settings,cache_mode.
- Require cache_check 0.5.4 for use of --clear-needs-check-flag.
- Fix lvmetad udev rules to not override SYSTEMD_WANTS, add the service instead.
- Fix 'dmstats list -o all' segfault.
- Separate dmstats statistics fields from region information fields.
- Add interval and interval_ns fields to dmstats reports.
- Do not include internal glibc headers in libdm-timestamp.c (1.02.104)
- Exit immediately if no device is supplied to dmsetup wipe_table.
- Suppress dmsetup report headings when no data is output. (1.02.104)
- Adjust dmsetup usage/help output selection to match command invoked.
- Fix dmsetup -o all to select correct fields in splitname report.
- Restructure internal dmsetup argument handling across all commands.
- Add dm_report_is_empty() to indicate there is no data awaiting output.
- Add more arg validation for dm_tree_node_add_cache_target().
- Add --alldevices switch to replace use of --force for stats create / delete.

* Mon Aug 10 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.127-1
- Do not init filters, locking, lvmetad, lvmpolld if command doesn't use it.
- Order fields in struct cmd_context more logically.
- Add lock_type to lvmcache VG summary and info structs.
- Fix regression in cache causing some PVs to bypass filters (2.02.105).
- Make configure --enable-realtime the default now. 
- Add dmstats.8 man page
- Add dmstats --segments switch to create one region per device segment.
- Add dmstats --regionid, --allregions to specify a single / all stats regions.
- Add dmstats --allprograms for stats commands that filter by program ID.
- Add dmstats --auxdata and --programid args to specify aux data and program ID.
- Add report stats sub-command to provide repeating stats reports.
- Add clear, delete, list, and print stats sub-commands.
- Add create stats sub-command and --start, --length, --areas and --areasize.
- Recognize 'dmstats' as an alias for 'dmsetup stats' when run with this name.
- Add a 'stats' command to dmsetup to configure, manage and report stats data.
- Add statistics fields to dmsetup -o.
- Add libdm-stats library to allow management of device-mapper statistics.
- Add --nosuffix to suppress dmsetup unit suffixes in report output.
- Add --units to control dmsetup report field output units.
- Add support to redisplay column headings for repeating column reports.
- Fix report header and row resource leaks.
- Report timestamps of ioctls with dmsetup -vvv.
- Recognize report field name variants without any underscores too.
- Add dmsetup --interval and --count to repeat reports at specified intervals.
- Add dm_timestamp functions to libdevmapper.
- Recognise vg/lv name format in dmsetup.
- Move size display code to libdevmapper as dm_size_to_string.

* Mon Jul 27 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.126-2
- Fix long option hyphen removal. (2.02.122)
- Fix clvmd freeze if client disappears without first releasing its locks.
- Fix lvconvert segfaults while performing snapshots merge.
- Ignore errors during detection if use_blkid_wiping=1 and --force is used.
- Recognise DM_ABORT_ON_INTERNAL_ERRORS env var override in lvm logging fn.
- Fix alloc segfault when extending LV with fewer stripes than in first seg.
- Fix handling of cache policy name.
- Set cache policy before with the first lvm2 cache pool metadata commit.
- Fix detection of thin-pool overprovisioning (2.02.124).
- Fix lvmpolld segfaults on 32 bit architectures.
- Add lvmlockd lock_args validation to vg_validate.
- Fix ignored --startstopservices option if running lvmconf with systemd.
- Hide sanlock LVs when processing LVs in VG unless named or --all used.
- Introduce libdevmapper wrappers for all malloc-related functions.

* Tue Jul 14 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.125-2
- Add Requires: system-release>=23 for lvmpolld to be enabled by default
  instead of original Requires: fedora-release which may break installations
  in environments where fedora-release is not available.

* Tue Jul 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.125-1
- Fix getline memory usage in lvmpolld.
- Add support --clear-needs-check-flag for cache_check of cache pool metadata.
- Add lvmetactl for developer use only.
- Rename global/lock_retries to lvmlockd_retries.
- Replace --enable-lvmlockd by --enable-lockd-sanlock and --enable-lockd-dlm.
- Include tool.h for default non-library use.
- Introduce format macros with embedded % such as FMTu64.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.124-1
- Move sending thin pool messages from resume to suspend phase.
- Report warning when pool is overprovisioned and not auto resized.
- Recognize free-form date/time values for lv_time field in selection criteria.
- Added experimental lvmlockd with configure --enable-lvmlockd.
- Fix regression in select to match string fields if using synonyms (2.02.123).
- Fix regression when printing more lv names via display_lvname (2.02.122).
- Add missing error logging to unlock_vg and sync_local_dev_names callers.
- Add experimental support to passing messages in suspend tree.
- Add dm_report_value_cache_{set,get} to support caching during report/select.
- Add dm_report_reserved_handler to handle report reserved value actions.
- Support dynamic value in select: DM_REPORT_FIELD_RESERVED_VALUE_DYNAMIC_VALUE.
- Support fuzzy names in select: DM_REPORT_FIELD_RESERVED_VALUE_FUZZY_NAMES.
- Thin pool trace messages show a device name and major:minor.
- Add new lvm2-lockd subpackage with lvmlockd daemon.

* Wed Jul 01 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.123-1
- Add report/time_format lvm.conf option to define time format for report.
- Fix makefile shell compare == when building lvmetad lvmpolld (2.02.120).
- Add --type full to lvmconfig for full configuration tree view.
- Add undocumented environment variables to lvm man page. (2.02.119)
- Add device synchronization point before activating a new snapshot.
- Add --withspaces to lvmconfig to add spaces in output for better readability.
- Add custom main function to libdaemon.
- Use lvmetad to track out-of-date metadata discovered.
- Fix makefile shell compare == when building lvmetad lvmpolld (2.02.120).
- Add --type full to lvmconfig for full configuration tree view.
- Add undocumented environment variables to lvm man page. (2.02.119)
- Add device synchronization point before activating a new snapshot.
- Add --withspaces to lvmconfig to add spaces in output for better readability.
- Add custom main function to libdaemon.
- Use lvmetad to track out-of-date metadata discovered.
- Add since, after, until and before time operators to be used in selection.
- Add support for time in reports and selection: DM_REPORT_FIELD_TYPE_TIME.
- Support report reserved value ranges: DM_REPORT_FIELD_RESERVED_VALUE_RANGE.
- Support report reserved value names: DM_REPORT_FIELD_RESERVED_VALUE_NAMED.
- Add DM_CONFIG_VALUE_FMT_{INT_OCTAL,STRING_NO_QUOTES} config value format flag.
- Add DM_CONFIG_VALUE_FMT_COMMON_{ARRAY,EXTRA_SPACE} config value format flag.
- Add dm_config_value_{get,set}_format_flags to get and set config value format.

* Mon Jun 22 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.122-1
- Flush stdout before printing to stderr.
- Use pre-allocated buffer for printed LV names in display_lvname.
- Support thins with size of external origin unaligned with thin pool chunk.
- Allow extension of reduced thin volumes with external origins.
- Consider snapshot and origin LV as unusable if component devices suspended.
- Fix lvmconfig segfault on settings with undefined default value (2.02.120).
- Add explicit 's' (shared) LV activation mode.
- Ignore hyphens in long options names (i.e. --long-option == --longoption).
- Distinguish between on-disk and lvmetad versions of text metadata.
- Remove DL_LIBS from Makefiles for daemons that don't need them.
- Zero errno in before strtoul call in dmsetup if tested after the call.
- Zero errno in before strtoul call in lvmpolld.
- Fix a segfault in pvscan --cache --background command.
- Fix test for AREA_PV when checking for failed mirrors.
- Do not use --sysinit in lvm2-activation{-early,-net}.service if lvmpolld used.
- Maintain outdated PV info in lvmetad till all old metadata is gone from disk.
- Do not fail polling when poll LV not found (already finished or removed).
- Replace poll_get_copy_vg/lv fns with vg_read() and find_lv() in polldaemon.
- Close all device fds only in before sleep call in polldaemon.
- Simplify Makefile targets that generate exported symbols.
- Move various -D settings from Makefiles to configure.h.
- New dm_tree_node_set_thin_pool_read_only(DM_1_02_99) for read-only thin pool.
- Enhance error message when thin-pool message fails.
- Fix dmeventd logging to avoid threaded use of static variable.
- Remove redundant dmeventd SIGALRM coded.
- Add dm_task_get_errno() to return any unexpected errno from a dm ioctl call.
- Use copy of errno made after each dm ioctl call in case errno changes later.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.120-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.120-1
- Enable and use lvmpolld - the LVM polling daemon by default.
- Add Requires: fedora-release>=23-0.13 for lvmpolld to be enabled by default.
- Make various adjustments to Makefile compilation flags.
- Add lvmpolld debug message class.
- Add lvmpolld client mode for querying running server instance for status info.
- Fix some libdaemon socket creation and reuse error paths.
- Daemons (libdaemon) support exit on idle also in non-systemd environment.
- Provide make dist and make rpm targets
- Configure lvm.conf for use_lvmetad and use_lvmpolld.
- Add lvpoll for cmdline communication with lvmpolld.
- Add lvmpolld acting as a free-standing version of polldaemon.
- Avoid repeated identical lvmetad VG lookups in commands processing all VGs. 
- Handle switches to alternative duplicate PVs efficiently with lvmetad.
- Properly validate PV size for pvcreate --restorefile.
- Fix check if pvcreate wiped device (2.02.117).
- Fix storing of vgid when caching metadata (2.02.118).
- Fix recursive lvm-config man page. (2.02.119)
- Refactor polldaemon interfaces to poll every operation by VG/LV couple
- Skip wait after testing in _wait_for_single_lv when polling finished
- Return 'None' in python for empty string properties instead of crashing.
- Distinguish signed numerical property type in reports for lvm2app library.
- Reread raid completion status immediately when progress appears to be zero.
- lvm2app closes locking on lvm_quit().
- Configure detects /run or /var/run.
- Add missing newline in clvmd --help output.
- New dm_task_get_info(DM_1_02_97) supports internal_suspend state.
- New symbols are versioned and comes with versioned symbol name (DM_1_02_97).

* Mon May 04 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.119-1
- New lvm2-python3-libs subpackage to provide Python 3 bindings for LVM2.
- New LVM_LOG_FILE_EPOCH, LVM_EXPECTED_EXIT_STATUS env vars. Man page to follow.
- Remove detailed content from lvm.conf man page: use lvmconfig instead.
- Generate complete config files with lvmconfig or 'make generate'.
- Also display info on deprecated config with lvmconfig --withcomments.
- Display version since which config is deprecated in lvmconfig --withversions.
- Add --showdeprecated to lvmconfig to also display deprecated settings.
- Hide deprecated settings in lvmconfig output for all types but current,diff.
- Introduce support for exit on idle feature in libdaemon
- Add --showunsupported to lvmconfig to also display unsupported settings.
- Display unsupported settings for lvmconfig --type current,diff only by default
- Honour lvmconfig --ignoreunsupported and --ignoreadvanced for all --type.
- Make python bindings usable with python3 (and compatible with 2.6 & 2.7).
- Add lvmconfig -l|--list as shortcut for lvmconfig --type list --withsummary.
- Add lvmconfig --type list to display plain list of configuration settings.
- Introduce lvmconfig as the preferred form of 'lvm dumpconfig'.
- Add lv_ancestors and lv_descendants reporting fields.
- Add --ignorelocal option to dumpconfig to ignore the local section.
- Close connection to lvmetad after fork.
- Make lvchange able to resume background pvmove polling again.
- Split pvmove update metadata fn in an initial one and a subsequent one.
- Refactor shared pvmove and lvconvert code into new _poll files.
- Add --unconfigured option to dumpconfig to print strings unconfigured.
- Add --withsummary option to dumpconfig to print first line - summary comment.
- Use number of device holders to help choose between duplicate PVs.
- Try to make lvmetad and non-lvmetad duplicate PV handling as similar as poss.
- Issue warnings about duplicate PVs discovered by lvmetad.
- Track alternative devices with matching PVIDs in lvmetad.
- Check for lvm binary in blkdeactivate and skip LVM processing if not present.
- Add --enable-halvm and --disable-halvm options to lvmconf script.
- Add --services, --mirrorservice and --startstopservices option to lvmconf.
- Use proper default value of global/use_lvmetad when processing lvmconf script.
- Respect allocation/cling_tag_list during intial contiguous allocation.
- Make changes persist with python addTag/removeTag.
- Set correct vgid when updating cache when writing PV metadata.
- More efficient clvmd singlenode locking emulation.
- Reject lvcreate -m with raid4/5/6 to avoid unexpected layout.
- Don't skip invalidation of cached orphans if vg write lck is held (2.02.118).
- Log relevant PV tags when using cling allocation.
- Fix selection to not match if using reserved value in criteria with >,<,>=,<.
- Fix selection to not match reserved values for size fields if using >,<,>=,<.
- Include uuid or device number in log message after ioctl failure.
- Add DM_INTERNAL_SUSPEND_FLAG to dm-ioctl.h.
- Move blkdeactivate script from lvm2 package to device-mapper subpackage.
- Install blkdeactivate script and its man page with make install_device-mapper.

* Tue Mar 24 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.118-1
- Fix LV processing with selection to always do the selection on initial state.
- Store metadata size + checksum in lvmcache and add struct lvmcache_vgsummary.
- Remove inaccessible clustered PVs from 'pvs -a'.
- Don't invalidate cached orphan information while global lock is held.
- Avoid rescan of all devices when requested pvscan for removed device.
- Measure configuration timestamps with nanoseconds when available.
- Disable lvchange of major and minor of pool LVs.
- Fix pvscan --cache to not scan and read ignored metadata areas on PVs.
- Add After=iscsi-shutdown.service to blk-availability.service systemd unit.
- Disallow vgconvert from changing metadata format when lvmetad is used.
- Don't do a full read of VG when creating a new VG with an existing name.
- Reduce amount of VG metadata parsing when looking for vgname on a PV.
- Avoid reparsing same metadata when reading same metadata from multiple PVs.
- Save extra device open/close when scanning device for size.
- Fix seg_monitor field to report status also for mirrors and thick snapshots.
- Replace LVM_WRITE with LVM_WRITE_LOCKED flags in metadata if system ID is set.
- Preserve original format type field when processing backup files.
- Implement status action for lvm2-monitor initscript to display monitored LVs.
- Allow lvchange -p to change kernel state only if metadata state differs.
- Fix incorrect persistent .cache after report with label fields only (2.02.106).
- Reinstate PV tag recognition for pvs if reporting label fields only (2.02.105).
- Rescan devices before vgimport with lvmetad so exported VG is seen.
- Fix hang by adjusting cluster mirror regionsize, avoiding CPG msg limit.
- Do not crash when --cachepolicy is given without --cachesettings.
- Add NEEDS_FOREIGN_VGS flag to vgimport so --foreign is always supplied.
- Add --foreign to the 6 display and reporting tools and vgcfgbackup.
- Install /etc/lvm/lvmlocal.conf template with local section for systemid.
- Record creation_host_system_id in lvm2 metadata (never set yet).
- Reinstate recursive config file tag section processing. (2.02.99)
- Add 'lvm systemid' to display the current system ID (never set yet).
- Fix configure to properly recognize --with-default-raid10-segtype option.
- Do not refresh filters/rescan if no signature is wiped during pvcreate.
- Enforce none external dev info for wiping during pvcreate to avoid races.
- Add global/system_id_source and system_id_file to lvm.conf (disabled).
- Add support for VG system_id to control host access to VGs.
- Update vgextend to use process_each_vg.
- Add --ignoreskippedcluster to pvchange.
- Allow pvchange to modify several properties at once.
- Update pvchange to use process_each_pv.
- Fix pvs -a used with lvmetad to filter out devices unsuitable for PVs.
- Fix selection to recognize units for ba_start, vg_free and seg_start fields.
- Add support for -S/--select to vgexport and vgimport.
- Add support for -S/--select to vgdisplay, lvdisplay and pvdisplay without -C.
- Add support for -S/--select to vgremove and lvremove.
- Add support for -S/--select to vgchange,lvchange and pvchange.
- Add infrastructure to support selection for non-reporting tools.
- Add LVM_COMMAND_PROFILE env var to set default command profile name to use.
- Set CLOEXEC flag on file descriptors originating in libdaemon.
- Add dm_report_object_is_selected for generalized interface for report/select.

* Fri Jan 30 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.116-3
- Deactivate unused thin pools activated with lvm2 pre-2.02.112 versions.
- Check lock holding LV when lvconverting stacked raid LV in cluster.
- Support udev external dev info for filters: PV min size, mpath, md, partition.
- Add fw_raid_component_detection lvm.conf option to enable FW raid detection.
- Add devices/external_device_info_source lvm.conf option ("none" by default).
- Scan pools in for_each_sub_lv() and add for_each_sub_lv_except_pools().
- Fix lvm2app lvm_lv_get_property return value for fields with info/status ioctl.
- Fix lvm2app regression in lvm_lv_get_attr causing unknown values (2.02.115).
- Preserve chunk size with repair and metadata swap of a thin pool.
- Fix raid --splitmirror 1 functionality (2.02.112).
- Fix tree preload to handle splitting raid images.
- Do not support unpartitioned DASD devices.
- Improve config validation to check if setting with string value can be empty.

* Thu Jan 29 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.115-2
- Set default cache_mode to writehrough when missing in metadata.
- Add BuildRequires: device-mapper-persistent-data
  for proper thin and cache tool configuration.

* Thu Jan 22 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.115-1
- Report segment types without monitoring support as undefined.
- Support lvchange --errorwhenfull for thin pools.
- Improve the processing and reporting of duplicate PVs.
- Report lv_health_status and health attribute also for thin pool.
- Add lv_when_full reporting field.
- Add support for lvcreate --errorwhenfull y|n for thin pools.
- Fix lvconvert --repair to honour resilience requirement for segmented RAID LV.
- Filter out partitioned device-mapper devices as unsuitable for use as PVs.
- Also notify lvmetad about filtered device if using pvscan --cache DevicePath.
- Use LVM's own selection instead of awk expressions in clvmd startup scripts.
- Do not filter out snapshot origin LVs as unusable devices for an LVM stack.
- Fix incorrect rimage names when converting from mirror to raid1 LV (2.02.112).
- Introduce pvremove_many to avoid excessive metadata re-reading and messages.
- Check for cmirror availability during cluster mirror creation and activation.
- Add cache_policy and cache_settings reporting fields.
- Add missing recognition for --binary option with {pv,vg,lv}display -C.
- Fix vgimportclone to notify lvmetad about changes done if lvmetad is used.
- Fix vgimportclone to properly override config if it is missing in lvm.conf.
- Fix automatic use of configure --enable-udev-systemd-background-jobs.
- Correctly rename active split LV with -splitmirrors for raid1.
- Add report/compact_output to lvm.conf to enable/disable compact report output.
- Still restrict mirror region size to power of 2 when VG extent size is not.
- Reduce severity of ioctl error message when dmeventd waitevent is interrupted.
- Report 'unknown version' when incompatible version numbers were not obtained.
- Report more info from thin pool status (out of data, metadata-ro, fail).
- Support error_if_no_space for thin pool target.
- Fix segfault while using selection with regex and unbuffered reporting.
- Add dm_report_compact_fields to remove empty fields from report output.
- Remove unimplemented dm_report_set_output_selection from libdevmapper.h.

* Fri Nov 28 2014 Alasdair Kergon <agk@redhat.com> - 2.02.114-3
- Avoid file descriptor leak in clients that open repeated lvmetad connections.
- Add --cachepolicy and --cachesettings to lvcreate.
- Fix regression when parsing /dev/mapper dir (2.02.112).
- Fix missing rounding to 64KB when estimating optimal thin pool chunk size.
- Fix typo in clvmd initscript causing CLVMD_STOP_TIMEOUT var to be ignored.
- Fix size in pvresize "Resizing to ..." verbose msg to show proper result size.

* Thu Nov 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.113-2
- Fix regression when parsing /dev/mapper dir (2.02.112).
- Fix missing rounding to 64KB when estimating optimal thin pool chunk size.
- Fix typo in clvmd initscript causing CLVMD_STOP_TIMEOUT variable to be ignored.
- Fix size in pvresize "Resizing to ..." verbose msg to show proper result size.

* Tue Nov 25 2014 Alasdair Kergon <agk@redhat.com> - 2.02.113-1
- Add --cachepolicy and --cachesettings options to lvchange.
- Validate that converted volume and specified pool volume differ in lvconvert.
- Fix regression in vgscan --mknodes usage (2.02.112).
- Default to configure --enable-udev-systemd-background-jobs for systemd>=205.
- Fix ignore_vg() to properly react on various vg_read errors (2.02.112).
- Failed recovery returns FAILED_RECOVERY status flag for vg_read().
- Exit with non-zero status code when pvck encounters a problem.
- Fix clean_tree after activation/resume for cache target (2.02.112).
- Fix memory corruption with sorting empty string lists (1.02.86).
- Fix man dmsetup.8 syntax warning of groff.
- Accept unquoted strings and / in place of {} when parsing configs.

* Tue Nov 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.112-1
- Add cache_{read,write}_{hits,misses} reporting fields.
- Add cache_{total,used,dirty}_blocks reporting fields.
- Add _corig as reserved suffix.
- Reduce number of VG writes and commits when creating spare volumes.
- When remove_layer_from_lv() removes layer, restore subLV names.
- Cache-pool in use becomes invisible LV.
- Don't prompt for removal of _pmspare in VG without pool metadata LV.
- Deactivation of snapshot origin detects and deactivates left-over snapshots.
- Properly report error when taking snapshot of any cache type LV.
- Add basic thread debugging messages to dmeventd.
- Include threads being shutdown in dmeventd device registration responses.
- Inital support for external users of thin pools based on transaction_id.
- Report some basic percentage info for cache pools.
- Introduce size_mb_arg_with_percent() for advanced size arg reading.
- Add extra support for '.' as decimal point in size args.
- Add configure parameters for default segment type choices.
- Add global/sparse_segtype_default setting to use thin for --type sparse.
- Update and correct lvcreate and lvcovert man pages.
- Mark pools and snapshots as unzeroable volumes.
- Check for zeroing of volume after segment type is fully detected.
- Better support for persistent major and minor options with lvcreate.
- Refactor lvcreate towards more complete validation of all supported options.
- Support lvcreate --type linear.
- Improve _should_wipe_lv() to warn with message.
- Inform about temporarily created volumes only in verbose mode.
- Better support for --test mode with pool creation.
- Query lock holding LV when replacing and converting raid volumes.
- Add extra validate for locked lv within validate_lv_cache_create().
- Add internal lvseg_name() function.
- Skip use of lock files for virtual internal VG names.
- Fix selection on {vg,lv}_permissions fields to properly match selection criteria.
- Fix lv_permissions reporting to display read-only{-override} instead of blank.
- Fix liblvm2cmd and lvm shell to respect quotes around args in cmd line string.
- Permit extent sizes > 128KB that are not power of 2 with lvm2 format.
- Remove workaround for lvm2-monitor.service hang on stop if lvmetad stopped.
- Change vgremove to use process_each_lv_in_vg.
- Allow lvconvert --repair and --splitmirrors on internal LVs.
- Introduce WARN_ flags to control some metadata warning messages.
- Use process_each_pv in vgreduce.
- Refactor process_each_pv in toollib.
- Introduce single validation routine for pool chunk size.
- Support --yes like --force in vg/lvremove to skip y|n prompt.
- Support --yes with lvconvert --splitsnapshot.
- Fix detection of unsupported thin external lvconversions.
- Fix detection of unsupported cache and thin pool lvconversions.
- Fix detection of unsupported lvconversion of cache to snapshot.
- Improve code for creation of cache and cache pool volumes.
- Check cluster-wide (not local) active status before removing LV.
- Properly check if activation of removed cached LV really activated.
- lvremove cached LV removes cachepool (keep with lvconvert --splitcache).
- Always remove spare LV with last removed pool volume.
- Support lvconvert --splitcache and --uncache of cached LV.
- Option --cache has also shortcut -H (i.e. lvcreate -H).
- Refactor lvcreate code and better preserve --type argument.
- Refactor filter processing around lvmetad.
- Refactor process_each_lv in toollib.
- Refactor process_each_vg in toollib.
- Pools cannot be used as external origin.
- Use lv_update_and_reload() for snapshot reload.
- Don't print message in adjusted_mirror_region_size() in activation.
- Improve lv_update_and_reload() to find out proper lock holding LV.
- Improve search of LV in lv_ondisk().
- Do not scan sysfs in lv_check_not_in_use() when device is closed.
- Backup final metadata after resync of mirror/raid.
- Unify handling of --persistent option for lvcreate and lvchange.
- Validate major and minor numbers stored in metadata.
- Use -fPIE when linking -pie executables.
- Support DEBUG_MEMLOCK to trap unsupported mmap usage.
- Enable cache segment type by default.
- Ensure only supported volume types are used with cache segments.
- Fix inablility to specify cachemode when 'lvconvert'ing to cache-pool.
- Grab cluster lock for active LVs when setting clustered attribute.
- Use va_copy to properly pass va_list through functions.
- Add function to detect rotational devices.
- Review internal checks for mirror/raid/pvmove volumes.
- Track mirror segment type with separate MIRROR flag.
- Fix cmirror endian conversions.
- Introduce lv_is_pvmove/locked/converting/merging macros.
- Avoid leaving linear logical volume when thin pool creation fails.
- Don't leak alloc_handle on raid target error path.
- Properly validate raid leg names.
- Archive metadata before starting their modification in raid target.
- Add missing vg_revert() in suspend_lv() raid and snapshot error path.
- Add missing backup of lvm2 metadata after some raid modifications.
- Use vg memory pool for extent allocation.
- Add allocation/physical_extent_size config option for default PE size of VGs.
- Demote an error to a warning when devices known to lvmetad are filtered out.
- Re-order filter evaluation, making component filters global.
- Fix logic that checks for full scan before iterating through devices.
- Introduce common code to modify metadata and reload updated LV.
- Fix rename of active snapshot volume in cluster.
- Make sure shared libraries are built with RELRO option.
- Update cache creation and dm_config_node to pass policy.
- Allow activation of any thin-pool if transaction_id supplied is 0.
- Don't print uninitialized stack bytes when non-root uses dm_check_version().
- Fix selection criteria to not match reserved values when using >, <, >=, <.
- Add DM_LIST_HEAD_INIT macro to libdevmapper.h.
- Fix dm_is_dm_major to not issue error about missing /proc lines for dm module.

* Mon Sep 01 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.111-1
- Pass properly sized char buffers for sscanf when initializing clvmd.
- Reinstate nosync logic when extending mirror. (2.02.110)
- Fix total area extent calculation when allocating cache pool. (2.02.110)
- Restore proper buffer size for parsing mountinfo line (1.02.89)

* Wed Aug 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.110-1
- Fix manipulation with thin-pools which are excluded via volume_list.
- Support lv/vgremove -ff to remove thin vols from broken/inactive thin pools.
- Fix typo breaking configure --with-lvm1=shared.
- Modify lvresize code to handle raid/mirrors and physical extents.
- Don't allow pvcreate to proceed if scanning or filtering fails.
- Cleanly error when creating RAID with stripe size < PAGE_SIZE.
- Print name of LV which on activation triggers delayed snapshot merge.
- Add lv_layout and lv_role LV reporting fields.
- Properly display lvs lv_attr volume type and target type bit for cache origin.
- Fix pvcreate_check() to update cache correctly after signature wiping.
- Fix primary device lookup failure for partition when processing mpath filter.
- If LV inactive and non-clustered, do not issue "Cannot deactivate" on -aln.
- Remove spurious "Skipping mirror LV" message on pvmove of clustered mirror.
- Improve libdevmapper-event select() error handling.
- Add extra check for matching transation_id after message submitting.
- Add dm_report_field_string_list_unsorted for str. list report without sorting.
- Support --deferred with dmsetup remove to defer removal of open devices.
- Update dm-ioctl.h to include DM_DEFERRED_REMOVE flag.
- Add support for selection to match string list subset, recognize { } operator.
- Fix string list selection with '[value]' to not match list that's superset.
- Fix string list selection to match whole words only, not prefixes.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.109-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 5 2014 Alasdair Kergon <agk@redhat.com> - 2.02.109-1
- Allow approximate allocation with +%%FREE in lvextend.
- Fix a segfault in lvscan --cache when devices were already missing. (2.02.108)
- Display actual size changed when resizing LV.
- Remove possible spurious "not found" message on PV create before wiping.
- Handle upgrade from 2.02.105 when an LV now gaining a uuid suffix is active.
- Remove lv_volume_type field from reports. (2.02.108)
- Fix incorrect persistent .cache after vgcreate with PV creation. (2.02.108)
- Add dm_tree_set_optional_uuid_suffixes to libdevmapper to handle upgrades.

* Wed Jul 23 2014 Alasdair Kergon <agk@redhat.com> - 2.02.108-1
- Remove an erroneous duplicate const from libdevmapper.h. (2.02.107)
- Add lvscan --cache which re-scans constituents of a particular LV.
- Make dmeventd's RAID plugin re-scan failed PVs when lvmetad is in use.
- Improve code sharing for lvconvert and lvcreate and pools (cache & thin).
- Improve lvconvert --merge validation.
- Improve lvconvert --splitsnapshot validation.
- Add report/list_item_separator lvm.conf option.
- Add lv_active_{locally,remotely,exclusively} LV reporting fields.
- Enhance lvconvert thin, thinpool, cache and cachepool command line support.
- Display 'C' only for cache and cache-pool target types in lvs.
- Prompt for confirmation before change LV into a snapshot exception store.
- Return proper error codes for some failing lvconvert funtions.
- Add initial code to use cache tools (cache_check|dump|repair|restore).
- Support lvdisplay --maps for raid.
- Add --activationmode degraded to activate degraded raid volumes by default.
- Add separate lv_active_{locally,remotely,exclusively} LV reporting fields.
- Recognize "auto"/"unmanaged" values in selection for appropriate fields only.
- Add report/binary_values_as_numeric lvm.conf option for binary values as 0/1.
- Add --binary arg to pvs,vgs,lvs and {pv,vg,lv}display -C for 0/1 on reports.
- Add separate reporting fields for each each {pv,vg,lv}_attr bit.
- Separate LV device status reporting fields out of LV fields.
- Fix regression causing PVs not in VGs to be marked as allocatable (2.02.59).
- Fix VG component of lvid in vgsplit/vgmerge and check in vg_validate.
- Add lv_full_name, lv_parent and lv_dm_path fields to reports.
- Change lv_path field to suppress devices that never appear in /dev/vg.
- Postpone thin pool lvconvert prompts (2.02.107).
- Require --yes option to skip prompt to lvconvert thin pool chunksize.
- Support lvremove -ff to remove thin volumes from broken thin pools.
- Require --yes to skip raid repair prompt.
- Change makefile %%.d generation to handle filename changes without make clean.
- Fix use of buildir in make pofile.
- Enhance private volumes UUIDs with suffixed for easier detection.
- Do not use reserved _[tc]meta volumes for temporary LVs.
- Leave backup pool metadata with _meta%%d suffix instead of reserved _tmeta%%d.
- Allow RAID repair to reuse PVs from same image that suffered a failure.
- New RAID images now avoid allocation on any PVs in the same parent RAID LV.
- Always reevaluate filters just before creating PV.
- Fix dm_report_field_string_list to handle delimiter with multiple chars.
- Add dm_report_field_reserved_value for per-field reserved value definition.

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.02.107-2
- fix license handling

* Tue Jun 24 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.107-1
- Add cmirror-standalone subpackage containing new lvm2-cmirrord.service
  systemd unit for standalone cmirrord daemon management without cluster
  resource manager involvement.
- Add lvm2-cluster-standalone subpackage containing new lvm2-clvmd.service
  and lvm2-cluster-activation.service systemd unit for standalone clvmd
  daemon management without cluster resource manager involvement.
- Add Requires: resource-agents for lvm2-cluster and cmirror subpackages.
  The resource-agents package provides "clvm" cluster resource to manage
  clvmd and cmirrord instances. This replaces obsolete clvmd and cmirrord
  initscripts.
- Introduce LCK_ACTIVATION to avoid concurrent activation of basic LV types.
- Fix open_count test for lvchange --refresh or mirrors and raids.
- Update pvs,vgs,lvs and lvm man page for selection support.
- Add -S/--select to lvm devtypes for report selection.
- Add -S/--select to pvs,vgs,lvs and {pv,vg,lv}display -C for report selection.
- Use dm_report_init_with_selection now, implicit "selected" field appears.
- Make use of libdm's DM_REPORT_FIELD_TYPE{SIZE,PERCENT,STRING_LIST} for fields.
- Support all-or-nothing pvmove --atomic.
- Automatically add snapshot metadata size for -l %%ORIGIN calculation.
- When converting RAID origin to cache LV, properly rename sub-LVs.
- Use RemoveOnStop for lvm2-lvmetad.socket systemd unit.
- Add thin-generic configuration profile for generic thin settings.
- Fix crash when reporting empty labels on pvs.
- Use retry_deactivation also when cleaning orphan devices.
- Wait for client threads when shutting down lvmetad.
- Remove PV from cache on pvremove.
- Avoid repeatedly reporting of failure to connect to lvmetad.
- Introduce MDA_FAILED to permit metadata updates even if some mdas are missing.
- Prompt when setting the VG cluster attr if the cluster is not setup.
- Allow --yes to skip prompt in vgextend (worked only with -f).
- Don't use name mangling for LVM - it never uses dm names with wrong char set.
- Remove default.profile and add {command,metadata}_profile_template.profile.
- Use proper umask for systemd units generated by lvm2-activation-generator.
- Check for failing mirror_remove_missing() function.
- Prompt before converting volumes to thin pool and thin pool metadata.
- Add dumpconfig --type profilable-{metadata,command} to select profile type.
- Exit immediately with error if command profile is found invalid.
- Separate --profile cmd line arg into --commandprofile and --metadataprofile.
- Strictly separate command profiles and per-VG/LV profiles referenced in mda.
- Fix dumpconfig --type diff when run as second and later cmd in lvm shell.
- Fix wrong profile reuse from previous run if another cmd is run in lvm shell.
- Move cache description from lvm(8) to new lvmcache(7) man page.
- Display skipped prompt in silent mode.
- Make reporting commands show help about possible sort keys on '-O help'.
- Add metadata_percent to lvs_cols.
- Take account of parity areas with alloc anywhere in _calc_required_extents.
- Use proper uint64 casting for calculation of cache metadata size.
- Better support for nesting of blocking signals.
- Use only sigaction handler and drop duplicate signal handler.
- Separate signal handling and flock code out into lib/misc.
- Don't start dmeventd checking seg_monitor and monitoring is disabled.
- Catch CTRL-c during pvremove prompts.
- Show correct availability status for snapshot origin in lvscan.
- Move segment thin pool/volume info into segment display 'lvdisplay --maps'.
- Display thin pool usage even when just thin volume is available.
- Display monitoring status for monitorable segments in 'lvdisplay --maps'.
- Display virtual extents for virtual LVs in 'lvdisplay --maps'.
- Make vgsplit fail cleanly when not all PVs are specified for RAID 4/5/6.
- Make vgsplit work on mirrors with logs that share PVs with images.
- Use devices/ignore_suspended_devices=0 by default if not defined in lvm.conf.
- Use proper libmem mempool for allocation of unknown segment name.
- Add --readonly to reporting and display tools for lock-free metadata access.
- Add locking_type 5 for dummy locking for tools that do not need any locks.
- Fix _recover_vg() error path when lock conversion fails.
- Use X for LV attributes that are unknown when activation disabled.
- Only output lvdisplay 'LV Status' field when activation is enabled.
- Use lvmetad_used() in pvscan instead of config_tree.
- Configure --enable-udev-systemd-background-jobs if not disabled explicitly.
- Add lvmdump -s to collect system info and context (currently systemd only).
- Refactor allocation code to make A_POSITIONAL_FILL explicit.
- Use thread-safe ctime_r() for clvmd debug logging.
- Skip adding replies to already finished reply thread.
- Use mutex to check number of replies in request_timed_out() in clvmd.
- Drop usage of extra reply_mutex for localsock in clvmd.
- Protect manipulation with finished flag with mutex in clvmd.
- Shift mutex creation and destroy for localsock in clvmd to correct place.
- Fix usage of --test option in clvmd.
- Skip more libraries to be mlocked in memory.
- Remove LOCKED flag for pvmove replaced with error target.
- Return invalid command when specifying negative polling interval.
- Make "help" and "?" reporting fields implicit.
- Recognize implicit "selected" field if using dm_report_init_with_selection.
- Add support for implicit reporting fields which are predefined in libdm.
- Add DM_REPORT_FIELD_TYPE_PERCENT: separate number and percent fields.
- Add dm_percent_range_t,dm_percent_to_float,dm_make_percent to libdm for reuse.
- Add dm_report_reserved_value to libdevmapper for reserved value definition.
- Also display field types when listing all fields in selection help.
- Recognize "help" keyword in selection string to show brief help for selection.
- Always order items reported as string list field lexicographically.
- Add dm_report_field_string_list to libdevmapper for direct string list report.
- Add DM_REPORT_FIELD_TYPE_STRING_LIST: separate string and string list fields.
- Add dm_str_list to libdevmapper for string list type definition and its reuse.
- Add dmsetup -S/--select to define selection criteria for dmsetup reports.
- Add dm_report_init_with_selection to intialize report with selection criteria.
- Add DM_REPORT_FIELD_TYPE_SIZE: separate number and size reporting fields.
- Use RemoveOnStop for dm-event.socket systemd unit.
- Document env var 'DM_DEFAULT_NAME_MANGLING_MODE' in dmsetup man page.
- Warn user about incorrect use of cookie with 'dmsetup remove --force'.
- Also recognize 'help'/'?' as reserved sort key name to show help.
- Add dm_units_to_factor for size unit parsing.
- Increase bitset size for minors for thin dmeventd plugin.

* Mon Jun 09 2014 Alasdair Kergon <agk@redhat.com> - 2.02.106-5
- Remove separate sub-package release tags to fix last commit.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.106-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-3
- Remove obsolete lvm2-sysvinit subpackage.

* Thu Apr 24 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-2
- Require exact lvm2/device-mapper version among LVM2 subpackages
  so all of them are always updated synchronously within one update.

* Fri Apr 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-1
- Require latest device-mapper-persistent-data 0.3.2-1.
- Fix ignored --dataalignment/dataalignmentoffset for pvcreate --restorefile.
- Fix lost information about bootloader area when using lvmetad.
- Don't require --major to be specified when using -My option on kernels > 2.4.
- Add configure --disable-thin_check_needs_check to support old thin_check.
- Use thin_check --clear-needs-check-flag by default.
- Add lvmthin man page to section 7.
- Ensure mapped device names are not too long in vg_validate and lvrename.
- Ensure resume failure in lvrename results in command failure.
- Add explicit error message when using lvdisplay -c -m.
- Report error if superfluous argument (e.g. PV name) supplied to pvscan.
- Fix error message for pvdisplay -c -m and add one for pvdisplay -c -s.
- Use EINVALID_CMD_LINE correctly instead of ECMD_FAILED in vgimport/export.
- Obtain list of known VGs from lvmetad for pvchange --all.
- Add man page for lvm-dumpconfig to section 8.
- Validate name for renamed sub LVs.
- When lvrename fails on argument parsing return EINVALID_CMD_LINE.
- Fix exit code regression in failing pvchange command (2.02.66).
- Include 'lvm dumpconfig --type missing' and '--type diff' output to lvmdump.
- Return failure when specifying negative size for pvresize.
- Fix memory corruption in cmd context refresh if clvmd leaks opened device.
- Reinitialise lvmcache properly on fork to fix premature polldaemon exit.
- Add 'lvm dumpconfig --type diff' to show differences from defaults.
- Fix swap signature detection for devices smaller then 2MB.
- Resolve memory release order for clvmd shutdown.
- Report error when lvm2 activation is released in critical_section.
- Fix memory corruption when pvscan reports long pv names.
- Do not report internal orphan VG names when reporting pvdisplay/pvscan.
- Fix pvdisplay -c man page referencing KB instead of sectors.
- Skip redundant synchronization calls on local clvmd.
- Use correct PATH_MAX for locking dir path.
- Do not check for backups when when its creation is disabled.
- Don't allow --mergedconfig without --type current in dumpconfig. Fix memleak.
- Make global/lvdisplay_shows_full_device_path lvm.conf setting profilable.
- Make global/{units|si_unit_consistency|suffix} lvm.conf setting profilable.
- Validate minimal chunk size for snapshot COW volume in lvconvert.
- Disallow lvconvert of origin to snapshot COW volume.
- Make report lvm.conf settings profilable.
- Add existing report settings to lvm.conf.
- Use VG read lock during 'pvscan --cache -aay' autoactivation.
- Issue a VG refresh before autoactivation only if the PV has changed/is new.
- Add flag to lvmetad protocol to indicate the PV scanned has changed/is new.
- Also add vgname to lvmetad protocol when referencing VGs for PVs scanned.
- Add man page for lvm2-activation-generator.
- Don't print an error and accept empty value for global/thin_disabled_features.
- Do not try to check empty pool with scheduled messages.
- Fix return value in pool_has_message() when quering for any message.
- Cleanup all client resources on clvmd exit.
- Use BLKID_CFLAGS when compiling with blkid support.
- Make lvm 'dumpconfig --type default' complete for it to be consumed by lvm.
- Run pvscan --cache via systemd-run in udev if the PV label is detected lost.
- Fix memleak when lvmetad discovers PV to appear on another device.
- Fix calculation of maximum size of COW device for snapshot (2.02.99).
- Do not allow stripe size to be bigger then extent size for lvresize.
- Zero snapshot COW header when creating read-only snapshot.
- Comment out config lines in dumpconfig output without default values defined.
- Improve detection of clustered mirror support.
- Enhance raid code with feature flags, for now checks for raid10.
- Move parsing of VG metadata from vg_commit() back to vg_write() (2.02.99)
- Avoid a PV label scan while in a critical section.
- Create /dev/disk/by-id/lvm-pv-uuid-<PV_UUID> symlink for each PV via udev.
- lvcreate computes RAID4/5/6 stripes if not given from # of allocatable PVs.
- Fix merging of old snapshot into thin volume origin.
- Use --ignoreskippedcluster in lvm2-monitor initscript/systemd unit.
- Do not use VG read/write state for LV read/write state.
- Use --ignoreskippedcluster in activation systemd units if use_lvmetad=0.
- Allow approximate allocation when specifying size in percentage terms.
- Add basic LVM support for cache[pool] segment types.
- Use local exclusive activation for creation of raid in cluster.
- Use correctly signed 64b constant when selecting raid volumes.
- Remove ExecReload from lvmetad systemd unit: lvmetad -R undefined. (2.02.98)
- Do not fork lvmetad if running under systemd.
- Wipe DM_snapshot_cow signature without prompt in new LVs with blkid wiping.
- Avoid exposing temporary devices when initializing raid metadata volumes.
- Add internal tags command to display any tags defined on the host.
- Prohibit use of external origin with size incompatible with thin pool.
- Avoid trying to convert single to thin pool and volume at the same time.
- Add support for partitions on ZFS zvol.
- Fix unwanted drop of hold flocks on forked children.
- Respect LVM_LVMETAD_PIDFILE env var for lvm command.
- Fix test when checking target version for available thin features.
- Detect thin feature external_origin_extend and limit extend when missing.
- Issue error if libbblkid detects signature and fails to return offset/length.
- Update autoconf config.guess/sub to 2014-01-01.
- Online thin pool metadata resize requires 1.10 kernel thin pool target.
- Check for sprintf error when building internal device path.
- Check for sprintf error when creating path for dm control node.
- When buffer for dm_get_library_version() is too small, return error code.
- Always reinitialize _name_mangling_mode in dm_lib_init().
- Stop timeout thread immediately when the last worker thread is finished.
- Fix dmeventd logging with parallel wait event processing.
- Reuse _node_send_messages() for validation of transaction_id in preload.
- Transaction_id could be lower by one only when messages are prepared.
- Wrap is_selinux_enabled() to be called just once.
- Use correctly signed 64b constant when working with raid volumes.
- Exit dmeventd with pidfile cleanup instead of raising SIGKILL on DIE request.
- Add new DM_EVENT_GET_PARAMETERS request to dmeventd protocol.
- Do not use systemd's reload for dmeventd restart, use dmeventd -R instead.

* Mon Jan 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-2
- Avoid exposing temporary devices when initializing thin pool volume.
- Remove udev rule for multipath's PATH_FAILED event processing,
  multipath handles that properly in its own udev rules now.
- Remove duplicate udev rule for cryptsetup temporary devices,
  cryptsetup handles that properly directly in its code.

* Tue Jan 21 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-1
- Fix thin LV flagging for udev to skip scanning only if the LV is wiped.
- Replace use of xfs_check with xfs_repair in fsadm.
- Mark lvm1 format metadata as FMT_OBSOLETE. Do not use it with lvmetad.
- Invalidate cached VG struct after a PV in it gets orphaned. (2.02.87)
- Mark pool format metadata as FMT_OBSOLETE.
- Use major:minor in lvm2-pvscan@.service for proper global_filter application.
- Syntax and spelling fixes in some man pages.
- Dependency scan counts with snapshots and external origins.
- Make sure VG extent size is always greater or equal to PV phys. block size.
- Optimize double call of stat() for cached devices.
- Enable support for thin provisioning for default configuration.
- Disable online thin pool metadata resize for 1.9 kernel thin target.
- Shortened code for initialization of raid segment types.
- Test for remote exclusive activation after activation fails.
- Support lvconvert --merge for thin snapshots.
- Add support to read thin device id from table line entry.
- Drop extra test for origin when testing merging origin in lv_refresh().
- Extend lv_remove_single() to not print info about removed LV.
- Replace open_count check with lv_check_not_in_use() for snapshot open test.
- Add error messages with LV names for failing lv refresh.
- Compile/link executables with new RELRO and PIE options (non-static builds).
- Support per-object compilation cflags via CFLAGS_object.o.
- Automatically detect support for compiler/linker options to use RELRO and PIE.
- Add --splitsnapshot to lvconvert to separate out cow LV.
- Reinstate origin reload to complete lvconvert -s with active LVs. (2.02.98)
- Select only active volume groups if vgdisplay -A is used.
- Add -p and LVM_LVMETAD_PID env var to lvmetad to change pid file.
- Allow lvmetad to reuse stale socket.
- Only unlink lvmetad socket on error if created by the same process.
- Append missing newline to lvmetad missing socket path error message.
- Add allocation/use_blkid_wiping to lvm.conf to enable blkid wiping.
- Enable blkid_wiping by default if the blkid library is present.
- Add configure --disable-blkid_wiping to disable libblkid signature detection.
- Add -W/--wipesignatures lvcreate option to support wiping on new LVs.
- Add allocation/wipe_signatures_when_zeroing_new_lvs to lvm.conf.
- Do not fail the whole autoactivation if the VG refresh done before fails.
- Do not connect to lvmetad on vg/lvchange --sysinit -aay and socket absent.
- Use lv_check_not_in_use() when testing device in use before merging.
- Check for failure of lvmcache_add_mda() when writing pv.
- Check for failure of dev_get_size() when reporting device size.
- Drop extra unneeded '/' when scanning sysfs directory.
- Fix undef value if skipped clustered VG ignored for toollib PV seg. (2.02.103)
- Support validation of VG/LV names in liblvm/python.
- Allow creation of PVs with arguments to liblvm/python.
- Ensure sufficient metadata copies retained in liblvm/python vgreduce.
- Fix installation of profiles from conf subdir when not building in srcdir.
- Show UUIDs for missing PVs in reports.
- Add reporting of thin_id device id for thin volumes.
- Fix reporting of empty numerical values for recently-added fields.
- Revert activation of activated nodes if a node preload callback fails.
- Avoid busy looping on CPU when dmeventd reads event DM_WAIT_RETRY.
- Ensure global mutex is held when working with dmeventd thread.
- Drop taking timeout mutex for un/registering dmeventd monitor.
- Allow section names in config file data to be quoted strings.
- Close fifos before exiting in dmeventd restart() error path.
- Catch invalid use of string sort values when reporting numerical fields.
- Require util-linux >= 2.24 for blkid wiping support (via device-mapper pkg).
- Add BuildRequires: libblkid-devel to build with blkid wiping functionality.
- Do not install /run and /run/lvm directory but only own them by lvm2 package.
  These dirs are controlled by systemd's tmpfiles.d/lvm2.conf configuration.
- Consolidate file permissions for all packaged files.

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.02.104-4
- Drop INSTALL from docs, escape percents in %%changelog.

* Fri Dec 13 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-3
- Change lvm2-python-libs to require lvm2, not just lvm2-libs.

* Wed Dec 11 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-2
- Fix SYSTEMD_READY assignment for foreign devs in lvmetad rules.

* Thu Nov 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-1
- Workaround VG refresh race during autoactivation by retrying the refresh.
- Handle failures in temporary mirror used when adding images to mirrors.
- Fix and improve logic for implicitely exclusive activations.
- Return success when LV cannot be activated because of volume_list filter.
- Return proper error state for remote exclusive activation.
- Fix clvmd message verification to not reject REMOTE flag. (2.02.100)
- Compare equality of double values with DBL_EPSILON predefined constant.
- Use additional gcc warning flags by default.
- Add ignore_lvm_mirrors to config file to read/ignore labels on mirrors.
- Use #ifdef __linux__ instead of linux throughout.
- Consistently report on stderr when device is not found for dmsetup info.
- Skip race errors when non-udev dmsetup build runs on udev-enabled system.
- Skip error message when holders are not present in sysfs.

* Wed Oct 30 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-3
- Fix missing lvmetad scan for PVs found on MD partitions.
- Respect DM_UDEV_DISABLE_OTHER_RULES_FLAG in lvmetad udev rules.

* Fri Oct 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-2
- Add internal flag for temporary LVs to properly direct udev to not interfere.
- Fix endless loop in blkdeactivate <device>... if unable to umount/deactivate.
- Add dev-block-<major>:<minor>.device systemd alias for complete PV tracking.
- Use major:minor as short form of --major and --minor arg for pvscan --cache.
- Remove 2>/dev/null from three lvm commands executed by vgimportclone.
- Add configure --enable-udev-systemd-background-jobs.
- Add lvm2-pvscan@.service to run pvscan as a service for lvmetad/autoactivation.
- Fix lvconvert swap of poolmetadata volume for active thin pool.
- Check for open count with a timeout before removal/deactivation of an LV.
- Report RAID images split with tracking as out-of-sync ("I").
- Improve parsing of snapshot lv segment.
- Add workaround for deactivation problem of opened virtual snapshot.
- Disable unsupported merge for virtual snapshot.
- Move code to remove virtual snapshot from tools to lib for lvm2app.
- Fix possible race during daemon worker thread creation (lvmetad).
- Fix possible deadlock while clearing lvmetad cache for full rescan.
- Fix possible race while creating/destroying memory pools.
- Recognise NVM Express devices in filter.
- Fix failing metadata repair when lvmetad is used.
- Fix incorrect memory handling when reading messages from lvmetad.
- Fix locking in lvmetad when handling the PV which is gone.
- Recognize new flag to skip udev scanning in udev rules and act appropriately.
- Add support for flagging an LV to skip udev scanning during activation.
- Improve message when unable to change discards setting on active thin pool.
- Run full scan before vgrename operation to avoid any cache name collision.
- Fix lvconvert when converting to a thin pool and thin LV at once.
- Skip race errors when non-udev dmsetup build runs on udev-enabled system.
- Skip error message when holders are not present in sysfs.
- Use __linux__ instead of linux define to make libdevmapper.h C compliant.

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-1
- Ensure vgid matches before removing vgname entry from lvmetad cache.
- Add --ignoreskippedcluster for exit status success when clustered VGs skipped.
- Fix 3 minute udev timeout so that it is applied for all LVM volumes.
- Fix thin/raid & activation config defaults with configure --disable-devmapper.
- Fix RAID calculation for sufficient allocatable space.
- lvconvert from linear to mirror or RAID1 now honors mirror_segtype_default.
- Add thin-performance configuration profile.
- Add lvm.conf allocation/thin_pool_chunk_size_policy option.
- Fix contiguous & cling allocation policies for parity RAID.  (2.02.100)
- Have lvmconf --enable/disable-cluster reset/set use_lvmetad.
- Add seg_size_pe field to reports.
- Support start+length notation with command line PE ranges.
- Exit cleanly with message when pvmove cannot restart because LV is inactive.
- Define symbolic names for subsystem udev flags in libdevmapper for easier use.
- Make subsystem udev rules responsible for importing DM_SUBSYSTEM_UDEV_FLAG*.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-1
- Fix missing build dependency for scripts subdir in Makefile.
- Fix node up/down handling in clvmd corosync module.
- Fix 3-thread clvmd deadlock triggered by cleanup on EOF from client.
- Remove VG from lvmetad before restoring it with vgcfgrestore.
- Add devtypes report command to display built-in recognised block device types.
- Fix CC Makefile override which had reverted to using built-in value. (2.02.75)
- Recognise bcache block devices in filter (experimental).
- Run lvm2-activation-net after lvm2-activation service to prevent parallel run.
- Add man page entries for lvmdump's -u and -l options.
- Fix lvm2app segfault while using lvm_list_pvs_free fn if there are no PVs.
- Improve of clvmd singlenode locking simulation.
- lvconvert no longer converts LVs of "mirror" segment type to thinpool.
- lvconvert no longer converts thinpool sub-LVs to "mirror" segment type.
- Direct udev to use 3min timeout for LVM devices. Recent udev has default 30s.
- Do not scan multipath or RAID components and avoid incorrect autoactivation.
- Fix MD/loop udev handling to fire autoactivation after setup or coldplug only.
- Make RAID capable of single-machine exclusive operations in a cluster.
- Drop calculation of read ahead for deactivated volume.
- Check for exactly one lv segment in validation of thin pools and volumes.
- Fix dmeventd unmonitoring of thin pools.
- Fix lvresize for stacked thin pool volumes (i.e. mirrors).
- Write Completed debug message before reinstating log defaults after command.
- Refresh existing VG before autoactivation (event retrigger/device reappeared).
- Use pvscan -b in udev rules to avoid a deadlock on udev process count limit.
- Add pvscan -b/--background for the command to be processed in the background.
- Don't assume stdin file descriptor is readable.
- Avoid unlimited recursion when creating dtree containing inactive pvmove LV.
- Require exactly 3 arguments for lvm2-activation-generator. Remove defaults.
- Inform lvmetad about any lost PV label to make it in sync with system state.
- Support most of lvchange operations on stacked thin pool meta/data LVs.
- Enable non-clustered pvmove of snapshots and snapshot origins.
- Add ability to pvmove non-clustered RAID, mirror, and thin volumes.
- Make lvm2-activation-generator silent unless it's in error state.
- Remove "mpath major is not dm major" msg for mpath component scan (2.02.94).
- Prevent cluster mirror logs from being corrupted by redundant checkpoints.
- Fix ignored lvmetad update on loop device configuration (2.02.99).
- Use LVM_PATH instead of hardcoded value in lvm2 activation systemd generator.
- Fix vgck to notice on-disk corruption even if lvmetad is used.
- Move mpath device filter before partitioned filter (which opens devices).
- Require confirmation for vgchange -c when no VGs listed explicitly.
- Also skip /var and /var/log by default in blkdeactivate when unmounting.
- Add support for bind mounts in blkdeactivate.
- Add blkdeactivate -v/--verbose for debug output from external tools used.
- Add blkdeactivate -e/--errors for error messages from external tools used.
- Suppress messages from external tools called in blkdeactivate by default.
- Fix inability to remove a VG's cluster flag if it contains a mirror.
- Fix bug making lvchange unable to change recovery rate for RAID.
- Prohibit conversion of thin pool to external origin.
- Workaround gcc v4.8 -O2 bug causing failures if config/checks=1 (32bit arch).
- Verify clvmd message validity before processing and log error if incorrect.
- When creating PV on existing LV don't forbid reserved LV names on LVs below.
- When converting mirrors, default segtype should be the same unless specified.
- Make "raid1" the default mirror segment type.
- Fix clogd descriptor leak when daemonizing.
- Fix clvmd descriptor leak on restart.
- Add pipe_open/close() to use instead of less efficient/secure popen().
- Inherit and apply any profile attached to a VG if creating new thin pool.
- Add initial support thin pool lvconvert --repair.
- Add --with-thin-repair and --with-thin-dump configure options.
- Add lvm.conf thin_repair/dump_executable and thin_repair_options.
- Require 1.9 thin pool target version for online thin pool metadata resize.
- Ignore previous LV seg with alloc contiguous & cling when num stripes varies.
- Fix segfault if devices/global_filter is not specified correctly.
- Tidy dmeventd fifo initialisation.
- Detect invalid sector supplied to 'dmsetup message'.
- Free any previously-set string if a dm_task_set_* function is called again.
- Do not allow passing empty new name for dmsetup rename.
- Display any output returned by 'dmsetup message'.
- Add dm_task_get_message_response to libdevmapper.
- Create dmeventd timeout threads as "detached" so exit status is freed.
- Add DM_ABORT_ON_INTERNAL_ERRORS env var support to abort on internal errors.

* Tue Aug 06 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-2
- Fix metadata area offset/size overflow if it's >= 4g and while using lvmetad.
- Require the newest device-mapper-persistent-data-0.2.3-1.
- Fix spec file's util-linux version definition for proper expansion when used.

* Thu Jul 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-1
-  o Features/Extensions/Additions:
- Add support for poolmetadataspare LV, that will be used for pool recovery.
- Improve activation order when creating thin pools in non-clustered VG.
- Add lvm2-activation-net systemd unit to activate LVs on net-attached storage.
- Automatically flag thin snapshots to be skipped during activation.
- Add support for persistent flagging of LVs to be skipped during activation.
- Make selected thinp settings customizable by a profile.
- Support storing profile name in metadata for both VGs and LVs.
- Add support for configuration profiles.
- Add support for thin volumes in vgsplit.
- Add lvresize support for online thin pool metadata volume resize.
- Add detection for thin pool metadata resize kernel support.
- Add vg->vg_ondisk / lv_ondisk() holding committed metadata.
- Add detection of mounted fs also for vgchange deactivation.
- Detect maximum usable size for snapshot for lvresize.
- Improve RAID kernel status retrieval to include sync_action/mismatch_cnt.
- Add external origin support for lvcreate.
- Support automatic config validation.
- Add PV header extension: extension version, flags and bootloader areas.
- Initial support for lvconvert of thin external origin.
- Improve activation code for better support of stacked devices.
- vgimport '--force' now allows import of VGs with missing PVs.
- Allow removal or replacement of RAID LV components that are error segments.
- Make 'vgreduce --removemissing' able to handle RAID LVs with missing PVs.
- Give precedence to EMC power2 devices with duplicate PVIDs.
- Recognise Storage Class Memory (IBM S/390) devices in filter.
- Recognise STEC skd devices in filter.
- Recognise Violin Memory vtms devices in filter.
- Automatically restore MISSING PVs with no MDAs.
- Detect mounted fs also via reading /proc/self/mountinfo.
-  o Command Interface/Options:
- Support ARG_GROUPABLE with merge_synonym (for --raidwritemostly).
- Add --ignoreactivationskip to lvcreate/vgchange/lvchange to ignore skip flag.
- Add --setactivationskip to lvcreate/lvchange to set activation skip flag.
- Add --type profilable to lvm dumpconfig to show profilable config settings.
- Add --mergedconfig to lvm dumpconfig for merged --config/--profile/lvm.conf.
- Support changing VG/LV profiles: vgchange/lvchange --profile/--detachprofile.
- Add new --profile command line arg to select a configuration profile for use.
- For creation of snapshot require size for at least 3 chunks.
- Do not accept size parameters bigger then 16EiB.
- Accept --yes in all commands so test scripts can be simpler.
- Add lvcreate/lvchange --[raid]{min|max}recoveryrate for raid LVs.
- Add lvchange --[raid]writemostly/writebehind support for RAID1
- Add lvchange --[raid]syncaction for scrubbing of RAID LVs.
- Add --validate option to lvm dumpconfig to validate current config on demand.
- Add --ignoreadvanced and --ignoreunsupported switch to lvm dumpconfig.
- Add --withcomments and --withversions switch to lvm dumpconfig.
- Add --type {current|default|missing|new} and --atversion to lvm dumpconfig.
- Add --bootloaderareasize to pvcreate and vgconvert to create bootloader area.
- Do not take a free lv name argument for lvconvert --thinpool option.
- Allow lvconvert --stripes/stripesize only with --mirrors/--repair/--thinpool.
- Do not ignore -f in lvconvert --repair -y -f for mirror and raid volumes.
- Support use of option --yes for lvchange --persistent.
- Fix clvmd support for option -d and properly use its argument.
-  o Reporting:
- Issue an error msg if lvconvert --type used incorrectly with other options.
- Use LOG_DEBUG/ERR msg severity instead default for lvm2-activation-generator.
- Add LV report fields: raid_mismatch_count/raid_sync_action/raid_write_behind.
- Add LV reporting fields raid_min_recovery_rate, raid_max_recovery_rate.
- Add sync_percent as alias for copy_percent LV reporting field.
- Add lv_ prefix to modules reporting field.
- Use units B or b (never E) with no decimal places when displaying sizes < 1k.
- List thin-pool and thin modules for thin volumes.
- Add 's(k)ip activation' bit to lvs -o lv_attr to indicate skip flag attached.
- Improve error loging when user tries to interrupt commands.
- Add vgs/lvs -o vg_profile/lv_profile to report profiles attached to VG/LV.
- Report lvs volume type 'e' with higher priority.
- Report lvs volume type 'o' also for external origin volumes.
- Report lvs target type 't' only for thin pools and thin volumes.
- Add "active" LV reporting field to show activation state.
- Add "monitor" segment reporting field to show dmevent monitoring status.
- Add explicit message about unsupported pvmove for thin/thinpool volumes.
- Add pvs -o pv_ba_start,pv_ba_size to report bootloader area start and size.
- Fix pvs -o pv_free reporting for PVs with zero PE count.
- Report blank origin_size field if the LV doesn't have an origin instead of 0.
- Report partial and in-sync RAID attribute based on kernel status
- Log output also to syslog when abort_on_internal_error is set.
- Change lvs heading Copy%% to Cpy%%Sync and print RAID4/5/6 sync%% there too.
- Report error for nonexisting devices in dmeventd communication.
- Reduce some log_error messages to log_warn where we don't fail.
-  o Configuration:
- Add activation/auto_set_activation_skip to control activation skip flagging.
- Add default.profile configuration profile and install it on make install.
- Add config/profile_dir to set working directory to load profiles from.
- Use mirror_segtype_default if type not specified for linear->mirror upconvert.
- Refine lvm.conf and man page documentation for autoactivation feature.
- Override system's global_filter settings for vgimportclone.
- Find newest timestamp of merged config files.
- Add 'config' section to lvm.conf to set the way the LVM configuration is handled.
- Add global/raid10_segtype_default to lvm.conf.
- Accept activation/raid_region_size in preference to mirror_region_size config.
- Add log/debug_classes to lvm.conf to control debug log messages.
- Allow empty activation/{auto_activation|read_only|}_volume_list config option.
- Relax ignore_suspended_devices to read from mirrors that don't have a device marked failed.
-  o Documentation:
- Add man page entries for profile configuration and related options.
- Document lvextend --use-policies option in man.
- Improve lvcreate, lvconvert and lvm man pages.
-  o API/interfaces:
- liblvm/python API: Additions: PV create/removal/resize/listing
- liblvm/python API: Additions: LV attr/origin/Thin pool/Thin LV creation
- Fix exported symbols regex for non-GNU busybox sed.
- Add LV snapshot support to liblvm and python-lvm.
- Remove python liblvm object. systemdir can only be changed using env var now.
- Add dm_get_status_snapshot() for parsing snapshot status.
- Append discards and read-only fields to exported struct dm_status_thin_pool.
- Validate passed params to dm_get_status_raid/thin/thin_pool().
- Add dm_mountinfo_read() for parsing /proc/self/mountinfo.
- Add dm_config_write_{node_out/one_node_out} for enhanced config output.
- Add dm_config_value_is_bool to check for boolean value in supported formats.
- Add DM_ARRAY_SIZE public macro.
- Add DM_TO_STRING public macro.
- Implement ref-counting for parents in python lib.
-  o Fixes (general):
- Do not zero init 4KB of thin snapshot for non-zeroing thin pool (2.02.94).
- Correct thin creation error paths.
- Add whole log_lv and metadata_lv sub volumes when creating partial tree.
- Properly use snapshot layer for origin which is also thin volume.
- Avoid generating metadata backup when calling update_pool_lv().
- Send thin messages also for active thin pool and inactive thin volume.
- Avoid creation of multiple archives for one command.
- Avoid flushing thin pool when just requesting transaction_id.
- Fix use of too big chunks of memory when communication with lvmetad.
- Also filter partitions on mpath components if multipath_component_detection=1.
- Do not use persistent filter with lvmetad.
- Move syslog code out of signal handle in dmeventd.
- Fix lvresize --use-policies of VALID but 100%% full snapshot.
- Skip monitoring of snapshots that are already bigger then origin.
- Refuse to init a snapshot merge in lvconvert if there's no kernel support.
- Fix alignment of PV data area if detected alignment less than 1 MB (2.02.74).
- Fix creation and removal of clustered snapshot.
- Fix clvmd caching of metadata when suspending inactive volumes.
- Fix lvmetad error path in lvmetad_vg_lookup() for null vgname.
- Fix clvmd _cluster_request() return code in memory fail path.
- Fix vgextend to not allow a PV with 0 MDAs to be used while already in a VG.
- Fix PV alignment to incorporate alignment offset if the PV has zero MDAs.
- Fix missing cleanup of flags when the LV is detached from pool.
- Fix check for some forbidden discards conversion of thin pools.
- Limit RAID device replacement to repair only if LV is not in-sync.
- Disallow RAID device replacement or repair on inactive LVs.
- Unlock vg mutex in error path when lvmetad tries to lock_vg.
- Detect key string duplication failure in config_make_nodes_v in libdaemon.
- Disallow pvmove on RAID LVs until they are addressed properly
- Recognize DM_DISABLE_UDEV environment variable for a complete fallback.
- When no --stripes argument is given when creating a RAID10 volume, default to 2 stripes.
- Do not allow lvconvert --splitmirrors on RAID10 logical volumes.
- Repair a mirrored log before the mirror itself when both fail.
- Avoid trying to read a mirror that has a failed device in its mirrored log.
- Fix segfault for truncated string token in config file after the first '"'.
- Fix config node lookup inside empty sections to not return the section itself.
- Fix parsing of 64bit snapshot status in dmeventd snapshot plugin.
- Always return success on dmeventd -V command call.
-  o Fixes (segfaults/crashes/deadlocks/races):
- Fix segfault when reporting raid_syncaction for older kernels.
- Fix vgcfgrestore crash when specified incorrect vg name.
- Check for memory failure of dm_config_write_node() in lvmetad.
- Prevent double free error after dmeventd call of _fill_device_data().
-  o Fixes (resource leaks/memleaks):
- Release memory allocated with _cached_info().
- Release memory and unblock signals in lock_vol error path.
- Fix memory resource leak in memlocking error path.
- Fix memleak in dmeventd thin plugin in device list obtaining err path.
- Fix socket leak on error path in lvmetad's handle_connect.
- Fix memleak on error path for lvmetad's pv_found.
- Fix memleak in device_is_usable mirror testing function.
- Fix memory leak on error path for pvcreate with invalid uuid.
- Fix resource leak in error path of dmeventd's umount of thin volume.
-  o Testing:
- Fix test for active snapshot in cluster before resizing it.
- Add python-lvm unit test case
-  o Other:
- Use local activation for clearing snapshot COW device.
- Add configure --with-default-profile-subdir to select dir to keep profiles in.
- Creation of snapshot takes at most 100%% origin coverage.
- Use LC_ALL to set locale in daemons and fsadm instead of lower priority LANG.
- Optimize out setting the same value of read_ahead.
- Automatically deactivate failed preloaded dm tree node.
- Process thin messages once to active thin pool target for dm_tree.
-  o Packaging:
- Add /etc/lvm/profile dir and /etc/lvm/profile/default.profile to lvm2 package.
- Do not include /lib/udev and /lib/udev/rules.d in device-mapper package.
- Fix some incorrect changelog dates.

* Tue May 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-9
- Fix 'dmsetup splitname -o' to not fail if used without '-c' switch (1.02.68).
- Close open dmeventd FIFO file descriptors on exec (FD_CLOEXEC).
- Fix premature DM version checking which caused useless mapper/control access.
- Recognize DM_DISABLE_UDEV environment variable for a complete fallback.
- Do not verify udev operations if --noudevsync command option is used.
- Fix blkdeactivate to handle nested mountpoints and mangled mount paths.
- Fix a crash-inducing race condition in lvmetad while updating metadata.
- Fix possible race while removing metadata from lvmetad.
- Fix possible deadlock when querying and updating lvmetad at the same time.
- Avoid a global lock in pvs when lvmetad is in use.
- Fix crash in pvscan --cache -aay triggered by non-mda PV.
- Fix lvm2app to return all property sizes in bytes.
- Add lvm.conf option global/thin_disabled_features.
- Add lvconvert support to swap thin pool metadata volume.
- Implement internal function detach_pool_metadata_lv().
- Fix lvm2app and return lvseg discards property as string.
- Allow forced vgcfgrestore of lvm2 metadata with thin volumes.
- Add lvm.conf thin pool defs thin_pool_{chunk_size|discards|zero}.
- Support discards for non-power-of-2 thin pool chunks.
- Support allocation of pool metadata with lvconvert command.
- Move common functionality for thin lvcreate and lvconvert to toollib.
- Use lv_is_active() instead of lv_info() call.

* Fri May 03 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-8
- Fix non-functional autoactivation of LVM volumes on top of MD devices.

* Fri Apr 19 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-7
- Autoactivate VG/LV on coldplug of DM-based PVs at boot.

* Tue Apr 09 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-6
- Synchronize with udev in pvscan --cache and fix dangling udev_sync cookies.
- Fix autoactivation to not autoactivate VG/LV on each change of the PVs used.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.98-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-4
- Skip mlocking [vectors] on arm architecture.

* Sat Nov 17 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-3
- Add lvm2-activation-generator systemd generator to automatically generate
  systemd units to activate LVM2 volumes even if lvmetad is not used.
  This replaces lvm activation part of the former fedora-storage-init
  script that was included in the initscripts package before.
- Enable lvmetad - the LVM metadata daemon by default.
- Exit pvscan --cache immediately if cluster locking used or lvmetad not used.
- Don't use lvmetad in lvm2-monitor.service ExecStop to avoid a systemd issue.
- Remove dependency on fedora-storage-init.service in lvm2 systemd units.
- Depend on lvm2-lvmetad.socket in lvm2-monitor.service systemd unit.
- Init lvmetad lazily to avoid early socket access on config overrides.
- Hardcode use_lvmetad=0 if cluster locking used and issue a warning msg.
- Fix dm_task_set_cookie to properly process udev flags if udev_sync disabled.

* Sat Oct 20 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-2
- Incorporate former python-lvm package in lvm2 as lvm2-python-libs subpackage.

* Tue Oct 16 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-1
- Don't try to issue discards to a missing PV to avoid segfault.
- Fix vgchange -aay not to activate non-matching LVs that follow a matching LV.
- Fix lvchange --resync for RAID LVs which had no effect.
- Add RAID10 support (--type raid10).
- Introduce blkdeactivate script to deactivate block devs with dependencies.
- Apply 'dmsetup mangle' for dm UUIDs besides dm names.
- Use -q as short form of --quiet.
- Suppress non-essential stdout with -qq.
- Add log/silent to lvm.conf equivalent to -qq.
- Add (p)artial attribute to lvs.
- Implement devices/global_filter to hide devices from lvmetad.
- Add lvmdump -l, to collect a state dump from lvmetad.
- Add --discards to lvconvert.
- Add support for lvcreate --discards.
- Add --poolmetadata to lvconvert and support thin meta/data dev stacking.
- Support creation of read-only thin volumes (lvcreate -p r).
- Support changes of permissions for thin snapshot volumes.
- Make lvremove ask before discarding data areas.
- Prohibit not yet supported change of thin-pool to read-only.
- Using autoextend percent 0 for thin pool fails 'lvextend --use-policies'.
- Make vgscan --cache an alias for pvscan --cache.
- Clear lvmetad metadata/PV cache before a rescan.
- Fix a segmentation fault upon receiving a corrupt lvmetad response.
- Give inconsistent metadata warnings in pvscan --cache.
- Avoid overlapping locks that could cause a deadlock in lvmetad.
- Fix memory leaks in libdaemon and lvmetad.
- Optimize libdaemon logging for a fast no-output path.
- Only create lvmetad pidfile when running as a daemon (no -f).
- Warn if lvmetad is running but disabled.
- Warn about running lvmetad with use_lvmetad = 0 in example.conf.
- Update lvmetad help output (flags and their meaning).
- Make pvscan --cache read metadata from LVM1 PVs.
- Make libdaemon buffer handling asymptotically more efficient.
- Make --sysinit suppress lvmetad connection failure warnings.
- Prohibit usage of lvcreate --thinpool with --mirrors.
- Fix lvm2api origin reporting for thin snapshot volume.
- Add implementation of lvm2api function lvm_percent_to_float.
- Allow non power of 2 thin chunk sizes if thin pool driver supports that.
- Allow limited metadata changes when PVs are missing via [vg|lv]change.
- Do not start dmeventd for lvchange --resync when monitoring is off.
- Remove pvscan --cache from lvm2-lvmetad init script.
- Remove ExecStartPost with pvscan --cache from lvm2-lvmetad.service.
- Report invalid percentage for property snap_percent of non-snaphot LVs.
- Disallow conversion of thin LVs to mirrors.
- Fix lvm2api data_percent reporting for thin volumes.
- Do not allow RAID LVs in a clustered volume group.
- Enhance insert_layer_for_lv() with recursive rename for _tdata LVs.
- Skip building dm tree for thin pool when called with origin_only flag.
- Ensure descriptors 0,1,2 are always available, using /dev/null if necessary.
- Use /proc/self/fd when available for closing opened descriptors efficiently.
- Fix inability to create, extend or convert to a large (> 1TiB) RAID LV.
- Update lvmetad communications to cope with clients using different filters.
- Clear LV_NOSYNCED flag when a RAID1 LV is converted to a linear LV.
- Disallow RAID1 upconvert if the LV was created with --nosync.
- Depend on systemd-udev-settle in units generated by activation generator.
- Disallow addition of RAID images until the array is in-sync.
- Fix RAID LV creation with '--test' so valid commands do not fail.
- Add lvm_lv_rename() to lvm2api.
- Fix setvbuf code by closing and reopening stream before changing buffer.
- Disable private buffering when using liblvm.
- When private stdin/stdout buffering is not used always use silent mode.
- Fix 32-bit device size arithmetic needing 64-bit casting throughout tree.
- Fix dereference of NULL in lvmetad error path logging.
- Fix buffer memory leak in lvmetad logging.
- Correct the discards field in the lvs manpage (2.02.97).
- Use proper condition to check for discards settings unsupported by kernel.
- Reinstate correct default to ignore discards for thin metadata from old tools.
- Issue error message when -i and -m args do not match specified RAID type.
- Change lvmetad logging syntax from -ddd to -l {all|wire|debug}.
- Add new libdaemon logging infrastructure.
- Support unmount of thin volumes from pool above thin pool threshold.
- Update man page to reflect that dm UUIDs are being mangled as well.
- Add 'mangled_uuid' and 'unmangled_uuid' fields to dmsetup info -c -o.
- Mangle device UUID on dm_task_set_uuid/newuuid call if necessary.
- Add dm_task_get_uuid_mangled/unmangled to libdevmapper.
- Always reset delay_resume_if_new flag when stacking thin pool over anything.
- Don't create value for dm_config_node and require dm_config_create_value call.
- Check for existing new_name for dmsetup rename.
- Fix memory leak in dmsetup _get_split_name() error path.
- Clean up spec file and keep support only for Fedora 18 upwards.
- Use systemd macros in rpm scriptlets to set up systemd units.
- Add Requires: bash >= 4.0 for blkdeactivate script.

* Tue Aug 07 2012 Alasdair Kergon <agk@redhat.com> - 2.02.97-1
- Improve documention of allocation policies in lvm.8.
- Increase limit for major:minor to 4095:1048575 when using -My option.
- Add generator for lvm2 activation systemd units.
- Add lvm_config_find_bool lvm2app fn to retrieve bool value from config tree.
- Respect --test when using lvmetad.
- No longer capitalise first LV attribute char for invalid snapshots.
- Allow vgextend to add PVs to a VG that is missing PVs.
- Recognise Micron PCIe SSDs in filter and move array out to device-types.h.
- Fix dumpconfig <node> to print only <node> without its siblings. (2.02.89)
- Do not issue "Failed to handle a client connection" error if lvmetad killed.
- Support lvchange --discards and -Z with thin pools.
- Add discard LV segment field to reports.
- Add --discards to lvcreate --thin.
- Set discard and external snapshot features if thin pool target is vsn 1.1+.
- Count percentage of completeness upwards not downwards when merging snapshot.
- Skip activation when using vg/lvchange --sysinit -a ay and lvmetad is active.
- Fix extending RAID 4/5/6 logical volumes
- Fix test for PV with unknown VG in process_each_pv to ignore ignored mdas.
- Fix _alloc_parallel_area to avoid picking already-full areas for raid devices.
- Never issue discards when LV extents are being reconfigured, not deleted.
- Allow release_lv_segment_area to fail as functions it calls can fail.
- Fix missing sync of filesystem when creating thin volume snapshot.
- Allow --noflush with dmsetup status and wait (for thin target).
- Add dm_config_write_one_node to libdevmapper.
- Add dm_vasprintf to libdevmapper.
- Support thin pool message release/reserve_metadata_snap in libdevmapper.
- Support thin pool discards and external origin features in libdevmapper.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.96-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.96-3
- Use configure --with-default-pid-dir=/run.
- Use globally set prefix for udev rules path.

* Mon Jul 02 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.96-2
- Compile with lvmetad support enabled.
- Add support for volume autoactivation using lvmetad.
- Update man pages with --activate ay option and auto_activation_volume_list.
- Use vgchange -aay instead of vgchange -ay in clmvd init script.
- Add activation/auto_activation_volume_list to lvm.conf.
- Add --activate ay to lvcreate, lvchange, pvscan and vgchange.
- Add --activate synonym for --available arg and prefer --activate.
- Open device read-only to obtain readahead value.
- Add configure --enable-udev-rule-exec-detection to detect exec path in rules.
- Use sbindir in udev rules by default and remove executable path detection.
- Remove hard-coded paths for dmeventd fifos and use default-dm-run-dir.
- Add configure --with-lvmetad-pidfile to remove hard-coded value.
- Add configure --with-default-pid-dir for common directory with pid files.
- Add configure --with-default-dm-run-dir to set run directory for dm tools.
- Add documentation references in systemd units.
- Clean up spec file and keep support only for Fedora 17 upwards.

* Mon Jun 18 2012 Alasdair Kergon <agk@redhat.com> - 2.02.96-1
- Require device-mapper-persistent-data package for thin provisioning.
- Set delay_resume_if_new on deptree snapshot origin.
- Log value chosen in _find_config_bool like other variable types do.
- Wait for dmeventd to exit after sending it DM_EVENT_CMD_DIE when restarting.
- Append 'Used' to {Blk}DevNames/DevNos dmsetup report headers for clarity.
- Remove dmeventd fifos on exit if they are not managed by systemd.
- Use SD_ACTIVATION environment variable in systemd units to detect systemd.
- Only start a new dmeventd instance on restart if one was already running.
- Extend the time waited for input from dmeventd fifo to 5 secs. (1.02.73)
- Fix error paths for regex filter initialization.
- Re-enable partial activation of non-thin LVs until it can be fixed. (2.02.90)
- Fix alloc cling to cling to PVs already found with contiguous policy.
- Fix cling policy not to behave like normal policy if no previous LV seg.
- Fix allocation loop not to use later policies when --alloc cling without tags.
- Fix division by zero if PV with zero PE count is used during vgcfgrestore.
- Add initial support for thin pool lvconvert.
- Fix lvrename for thin volumes (regression in for_each_sub_lv). (2.02.89)
- Fix up-convert when mirror activation is controlled by volume_list and tags.
- Warn of deadlock risk when using snapshots of mirror segment type.
- Fix bug in cmirror that caused incorrect status info to print on some nodes.
- Remove statement that snapshots cannot be tagged from lvm man page.
- Disallow changing cluster attribute of VG while RAID LVs are active.
- Fix lvconvert error message for non-mergeable volumes.
- Allow subset of failed devices to be replaced in RAID LVs.
- Prevent resume from creating error devices that already exist from suspend.
- Update and correct lvs man page with supported column names.
- Handle replacement of an active device that goes missing with an error device.
- Change change raid1 segtype always to request a flush when suspending.
- Add udev info and context to lvmdump.
- Add lvmetad man page.
- Fix RAID device replacement code so that it works under snapshot.
- Fix inability to split RAID1 image while specifying a particular PV.
- Update man pages to give them all the same look&feel.
- Fix lvresize of thin pool for striped devices.
- For lvresize round upward when specifying number of extents.
- For lvcreate with %%FREE support rounding downward stripe alignment.
- Change message severity to log_very_verbose for missing dev info in udev db.
- Fix lvconvert when specifying removal of a RAID device other than last one.
- Fix ability to handle failures in mirrored log in dmeventd plugin. (2.02.89)
- Fix unlocking volume group in vgreduce in error path.
- Cope when VG name is part of the supplied name in lvconvert --splitmirrors -n.
- Fix exclusive lvchange running from other node. (2.02.89)
- Add 'vgscan --cache' functionality for consistency with 'pvscan --cache'.
- Keep exclusive activation in pvmove if LV is already active.
- Disallow exclusive pvmove if some affected LVs are not exclusively activated.
- Remove unused and wrongly set cluster VG flag from clvmd lock query command.
- Fix pvmove for exclusively activated LV pvmove in clustered VG. (2.02.86)
- Update and fix monitoring of thin pool devices.
- Check hash insert success in lock_vg in clvmd.
- Check for buffer overwrite in get_cluster_type() in clvmd.
- Fix global/detect_internal_vg_cache_corruption config check.
- Fix initializiation of thin monitoring. (2.02.92)
- Cope with improperly formatted device numbers in /proc/devices. (2.02.91)
- Exit if LISTEN_PID environment variable incorrect in lvmetad systemd handover.
- Fix fsadm propagation of -e option.
- Fix fsadm parsing of /proc/mounts files (don't check for substrings).
- Fix fsadm usage of arguments with space.
- Fix arg_int_value alongside ARG_GROUPABLE --major/--minor for lvcreate/change.
- Fix name conflicts that prevent down-converting RAID1 when specifying a device
- Improve thin_check option passing and use configured path.
- Add --with-thin-check configure option for path to thin_check.
- Fix error message when pvmove LV activation fails with name already in use.
- Better structure layout for device_info in dev_subsystem_name().
- Change message severity for creation of VG over uninitialised devices.
- Fix error path for failed toolcontext creation.
- Don't unlink socket on lvmetad shutdown if instantiated from systemd.
- Restart lvmetad automatically from systemd if it exits from uncaught signal.
- Fix warn msg for thin pool chunk size and update man for chunksize. (2.02.89)

* Thu Jun 07 2012 Kay Sievers - 2.02.95-8
- Remove explicit Requires: libudev, rpm takes care of that:
    $ rpm -q --requires device-mapper | grep udev
    libudev.so...

* Tue Jun 05 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-7
- Use BuildRequires: systemd-devel instead of BuildRequires: libudev-devel.
- Remove unsupported udev_get_dev_path libudev call used for checking udev dir.

* Thu Mar 29 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.95-6
- BuildRequires and Requires on newer version of corosync and dlm.
- Restart clvmd on upgrades.

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-5
- Do not strictly require openais for cmirror subpackage.

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-4
- Reinstate cmirror support.
- Detect lvm binary path in lvmetad udev rules.
- Use pvscan --cache instead of vgscan in systemd units/init scripts.

* Fri Mar 16 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.95-3
- Rebuild against new corosync (soname change).
- BuildRequires and Requires on newer version of corosync.

* Thu Mar 08 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-2
- Reload dm-event systemd service on upgrade.

* Tue Mar 06 2012 Alasdair Kergon <agk@redhat.com> - 2.02.95-1
- If unspecified, adjust thin pool metadata and chunk size to fit into 128MB.
- Deactivation of failed thin check on thin pool returns success.
- Check for multiply-mangled names in auto mangling mode.
- Fix dm_task_get_name_unmangled to not unmangle already unmangled name.
- Check whether device names are properly mangled on ioctl return.

* Sat Mar 03 2012 Alasdair Kergon <agk@redhat.com> - 2.02.94-1
- Add support to execute thin_check with each de/active of thin pool.
- Fix automatic estimation of metadata device size for thin pool.
- Wipe initial 4KiB of non zeroed thin volumes.
- Update code-base to incorporate new metadata daemon. (Not used in Fedora yet.)
- Numerous minor cleanups across the code-base.
- Fix dmsetup / dm_task_set_name to properly resolve path to dm name. (2.02.93)

* Thu Feb 23 2012 Alasdair Kergon <agk@redhat.com> - 2.02.93-1
- Moved systemd tmpfiles installation upstream for lvm2 lock and run dirs.
- Require number of stripes to be greater than parity devices in higher RAID.
- Fix allocation code to allow replacement of single RAID 4/5/6 device.
- Check all tags and LV names are in a valid form before writing any metadata.
- Allow 'lvconvert --repair' to operate on RAID 4/5/6.
- Fix build_parallel_areas_from_lv to account correctly for raid parity devices.
- Print message when faulty raid devices have been replaced.

* Mon Feb 20 2012 Alasdair Kergon <agk@redhat.com> - 2.02.92-1
- Read dmeventd monitoring config settings for every lvm command.
- For thin devices, initialize monitoring only for thin pools not thin volumes.
- Make conversion from a synced 'mirror' to 'raid1' not cause a full resync.
- Add clvmd init dependency on dlm service when running with new corosync.
- Switch to using built-in blkid in 13-dm-disk.rules.
- Add "watch" rule to 13-dm-disk.rules.
- Detect failing fifo and skip 20s retry communication period.
- Replace any '\' char with '\\' in dm table specification on input.
- New 'mangle' options in dmsetup/libdevmapper for transparent reversible 
  encoding of characters that udev forbids in device names.
- Add --manglename option to dmsetup to select the name mangling mode.
- Add mangle command to dmsetup to provide renaming to correct mangled form.
- Add 'mangled_name' and 'unmangled_name' fields to dmsetup info -c -o.
- Mangle device name on dm_task_set_name/newname call if necessary.
- Add dm_task_get_name_mangled/unmangled to libdevmapper.
- Add dm_set/get_name_mangling_mode to set/get name mangling in libdevmapper.

* Mon Feb 13 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.91-2
- Add configure --with-systemdsystemunitdir.

* Sun Feb 12 2012 Alasdair Kergon <agk@redhat.com> - 2.02.91-1
- New upstream with trivial fixes and refactoring of some lvmcache and orphan code.

* Wed Feb 1 2012 Alasdair Kergon <agk@redhat.com> - 2.02.90-1
- Drop support for cman, openais and cmirror for f17. Require dlm not cluster.
- Automatically detect whether corosync clvmd needs to use confdb or cmap.
- Disable partial activation for thin LVs and LVs with all missing segments.
- sync_local_dev_names before (re)activating mirror log for initialisation.
- Do not print warning for pv_min_size between 512KB and 2MB.
- Clean up systemd unit ordering and requirements.
- Allow ALLOC_NORMAL to track reserved extents for log and data on same PV.
- Fix data%% report for thin volume used as origin for non-thin snapshot.

* Thu Jan 26 2012 Alasdair Kergon <agk@redhat.com> - 2.02.89-2
- New upstream release with experimental support for thinly-provisioned devices.
- The changelog for this release is quite long and contained in 
  WHATS_NEW and WHATS_NEW_DM in the documentation directory.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.02.88-2
- update util-linux-ng -> util-linux dependency as it changed long ago.

* Mon Aug 22 2011 Alasdair Kergon <agk@redhat.com> - 2.02.88-1
- Remove incorrect 'Breaking' error message from allocation code. (2.02.87)
- Add lvconvert --merge support for raid1 devices split with --trackchanges.
- Add --trackchanges support to lvconvert --splitmirrors option for raid1.
- Add dm_tree_node_add_null_area for temporarily-missing raid devs tracked.
- Support lvconvert of -m1 raid1 devices to a higher number.
- Support splitting off a single raid1 rimage in lvconvert --splitmirrors.
- Add -V as short form of --virtualsize in lvcreate.

* Fri Aug 12 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.87-1
- Cache and share generated VG structs to improve performance.
- Suppress locking error messages in monitoring init scripts.
- Add global/detect_internal_vg_cache_corruption to lvm.conf.
- If pipe in clvmd fails return busy instead of using uninitialised descriptors.
- Initialise clvmd locks before lvm context to avoid open descriptor leaks.
- Suppress low-level locking errors and warnings while using --sysinit.
- Add test for fcntl error in singlenode client code.
- Compare file size (as well as timestamp) to detect changed config file.
- Change DEFAULT_UDEV_SYNC to 1 so udev_sync is used if there is no config file.
- Update udev rules to skip DM flags decoding for removed devices.
- Remove device name prefix from dmsetup line output if -j & -m or -u supplied.
- Add new segtype 'raid' for MD RAID 1/4/5/6 support with dmeventd plugin.
- Add ability to reduce the number of mirrors in raid1 arrays to lvconvert.
- Add support for systemd file descriptor handover in dmeventd.
- Add systemd unit file to provide lvm2 monitoring.
- Add systemd unit files for dmeventd.
- Use new oom killer adjustment interface (oom_score_adj) when available.
- Fix read-only identical table reload supression.
- Remove --force option from lvrename manpage.

* Wed Aug 03 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-5
- Change DEFAULT_UDEV_SYNC to 1 so udev_sync is used even without any config.

* Thu Jul 28 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-4
- Add support for systemd file descriptor handover to dmeventd.
- Add support for new oom killer adjustment interface (oom_score_adj).

* Wed Jul 20 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-3
- Fix broken lvm2-sysinit Requires: lvm2 dependency.

* Mon Jul 18 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-2
- Add dm-event and lvm2-monitor unit files for use with systemd.
- Add sysvinit subpackage for legacy SysV init script support.

* Fri Jul 8 2011 Alasdair Kergon <agk@redhat.com> - 2.02.86-1
- Fix activation sequences to avoid trapped I/O with multiple LVs.
- Fix activation sequences to avoid allocating tables while devs suspended.
- Remove unnecessary warning in pvcreate for MD linear devices.
- Add activation/checks to lvm.conf to perform additional ioctl validation.
- Append 'm' attribute to pv_attr for missing PVs.
- Fix to preserve exclusive activation of mirror while up-converting.
- Reject allocation if number of extents is not divisible by area count.
- Fix cluster mirror creation to work with new mirror allocation algorithm.
- Ignore activation/verify_udev_operations if dm kernel driver vsn < 4.18.
- Add activation/verify_udev_operations to lvm.conf, disabled by default.
- Ignore inconsistent pre-commit metadata on MISSING_PV devs while activating.
- Add proper udev library context initialization and finalization to liblvm.
- Downgrade critical_section errors to debug level until it is moved to libdm.
- Fix ignored background polling default in vgchange -ay.
- Fix reduction of mirrors with striped segments to always align to stripe size.
- Validate mirror segments size.
- Fix extent rounding for striped volumes never to reduce more than requested.
- Fix create_temp_name to replace any '/' found in the hostname with '?'.
- Always use append to file in lvmdump. selinux policy may ban file truncation.
- Propagate test mode to clvmd to skip activation and changes to held locks.
- Permit --available with lvcreate so non-snapshot LVs need not be activated.
- Clarify error message when unable to convert an LV into a snapshot of an LV.
- Do not issue an error message when unable to remove .cache on read-only fs.
- Avoid memlock size mismatch by preallocating stdio line buffers.
- Report internal error if suspending a device using an already-suspended dev.
- Report internal error if any table is loaded while any dev is known suspended.
- Report error if a table load requiring target parameters has none supplied.
- Add dmsetup --checks and dm_task_enable_checks framework to validate ioctls.
- Add age_in_minutes parameter to dmsetup udevcomplete_all.
- Disable udev fallback by default and add --verifyudev option to dmsetup.
- Add dm_get_suspended_counter() for number of devs in suspended state by lib.
- Fix "all" report field prefix matching to include label fields with pv_all.
- Delay resuming new preloaded mirror devices with core logs in deptree code.

* Wed Jun 22 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-3
- Updated uname string test.

* Sat Jun 4 2011 Milan Broz <mbroz@redhat.com> - 2.02.84-2
- Accept kernel 3.0 uname string in libdevmapper initialization.
- Make systemd initscripts configurable.

* Wed Feb 9 2011 Alasdair Kergon <agk@redhat.com> - 2.02.84-1
- Fix big-endian CRC32 checksumming broken since 2.02.75.  If affected,
  ensure metadata backups in /etc/lvm/backup are up-to-date (vgcfgbackup)
  then after updating to 2.02.84 restore metadata from them (using pvcreate
  with -Zn --restorefile and -u if PVs can no longer be seen, then
  vgcfgrestore -f).
- Reinstate libdevmapper DEBUG_MEM support. (Removed in 1.02.62.)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 4 2011 Alasdair Kergon <agk@redhat.com> - 2.02.83-1
- Allow exclusive activation of snapshots in a cluster.
- Don't lose LV exclusive lock state when suspending clustered devices.
- Fix fs operation stack handling when multiple operations on same device.
- Increase hash table sizes to 1024 LV names and 64 PV uuids.
- When setting up mda wipe first 4k of it as was intended.
- Remove unneeded checks for open_count in lv_info().
- Synchronize with udev before checking open_count in lv_info().
- Add "dmsetup ls --tree" output to lvmdump.
- Fix udev synchronization with no-locking --sysinit (2.02.80).
- Improve man page style consistency for pvcreate, pvremove, pvresize, pvscan.
- Avoid rebuilding of uuid validation table.
- Improve lvcreate error text from insufficient "extents" to "free space".
- Always use O_DIRECT when opening block devices to check for partitioning.
- Move creation of device nodes from 'create' to 'resume'.
- Add --addnodeonresume and --addnodeoncreate options to dmsetup.
- Add dm_task_set_add_node to libdevmapper to control dev node creation time.
- Add dm_task_secure_data to libdevmapper to wipe ioctl buffers in kernel.
- Log debug message when expected uevent is not generated.
- Set DM_UDEV_DISABLE_OTHER_RULES_FLAG for suspended DM devices in udev rules.
- Begin a new pool object for each row in _output_as_rows() correctly.

* Mon Jan 24 2011 Alasdair Kergon <agk@redhat.com> - 2.02.82-2
- Bring lvscan man page up-to-date.
- Fix lvchange --test to exit cleanly.
- Add change_tag to toollib.
- Allow multiple pvchange command line options to be specified together.
- Do not fail pvmove polling if another process cleaned up first.
- Avoid clvmd incrementing dlm lockspace reference count more than once.
- Add -f (don't fork) option to clvmd and fix clvmd -d<num> description.

* Mon Jan 17 2011 Alasdair Kergon <agk@redhat.com> - 2.02.81-1
- Add disk to allowed mirrored log type conversions.
- Accept fusion fio in device type filter.
- Speed up command processing by caching resolved config tree.
- Use same dm cookie for consecutive dm ops in same VG to reduce udev waits.
- Do not scan devices in dev_reset_error_count() when forking.
- Skip unnecessary LOCK_NULL unlock call during volume deactivation.
- Skip fs_unlock when calling exec_cmd within activation code (for modprobe).
- Replace fs_unlock by sync_local_dev_names to notify local clvmd. (2.02.80)
- Fix wrongly paired unlocking of VG_GLOBAL in pvchange. (2.02.66)
- Return 0 from cmirrord initscript 'start' if daemon is already running.
- Add DM_COOKIE_AUTO_CREATE to libdevmapper.h.
- Improve general lvconvert man page description.
- Detect NULL handle in get_property().
- Fix memory leak in persistent filter creation error path.
- Check for errors setting up dm_task struct in _setup_task().
- Fail polldaemon creation when lvmcache_init() fails.
- Return PERCENT_INVALID for errors in _copy_percent() and _snap_percent().
- Detect errors from dm_task_set calls in _get_device_info (dmeventd).
- Fix memory leak in debug mode of restart_clvmd() error path.
- Log error message for pthread_join() failure in clvmd.
- Use tmpfiles.d/lvm2.conf to create /var/lock/lvm and /var/run/lvm at boot.
- Require initscripts for tmpfiles.d/lvm2.conf.

* Tue Dec 21 2010 Alasdair Kergon <agk@redhat.com> - 2.02.79-1
- Create /var/run/lvm directory during clvmd initialisation if missing.
- Avoid revalidating the label cache immediately after scanning.
- Support scanning for a single VG in independent mdas.
- Don't skip full scan when independent mdas are present even if memlock is set.
- Add copy_percent and snap_percent to liblvm.
- Add new dm_prepare_selinux_context fn to libdevmapper and use it throughout.
- Enhance vg_validate to ensure integrity of LV and PV structs referenced.
- Enhance vg_validate to check composition of pvmove LVs.
- Avoid writing to freed memory in vg_release.  (2.02.78)
- Add missing test for reallocation error in _find_parallel_space().
- Add checks for allocation errors in config node cloning.
- Fix error path if regex engine cannot be created in _build_matcher().
- Check read() and close() results in _get_cmdline().
- Fix NULL pointer check in error path in clvmd do_command(). (2.02.78)
- Check for unlink failure in remove_lockfile() in dmeventd.
- Use dm_free for dm_malloc-ed areas in _clog_ctr/_clog_dtr in cmirrord.
- Change dm_regex_create() API to accept const char * const *patterns.

* Mon Dec 6 2010 Alasdair Kergon <agk@redhat.com> - 2.02.78-1
- Miscellaneous error path corrections and minor leaks fixed.
- Avoid misleading PV missing warnings in vgextend --restoremissing.
- Ignore unrecognised allocation policy found in metadata instead of aborting.
- Disallow lvconvert ops that both allocate & free supplied PEs in a single cmd.
- Fix liblvm seg_size to give bytes not sectors.
- Add functions to look up LV/PV by name/uuid to liblvm.
- Suppress 'No PV label' message when removing several PVs without mdas.
- Fix default /etc/lvm permissions to be 0755. (2.02.66)

* Mon Nov 22 2010 Alasdair Kergon <agk@redhat.com> - 2.02.77-1
- Add PV and LV segment types and functions to liblvm.
- Add set_property functions to liblvm.
- Remove tag length restriction and allow / = ! : # & characters.
- Support repetition of --addtag and --deltag arguments.
- Add infrastructure for specific cmdline arguments to be repeated in groups.
- Fix fsadm no longer to require '-f' to resize an unmounted filesystem.
- Fix fsadm to detect mounted filesystems on older systems. (2.0.75)
- Extend cling allocation policy to recognise PV tags (cling_by_tags).
- Add allocation/cling_tag_list to lvm.conf.

* Tue Nov 9 2010 Alasdair Kergon <agk@redhat.com> - 2.02.76-1
- Clarify error messages when activation fails due to activation filter use.
- Fix handling of online filesystem resize (using new fsadm return code).
- Modify fsadm to return different status code for check of mounted filesystem.
- Add DIAGNOSTICS section to fsadm man page.
- Update VG metadata only once in vgchange when making multiple changes.
- Allow independent vgchange arguments to be used together.
- Fix vgchange to process -a, --refresh, --monitor and --poll like lvchange.
- Add dmeventd -R to restart dmeventd without losing monitoring state. (1.02.56)
- Automatically unmount invalidated snapshots in dmeventd.
- Add lvm2app functions to query any pv, vg, or lv property / report field.
- Fix a deadlock caused by double close in clvmd.
- Fix NULL pointer dereference on too-large MDA error path in _vg_read_raw_area.
- Fix regex optimiser not to ignore RHS of OR nodes in _find_leftmost_common.
- Fix memory leak of field_id in _output_field function.
- Allocate buffer for reporting functions dynamically to support long outputs.

* Mon Oct 25 2010 Alasdair Kergon <agk@redhat.com> - 2.02.75-1
- Fix pthread mutex usage deadlock in clvmd.
- Avoid segfault by limiting partial mode for lvm1 metadata. (2.02.74)
- Skip dm devices in scan if they contain only error targets or are empty.
- Don't take write lock in vgchange --refresh, --poll or --monitor.
- Fix hang when repairing a mirrored-log that had both devs fail.
- Speed up unquoting of quoted double quotes and backslashes.
- Speed up CRC32 calculations by using a larger lookup table.
- Implement dmeventd -R to restart without state loss.
- Add --setuuid to dmsetup rename.
- Add global/metadata_read_only to use unrepaired metadata in read-only cmds.
- Automatically extend snapshots with dmeventd according to policy in lvm.conf.
- Add activation/snapshot_autoextend_threshold/percent to lvm.conf.
- Add devices/disable_after_error_count config to limit access to failing devs.
- Implement vgextend --restoremissing to reinstate missing devs that return.
- Read whole /proc/self/maps file before working with maps entries.
- Convey need for snapshot-merge target in lvconvert error message and man page.
- Give correct error message when creating a too-small snapshot.
- Make lvconvert respect --yes and --force when converting an inactive log.
- Better support of noninteractive shell execution of fsadm.
- Fix usage of --yes flag for ReiserFS resize in fsadm.
- Fix detection of mounted filesystems for fsadm when udev is used.
- Fix assignment of default value to LVM variable in fsadm.
- Fix support for --yes flag for fsadm.
- Do not execute lvresize from fsadm --dry-run.
- Fix fsadm return error code from user's break action.
- Return const pointer from dm_basename() in libdevmapper.
- Add dm_zalloc and use it and dm_pool_zalloc throughout.
- Add dm_task_set_newuuid to set uuid of mapped device post-creation.
- Fix missing variable initialization in cluster_send() function from cmirrord.
- Fix pointer for VG name in _pv_resize_single error code path.
- Fix vg_read memory leak with directory-based metadata.
- Fix memory leak of config_tree in reinitialization code path.
- Fix pool destruction order in dmeventd_lvm2_exit() to avoid leak debug mesg.
- Remove dependency on libm by replacing floor() by an integer-based algorithm.
- Refactor and add 'get' functions for pv, vg and lv properties/fields.
- Add pv_get_property and create generic internal _get_property function.
- Make generic GET_*_PROPERTY_FN macros with secondary macro for vg, pv & lv.

* Fri Oct 15 2010 Alasdair Kergon <agk@redhat.com> - 2.02.73-3
- Add --setuuid to dmsetup rename.
- Add dm_task_set_newuuid to set uuid of mapped device post-creation.

* Wed Sep 29 2010 jkeating - 2.02.74-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Alasdair Kergon <agk@redhat.com> - 2.02.74-1
- Fix the way regions are marked complete to avoid slow --nosync cmirror I/O.
- Add DM_REPORT_FIELD_TYPE_ID_LEN to libdevmapper.h.
- Allow : and @ to be escaped with \ in device names of PVs.
- Avoid stack corruption when reading in large metadata.
- Fix partial mode operations for lvm1 metadata format.
- Track recursive filter iteration to avoid refreshing while in use. (2.02.56)
- Allocate buffer for metadata tags dynamically to remove 4k limit.
- Add random suffix to archive file names to prevent races when being created.
- Reinitialize archive and backup handling on toolcontext refresh.
- Make poll_mirror_progress report PROGRESS_CHECK_FAILED if LV is not a mirror.
- Like mirrors, don't scan origins if ignore_suspended_devices() is set.
- Automatically generate tailored LSB Requires-Start for clvmd init script.
- Fix return code of pvmove --abort PV.
- Fix pvmove --abort to remove even for empty pvmove LV.
- Add implementation for simple numeric 'get' property functions.
- Simplify MD/swap signature detection in pvcreate and allow aborting.
- Allow --yes to be used without --force mode.
- Fix file descriptor leak in swap signature detection error path.
- Detect and allow abort in pvcreate if LUKS signature is detected.

* Wed Aug 25 2010 Peter Rajnoha <prajnoha@redhat.com> - 2.02.73-2
- Add configure --with-default-data-alignment.
- Update heuristic used for default and detected data alignment.
- Add "devices/default_data_alignment" to lvm.conf.

* Wed Aug 18 2010 Alasdair Kergon <agk@redhat.com> - 2.02.73-1
- Change default alignment of data extents to 1MB.
- Add --norestorefile option to pvcreate.
- Require --restorefile when using pvcreate --uuid.
- Fix potential for corruption during cluster mirror device failure.
- Ignore snapshots when performing mirror recovery beneath an origin.
- Monitor origin -real device below snapshot instead of overlay device.
- Don't really change monitoring status when in test mode.
- Fix some exit statuses when starting/stopping monitoring fails.
- Enable snapshot monitoring by default when dmeventd is enabled.
- Fix 'lvconvert --splitmirrors' in cluster operation.
- Fix clvmd init script exit code to return 4 when executed as non-root user.
- Recognise and give preference to md device partitions (blkext major).
- Never scan internal LVM devices.
- Don't ignore user-specified PVs in split-mirror operations. (2.02.71)
- Fix data corruption bug in cluster mirrors.
- Require logical volume(s) to be explicitly named for lvconvert --merge.
- Avoid changing aligned pe_start as a side-effect of a log message.
- Use built-in rule for device aliases: block/ < dm- < disk/ < mapper/ < other.
- Handle failure of all mirrored log devices and all but one mirror leg. 
- Disallow 'mirrored' log type for cluster mirrors.
- Fix configure to supply DEFAULT_RUN_DIR to Makefiles.
- Fix allocation of wrong number of mirror logs with 'remove' fault policy.
- Add dmeventd/executable to lvm.conf to test alternative dmeventd.
- Fix udev rules to support udev database content generated by older rules.
- Reinstate detection of inappropriate uevent with DISK_RO set and suppress it.
- Fix regex ttree off-by-one error.
- Fix segfault in regex matcher with characters of ordinal value > 127.
- Wait for node creation before displaying debug info in dmsetup.
- Fix return status 0 for "dmsetup info -c -o help".

* Mon Aug 2 2010 Alasdair Kergon <agk@redhat.com> - 2.02.72-5
- Make udev configurable and merge with f12.

* Mon Aug 2 2010 Alasdair Kergon <agk@redhat.com> - 2.02.72-4
- Merge f13, f14 and rawhide spec files.

* Sat Jul 31 2010 Alasdair Kergon <agk@redhat.com> - 2.02.72-3
- Address lvm2-cluster security flaw CVE-2010-2526.
    https://bugzilla.redhat.com/CVE-2010-2526
- Change clvmd to communicate with lvm2 via a socket in /var/run/lvm.
- Return controlled error if clvmd is run by non-root user.
- Never use clvmd singlenode unless explicitly requested with -Isinglenode.
- Fix exported_symbols generation to use standard compiler arguments.
- Use #include <> not "" in lvm2app.h which gets installed on the system.
- Make liblvm.device-mapper wait for include file generation.
- Fix configure to supply DEFAULT_RUN_DIR to Makefiles.
- Fix wrong number of mirror log at allocate policy

* Wed Jul 28 2010 Alasdair Kergon <agk@redhat.com> - 2.02.71-1
- Make vgck warn about missing PVs.
- Revert failed table load preparation after "create, load and resume".
- Check if cluster log daemon is running before allowing cmirror create.
- Add dm_create_lockfile to libdm and use for pidfiles for all daemons.
- Correct LV list order used by lvconvert when splitting a mirror.
- Check if LV with specified name already exists when splitting a mirror.
- Fix suspend/resume logic for LVs resulting from splitting a mirror.
- Fix possible hang when all mirror images of a mirrored log fail.
- Adjust auto-metadata repair and caching logic to try to cope with empty mdas.
- Update pvcreate, {pv|vg}change, and lvm.conf man pages about metadataignore.
- Prompt if metadataignore with vgextend or pvchange would adjust vg_mda_copies.
- Adjust vg_mda_copies if metadataignore given with vgextend or pvchange.
- Speed up the regex matcher.
- Use "nowatch" udev rule for inappropriate devices.
- Document LVM fault handling in lvm_fault_handling.txt.
- Clarify help text for vg_mda_count.
- Add more verbose messages while checking volume_list and hosttags settings.
- Add log_error when strdup fails in {vg|lv}_change_tag().
- Do not log backtrace in valid _lv_resume() code path.

* Wed Jul 7 2010 Alasdair Kergon <agk@redhat.com> - 2.02.70-1
- Remove log directly if all mirror images of a mirrored log fail.
- Randomly select which mdas to use or ignore.
- Add printf format attributes to yes_no_prompt and fix a caller.
- Always pass unsuspended dm devices through persistent filter to other filters.
- Move test for suspended dm devices ahead of other filters.
- Fix another segfault in clvmd -R if no response from daemon received. (2.02.68)
- Remove superfluous suspended device counter from clvmd.
- Fix lvm shell crash when input is entirely whitespace.
- Update partial mode warning message.
- Preserve memlock balance in clvmd when activation triggers a resume.
- Restore the removemissing behaviour of lvconvert --repair --use-policies.

* Wed Jun 30 2010 Alasdair Kergon <agk@redhat.com> - 2.02.69-1
- Fix vgremove to allow removal of VG with missing PVs. (2.02.52)
- Add metadata/vgmetadatacopies to lvm.conf.
- Add --metadataignore to pvcreate and vgextend.
- Add vg_mda_copies, pv_mda_used_count and vg_mda_used_count to reports.
- Describe --vgmetadatacopies in lvm.conf and other man pages.
- Add --[vg]metadatacopies to select number of mdas to use in a VG.
- Make the metadata ignore bit control read/write metadata areas in a PV.
- Add pvchange --metadataignore to set or clear a metadata ignore bit.
- Refactor metadata code to prepare for --metadataignore / --vgmetadatacopies.
- Ensure region_size of mirrored log does not exceed its full size.
- Preload libc locale messages to prevent reading it in memory locked state.
- Fix handling of simultaneous mirror image and mirrored log image failure.

* Thu Jun 24 2010 Peter Rajnoha <prajnoha@redhat.com> - 2.02.68-2
- Fix udev rules to handle spurious events properly.
- Add Requires: udev >= 158-1 (needed for the change in udev rules).

* Wed Jun 23 2010 Alasdair Kergon <agk@redhat.com> - 2.02.68-1
- Have device-mapper-libs require device-mapper (circular) for udev rules.
- Clear exec_prefix.
- Use early udev synchronisation and update of dev nodes for clustered mirrors.
- Add lv_path to reports to offer full /dev pathname.
- Avoid abort when generating cmirror status.
- Fix clvmd initscript status to print only active clustered LVs.
- Fix segfault in clvmd -R if no response from daemon received.
- Honour log argument when down-converting stacked mirror.
- Sleep to workaround clvmd -S race: socket closed early and server drops cmd.
- Exit successfully when using -o help (but not -o +help) with LVM reports.
- Add man pages for lvmconf, dmeventd and non-existent lvmsadc and lvmsar tools.
- Add --force, --nofsck and --resizefs to lvresize/extend/reduce man pages.
- Fix lvm2cmd example in documentation.
- Fix typo in warning message about missing device with allocated data areas.
- Add device name and offset to raw_read_mda_header error messages.
- Allow use of lvm2app and lvm2cmd headers in C++ code.

* Fri Jun 4 2010 Alasdair Kergon <agk@redhat.com> - 2.02.67-1
- Require partial option in lvchange --refresh for partial LVs.
- Don't merge unchanged persistent cache file before dumping if tool scanned.
- Avoid selecting names under /dev/block if there is an alternative.
- Fix semctl parameter (union) to avoid misaligned parameter on some arches.
- Fix clvmd initscript restart command to start clvmd if not yet running.
- Handle failed restart of clvmd using -S switch properly.
- Use built-in absolute paths in clvmd (clvmd restart and PV and LV queries).
- Consistently return ECMD_FAILED if interrupted processing multiple LVs.
- Add --type parameter description to the lvcreate man page.
- Document 'clear' in dmsetup man page.
- Replace strncmp kernel version number checks with proper ones.
- Update clustered log kernel module name to log-userspace for 2.6.31 onwards.
- Support autoloading of dm-mod module for kernels from 2.6.35.
- Add dm_tree_node_set_presuspend_node() to presuspend child when deactivating.
- Do not fail lvm_init() if init_logging() or _init_rand() generates an errno.
- Fix incorrect memory pool deallocation while using vg_read for files.

* Thu May 20 2010 Alasdair Kergon <agk@redhat.com> - 2.02.66-2
- Simplify and fix Requires package headers.
- If unable to obtain snapshot percentage leave value blank on reports.
- Use new install_system_dirs and install_initscripts makefile targets.
- Add lvm2app functions to lookup a vgname from a pvid and pvname.
- Change internal processing of PVs in pvchange.
- Validate internal lock ordering of orphan and VG_GLOBAL locks.

* Mon May 17 2010 Alasdair Kergon <agk@redhat.com> - 2.02.65-1
- Disallow vgchange --clustered if there are active mirrors or snapshots.
- Fix truncated total size displayed by pvscan.
- Skip internal lvm devices in scan if ignore_suspended_devices is set.
- Do not merge old device cache after we run full scan. (2.02.56)
- Add new --sysinit compound option to vgchange and lvchange.
- Fix clvmd init script never to deactivate non-clustered volume groups.
- Drop duplicate errors for read failures and missing devices to verbose level.
- Do not print encryption key in message debug output (cryptsetup luksResume).
- Use -d to control level of messages sent to syslog by dmeventd.
- Change -d to -f to run dmeventd in foreground.
- Fix udev flags on remove in create_and_load error path.
- Add dm_list_splice() function to join two lists together.
- Use /bin/bash for scripts with bashisms.
- Switch Libs.private to Requires.private in devmapper.pc and lvm2app.pc.
- Use pkgconfig Requires.private for devmapper-event.pc.

* Fri Apr 30 2010 Alasdair Kergon <agk@redhat.com> - 2.02.64-1
- Avoid pointless initialisation when the 'version' command is run directly.
- Fix memory leak for invalid regex pattern input.
- Display invalid regex pattern for filter configuration in case of error.
- Fix -M and --type to use strings, not pointers that change on config refresh.
- Fix lvconvert error message when existing mirrored LV is not found.
- Set appropriate udev flags for reserved LVs.
- Disallow the direct removal of a merging snapshot.
- Don't preload the origin when removing a snapshot whose merge is pending.
- Disallow the addition of mirror images while a conversion is happening.
- Disallow primary mirror image removal when mirror is not in-sync.
- Remove obsolete --name parameter from vgcfgrestore.
- Add -S command to clvmd to restart the daemon preserving exclusive locks.
- Increment lvm2app version from 1 to 2 (memory allocation changes).
- Change lvm2app memory alloc/free for pv/vg/lv properties.
- Change daemon lock filename from lvm2_monitor to lvm2-monitor for consistency.
- Add support for new IMPORT{db} udev rule.
- Add DM_UDEV_PRIMARY_SOURCE_FLAG udev flag to recognize proper DM events.
- Also include udev libs in libdevmapper.pc.
- Cache bitset locations to speed up _calc_states.
- Add a regex optimisation pass for shared prefixes and suffixes.
- Add dm_bit_and and dm_bitset_equal to libdevmapper.
- Speed up dm_bit_get_next with ffs().

* Thu Apr 15 2010 Alasdair Kergon <agk@redhat.com> - 2.02.63-2
- Remove 'lvmconf --lockinglibdir' from cluster post: locking is now built-in.
- Move libdevmapper-event-lvm2.so to devel package.
- Explicitly specify libdevmapper-event.so* attributes.
- Drop support for upgrades from very old versions that used lvm not lvm2.
- Move libdevmapper-event plug-in libraries into new device-mapper subdirectory.
- Don't verify lvm.conf contents when using rpm --verify.

* Wed Apr 14 2010 Alasdair Kergon <agk@redhat.com> - 2.02.63-1
- Move development links to shared objects to /usr (hard-coded temporarily).
- Change libdevmapper deactivation to fail if device is open.
- Wipe memory buffers for libdevmapper dm-ioctl parameters before releasing.
- Strictly require libudev if udev_sync is used.
- Add support for ioctl's DM_UEVENT_GENERATED_FLAG.
- Allow incomplete mirror restore in lvconvert --repair upon insufficient space.
- Do not reset position in metadata ring buffer on vgrename and vgcfgrestore.
- Allow VGs with active LVs to be renamed.
- Only pass visible LVs to tools in cmdline VG name/tag expansions without -a.
- Use C locale and mlockall in clvmd and dmeventd.
- Mask LCK_HOLD in cluster VG locks for upgrade compatibility with older clvmd.
- Add activation/polling_interval to lvm.conf as --interval default.
- Don't ignore error if resuming any LV fails when resuming groups of LVs.
- Skip closing persistent filter cache file if open failed.
- Permit mimage LVs to be striped in lvcreate, lvresize and lvconvert.
- Fix pvmove allocation to take existing parallel stripes into account.
- Fix incorrect removal of symlinks after LV deactivation fails.
- Fix is_partitioned_dev not to attempt to reopen device.
- Fix another thread race in clvmd.
- Improve vg_validate to detect some loops in lists.
- Change most remaining log_error WARNING messages to log_warn.
- Always use blocking lock for VGs and orphan locks.
- Allocate all memory for segments from private VG mempool.
- Optimise searching PV segments for seeking the most recently-added.
- Remove duplicated vg_validate checks when parsing cached metadata.
- Use hash table of LVs to speed up parsing of text metadata with many LVs.
- Fix two vg_validate messages, adding whitespace and parentheses.
- When dmeventd is not forking because of -d flag, don't kill parent process.
- Fix dso resource leak in error path of dmeventd.
- Fix --alloc contiguous policy only to allocate one set of parallel areas.
- Do not allow {vg|lv}change --ignoremonitoring if on clustered VG.
- Add ability to create mirrored logs for mirror LVs.
- Fix clvmd cluster propagation of dmeventd monitoring mode.
- Allow ALLOC_ANYWHERE to split contiguous areas.
- Add some assertions to allocation code.
- Introduce pv_area_used into allocation algorithm and add debug messages.
- Add activation/monitoring to lvm.conf.
- Add --monitor and --ignoremonitoring to lvcreate.
- Don't allow resizing of internal logical volumes.
- Fix libdevmapper-event pkgconfig version string to match libdevmapper.
- Avoid scanning all pvs in the system if operating on a device with mdas.
- Disable long living process flag in lvm2app library.
- Fix pvcreate device md filter check.
- Suppress repeated errors about the same missing PV uuids.
- Bypass full device scans when using internally-cached VG metadata.
- Only do one full device scan during each read of text format metadata.
- Look up missing PVs by uuid not dev_name in pvs to avoid invalid stat.

* Tue Mar 09 2010 Alasdair Kergon <agk@redhat.com> - 2.02.62-1
- Rewrite clvmd init script.
- Add default alternative to mlockall using mlock to reduce pinned memory size.
- Add use_mlockall and mlock_filter to activation section of lvm.conf.
- Handle misaligned devices that report alignment_offset of -1.
- Extend core allocation code in preparation for mirrored log areas.
- No longer fall back to looking up active devices by name if uuid not found.
- Don't touch /dev in vgmknodes if activation is disabled.
- Add --showkeys parameter description to dmsetup man page.
- Add --help option as synonym for help command.
- Add lvm2app functions lvm_{vg|lv}_{get|add|remove}_tag() functions.
- Refactor snapshot-merge deptree and device removal to support info-by-uuid.

* Fri Mar 05 2010 Peter Rajnoha <prajnoha@redhat.com> - 2.02.61-2
- Change spec file to support excluding cluster components from the build.

* Tue Feb 16 2010 Alasdair Kergon <agk@redhat.com> - 2.02.61-1
- Add %%ORIGIN support to lv{create,extend,reduce,resize} --extents.
- Accept a list of LVs with 'lvconvert --merge @tag' using process_each_lv.
- Remove false "failed to find tree node" error when activating merging origin.
- Exit with success when lvconvert --repair --use-policies performs no action.
- Avoid unnecessary second resync when adding mimage to core-logged mirror.
- Make clvmd -V return status zero.
- Fix cmirrord segfault in clog_cpg list processing when converting mirror log.
- Deactivate temporary pvmove mirror cluster-wide when activating it fails.
- Add missing metadata vg_reverts in pvmove error paths.
- Unlock shared lock in clvmd if activation calls fail.
- Add lvm_pv_get_size, lvm_pv_get_free and lvm_pv_get_dev_size to lvm2app.
- Change lvm2app to return all sizes in bytes as documented (not sectors).
- Exclude internal VG names and uuids from lists returned through lvm2app.
- Add LVM_SUPPRESS_LOCKING_FAILURE_MESSAGES environment variable.
- Add DM_UDEV_DISABLE_LIBRARY_FALLBACK udev flag to rely on udev only.
- Remove hard-coding that skipped _mimage devices from 11-dm-lvm.rules.
- Export dm_udev_create_cookie function to create new cookies on demand.
- Add --udevcookie, udevcreatecookie and udevreleasecookie to dmsetup.
- Set udev state automatically instead of using DM_UDEV_DISABLE_CHECKING.
- Set udev state automatically instead of using LVM_UDEV_DISABLE_CHECKING.
- Remove pointless versioned symlinks to dmeventd plugin libraries.

* Fri Jan 29 2010 Alasdair Kergon <agk@redhat.com> - 2.02.60-5
- Replace spaces with tabs in a couple of places in spec file.

* Sat Jan 23 2010 Alasdair Kergon <agk@redhat.com> - 2.02.60-4
- Extend cmirrord man page.
- Sleep before first progress check iff pvmove/lvconvert interval has prefix '+'.
- Fix cmirror initscript syntax problems.
- Fix first syslog message prefix for dmeventd plugins.
- Make failed locking initialisation messages more descriptive.

* Fri Jan 22 2010 Alasdair Kergon <agk@redhat.com> - 2.02.59-3
- Fix dmeventd lvm2 wrapper (plug-ins unusable in last build).
- Make failed locking initialisation messages more descriptive.

* Fri Jan 22 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.59-2
- Drop duplicated BuildRequires on openaislib-devel.
- Drop Requires on clusterlib for cmirror subpackage.
- clvmd subpackage should Requires cman (#506592).

* Fri Jan 22 2010 Alasdair Kergon <agk@redhat.com> - 2.02.59-1
- Add cmirror subpackage for clustered mirrors.
- Set 'preferred_names' in default lvm.conf.
- Add libdevmapper-event-lvm2.so to serialise dmeventd plugin liblvm2cmd use.
- Stop dmeventd trying to access already-removed snapshots.
- Fix clvmd to never scan suspended devices.
- Fix detection of completed snapshot merge.
- Improve snapshot merge metadata import validation.

* Thu Jan 14 2010 Alasdair Kergon <agk@redhat.com> - 2.02.58-1
- Fix clvmd automatic target module loading crash.
- Fix allocation code not to stop at the first area of a PV that fits.
- Add support for the "snapshot-merge" kernel target (2.6.33-rc1).
- Add --merge to lvconvert to merge a snapshot into its origin.

* Tue Jan 12 2010 Alasdair Kergon <agk@redhat.com> - 2.02.57-1
- Add --splitmirrors to lvconvert to split off part of a mirror.
- Allow vgremove to remove a VG with PVs missing after a prompt.
- Add activation/udev_rules config option in lvm.conf.
- Add --poll flag to vgchange and lvchange to control background daemon launch.
- Impose limit of 8 mirror images to match the in-kernel kcopyd restriction.
- Log failure type and recognise type 'F' (flush) in dmeventd mirror plugin.
- Add --noudevrules option for dmsetup to disable /dev node management by udev.
- Fix 'dmsetup info -c -o all' to show all fields.
- Fix coredump and memory leak for 'dmsetup help -c'.
- Rename mirror_device_fault_policy to mirror_image_fault policy.
- Use extended status of new kernel snapshot target 1.8.0 to detect when empty.
- Allow use of precommitted metadata when a PV is missing.
- Add global/abort_on_internal_errors to lvm.conf to assist testing.
- If aborting due to internal error, always send that message to stderr.
- Keep log type consistent when changing mirror image count.
- Exit with success in lvconvert --repair --use-policies on failed allocation.
- Ensure any background daemon exits without duplicating parent's functionality.
- Change background daemon process names to "(lvm2)".
- Fix internal lock state after forking.
- Remove empty PV devices if lvconvert --repair is using defined policies.
- Use fixed buffer to prevent stack overflow in persistent filter dump.
- Propagate metadata commit and revert notifications to other cluster nodes.
- Fix metadata caching and lock state propagation to remote nodes in clvmd.
- Properly decode all flags in clvmd messages including VG locks.
- Drop cached metadata after device was auto-repaired and removed from VG.
- Clear MISSING_PV flag if PV reappeared and is empty.
- Fix removal of multiple devices from a mirror.
- Also clean up PVs flagged as missing in vgreduce --removemissing --force.
- Fix some pvresize and toollib error paths with missing VG releases/unlocks.
- Explicitly call suspend for temporary mirror layer.
- Add memlock information to do_lock_lv debug output.
- Always bypass calls to remote cluster nodes for non-clustered VGs.
- Permit implicit cluster lock conversion in pre/post callbacks on local node.
- Permit implicit cluster lock conversion to the lock mode already held.
- Fix lock flag masking in clvmd so intended code paths get invoked.
- Remove newly-created mirror log from metadata if initial deactivation fails.
- Improve pvmove error message when all source LVs are skipped.
- Fix memlock imbalance in lv_suspend if already suspended.
- Fix pvmove test mode not to poll (and fail).
- Fix vgcreate error message if VG already exists.
- Fix tools to use log_error when aborted due to user response to prompt.
- Fix ignored readahead setting in lvcreate --readahead.
- Fix clvmd memory leak in lv_info_by_lvid by calling release_vg.
- If LVM_UDEV_DISABLE_CHECKING is set in environment, disable udev warnings.
- If DM_UDEV_DISABLE_CHECKING is set in environment, disable udev warnings.
- Always set environment variables for an LVM2 device in 11-dm-lvm.rules.
- Disable udev rules for change events with DISK_RO set.
- Add dm_tree_add_dev_with_udev_flags to provide wider support for udev flags.
- Correct activated or deactivated text in vgchange summary message.
- Fix fsadm man page typo (fsdam).

* Tue Nov 24 2009 Alasdair Kergon <agk@redhat.com> - 2.02.56-2
- Revert vg_read_internal change as clvmd was not ready for vg_read. (2.02.55)
- Fix unbalanced memory locking when deactivating LVs.
- Add missing vg_release to pvs and pvdisplay to fix memory leak.
- Do not try to unlock VG which is not locked when processing a VG.
- Update .cache file after every full device rescan in clvmd.
- Refresh all device filters (including sysfs) before each full device rescan.
- Return error status if vgchange fails to activate any volume.

* Thu Nov 19 2009 Alasdair Kergon <agk@redhat.com> - 2.02.55-1
- Fix deadlock when changing mirrors due to unpaired memlock refcount changes.
- Fix pvmove region_size overflow for very large PVs.
- Fix lvcreate and lvresize %%PVS argument always to use sensible total size.
- Directly restrict vgchange to activating visible LVs.
- Fix hash lookup segfault when keys compared are different lengths.
- Flush stdout after yes/no prompt.
- Recognise DRBD devices and handle them like md devices.
- Add dmsetup --inactive support (requires kernel support targetted for 2.6.33).

* Fri Nov 13 2009 Peter Rajnoha <prajnoha@redhat.com> - 2.02.54-3
- Support udev flags even when udev_sync is disabled.
- Remove last_rule from udev_rules.
- Udev rules cleanup.

* Tue Nov 3 2009 Peter Rajnoha <prajnoha@redhat.com> - 2.02.54-2
- Enable udev synchronisation code.
- Install default udev rules for device-mapper and LVM2.
- Add BuildRequires: libudev-devel.
- Add Requires: libudev (to check udev is running).
- Add Requires: util-linux-ng (blkid used in udev rules).
- Add Conflicts: dracut < 002-18 (for dracut to install required udev rules)

* Tue Oct 27 2009 Alasdair Kergon <agk@redhat.com> - 2.02.54-1
- Add implict pvcreate support to vgcreate and vgextend.
- Add --pvmetadatacopies for pvcreate, vgcreate, vgextend, vgconvert.
- Distinguish between powers of 1000 and powers of 1024 in unit suffixes.
- Restart lvconverts in vgchange.
- Don't attempt to deactivate an LV if any of its snapshots are in use.
- Return error if lv_deactivate fails to remove device from kernel.
- Treat input units of both 's' and 'S' as 512-byte sectors.  (2.02.49)
- Use standard output units for 'PE Size' and 'Stripe size' in pv/lvdisplay.
- Add global/si_unit_consistency to enable cleaned-up use of units in output.
- Only do lock conversions in clvmd if we are explicitly asked for one.
- Fix clvmd segfault when refresh_toolcontext fails.
- Cleanup mimagetmp LV if allocation fails for new lvconvert mimage.
- Handle metadata with unknown segment types more gracefully.
- Make clvmd return 0 on success rather than 1.
- Correct example.conf to indicate that lvm2 not lvm1 is the default format.
- Delay announcing mirror monitoring to syslog until initialisation succeeded.
- Update lvcreate/lvconvert man pages to explain PhysicalVolume parameter.
- Document --all option in man pages and cleanup {pv|vg|lv}{s|display} pages.

* Mon Oct 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.53-3
- Enable openais support in clvmd.

* Fri Sep 25 2009 Alasdair Kergon <agk@redhat.com> - 2.02.53-2
- Reissued tarball to fix compilation warning from lvm2_log_fn prototype.

* Fri Sep 25 2009 Alasdair Kergon <agk@redhat.com> - 2.02.53-1
- Create any directories in /dev with umask 022. (#507397)
- Handle paths supplied to dm_task_set_name by getting name from /dev/mapper.
- Add splitname and --yes to dmsetup man page.

* Thu Sep 24 2009 Peter Rajnoha <prajnoha@redhat.com> - 2.02.52-4
- Disable udev synchronisation code (revert previous build).

* Mon Sep 21 2009 Peter Rajnoha <prajnoha@redhat.com> - 2.02.52-3
- Enable udev synchronisation code.
- Install default udev rules for device-mapper and LVM2.
- Add BuildRequires: libudev-devel.
- Add Requires: libudev (to check udev is running).
- Add Requires: util-linux-ng (blkid used in udev rules).

* Wed Sep 16 2009 Alasdair Kergon <agk@redhat.com> - 2.02.52-2
- Build dmeventd and place into a separate set of subpackages.
- Remove no-longer-needed BuildRoot tag and buildroot emptying at install.

* Tue Sep 15 2009 Alasdair Kergon <agk@redhat.com> - 2.02.52-1
- Prioritise write locks over read locks by default for file locking.
- Add local lock files with suffix ':aux' to serialise locking requests.
- Fix readonly locking to permit writeable global locks (for vgscan). (2.02.49)
- Make readonly locking available as locking type 4.
- Fix global locking in PV reporting commands (2.02.49).
- Make lvchange --refresh only take a read lock on volume group.
- Fix race where non-blocking file locks could be granted in error.
- Fix pvcreate string termination in duplicate uuid warning message.
- Don't loop reading sysfs with pvcreate on a non-blkext partition (2.02.51).
- Fix vgcfgrestore error paths when locking fails (2.02.49).
- Make clvmd check corosync to see what cluster interface it should use.
- Fix vgextend error path - if ORPHAN lock fails, unlock / release vg (2.02.49).
- Clarify use of PE ranges in lv{convert|create|extend|resize} man pages.
- Restore umask when device node creation fails.
- Check kernel vsn to use 'block_on_error' or 'handle_errors' in mirror table.

* Mon Aug 24 2009 Milan Broz <mbroz@redhat.com> - 2.02.51-3
- Fix global locking in PV reporting commands (2.02.49).
- Fix pvcreate on a partition (2.02.51).
- Build clvmd with both cman and corosync support.

* Thu Aug 6 2009 Alasdair Kergon <agk@redhat.com> - 2.02.51-2
- Fix clvmd locking broken in 2.02.50-1.
- Only change LV /dev symlinks on ACTIVATE not PRELOAD (so not done twice).
- Make lvconvert honour log mirror options combined with downconversion.
- Add devices/data_alignment_detection to lvm.conf.
- Add devices/data_alignment_offset_detection to lvm.conf.
- Add --dataalignmentoffset to pvcreate to shift start of aligned data area.
- Update synopsis in lvconvert manpage to mention --repair.
- Document -I option of clvmd in the man page.

* Thu Jul 30 2009 Alasdair Kergon <agk@redhat.com> - 2.02.50-2
- lvm2-devel requires device-mapper-devel.
- Fix lvm2app.pc filename.

* Tue Jul 28 2009 Alasdair Kergon <agk@redhat.com> - 2.02.50-1
- Add libs and devel subpackages to include shared libraries for applications.
  N.B. The liblvm2app API is not frozen yet and may still be changed
  Send any feedback to the mailing list lvm-devel@redhat.com.
- Remove obsolete --with-dmdir from configure.
- Add global/wait_for_locks to lvm.conf so blocking for locks can be disabled.
- Fix race condition with vgcreate and vgextend on same device since 2.02.49.
- Add an API version number, LVM_LIBAPI, to the VERSION string.
- Return EINVALID_CMD_LINE not success when invalid VG name format is used.
- Remove unnecessary messages after vgcreate/vgsplit code change in 2.02.49.
- Store any errno and error messages issued while processing each command.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Alasdair Kergon <agk@redhat.com> - 2.02.49-1
- Exclude VG_GLOBAL from vg_write_lock_held so scans open devs read-only again.
- Fix dev name mismatch in vgcreate man page example.
- Check md devices for a partition table during device scan.
- Add extended device (blkext) and md partition (mdp) types to filters.
- Make text metadata read errors for segment areas more precise.
- Fix text segment metadata read errors to mention correct segment name.
- Include segment and LV names in text segment import error messages.
- Fix memory leak in vgsplit when re-reading the vg.
- Permit several segment types to be registered by a single shared object.
- Update the man pages to document size units uniformly.
- Allow commandline sizes to be specified in terms of bytes and sectors.
- Update 'md_chunk_alignment' to use stripe-width to align PV data area.
- Fix segfault in vg_release when vg->cmd is NULL.
- Add dm_log_with_errno and dm_log_with_errno_init, deprecating the old fns.
- Fix whitespace in linear target line to fix identical table line detection.
- Add device number to more log messages during activation.

* Fri Jul 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> 2.02.48-2
- BuildRequires and Requires on stable versions of both corosync-lib (1.0.0-1)
  and cluster-lib (3.0.0-20).

* Tue Jun 30 2009 Alasdair Kergon <agk@redhat.com> - 2.02.48-1
- Abort if automatic metadata correction fails when reading VG to update it.
- Don't fallback to default major number in libdm: use dm_task_set_major_minor.
- Explicitly request fallback to default major number in device mapper.
- Ignore suspended devices during repair.
- Suggest using lvchange --resync when adding leg to not-yet-synced mirror.
- Destroy toolcontext on clvmd exit to avoid memory pool leaks.
- Fix lvconvert not to poll mirror if no conversion in progress.
- Fix memory leaks in toolcontext error path.
- Reinstate partial activation support in clustered mode.
- Allow metadata correction even when PVs are missing.
- Use 'lvm lvresize' instead of 'lvresize' in fsadm.
- Do not use '-n' realine option in fsadm for rescue disk compatiblity.
- Round up requested readahead to at least one page and print warning.
- Try to repair vg before actual vgremove when force flag provided.
- Unify error messages when processing inconsistent volume group.
- Introduce lvconvert --use_policies (repair policy according to lvm.conf).
- Fix rename of active snapshot with virtual origin.
- Fix convert polling to ignore LV with different UUID.
- Cache underlying device readahead only before activation calls.
- Fix segfault when calculating readahead on missing device in vgreduce.
- Remove verbose 'visited' messages.
- Handle multi-extent mirror log allocation when smallest PV has only 1 extent.
- Add LSB standard headers and functions (incl. reload) to clvmd initscript.
- When creating new LV, double-check that name is not already in use.
- Remove /dev/vgname/lvname symlink automatically if LV is no longer visible.
- Rename internal vorigin LV to match visible LV.
- Suppress 'removed' messages displayed when internal LVs are removed.
- Fix lvchange -a and -p for sparse LVs.
- Fix lvcreate --virtualsize to activate the new device immediately.
- Make --snapshot optional with lvcreate --virtualsize.
- Generalise --virtualoriginsize to --virtualsize.
- Skip virtual origins in process_each_lv_in_vg() without --all.
- Fix counting of virtual origin LVs in vg_validate.
- Attempt to load dm-zero module if zero target needed but not present.
- Add crypt target handling to libdevmapper tree nodes.
- Add splitname command to dmsetup.
- Add subsystem, vg_name, lv_name, lv_layer fields to dmsetup reports.
- Make mempool optional in dm_split_lvm_name() in libdevmapper.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.47-2
- BuildRequire newer version of corosynclib (0.97-1) to link against
  latest libraries version (soname 4.0.0).
- Add lvm2-2_02_48-cluster-cpg-new-api.patch to port clvmd-corosync
  to new corosync cpg API.

* Fri May 22 2009 Alasdair Kergon <agk@redhat.com> - 2.02.47-1
- Inherit readahead setting from underlying devices during activation.
- Detect LVs active on remote nodes by querying locks if supported.
- Enable online resizing of mirrors.
- Use suspend with flush when device size was changed during table preload.
- Implement query_resource_fn for cluster_locking.
- Support query_resource_fn in locking modules.
- Fix pvmove to revert operation if temporary mirror creation fails.
- Fix metadata export for VG with missing PVs.
- Add vgimportclone and install it and the man page by default.
- Force max_lv restriction only for newly created LV.
- Do not query nonexistent devices for readahead.
- Reject missing PVs from allocation in toollib.
- Fix PV datalignment for values starting prior to MDA area. (2.02.45)
- Add sparse devices: lvcreate -s --virtualoriginsize (hidden zero origin).
- Fix minimum width of devices column in reports.
- Add lvs origin_size field.
- Implement lvconvert --repair for repairing partially-failed mirrors.
- Fix vgreduce --removemissing failure exit code.
- Fix remote metadata backup for clvmd.
- Fix metadata backup to run after vg_commit always.
- Fix pvs report for orphan PVs when segment attributes are requested.
- Fix pvs -a output to not read volume groups from non-PV devices.
- Introduce memory pools per volume group (to reduce memory for large VGs).
- Always return exit error status when locking of volume group fails.
- Fix mirror log convert validation question.
- Enable use of cached metadata for pvs and pvdisplay commands.
- Fix memory leak in mirror allocation code.
- Save and restore the previous logging level when log level is changed.
- Fix error message when archive initialization fails.
- Make sure clvmd-corosync releases the lockspace when it exits.
- Fix segfault for vgcfgrestore on VG with missing PVs.
- Block SIGTERM & SIGINT in clvmd subthreads.
- Detect and conditionally wipe swapspace signatures in pvcreate.
- Fix maximal volume count check for snapshots if max_lv set for volume group.
- Fix lvcreate to remove unused cow volume if the snapshot creation fails.
- Fix error messages when PV uuid or pe_start reading fails.
- Flush memory pool and fix locking in clvmd refresh and backup command.
- Fix unlocks in clvmd-corosync. (2.02.45)
- Fix error message when adding metadata directory to internal list fails.
- Fix size and error message of memory allocation at backup initialization.
- Remove old metadata backup file after renaming VG.
- Restore log_suppress state when metadata backup file is up-to-date.
- Export dm_tree_node_size_changed() from libdevmapper.
- Fix segfault when getopt processes dmsetup -U, -G and -M options.
- Add _smp_mflags to compilation and remove DESTDIR.

* Fri Apr 17 2009 Milan Broz <mbroz@redhat.com> - 2.02.45-4
- Add MMC (mmcblk) device type to filters. (483686)

* Mon Mar 30 2009 Jussi Lehtola <jussi.lehtola@iki.fi> 2.02.45-3
- Add FTP server location to Source0.

* Mon Mar 30 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.45-2
- BuildRequires a newer version of corosync (0.95-2) to fix linking.

* Tue Mar 3 2009 Alasdair Kergon <agk@redhat.com> - 2.02.45-1
- Update clusterlib and corosync dependencies.
- Attempt proper clean up in child before executing fsadm or modprobe.
- Do not scan devices if reporting only attributes from PV label.
- Use pkgconfig to obtain corosync library details during configuration.
- Fix error returns in clvmd-corosync interface to DLM.
- Add --refresh to vgchange and vgmknodes man pages.
- Pass --test from lvresize to fsadm as --dry-run.
- Prevent fsadm from checking mounted filesystems.
- No longer treats any other key as 'no' when prompting in fsadm.
- Add --dataalignment to pvcreate to specify alignment of data area.
- Fix unblocking of interrupts after several commands.
- Provide da and mda locations in debug message when writing text format label.
- Mention the restriction on file descriptors at invocation on the lvm man page.
- Index cached vgmetadata by vgid not vgname to cope with duplicate vgnames.
- No longer require kernel and metadata major numbers to match.
- If kernel supports only one dm major number, use in place of any supplied.
- Add option to /etc/sysconfig/cluster to select cluster type for clvmd.
- Allow clvmd to start up if its lockspace already exists.
- Separate PV label attributes which do not need parse metadata when reporting.
- Remove external dependency on the 'cut' command from fsadm.
- Fix pvs segfault when pv mda attributes requested for unavailable PV.
- Add fsadm support for reszing ext4 filesysystems.
- Change lvm2-cluster to corosync instead of cman.
- Fix some old changelog typos in email addresses.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Alasdair Kergon <agk@redhat.com> - 2.02.44-1
- Add --nameprefixes, --unquoted, --rows to pvs, vgs, lvs man pages.
- Fix lvresize size conversion for fsadm when block size is not 1K.
- Fix pvs segfault when run with orphan PV and some VG fields.
- Display a 'dev_size' of zero for missing devices in reports.
- Add pv_mda_size to pvs and vg_mda_size to vgs.
- Fix lvmdump /sys listing to include virtual devices directory.
- Add "--refresh" functionality to vgchange and vgmknodes.
- Avoid exceeding LV size when wiping device.
- Calculate mirror log size instead of using 1 extent.
- Ensure requested device number is available before activating with it.
- Fix incorrect exit status from 'help <command>'.
- Fix vgrename using UUID if there are VGs with identical names.
- Fix segfault when invalid field given in reporting commands.
- Use better random seed value in temp file creation.
- Add read_urandom to read /dev/urandom. Use in uuid calculation.
- Fix race in vgcreate that would result in second caller overwriting first.
- Fix uninitialised lv_count in vgdisplay -c.
- Don't skip updating pvid hash when lvmcache_info struct got swapped.
- Fix startup race in clvmd.
- Cope with snapshot dependencies when removing a whole VG with lvremove.
- Make man pages and tool help text consistent using | for alternative options.
- Add "all" field to reports expanding to all fields of report type.
- Enforce device name length and character limitations in libdm.

* Mon Nov 10 2008 Alasdair Kergon <agk@redhat.com> - 2.02.43-1
- Upstream merge of device-mapper and lvm2 source.
- Correct prototype for --permission on lvchange and lvcreate man pages.
- Exit with non-zero status from vgdisplay if couldn't show any requested VG.
- libdevmapper.pc: Use simplified x.y.z version number.
- Accept locking fallback_to_* options in the global section as documented.
- Several fixes to lvconvert involving mirrors.
- Avoid overwriting in-use on-disk text metadata when metadataarea fills up.
- Generate man pages from templates and include version.
- Fix misleading error message when there are no allocatable extents in VG.
- Fix handling of PVs which reappeared with old metadata version.
- Fix validation of --minor and --major in lvcreate to require -My always.
- Allow lvremove to remove LVs from VGs with missing PVs.
- In VG with PVs missing, by default allow activation of LVs that are complete.
- Require --force with --removemissing in vgreduce to remove partial LVs.
- No longer write out PARTIAL flag into metadata backups.
- Treat new default activation/missing_stripe_filler "error" as an error target.
- Add devices/md_chunk_alignment to lvm.conf.
- Pass struct physical_volume to pe_align and adjust for md chunk size.
- Avoid shuffling remaining mirror images when removing one, retaining primary.
- Prevent resizing an LV while lvconvert is using it.
- Avoid repeatedly wiping cache while VG_GLOBAL is held in vgscan & pvscan.
- Fix pvresize to not allow resize if PV has two metadata areas.
- Fix setting of volume limit count if converting to lvm1 format.
- Fix vgconvert logical volume id metadata validation.
- Fix lvmdump metadata gather option (-m) to work correctly.
- Fix allocation bug in text metadata format write error path.
- Fix vgcfgbackup to properly check filename if template is used.
- vgremove tries to remove lv snapshot first.
- Improve file descriptor leak detection to display likely culprit and filename.
- Avoid looping forever in _pv_analyze_mda_raw used by pvck.
- Change lvchange exit status to indicate if any part of the operation failed.
- Fix pvchange and pvremove to handle PVs without mdas.
- Fix pvchange -M1 -u to preserve existing extent locations when there's a VG.
- Cease recognising snapshot-in-use percentages returned by early devt kernels.
- Add backward-compatible flags field to on-disk format_text metadata.
- libdevmapper: Only resume devices in dm_tree_preload_children if size changes.
- libdevmapper: Extend deptree buffers so the largest possible device numbers fit.
- libdevmapper: Underline longer report help text headings.

* Tue Oct 7 2008 Alasdair Kergon <agk@redhat.com> - 2.02.39-6
- Only set exec_prefix once and configure explicit directories to work with
  new version of rpm.

* Fri Sep 26 2008 Fabio M. Di Nitto <fdinitto@redhat.cm> - 2.02.39-5
- Add BuildRequires on cmanlib-devel. This is required after libcman split
  from cman and cman-devel into cmanlib and cmanlib-devel.
- Make versioned BuildRequires on cman-devel and cmanlib-devel more strict
  to guarantee to get the right version.

* Thu Sep 25 2008 Fabio M. Di Nitto <fdinitto@redhat.cm> - 2.02.39-5
- Add versioned BuildRequires on new cman-devel.

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.02.39-5
- Change %%patch to %%patch0 to match Patch0 as required by RPM package update.

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.02.39-4
- Fix license tag.

* Fri Jun 27 2008 Alasdair Kergon <agk@redhat.com> - 2.02.39-3
- Fix up cache for PVs without mdas after consistent VG metadata is processed.
- Update validation of safe mirror log type conversions in lvconvert.
- Fix lvconvert to disallow snapshot and mirror combinations.
- Fix reporting of LV fields alongside unallocated PV segments.
- Add --unquoted and --rows to reporting tools.
- Avoid undefined status code after _memlock commands in lvm shell.
- Fix and improve readahead 'auto' calculation for stripe_size.
- Fix lvchange output for -r auto setting if auto is already set.
- Fix add_mirror_images not to dereference uninitialized log_lv upon failure.
- Add --force to lvextend and lvresize.
- Fix vgchange to not activate component mirror volumes directly.

* Wed Jun 25 2008 Alasdair Kergon <agk@redhat.com> - 2.02.38-2
- dmsetup: Add --unquoted and --rows to 'info -c' command.
- libdevmapper: Fix inverted no_flush debug message.

* Fri Jun 13 2008 Alasdair Kergon <agk@redhat.com> - 2.02.38-1
- libdevmapper: Make dm_hash_iter safe against deletion.
- libdevmapper: Accept a NULL pointer to dm_free silently.
- libdevmapper: Calculate string size within dm_pool_grow_object.
- libdevmapper: Send reporting field help text to stderr not stdout.

- dmsetup: Add tables_loaded, readonly and suspended columns to reports.
- dmsetup: Add --nameprefixes for new report output format FIELD=VALUE.

- Add --nameprefixes to reporting tools for field name prefix output format.
- Fix return values for reporting commands when run with no PVs, LVs, or VGs.
- Add omitted unlock_vg() call when sigint_caught() during vg processing.
- Fix free_count when reading pool metadata.
- Fix segfault when using pvcreate on a device containing pool metadata.
- In script-processing mode, stop if any command fails.
- Warn if command exits with non-zero status code without a prior log_error.
- Correct config file line numbers in messages when parsing comments.
- Add missing deactivation after activation failure in lvcreate -Zy.
- When removing LV symlinks, skip any where the VG name is not determined.
- Fix vgsplit internal counting of snapshot LVs.
- Update vgsplit to only restrict split with active LVs involved in split.
- Fix vgsplit to only move hidden 'snapshotN' LVs when necessary.
- Update vgsplit man page to reflect lvnames on the cmdline.
- Update vgsplit to take "-n LogicalVolumeName" on the cmdline.
- Fix vgsplit error paths to release vg_to lock.
- Avoid spurious duplicate VG messages referring to VGs that are gone.
- Drop dev_name_confirmed error message to debug level.
- Fix setpriority error message to signed int.
- Add assertions to trap deprecated P_ and V_ lock usage.
- Avoid using DLM locks with LCK_CACHE type P_ lock requests.
- Don't touch /dev in vgrename if activation is disabled.
- Exclude VG_GLOBAL from internal concurrent VG lock counter.
- Fix vgmerge snapshot_count when source VG contains snapshots.
- Fix internal LV counter when a snapshot is removed.
- Fix metadata corruption writing lvm1-formatted metadata with snapshots.
- Fix lvconvert -m0 allocatable space check.
- Don't attempt remote metadata backups of non-clustered VGs.
- Improve preferred_names lvm.conf example.
- Fix vgdisplay 'Cur LV' field to match lvdisplay output.
- Fix lv_count report field to exclude hidden LVs.
- Fix some pvmove error status codes.
- Indicate whether or not VG is clustered in vgcreate log message.
- Mention default --clustered setting in vgcreate man page.
- Fix vgreduce to use vg_split_mdas to check sufficient mdas remain.
- Update lvmcache VG lock state for all locking types now.
- Fix output if overriding command_names on cmdline.
- Add check to vg_commit() ensuring VG lock held before writing new VG metadata.
- Add validation of LV name to pvmove -n.
- Add some basic internal VG lock validation.
- Fix vgsplit internal counting of snapshot LVs.
- Update vgsplit to only restrict split with active LVs involved in split.
- Fix vgsplit to only move hidden 'snapshotN' LVs when necessary.
- Update vgsplit man page to reflect lvnames on the cmdline.
- Update vgsplit to take "-n LogicalVolumeName" on the cmdline.
- Fix vgsplit error paths to release vg_to lock.
- Fix vgsplit locking of new VG.
- Avoid erroneous vgsplit error message for new VG.
- Suppress duplicate message when lvresize fails because of invalid vgname.
- Cache VG metadata internally while VG lock is held.
- Fix redundant lvresize message if vg doesn't exist.
- Make clvmd-cman use a hash rather than an array for node updown info.
- Decode numbers in clvmd debugging output.
- Fix uninitialised mutex in clvmd if all daemons are not running at startup.
- Add config file overrides to clvmd when it reads the active LVs list.
- Make clvmd refresh the context correctly when lvm.conf is updated.
- Fix another allocation bug with clvmd and large node IDs.
- Fix uninitialised variable in clvmd that could cause odd hangs.
- Correct command name in lvmdiskscan man page.
- clvmd no longer crashes if it sees nodeids over 50.
- Fix potential deadlock in clvmd thread handling.
- Update usage message for clvmd.
- Fix clvmd man page not to print <br> and clarified debug options.
- Escape double quotes and backslashes in external metadata and config data.
- Correct a function name typo in _line_append error message.
- Fix resetting of MIRROR_IMAGE and VISIBLE_LV after removal of LV.
- Fix remove_layer_from_lv to empty the LV before removing it.
- Add missing no-longer-used segs_using_this_lv test to check_lv_segments.
- Fix lvconvert detection of mirror conversion in progress.
- Avoid automatic lvconvert polldaemon invocation when -R specified.
- Fix 'pvs -a' to detect VGs of PVs without metadata areas.
- Divide up internal orphan volume group by format type.
- Fix lvresize to support /dev/mapper prefix in the LV name.
- Fix lvresize to pass new size to fsadm when extending device.
- Fix unfilled parameter passed to fsadm from lvresize.
- Update fsadm to call lvresize if the partition size differs (with option -l).
- Fix fsadm to support VG/LV names.

* Wed Apr  2 2008 Jeremy Katz <katzj@redhat.com> - 2.02.33-11
- Adjust for new name for vio disks (from danpb)
- And fix the build (also from danpb)

* Wed Mar  5 2008 Jeremy Katz <katzj@redhat.com> - 2.02.33-10
- recognize vio disks

* Thu Jan 31 2008 Alasdair Kergon <agk@redhat.com> - 2.02.33-9
- Improve internal label caching performance while locks are held.
- Fix mirror log name construction during lvconvert.

* Tue Jan 29 2008 Alasdair Kergon <agk@redhat.com> - 2.02.32-8
- Fix pvs, vgs, lvs error exit status on some error paths.
- Fix new parameter validation in vgsplit and test mode.
- Fix internal metadata corruption in lvchange --resync.

* Sat Jan 19 2008 Alasdair Kergon <agk@redhat.com> - 2.02.31-7
- Avoid readahead error message when using default setting of lvcreate -M1.
- Fix lvcreate --nosync not to wait for non-happening sync.
- Add very_verbose lvconvert messages.

* Thu Jan 17 2008 Alasdair Kergon <agk@redhat.com> - 2.02.30-6
- Remove static libraries and binaries and move most binaries out of /usr.
- Fix a segfault if using pvs with --all argument.
- Fix vgreduce PV list processing not to process every PV in the VG.
- Reinstate VG extent size and stripe size defaults (halved).
- Set default readahead to twice maximium stripe size.
- Detect non-orphans without MDAs correctly.
- Prevent pvcreate from overwriting MDA-less PVs belonging to active VGs.
- Don't use block_on_error with mirror targets version 1.12 and above.
- Change vgsplit -l (for unimplemented --list) into --maxlogicalvolumes.
- Update vgsplit to accept vgcreate options when new VG is destination.
- Update vgsplit to accept existing VG as destination.
- Major restructuring of pvmove and lvconvert code, adding stacking support.
- Add new convert_lv field to lvs output.
- Permit LV segment fields with PV segment reports.
- Extend lvconvert to use polldaemon and wait for completion of initial sync.
- Add seg_start_pe and seg_pe_ranges to reports.
- Add fsadm interface to filesystem resizing tools.
- Update --uuid argument description in man pages.
- Print warning when lvm tools are running as non-root.

* Thu Dec 20 2007 Alasdair Kergon <agk@redhat.com> - 2.02.29-5
- Fix libdevmapper readahead processing with snapshots (for example).

* Thu Dec 13 2007 Alasdair Kergon <agk@redhat.com> - 2.02.29-4
- Add missing lvm2 build & runtime dependencies on module-init-tools (modprobe).

* Thu Dec  6 2007 Jeremy Katz <katzj@redhat.com> - 2.02.29-3
- fix requirements

* Thu Dec 06 2007 Alasdair Kergon <agk@redhat.com> - 2.02.29-2
- Fold device-mapper build into this lvm2 spec file.

* Wed Dec 05 2007 Alasdair Kergon <agk@redhat.com> - 2.02.29-1
- Make clvmd backup vg metadata on remote nodes.
- Decode cluster locking state in log message.
- Change file locking state messages from debug to very verbose.
- Fix --addtag to drop @ prefix from name.
- Stop clvmd going haywire if a pre_function fails.
- Avoid nested vg_reads when processing PVs in VGs and fix associated locking.
- Attempt to remove incomplete LVs with lvcreate zeroing/activation problems.
- Add full read_ahead support.
- Add lv_read_ahead and lv_kernel_read_ahead fields to reports and lvdisplay.
- Prevent lvconvert -s from using same LV as origin and snapshot.
- Fix human-readable output of odd numbers of sectors.
- Add pv_mda_free and vg_mda_free fields to reports for raw text format.
- Add LVM2 version to 'Generated by' comment in metadata.
- Show 'not usable' space when PV is too large for device in pvdisplay.
- Ignore and fix up any excessive device size found in metadata.
- Fix error message when fixing up PV size in lvm2 metadata (2.02.11).
- Fix orphan-related locking in pvdisplay and pvs.
- Fix missing VG unlocks in some pvchange error paths.
- Add some missing validation of VG names.
- Detect md superblocks version 1.0, 1.1 and 1.2.
- Add some pv-related error paths.
- Handle future sysfs subsystem/block/devices directory structure.
- Fix a bug in lvm_dump.sh checks for lvm/dmsetup binaries.
- Fix underquotations in lvm_dump.sh.
- Print --help output to stdout, not stderr.
- After a cmdline processing error, don't print help text but suggest --help.
- Add %%PVS extents option to lvresize, lvextend, and lvcreate.
- Remove no-longer-correct restrictions on PV arg count with stripes/mirrors.
- Fix strdup memory leak in str_list_dup().
- Link with -lpthread when static SELinux libraries require that.
- Detect command line PE values that exceed their 32-bit range.
- Include strerror string in dev_open_flags' stat failure message.
- Avoid error when --corelog is provided without --mirrorlog. (2.02.28)
- Correct --mirrorlog argument name in man pages (not --log).
- Clear MIRROR_NOTSYNCED LV flag when converting from mirror to linear.
- Modify lvremove to prompt for removal if LV active on other cluster nodes.
- Add '-f' to vgremove to force removal of VG even if LVs exist.

* Fri Aug 24 2007 Alasdair Kergon <agk@redhat.com> - 2.02.28-1
- vgscan and pvscan now trigger clvmd -R, which should now work.
- Fix clvmd logging so you can get lvm-level debugging out of it.
- Allow clvmd debug to be turned on in a running daemon using clvmd -d [-C].
- Add more cluster info to lvmdump.
- Fix lvdisplay man page to say LV size is reported in sectors, not KB.
- Fix loading of persistent cache if cache_dir is used.
- Only permit --force, --verbose and --debug arguments to be repeated.
- Add support for renaming mirrored LVs.
- Add --mirrorlog argument to specify log type for mirrors.
- Don't leak a file descriptor if flock or fcntl fails.
- Detect stream write failure reliably.
- Reduce severity of lstat error messages to very_verbose.
- Update to use autoconf 2.61, while still supporting 2.57.

* Thu Aug 09 2007 Alasdair Kergon <agk@redhat.com> - 2.02.27-3
- Clarify GPL licence as being version 2.

* Wed Aug 01 2007 Milan Broz <mbroz@redhat.com> - 2.02.27-2
- Add SUN's LDOM virtual block device (vdisk) and ps3disk to filters.

* Wed Jul 18 2007 Alasdair Kergon <agk@redhat.com> - 2.02.27-1
- Add -f to vgcfgrestore to list metadata backup files.
- Add pvdisplay --maps implementation.
- Add devices/preferred_names config regex list for displayed device names.
- Add vg_mda_count and pv_mda_count columns to reports.
- Change cling alloc policy attribute character from 'C' to l'.
- Print warnings to stderr instead of stdout.
- Fix snapshot cow area deactivation if origin is not active.
- Reinitialise internal lvmdiskscan variables when called repeatedly.
- Allow keyboard interrupt during user prompts when appropriate.
- Fix deactivation code to follow dependencies and remove symlinks.
- Fix a segfault in device_is_usable() if a device has no table.
- Fix creation and conversion of mirrors with tags.
- Add command stub for pvck.
- Handle vgsplit of an entire VG as a vgrename.
- Fix vgsplit for lvm1 format (set and validate VG name in PVs metadata).
- Split metadata areas in vgsplit properly.
- Fix and clarify vgsplit error messages.
- Update lists of attribute characters in man pages.
- Remove unsupported LVM1 options from vgcfgrestore man page.
- Update vgcfgrestore man page to show mandatory VG name.
- Update vgrename man page to include UUID and be consistent with lvrename.
- Add some more debug messages to clvmd startup.
- Fix thread race in clvmd.
- Make clvmd cope with quorum devices.
- Add extra internal error checking to clvmd.
- Fix missing lvm_shell symbol in lvm2cmd library.
- Move regex functions into libdevmapper.
- Add kernel and device-mapper targets versions to lvmdump.
- Add /sys/block listings to lvmdump.
- Make lvmdump list /dev recursively.
- Mark /etc/lvm subdirectories as directories in spec file.

* Mon Mar 19 2007 Alasdair Kergon <agk@redhat.com> - 2.02.24-1
- Add BuildRequires readline-static until makefiles get fixed.
- Fix processing of exit status in init scripts
- Fix vgremove to require at least one vg argument.
- Fix reading of striped LVs in LVM1 format.
- Flag nolocking as clustered so clvmd startup sees clustered LVs.
- Add a few missing pieces of vgname command line validation.
- Support the /dev/mapper prefix on most command lines.

* Thu Mar 08 2007 Alasdair Kergon <agk@redhat.com> - 2.02.23-1
- Fix vgrename active LV check to ignore differing vgids.
- Fix two more segfaults if an empty config file section encountered.
- Fix a leak in a reporting error path.
- Add devices/cache_dir & devices/cache_file_prefix, deprecating devices/cache.

* Tue Feb 27 2007 Alasdair Kergon <agk@redhat.com> - 2.02.22-3
- Move .cache file to /etc/lvm/cache.

* Wed Feb 14 2007 Alasdair Kergon <agk@redhat.com> - 2.02.22-2
- Rebuild after device-mapper package split.

* Wed Feb 14 2007 Alasdair Kergon <agk@redhat.com> - 2.02.22-1
- Add ncurses-static BuildRequires after package split.
- Fix loading of segment_libraries.
- If a PV reappears after it was removed from its VG, make it an orphan.
- Don't update metadata automatically if VGIDs don't match.
- Fix some vgreduce --removemissing command line validation.
- Trivial man page corrections (-b and -P).
- Add global/units to example.conf.
- Remove readline support from lvm.static.

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 2.02.21-4
- Remove file wildcards and unintentional lvmconf installation.

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 2.02.21-3
- Add build dependency on new device-mapper-devel package.

* Wed Jan 31 2007 Alasdair Kergon <agk@redhat.com> - 2.02.21-2
- Remove superfluous execute perm from .cache data file.

* Tue Jan 30 2007 Alasdair Kergon <agk@redhat.com> - 2.02.21-1
- Fix vgsplit to handle mirrors.
- Reorder fields in reporting field definitions.
- Fix vgs to treat args as VGs even when PV fields are displayed.
- Fix md signature check to handle both endiannesses.

* Fri Jan 26 2007 Alasdair Kergon <agk@redhat.com> - 2.02.20-1
- Fix exit statuses of reporting tools.
- Add some missing close() and fclose() return code checks.
- Add devices/ignore_suspended_devices to ignore suspended dm devices.
- Fix refresh_toolcontext() always to wipe persistent device filter cache.
- Long-lived processes write out persistent dev cache in refresh_toolcontext().
- Streamline dm_report_field_* interface.
- Update reporting man pages.
- Add --clustered to man pages.
- Add field definitions to report help text.

* Mon Jan 22 2007 Milan Broz <mbroz@redhat.com> - 2.02.19-2
- Remove BuildRequires libtermcap-devel
  Resolves: #223766

* Wed Jan 17 2007 Alasdair Kergon <agk@redhat.com> - 2.02.19-1
- Fix a segfault if an empty config file section encountered.
- Fix partition table processing after sparc changes.
- Fix cmdline PE range processing segfault.
- Move basic reporting functions into libdevmapper.

* Fri Jan 12 2007 Alasdair Kergon <agk@redhat.com> - 2.02.18-2
- Rebuild.

* Thu Jan 11 2007 Alasdair Kergon <agk@redhat.com> - 2.02.18-1
- Use CFLAGS when linking so mixed sparc builds can supply -m64.
- Prevent permission changes on active mirrors.
- Print warning instead of error message if lvconvert cannot zero volume.
- Add snapshot options to lvconvert man page.
- dumpconfig accepts a list of configuration variables to display.
- Change dumpconfig to use --file to redirect output to a file.
- Avoid vgreduce error when mirror code removes the log LV.
- Fix ambiguous vgsplit error message for split LV.
- Fix lvextend man page typo.
- Use no flush suspending for mirrors.
- Fix create mirror with name longer than 22 chars.

* Thu Dec 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.17-1
- Add missing pvremove error message when device doesn't exist.
- When lvconvert allocates a mirror log, respect parallel area constraints.
- Check for failure to allocate just the mirror log.
- Support mirror log allocation when there is only one PV: area_count now 0.
- Fix detection of smallest area in _alloc_parallel_area() for cling policy.
- Add manpage entry for clvmd -T
- Fix hang in clvmd if a pre-command failed.

* Fri Dec 01 2006 Alasdair Kergon <agk@redhat.com> - 2.02.16-1
- Fix VG clustered read locks to use PR not CR.
- Adjust some alignments for ia64/sparc.
- Fix mirror segment removal to use temporary error segment.
- Always compile debug logging into clvmd.
- Add startup timeout to clvmd startup script.
- Add -T (startup timeout) switch to clvmd.
- Improve lvm_dump.sh robustness.

* Tue Nov 21 2006 Alasdair Kergon <agk@redhat.com> - 2.02.15-3
- Fix clvmd init script line truncation.

* Tue Nov 21 2006 Alasdair Kergon <agk@redhat.com> - 2.02.15-2
- Fix lvm.conf segfault.

* Mon Nov 20 2006 Alasdair Kergon <agk@redhat.com> - 2.02.15-1
- New upstream - see WHATS_NEW.

* Sat Nov 11 2006 Alasdair Kergon <agk@redhat.com> - 2.02.14-1
- New upstream - see WHATS_NEW.

* Mon Oct 30 2006 Alasdair Kergon <agk@redhat.com> - 2.02.13-2
- Fix high-level free-space check on partial allocation.
  Resolves: #212774

* Fri Oct 27 2006 Alasdair Kergon <agk@redhat.com> - 2.02.13-1
- New upstream - see WHATS_NEW.
  Resolves: #205818

* Fri Oct 20 2006 Alasdair Kergon <agk@redhat.com> - 2.02.12-2
- Remove no-longer-used ldconfig from lvm2-cluster and fix lvmconf
  to cope without the shared library.

* Mon Oct 16 2006 Alasdair Kergon <agk@redhat.com> - 2.02.12-1
- New upstream.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-6
- Incorporate lvm2-cluster as a subpackage.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-5
- Install lvmdump script.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-4
- Build in cluster locking with fallback if external locking fails to load.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-3
- Drop .0 suffix from release.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-2.0
- Append distribution to release.

* Fri Oct 13 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-1.0
- New upstream with numerous fixes and small enhancements.
  (See the WHATS_NEW documentation file for complete upstream changelog.)

* Thu Sep 28 2006 Peter Jones <pjones@redhat.com> - 2.02.06-4
- Fix metadata and map alignment problems on ppc64 (#206202)

* Tue Aug  1 2006 Jeremy Katz <katzj@redhat.com> - 2.02.06-3
- require new libselinux to avoid segfaults on xen (#200783)

* Thu Jul 27 2006 Jeremy Katz <katzj@redhat.com> - 2.02.06-2
- free trip through the buildsystem

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.02.06-1.2.1
- rebuild

* Tue Jun  6 2006 Stephen C. Tweedie <sct@redhat.com> - 2.02.06-1.2
- Rebuild to pick up new nosegneg libc.a for lvm.static

* Mon May 22 2006 Alasdair Kergon <agk@redhat.com> - 2.02.06-1.1
- Reinstate archs now build system is back.
- BuildRequires libsepol-devel.

* Fri May 12 2006 Alasdair Kergon <agk@redhat.com> - 2.02.06-1.0
- New upstream release.

* Sat Apr 22 2006 Alasdair Kergon <agk@redhat.com> - 2.02.05-1.1
- Exclude archs that aren't building.

* Fri Apr 21 2006 Alasdair Kergon <agk@redhat.com> - 2.02.05-1.0
- Fix VG uuid comparisons.

* Wed Apr 19 2006 Alasdair Kergon <agk@redhat.com> - 2.02.04-1.0
- New release upstream, including better handling of duplicated VG names.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.02.01-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.02.01-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Peter Jones <pjones@redhat.com> - 2.02.01-1
- update to 2.02.01

* Tue Nov  8 2005 Jeremy Katz <katzj@redhat.com> - 2.01.14-4
- add patch for xen block devices

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- add -lselinux -lsepol to the static linking -ldevice-mapper requires it

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 2.01.14-2
- the distro doesn't really work without a 2.6 kernel, so no need to require it

* Thu Aug 4 2005 Alasdair Kergon <agk@redhat.com> - 2.01.14-1.0
- And a few more bugs fixes.

* Wed Jul 13 2005 Alasdair Kergon <agk@redhat.com> - 2.01.13-1.0
- Fix several bugs discovered in the last release.

* Tue Jun 14 2005 Alasdair Kergon <agk@redhat.com> - 2.01.12-1.0
- New version upstream with a lot of fixes and enhancements.

* Wed Apr 27 2005 Alasdair Kergon <agk@redhat.com> - 2.01.08-2.1
- Add /etc/lvm

* Wed Apr 27 2005 Alasdair Kergon <agk@redhat.com> - 2.01.08-2.0
- No longer abort read operations if archive/backup directories aren't there.
- Add runtime directories and file to the package.

* Tue Mar 22 2005 Alasdair Kergon <agk@redhat.com> - 2.01.08-1.0
- Improve detection of external changes affecting internal cache.
- Add clustered VG attribute.
- Suppress rmdir opendir error message.

* Tue Mar 08 2005 Alasdair Kergon <agk@redhat.com> - 2.01.07-1.3
* Tue Mar 08 2005 Alasdair Kergon <agk@redhat.com> - 2.01.07-1.2
* Tue Mar 08 2005 Alasdair Kergon <agk@redhat.com> - 2.01.07-1.1
- Suppress some new compiler messages.

* Tue Mar 08 2005 Alasdair Kergon <agk@redhat.com> - 2.01.07-1.0
- Remove build directory from built-in path.
- Extra /dev scanning required for clustered operation.

* Thu Mar 03 2005 Alasdair Kergon <agk@redhat.com> - 2.01.06-1.0
- Allow anaconda to suppress warning messages.

* Fri Feb 18 2005 Alasdair Kergon <agk@redhat.com> - 2.01.05-1.0
- Upstream changes not affecting Fedora.

* Wed Feb 09 2005 Alasdair Kergon <agk@redhat.com> - 2.01.04-1.0
- Offset pool minors; lvm2cmd.so skips open fd check; pvmove -f gone.

* Tue Feb 01 2005 Alasdair Kergon <agk@redhat.com> - 2.01.03-1.0
- Fix snapshot device size & 64-bit display output.

* Fri Jan 21 2005 Alasdair Kergon <agk@redhat.com> - 2.01.02-1.0
- Minor fixes.

* Mon Jan 17 2005 Alasdair Kergon <agk@redhat.com> - 2.01.01-1.0
- Update vgcreate man page.  Preparation for snapshot origin extension fix.

* Mon Jan 17 2005 Alasdair Kergon <agk@redhat.com> - 2.01.00-1.0
- Fix metadata auto-correction. Only request open_count when needed.

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> - 2.00.33-2.0
- Rebuilt for new readline.

* Fri Jan 7 2005 Alasdair Kergon <agk@redhat.com> - 2.00.33-1.0
- pvcreate wipes ext label
- several clvm fixes

* Thu Jan 6 2005 Alasdair Kergon <agk@redhat.com> - 2.00.32-2.0
- Remove temporary /sbin symlinks no longer needed.
- Include read-only pool support in the build.

* Wed Dec 22 2004 Alasdair Kergon <agk@redhat.com> - 2.00.32-1.0
- More fixes (143501).

* Sun Dec 12 2004 Alasdair Kergon <agk@redhat.com> - 2.00.31-1.0
- Fix pvcreate install issues.

* Fri Dec 10 2004 Alasdair Kergon <agk@redhat.com> - 2.00.30-1.0
- Additional debugging code.
- Some trivial man page corrections.

* Tue Nov 30 2004 Alasdair Kergon <agk@redhat.com> - 2.00.29-1.3
- Reinstate all archs.

* Sun Nov 28 2004 Alasdair Kergon <agk@redhat.com> - 2.00.29-1.2
- Try excluding more archs.

* Sat Nov 27 2004 Alasdair Kergon <agk@redhat.com> - 2.00.29-1.1
- Exclude s390x which fails.

* Sat Nov 27 2004 Alasdair Kergon <agk@redhat.com> - 2.00.29-1
- Fix last fix.

* Sat Nov 27 2004 Alasdair Kergon <agk@redhat.com> - 2.00.28-1
- Endian fix to partition/md signature detection.

* Wed Nov 24 2004 Alasdair Kergon <agk@redhat.com> - 2.00.27-1
- Fix partition table detection & an out of memory segfault.

* Tue Nov 23 2004 Alasdair Kergon <agk@redhat.com> - 2.00.26-1
- Several installation-related fixes & man page updates.

* Mon Oct 25 2004 Elliot Lee <sopwith@redhat.com> - 2.00.25-1.01
- Fix 2.6 kernel requirement

* Wed Sep 29 2004 Alasdair Kergon <agk@redhat.com> - 2.00.25-1
- Fix vgmknodes return code & vgremove locking.

* Fri Sep 17 2004 Alasdair Kergon <agk@redhat.com> - 2.00.24-2
- Obsolete old lvm1 packages; refuse install if running kernel 2.4. [bz 128185]

* Thu Sep 16 2004 Alasdair Kergon <agk@redhat.com> - 2.00.24-1
- More upstream fixes.  (Always check WHATS_NEW file for details.)
- Add requested BuildRequires. [bz 124916, 132408]

* Wed Sep 15 2004 Alasdair Kergon <agk@redhat.com> - 2.00.23-1
- Various minor upstream fixes.

* Fri Sep  3 2004 Alasdair Kergon <agk@redhat.com> - 2.00.22-1
- Permission fix included upstream; use different endian conversion macros.

* Thu Sep  2 2004 Jeremy Katz <katzj@redhat.com> - 2.00.21-2
- fix permissions on vg dirs

* Thu Aug 19 2004 Alasdair Kergon <agk@redhat.com> - 2.00.21-1
- New upstream release incorporating fixes plus minor enhancements.

* Tue Aug 17 2004 Jeremy Katz <katzj@redhat.com> - 2.00.20-2
- add patch for iSeries viodasd support
- add patch to check file type using stat(2) if d_type == DT_UNKNOWN (#129674)

* Sat Jul 3 2004 Alasdair Kergon <agk@redhat.com> - 2.00.20-1
- New upstream release fixes 2.6 kernel device numbers.

* Tue Jun 29 2004 Alasdair Kergon <agk@redhat.com> - 2.00.19-1
- Latest upstream release.  Lots of changes (see WHATS_NEW).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> - 2.00.15-5
- rebuilt

* Wed May 26 2004 Alasdair Kergon <agk@redhat.com> - 2.00.15-4
- clone %%description from LVM rpm

* Wed May 26 2004 Alasdair Kergon <agk@redhat.com> - 2.00.15-3
- vgscan shouldn't return error status when no VGs present

* Thu May 06 2004 Warren Togami <wtogami@redhat.com> - 2.00.15-2
- i2o patch from Markus Lidel

* Tue Apr 20 2004 Bill Nottingham <notting@redhat.com> - 2.00.15-1.1
- handle disabled SELinux correctly, so that LVMs can be detected in a
  non-SELinux context
  
* Mon Apr 19 2004 Alasdair Kergon <agk@redhat.com> - 2.00.15-1
- Fix non-root build with current version of 'install'.

* Fri Apr 16 2004 Alasdair Kergon <agk@redhat.com> - 2.00.14-1
- Use 64-bit file offsets.

* Fri Apr 16 2004 Alasdair Kergon <agk@redhat.com> - 2.00.13-1
- Avoid scanning devices containing md superblocks.
- Integrate ENOTSUP patch.

* Thu Apr 15 2004 Jeremy Katz <katzj@redhat.com> - 2.00.12-4
- don't die if we get ENOTSUP setting selinux contexts

* Thu Apr 15 2004 Alasdair Kergon <agk@redhat.com> 2.00.12-3
- Add temporary pvscan symlink for LVM1 until mkinitrd gets updated.

* Wed Apr 14 2004 Alasdair Kergon <agk@redhat.com> 2.00.12-2
- Mark config file noreplace.

* Wed Apr 14 2004 Alasdair Kergon <agk@redhat.com> 2.00.12-1
- Install default /etc/lvm/lvm.conf.
- Move non-static binaries to /usr/sbin.
- Add temporary links in /sbin to lvm.static until rc.sysinit gets updated.

* Thu Apr 08 2004 Alasdair Kergon <agk@redhat.com> 2.00.11-1
- Fallback to using LVM1 tools when using a 2.4 kernel without device-mapper.

* Wed Apr 07 2004 Alasdair Kergon <agk@redhat.com> 2.00.10-2
- Install the full toolset, not just 'lvm'.

* Wed Apr 07 2004 Alasdair Kergon <agk@redhat.com> 2.00.10-1
- Update to version 2.00.10, which incorporates the RH-specific patches
  and includes various fixes and enhancements detailed in WHATS_NEW.

* Wed Mar 17 2004 Jeremy Katz <katzj@redhat.com> 2.00.08-5
- Fix sysfs patch to find sysfs
- Take patch from dwalsh and tweak a little for setting SELinux contexts on
  device node creation and also do it on the symlink creation.  
  Part of this should probably be pushed down to device-mapper instead

* Thu Feb 19 2004 Stephen C. Tweedie <sct@redhat.com> 2.00.08-4
- Add sysfs filter patch
- Allow non-root users to build RPM

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec  5 2003 Jeremy Katz <katzj@redhat.com> 2.00.08-2
- add static lvm binary

* Tue Dec  2 2003 Jeremy Katz <katzj@redhat.com> 
- Initial build.



