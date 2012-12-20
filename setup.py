from setuptools import setup
import py2app

# Build the .app file
setup(
    options=dict(
        py2app=dict(
            #iconfile='resources/myapp-icon.icns',
            packages='wx',
            site_packages=True,
            #resources=['resources/License.txt'],
            plist=dict(
                CFBundleName               = "Cryptography",
                CFBundleShortVersionString = "1.0.0",     # must be in X.X.X format
                CFBundleGetInfoString      = "Cryptography 1.0.0",
                CFBundleExecutable         = "Cryptography",
                CFBundleIdentifier         = "com.tbsoftware.Cryptography",
            ),
        ),
    ),
    app=[ 'wxCrytopgraphywidget.py' ]
)