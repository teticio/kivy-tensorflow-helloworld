# create TFLite model or use demo with notebook
install buildozer https://pypi.org/project/buildozer/

# create buildozer.spec file or use demo
buildozer init
source.include_exts = py,png,jpg,kv,atlas,tflite
android.gradle_dependencies = "org.tensorflow:tensorflow-lite:+","org.tensorflow:tensorflow-lite-support:0.0.0-nightly"
requirements = python3,kivy,numpy
android.arch = x86
buildozer android debug

# you will need an apple developer account
brew install cocoapods
pip install git+https://github.com/kivy/buildozer.git@master cython pbxproj cookiecutter
buildozer ios list_identities
ios.codesign.debug = "Apple Development:  (MZTP9TD3KK)"
buildozer ios debug
cd .buildozer/ios/platform/kivy-ios/myapp-ios/
cp YourApp/Podfile .
pod install
open -a Xcode myapp.xcworkspace
click on myapp, Signing & Capabilities, Team
add $(inherited) to GCC_PREPROCESSOR_DEFINITIONS, HEADER_SEARCH_PATHS and OTHER_LDFLAGS

pip install tensorflow numpy kivy