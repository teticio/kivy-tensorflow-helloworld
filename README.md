# create TFLite model or use demo with notebook

install buildozer https://pypi.org/project/buildozer/
pip install --force git+https://github.com/kivy/buildozer.git ???

# create buildozer.spec file or use demo
buildozer init
source.include_exts = py,png,jpg,kv,atlas,tflite
android.gradle_dependencies = "org.tensorflow:tensorflow-lite:+","org.tensorflow:tensorflow-lite-support:0.0.0-nightly"
requirements = python3,kivy,numpy
####android.minapi = 24
android.arch = x86
buildozer android debug

pip install tensorflow numpy kivy