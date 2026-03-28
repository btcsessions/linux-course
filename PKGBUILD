# Maintainer: CachyCLI Contributors
pkgname=cachycli-git
pkgver=0.1.0
pkgrel=1
pkgdesc="A terminal-based Linux CLI learning app for CachyOS"
arch=('any')
url="https://github.com/btcsessions/linux-course"
license=('MIT')
depends=(
    'python>=3.11'
    'python-rich'
    'python-textual'
    'python-click'
    'python-yaml'
    'python-frontmatter'
    'python-flask'
)
makedepends=(
    'python-build'
    'python-installer'
    'python-wheel'
    'python-setuptools'
    'git'
)
source=("git+${url}.git")
sha256sums=('SKIP')

pkgver() {
    cd linux-course
    git describe --long --tags 2>/dev/null | sed 's/^v//;s/-/.r/;s/-/./' || echo "$pkgver"
}

build() {
    cd linux-course
    python -m build --wheel --no-isolation
}

package() {
    cd linux-course
    python -m installer --destdir="$pkgdir" dist/*.whl

    # Install content files alongside the package.
    install -dm755 "$pkgdir/usr/share/cachycli/content"
    cp -r content/* "$pkgdir/usr/share/cachycli/content/"
}
