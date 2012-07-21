#Maintainer: Inkane <neoinkaneglade@aol.com> 
 
pkgname="rdepend-finder-git"
pkgrel=1
pkgdesc="Allows to upload text files to paste.chakra-project.org"
arch=("any")
url="https://github.com/Inkane/chakra-paste"
license=('BSD')
depends=('python3-termcolor')
makedepends=('git')
 
_gitroot="git://github.com/Inkane/pacman-rdepfinder.git"
_gitname="pacman-rdepfinder"
 
package() {
  cd "$srcdir"
  msg "Connecting to GIT server...."
 
  if [[ -d "$_gitname" ]]; then
    cd "$_gitname" && git pull origin
    msg "The local files are updated."
  else
    git clone "$_gitroot" "$_gitname"
  fi
 
  msg "GIT checkout done or server timeout"
  msg "Starting build..."
 
  rm -rf "$srcdir/$_gitname-build"
  git clone "$srcdir/$_gitname" "$srcdir/$_gitname-build"
  cd "$srcdir/$_gitname-build"
  python2 setup.py install --root="${pkgdir}"
  ln -s "$pkgdir"/rdepends.py "$pkdir"/rdepend-finder
}
 
# vim:set ts=2 sw=2 et:
