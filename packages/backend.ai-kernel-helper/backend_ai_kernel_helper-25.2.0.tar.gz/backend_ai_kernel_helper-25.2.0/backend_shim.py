
# DO NOT EDIT THIS FILE -- AUTOGENERATED BY PANTS

import errno
import os
import setuptools.build_meta

backend = setuptools.build_meta.__legacy__

dist_dir = "dist/"
build_wheel = True
build_sdist = True
wheel_config_settings = {
}
sdist_config_settings = {
}

# Python 2.7 doesn't have the exist_ok arg on os.makedirs().
try:
    os.makedirs(dist_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

wheel_path = backend.build_wheel(dist_dir, wheel_config_settings) if build_wheel else None
sdist_path = backend.build_sdist(dist_dir, sdist_config_settings) if build_sdist else None

if wheel_path:
    print("wheel: {wheel_path}".format(wheel_path=wheel_path))
if sdist_path:
    print("sdist: {sdist_path}".format(sdist_path=sdist_path))
