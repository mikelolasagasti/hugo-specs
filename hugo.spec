%bcond_without check
# Some tests use a package that uses this.
%bcond_with bootstrap

# https://github.com/gohugoio/hugo
%global goipath github.com/gohugoio/hugo
Version:        0.87.0

%gometa

%global common_description %{expand:
Hugo is a static HTML and CSS website generator written in Go. It is optimized
for speed, easy use and configurability. Hugo takes a directory with content
and templates and renders them into a full HTML website.}

%global golicenses      LICENSE docs/LICENSE.md docs/themes/gohugoioTheme/license.md
%global godocs          docs examples README.md CONTRIBUTING.md

Name:           hugo
Release:        1%{?dist}
Summary:        The world’s fastest framework for building websites

# Upstream license specification: Apache-2.0 and MIT
License:        ASL 2.0 and MIT
URL:            %{gourl}
Source0:        %{gosource}
# Skip tests that uses the network.
# https://sources.debian.org/data/main/h/hugo/0.58.3-1/debian/patches/0005-skip-modules-TestClient.patch
#Patch0001:      0005-skip-modules-TestClient.patch
# https://sources.debian.org/data/main/h/hugo/0.69.0-1/debian/patches/0006-skip-TestHugoModulesTargetInSubFolder.patch
#Patch0002:      0006-skip-TestHugoModulesTargetInSubFolder.patch
# Minify 2.9.3 removed Decimals in favor of Precision
#Patch0004:      0001-Update-to-minify-2.9.4.patch
# Fix for TestResourceChains/minify failure
#Patch0005:      0001-Remove-trailing-semicolon.patch
# Bump afero to 1.5.1
#Patch0006:      0001-Bump-afero-to-1.5.1.patch

BuildRequires:  golang(github.com/bep/golibsass/libsass) >= 0.7.0

%description
%{common_description}

%gopkg

%prep
%goprep

#%patch0001 -p1
#%patch0002 -p1
#%patch0004 -p1
#%patch0005 -p1
#%patch0006 -p1

sed -i -e 's|"github.com/gohugoio/go-i18n/v2/i18n|"github.com/nicksnyder/go-i18n/v2/i18n|' $(find . -name '*.go')


# Replace blackfriday import path to avoid conflict with v2
sed -i -e 's|"github.com/russross/blackfriday|"gopkg.in/russross/blackfriday.v1|' $(find . -name '*.go')

# Pin github.com/evanw/esbuild to v0.8.20
# See https://github.com/gohugoio/hugo/issues/8141
sed -i -e 's|"github.com/evanw/esbuild|"github.com/evanw/esbuild-0.8.20|' $(find . -name '*.go')

# Skip test that assumes directory is in a git repository
sed -i '/TestPageWithLastmodFromGitInfo/a t.Skip()' hugolib/page_test.go

%if %{with bootstrap}
# Delete test using github.com/gohugoio/testmodBuilder/mods which has a
# dependency loop.
rm hugolib/hugo_modules_test.go
%endif

%generate_buildrequires
%go_generate_buildrequires

%build
BUILDTAGS=extended %gobuild -o %{gobuilddir}/bin/hugo %{goipath}
%{gobuilddir}/bin/hugo gen autocomplete --completionfile hugo-completion
%{gobuilddir}/bin/hugo gen man


%install
%gopkginstall

install -d -p %{buildroot}%{_bindir}
install -Dp -m 0755 %{gobuilddir}/bin/hugo %{buildroot}%{_bindir}
install -Dp hugo-completion %{buildroot}%{_datadir}/bash-completion/completions/hugo
install -Dp man/* -t %{buildroot}%{_mandir}/man1


%if %{with check}
%check
# releaser: We do not want to test upstream release process (needs git repo)
# tpl/time: A test depends on the host timezone, we do now want to test it.
# time_test.go:49: [3] DateFormat failed: Unable to Cast 1421733600 to Time # line 35 returns different results
%gocheck -d releaser -d tpl/time
%endif


%files
%doc CONTRIBUTING.md README.md docs examples
%license LICENSE
%{_bindir}/hugo
%{_datadir}/bash-completion/completions/hugo
%{_mandir}/man1/*.1*

%gopkgfiles


%changelog
* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.80.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.80.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 17 22:04:05 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.80.0-1
- Update to 0.80.0
- Close: rhbz#1856494

* Fri Sep 18 04:37:22 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.75.1-1
- Update to 0.75.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.73.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.73.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.73.0-1
- Update to latest version

* Sun Jun 07 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.72.0-1
- Update to latest version

* Thu May 07 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.70.0-2
- Use generated dynamic buildrequires

* Thu May 07 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.70.0-1
- Update to latest version

* Sat May 02 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.69.2-1
- Update to latest version

* Sun Apr 19 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.69.0-3
- Add patch for latest go-org

* Sat Apr 18 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.69.0-2
- Update golang-github-kyokomi-emoji required version

* Sat Apr 18 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.69.0-1
- Update to latest version

* Mon Apr 13 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.68.3-2
- Build hugo with extended features for SCSS support

* Wed Apr 08 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.68.3-1
- Update to latest version

* Mon Feb 24 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.65.3-1
- Update to latest version

* Sat Feb 22 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.65.2-1
- Update to latest version

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.59.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.59.1-1
- Update to latest version

* Wed Oct 16 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.58.3-1
- Update to latest version

* Thu Aug 01 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.55.6-3
- Update to latest Go macros

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.55.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 18 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.55.6-1
- Update to latest version

* Sat May 11 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.55.5-1
- Update to latest version

* Wed Apr 24 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.55.3-1
- Update to latest version

* Sat Apr 13 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.55.1-1
- Update to latest version

* Wed Apr 10 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.55.0-1
- Update to latest version

* Fri Mar 22 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.54.0-2
- Add bash-completion
- Add man pages

* Mon Mar 04 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.54.0-1
- Update to latest version

* Thu Feb 28 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.38-4
- Fix FTBFS (#1675118)

* Tue Feb 26 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.38-4
- Rewrite spec using latest template

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 04 2018 Pierre-Alain TORET <pierre-alain.toret@protonmail.com> - 0.38-1
- Update version

* Thu Mar 08 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.37.1-1
- Update version

* Thu Mar 01 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.37-1
- Update version

* Wed Feb 21 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.36.1-2
- Include resource/testdata in unit tests package

* Fri Feb 16 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.36.1-1
- Update version

* Tue Feb 13 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.36-1
- Update version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Pierre-Alain TORET <pierre-alain.toret@protonmail.com> - 0.31.1-1
- Update Version

* Mon Nov 20 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.31-1
- Update Version

* Sat Oct 21 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.30.2-1
- Update Version

* Tue Oct 17 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.30-1
- Update Version

* Wed Oct 11 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.29-1
- Update Version

* Fri Sep 15 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.27.1-2
- Add MIT License

* Wed Sep 13 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.27.1-1
- Update version

* Tue Sep 12 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.27-1
- Update version

* Fri Aug 11 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.26-2
- Substitute bep/inflect for markbates/inflect

* Fri Aug 11 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.26-1
- Update version

* Mon Jul 31 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.25.1-1
- Update version
- Fix unit-test subpackage requires to correct devel package
- Use global instead of define for gobuild

* Mon Jun 26 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.24-2
- Add external test dependencies

* Fri Jun 23 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.24-1
- New version
- Regenerate specfile with gofed

* Fri Mar 17 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.19-4
- Remove empty conditionals

* Sun Mar 12 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.19-3
- Use dist tag

* Fri Mar 03 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.19-2
- Move test data to unit-test subpackage path

* Fri Mar 03 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.19-1
- New version

* Fri Mar 03 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-5
- Include testdata in unit-test-devel subpackage

* Wed Mar 01 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-4
- Change binary name

* Wed Mar 01 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-3
- Use lowercase for jww package

* Tue Feb 28 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-2
- Use cammelcase for jww package

* Sun Feb 26 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-1
- Initial package
