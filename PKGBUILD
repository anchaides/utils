pkgname=anchaides-utils
pkgver=1.1
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
sha256sums=('d0bd25ea1dda75ca4b80a555d19daaca7f6ef4d21e2f0a5e46a387e5df8c6f0d')

build() {
    cd $srcdir 
    make 
}

package() { 

    for bin in $srcdir/../bin/*; do 
        if [[ -f "$bin" ]]; then
             echo install -Dm755 $bin  "$pkgdir/usr/bin/${bin##*/}" 
             install -Dm755 $bin  "$pkgdir/usr/bin/${bin##*/}" 

        fi 
    done 
}

