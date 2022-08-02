%define lua_dir	%{_datarootdir}/lua
%define lua_dir_resty	%{lua_dir}/5.3/resty
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define nginx_loggroup adm

%define WITH_CC_OPT $(echo %{optflags} $(pcre2-config --cflags)) -fPIC
%define WITH_LD_OPT -Wl,-z,relro -Wl,-z,now -pie

%define BASE_CONFIGURE_ARGS $(echo "--prefix=%{_sysconfdir}/nginx --sbin-path=%{_sbindir}/nginx --modules-path=%{_libdir}/nginx/modules --conf-path=%{_sysconfdir}/nginx/nginx.conf --error-log-path=%{_localstatedir}/log/nginx/error.log --http-log-path=%{_localstatedir}/log/nginx/access.log --pid-path=%{_localstatedir}/run/nginx.pid --lock-path=%{_localstatedir}/run/nginx.lock --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp --user=%{nginx_user} --group=%{nginx_group} --with-compat --with-file-aio --with-threads")


Name: nginx-module-ndk
Summary: Nginx Development Kit - an Nginx module that adds additional generic tools that module developers can use in their own modules
Version: 0.3.1
Release: 1%{?dist}
URL: https://github.com/yoannguion/nginx-module-ndk
License: BSD

Source0:  http://nginx.org/download/nginx-1.22.0.tar.gz
Requires: nginx >= 1.22
BuildRequires: openssl-devel, lua, luajit, luajit-devel, zlib-devel, pcre2-devel

%description
Nginx Development Kit - an Nginx module that adds additional generic tools that module developers can use in their own modules

%prep
%setup -n nginx-1.22.0 -q

%build
export LUAJIT_INC=/usr/include/luajit-2.1
./configure %{BASE_CONFIGURE_ARGS} \
    --with-cc-opt="%{WITH_CC_OPT}" \
    --with-ld-opt="%{WITH_LD_OPT}" \
    --add-dynamic-module=%{_sourcedir}

make -j2

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/nginx/modules/
cp objs/ndk_http_module.so $RPM_BUILD_ROOT%{_libdir}/nginx/modules/

%files
%{_libdir}/nginx/modules/ndk_http_module.so


%changelog
* Mon Aug 01 2022 Yoann GUION <yoann.guion@gmail.com> - 0.3.1-1
- Initial release 0.3.1
