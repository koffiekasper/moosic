#!/bin/bash

youtube-dl  -x --audio-format mp3 --prefer-ffmpeg $1 -o ./workdir/audio.mp3
