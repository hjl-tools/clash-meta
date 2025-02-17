# Generated by go2rpm 1.14.0
%bcond check 1


# https://github.com/metacubex/mihomo
%global goipath         github.com/metacubex/mihomo
Version:                1.18.7

# Fix error about undefined reference
# golang.org/x/sys/unix.sendmsg
# golang.org/x/sys/unix.ioctlPtr
%global gomodulesmode   GO111MODULE=on

%gometa -L -f

%global common_description %{expand:
A rule based network proxy tool, focus on censorship bypass. Also be known as mihomo.}

Name:           clash-meta
Release:        %autorelease
Summary:        A rule based network proxy tool, focus on censorship bypass. Also be known as mihomo.

# Generated by go-vendor-tools
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND GPL-3.0-only AND ISC AND MIT AND MPL-2.0
URL:            %{gourl}
Source0:        %{gosource}
# Generated by go-vendor-tools
Source1:        %{archivename}-vendor.tar.bz2
Source2:        go-vendor-tools.toml

BuildRequires:  go-vendor-tools

%description %{common_description}

%prep
%goprep -A
%setup -q -T -D -a1 %{forgesetupargs}
%autopatch -p1

# Note: Removing "// import" to pass check
# Upstream: https://github.com/golang/go/issues/37747
# Similar to https://github.com/containers/podman/issues/10009

# _build/src/github.com/metacubex/mihomo/vendor/github.com/RyuaNerin/go-krypto/lea/cipher_cbc.go:8:2: code in directory /builddir/build/BUILD/mihomo-1.18.7/_build/src/github.com/metacubex/mihomo/vendor/github.com/RyuaNerin/go-krypto/internal/subtle expects import "crypto/internal/subtle"
sed --follow-symlinks -i 's/\/\/ \s*import \s*".*"//' _build/src/github.com/metacubex/mihomo/vendor/github.com/RyuaNerin/go-krypto/internal/subtle/*.go
grep -r '//\s*import\s*"' _build/src/github.com/metacubex/mihomo/vendor/github.com/RyuaNerin/go-krypto/internal/subtle || echo "Removed!"
# _build/src/github.com/metacubex/mihomo/vendor/github.com/metacubex/chacha/chachapoly1305/chacha20poly1305.go:15:2: code in directory /builddir/build/BUILD/mihomo-1.18.7/_build/src/github.com/metacubex/mihomo/vendor/github.com/metacubex/chacha/poly1305 expects import "github.com/aead/poly1305"
# actually identified as "github.com/metacubex/chacha/poly1305"
sed --follow-symlinks -i 's/\/\/ \s*import \s*".*"//' _build/src/github.com/metacubex/mihomo/vendor/github.com/metacubex/chacha/poly1305/*.go
grep -r '//\s*import\s*"' _build/src/github.com/metacubex/mihomo/vendor/github.com/metacubex/chacha/poly1305 || echo "Removed!"

%generate_buildrequires
%go_vendor_license_buildrequires -c %{S:2}

%build
%gobuild -o %{gobuilddir}/bin/clash-meta "-tags=with_gvisor" %{goipath}

%install
%go_vendor_license_install -c %{S:2}
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%check
%go_vendor_license_check -c %{S:2}
%if %{with check}
# Because of it's network related nature (tun mode, iptables rules, etc),
# Check of clash-meta requires a running docker instance to run,
# Which is not possible in building environment (mock)
# See: https://github.com/MetaCubeX/mihomo/blob/Meta/test/README.md
%endif

%files -f %{go_vendor_license_filelist}
%license vendor/modules.txt
%doc docs README.md transport/shadowsocks/README.md
%{_bindir}/clash-meta


%changelog
%autochangelog
