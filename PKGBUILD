pkgname=anchaides-utils
pkgver=1.3
pkgrel=5
metanam=utils-meta 
metaver=1.1
metarel=3
# https://github.com/anchaides/utils-meta/archive/refs/tags/v1.03.tar.gz
pkgdesc="helper utils and scripts I have made over time" 
arch=('x86_64')
url="https://github.com/anchaides/utils"
license=('GPL')
source=("https://github.com/anchaides/$metanam/releases/download/v$metaver-$metarel/$metanam-$metaver-$metarel-$arch.pkg.tar.zst"
        "https://github.com/anchaides/$metanam/releases/download/v$metaver-$metarel/$metanam-$metaver-$metarel-$arch.pkg.tar.zst.sig"
)
sha256sums=('c041b3b4f76a332827def47f6dde7d398260b332a83bfea04362c03f298b03b8'
            'SKIP'
            )

validpgpkeys=('E807522FC5E58C299212FA90B20C037A4409DF78')

changelog=CHANGELOG.md 
build() {

    #sudo pacman -U $metanam-$metaver-$metarel-$arch.pkg.tar.zst --noconfirm 
    echo $PWD
    echo realpath $srcdir 
    mkdir -p "$srcdir"
    cd "$srcdir"
    #cp ../$changelog  $srcdir/usr/share/doc/$pkgname/ChangeLog 

    make 
}

pkgver() {
    branch=$(git symbolic-ref --short -q HEAD )
    if [[ $branch =~ ([0-9]+\.[0-9]+) ]]; then
        ver=${BASH_REMATCH[1]} 
        echo "$ver"
    else
        #printf "r%s" "$(git rev-list --count HEAD)"
        echo "$pkgver"
    fi
}

package() { 

    for bin in $srcdir/usr/bin/*; do 
        if [[ -f "$bin" ]]; then
             echo install -Dm755 $bin  "$pkgdir/usr/bin/${bin##*/}" 
             install -Dm755 $bin  "$pkgdir/usr/bin/${bin##*/}" 

        fi 
        #mkdir -p $pkgdir/usr/share/doc/$pkgname/
        #install -Dm644 $srcdir/CHANGELOG.md "$pkgdir/usr/share/doc/$pkgname/ChangeLog" 
    done 
}

