%global package_speccommit bced7835bed6e955ba5ddd504cb089a5e6b25d23
%global usver 2.9.21
%global xsver 3
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 2.9.21
%define vendor_name Intel
%define vendor_label intel
%define driver_name i40e

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 2.9.21
Release: %{?xsrel}%{?dist}
License: GPL
Source0: intel-i40e-2.9.21.tar.gz

BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

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

%{?_cov_results_package}

%changelog
* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.9.21-3
- CP-38416: Enable static analysis

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.9.21-2
- CP-35517: Fix the build for koji

* Fri Nov 1 2019 Igor Druzhinin <igor.druzhinin@citrix.com> - 2.9.21-1
- CP-32416: Updating i40e drivers to version 2.9.21

* Fri Nov 16 2018 Deli Zhang <deli.zhang@citrix.com> - 2.7.12-1
- CP-29877: Updating i40e drivers to version 2.7.12

* Wed Jun 28 2017 Simon Rowe <simon.rowe@citrix.com> - 2.0.23-1
- Updating i40e drivers to version 2.0.23
