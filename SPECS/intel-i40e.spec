%define vendor_name Intel
%define vendor_label intel
%define driver_name i40e

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 2.9.21
Release: 1
License: GPL
#Source: http://hg.uk.xensource.com/git/carbon/trunk-ring0/driver-%{name}.git/snapshot/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-intel-i40e/archive?at=2.9.21&format=tgz&prefix=driver-intel-i40e-2.9.21#/intel-i40e-2.9.21.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-intel-i40e/archive?at=2.9.21&format=tgz&prefix=driver-intel-i40e-2.9.21#/intel-i40e-2.9.21.tar.gz) = b80bead583e02fe32effdac522970bf1201cafc5


BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Nov 1 2019 Igor Druzhinin <igor.druzhinin@citrix.com> - 2.9.21-1
- CP-32416: Updating i40e drivers to version 2.9.21

* Fri Nov 16 2018 Deli Zhang <deli.zhang@citrix.com> - 2.7.12-1
- CP-29877: Updating i40e drivers to version 2.7.12

* Wed Jun 28 2017 Simon Rowe <simon.rowe@citrix.com> - 2.0.23-1
- Updating i40e drivers to version 2.0.23

