pkgname=anchaides-utils
pkgver=rc1.1
pkgrel=3
metaname=utils-meta 
metatag=rc1.1 
# https://github.com/anchaides/utils-meta/archive/refs/tags/v1.03.tar.gz
pkgdesc="helper utils and scripts I have made over time" 
arch=('x86_64')
url="https://github.com/anchaides/utils"
license=('GPL')
source=("$metaname-$metatag.tar.gz::https://github.com/anchaides/utils-meta/archive/refs/tags/$metatag.tar.gz"
)
sha256sums=('2489a515971e5fe197fce3a6e9777869f5dbf8e31f764c8e5b9a4d2bb2d4de11')

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

