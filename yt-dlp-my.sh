#!/usr/bin/env bash
yt-dlp --version
yt-dlp --write-info-json --write-comments --write-thumbnail --write-subs "$1"
