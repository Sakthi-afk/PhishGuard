[app]
title = PhishGuard
package.name = phishguard
package.domain = org.phishguard
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,pkl,arff
version = 1.0.0

# Critical Requirements for Machine Learning on Android
requirements = python3,kivy==2.3.0,numpy,scikit-learn,joblib

orientation = portrait
osx.kivy_version = 2.3.0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
fullscreen = 0
archs = arm64-v8a
allow_backup = True
accept_sdk_license = True
api = 33
minapi = 21
ndk = 25.2.9519653

# Enable C-compiler for numpy/scikit-learn
p4a.branch = master
