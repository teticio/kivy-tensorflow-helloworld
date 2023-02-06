# Kivy Tensorflow Hello World

This is a "Hello World" for running Tensorflow Lite on iOS, Android, MacOS, Windows and Linux using Python and Kivy.

## Create a Tensorflow Lite model

You can use the Jupyter notebook in notebooks to create a Tensorflow Lite model file. A dummy example is provided for testing purposes.

## Install buildozer

Install basic Python requirements (all platforms)

```bash
pip install buildozer cython
```

Follow the instructions for your platform [here](https://pypi.org/project/buildozer/).

## MacOS, Windows and Linux

```bash
pip install tensorflow numpy kivy
python3 main.py
```

## Android

Currently you can only build for Android using `buildozer` on Linux.

Use the included `buildozer.spec` file or make the following changes to one created by `buildozer init`

```
source.include_exts = py,png,jpg,kv,atlas,tflite
requirements = python3,kivy,numpy
android.api = 30
android.minapi = 24
android.gradle_dependencies = "org.tensorflow:tensorflow-lite:+","org.tensorflow:tensorflow-lite-support:+"
```

Note that if your `tflite` model file is too big to be packaged with your APK, you will have to find some other way of getting it on to the device. If this is the case then change this line to ensure it is not included in the package.

```
source.include_exts = py,png,jpg,kv,atlas
```

Change the architecture you are building for to match that of your device or emulator

```
android.arch = x86
```

Build the APK

```bash
buildozer android debug
```

and install it with

```bash
adb install bin/myapp-0.1-x86-debug.apk
```

## iOS

Remember that you will need an Apple developer account to be able to install your app on a real iPhone.

Install prerequisite system packages

```bash
brew install cocoapods pkg-config autoconf automake
```

Install additional Python requirements

```bash
pip install pbxproj cookiecutter
```

Build your app and install the Tensorflow Lite pod

```bash
buildozer ios debug
cd .buildozer/ios/platform/kivy-ios/myapp-ios/
cp YourApp/Podfile .
pod install
open -a Xcode myapp.xcworkspace
```

As indicated in the warning messages, you will need to make some changes to the project configuration. You can either do this by editing `myapp-ios\myapp.xcodeproj` or by editing the Build Settings for `myapp` in Xcode. Search for `GCC_PREPROCESSOR_DEFINITIONS` and add `$(inherited)` to the Debug target. Then repeat the process for `HEADER_SEARCH_PATHS`, `OTHER_LDFLAGS` and (possibly) `EXCLUDED_ARCHS[sdk=iphonesimulator*]` for all targets. Now you should be able to build and run your app.

Every time you build you will need to run `buildozer ios debug` and then build and deploy from Xcode.
