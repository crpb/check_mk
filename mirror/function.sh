#!/usr/bin/env bash
# source me in env'
# and use me like that...
# DownloadCheckMK 2.1.0p6

DownloadCheckMK() {
  local RELEASES TARGETDIR VERSION BASEURL RELEASE
  RELEASES="stretch buster bullseye bionic focal jammy"
  TARGETDIR=/var/www/domain.tld/www/html
  #TARGETDIR=$HOME/test
  VERSION="$1"
  BASEURL="https://download.checkmk.com/checkmk/${VERSION}/check-mk-raw-${VERSION}_0."
  cd "$TARGETDIR" || exit
  for RELEASE in $RELEASES ; do
    wget -nc "${BASEURL}${RELEASE}_amd64.deb"
    if [[ "$RELEASE" = "bullseye" ]]; then
      TMPDIR=$(mktemp -d)
      ar -x "${TARGETDIR}/check-mk-raw-${VERSION}_0.${RELEASE}_amd64.deb" data.tar.xz --output="$TMPDIR"
      FILE="$TMPDIR/data.tar.xz"
      tar Jft "$FILE" |grep -E '(agent.msi|all.deb|rpm|agent.freebsd)$' |xargs -n 1 tar Jfx "$FILE" --transform='s/.*\///' -C $TARGETDIR
      mv "$TARGETDIR/check_mk_agent.msi" "$TARGETDIR/check_mk_agent-$VERSION-1.msi"
      rm -Rf "$TMPDIR"
    fi
  done
}

alias get_mirrored_files="ls -1 /var/www/domain.tld/www/html| sed 's|^|https://domain.tld/|g'"
# and for remote-listing...
# alias get_mirrored_files="ssh mirror-host ls -1 /var/www/domain.tld/www/html| sed 's|^|https://domain.tld/|g'"
# For Later
# curl https://checkmk.com/download |grep -Po '.*window.downloads = \K.*' |jq

