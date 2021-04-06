# Kivy Tensorflow Hello World

This is a "Hello World" for running Tensorflow Lite on iOS, Android, MacOS, Windows and Linux using Python and Kivy.

## Create a Tensorflow Lite model

You can use the Jupyter notebook in notebooks to create a Tensorflow Lite model file. A dummy example is provided for testing purposes.

## Install buildozer

Follow the instructions for your platform [here](https://pypi.org/project/buildozer/) 

At the time of writing I had to install buildozer from the master branch for building on iOS (on a Mac) like so

```
pip install git+https://github.com/kivy/buildozer.git@master cython pbxproj cookiecutter
```

## MacOS, Windows and Linux

```
pip install tensorflow numpy kivy

python3 main.py
```

## Android

Currently you can only build for Android using buildozer on Linux. Create a new buildozer.spec file or use the example one from the repo.
```
buildozer init
```

Make the following changes to the buildozer.spec file
```
source.include_exts = py,png,jpg,kv,atlas,tflite

android.gradle_dependencies = "org.tensorflow:tensorflow-lite:+","org.tensorflow:tensorflow-lite-support:0.0.0-nightly"

requirements = python3,kivy,numpy
```
Note that if your tflite model file is too big to be packaged with your APK, you will have to find some other way of getting it on to the device. If this is the case then change this line to ensure it is not included in the package.
```
source.include_exts = py,png,jpg,kv,atlas
```
Change the architecture you are building for to match that of your device or emulator
```
android.arch = x86
```

Build the APK
```
buildozer android debug
```
and install it with
```
adb install bin/myapp-0.1-x86-debug.apk
```

## iOS

Remember that you will need an Apple developer account to be able to install your app on a real iPhone.

Install Cocoapods if you haven't already
```
brew install cocoapods
```

Build your app and install the Tensorflow Lite pod
```
buildozer ios debug

cd .buildozer/ios/platform/kivy-ios/myapp-ios/

cp YourApp/Podfile .

pod install

open -a Xcode myapp.xcworkspace
```

From now on you should open the workspace as opposed to the project. You will almost certainly have to make some changes to the myapp target in Xcode as indicated by `buildozer ios debug` and `pod install`. Every time you build you will need to run `buildozer ios debug` and then build and deploy from Xcode.
