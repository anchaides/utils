pkgname=anchaides-utils
pkgver=1.4
pkgrel=1
metanam=utils-meta 
metaver=1.1
metarel=8
# https://github.com/anchaides/utils-meta/archive/refs/tags/v1.03.tar.gz
pkgdesc="helper utils and scripts I have made over time" 
arch=('x86_64')
url="https://github.com/anchaides/utils"
license=('GPL')
#source=("https://github.com/anchaides/$metanam/releases/download/v$metaver-$metarel/$metanam-$metaver-$metarel-$arch.pkg.tar.zst"
#        "https://github.com/anchaides/$metanam/releases/download/v$metaver-$metarel/$metanam-$metaver-$metarel-$arch.pkg.tar.zst.sig"
#)
#source=("file:///tmp/utils-meta/utils-meta-1.1-5-x86_64.pkg.tar.zst"
#        "file:///tmp/utils-meta/utils-meta-1.1-5-x86_64.pkg.tar.zst.sig"
#)
#sha256sums=('87bcfd14e097f63e3c2bec011bb5727928791cb6f060dcb3592a64ae1fd23beb'
#            'SKIP'
#            )

validpgpkeys=('E807522FC5E58C299212FA90B20C037A4409DF78')
depends=("anchaides-meta>=$metaver-$metarel")
changelog=CHANGELOG.md 
build() {

    #sudo pacman -U $metanam-$metaver-$metarel-$arch.pkg.tar.zst --noconfirm 
    echo $PWD
    echo realpath $srcdir 
    mkdir -p "$srcdir/usr/bin"
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

