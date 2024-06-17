pkgname=utils
pkgver=0.1
pkgrel=0
metaname=utils-meta 
metatag=1.03
# https://github.com/anchaides/utils-meta/archive/refs/tags/v1.03.tar.gz
pkgdesc="helper utils and scripts I have made over time" 
arch=('x86_64')
url="https://github.com/anchaides/utils"
license=('GPL')
source=("$metaname-v$metatag.tar.gz::https://github.com/anchaides/utils-meta/archive/refs/tags/v$metatag.tar.gz"
)
sha256sums=('SKIP' 'SKIP') 

build() {
    cd $srcdir 
    make 
}

package() {
    install -Dm755 $pkgdir/bin/* "$pkgdir/usr/bin/" 
}

