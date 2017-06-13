#!/usr/bin/env bash

if [ ! -f "com.adobe.acs.bundles.twitter4j-content-1.0.0.zip" ]; then
    curl -O https://repo.adobe.com/nexus/content/groups/public/com/adobe/acs/bundles/com.adobe.acs.bundles.twitter4j-content/1.0.0/com.adobe.acs.bundles.twitter4j-content-1.0.0.zip
fi

python upload-package.py
