#!/bin/bash

echo 'Installing Coursier'
brew install --HEAD coursier/formulas/coursier

echo 'Installing Nailgun'
brew install nailgun

echo 'Creating Scalafmt Nailgun runner in /usr/local/bin/scalafmt_ng'
coursier bootstrap --standalone com.geirsson:scalafmt-cli_2.12:1.2.0 \
  -o /usr/local/bin/scalafmt_ng -f --main com.martiansoftware.nailgun.NGServer