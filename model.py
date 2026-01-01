import numpy as np
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass # type: ignore

    File = autoclass('java.io.File')
    Interpreter = autoclass('org.tensorflow.lite.Interpreter')
    InterpreterOptions = autoclass('org.tensorflow.lite.Interpreter$Options')
    Tensor = autoclass('org.tensorflow.lite.Tensor')
    DataType = autoclass('org.tensorflow.lite.DataType')
    TensorBuffer = autoclass('org.tensorflow.lite.support.tensorbuffer.TensorBuffer')
    ByteBuffer = autoclass('java.nio.ByteBuffer')
    GpuDelegate = autoclass('org.tensorflow.lite.gpu.GpuDelegate')
    GpuDelegateOptions = autoclass('org.tensorflow.lite.gpu.GpuDelegate$Options')
    CompatibilityList = autoclass('org.tensorflow.lite.gpu.CompatibilityList')

    # dummy import so buildozer isn't cutting it away since it's used by options.setNumThreads
    InterpreterApiOptions = autoclass('org.tensorflow.lite.InterpreterApi$Options')
    Delegate = autoclass('org.tensorflow.lite.Delegate')

    class TensorFlowModel():
        """
        Crossplatform inference for .tflite models
        
        :param model_filename: Path to the model
        :type model_filename: str
        :param num_threads: Number of threads to use
        :type num_threads: int
        :param use_gpu: Use GPU acceleration if available
        :type use_gpu: bool
        :param precision_loss: GPU only: Uses FP16 internally providing significant speed ups, might come with major quality degradation
        :type precision_loss: bool
        :param sustained_speed: GPU only: Load the model to achieve maximum speed (takes really long; only for small models worth it)
        :type sustained_speed: bool
        """
        def __init__(self, model_filename: str, num_threads: int = 1, use_gpu: bool = True, precision_loss: bool = True, sustained_speed: bool = False):
            self.model_filename = model_filename
            self.options = InterpreterOptions()
            self.compatList = CompatibilityList()
            if use_gpu and self.compatList.isDelegateSupportedOnThisDevice():
                delegate_options = self.compatList.getBestOptionsForThisDevice()
                delegate_options = (
                    delegate_options
                    .setPrecisionLossAllowed(precision_loss)
                    .setInferencePreference(1 if sustained_speed else 0)
                )
                gpu_delegate = GpuDelegate(delegate_options)
                self.options.addDelegate(gpu_delegate)
                print("set gpu")
            else:
                self.options.setNumThreads(num_threads)
                self.options.setUseXNNPACK(True)

        def load(self):
            """
            Loads the model from the path given in the constructor. This takes some time (for a CNN with 15M parameters around 2s)
            """
            model = File(self.model_filename)
            self.interpreter = Interpreter(model, self.options)
            self.allocate_tensors()

        def allocate_tensors(self):
            self.interpreter.allocateTensors()
            self.input_shape = self.interpreter.getInputTensor(0).shape()
            self.output_shape = self.interpreter.getOutputTensor(0).shape()
            self.output_type = self.interpreter.getOutputTensor(0).dataType()

        def get_input_shape(self):
            return self.input_shape

        def resize_input(self, shape):
            if self.input_shape != shape:
                self.interpreter.resizeInput(0, shape)
                self.allocate_tensors()

        def pred(self, x):
            """
            Run inference.
            
            :param x: Input numpy array
            """
            # assumes one input and one output for now
            input = ByteBuffer.wrap(x.tobytes())
            output = TensorBuffer.createFixedSize(self.output_shape, self.output_type)
            self.interpreter.run(input, output.getBuffer().rewind())
            return np.reshape(np.array(output.getFloatArray()), self.output_shape)

elif platform == 'ios':
    from pyobjus import autoclass, objc_arr # type: ignore
    from ctypes import c_float, cast, POINTER

    NSString = autoclass('NSString')
    NSError = autoclass('NSError')
    Interpreter = autoclass('TFLInterpreter')
    InterpreterOptions = autoclass('TFLInterpreterOptions')
    NSData = autoclass('NSData')
    NSMutableArray = autoclass('NSMutableArray')

    class TensorFlowModel:
        def load(self, model_filename, num_threads=None):
            self.error = NSError.alloc()
            model = NSString.stringWithUTF8String_(model_filename)
            options = InterpreterOptions.alloc().init()
            if num_threads is not None:
                options.numberOfThreads = num_threads
            self.interpreter = Interpreter.alloc(
            ).initWithModelPath_options_error_(model, options, self.error)
            self.allocate_tensors()

        def allocate_tensors(self):
            self.interpreter.allocateTensorsWithError_(self.error)
            self.input_shape = self.interpreter.inputTensorAtIndex_error_(
                0, self.error).shapeWithError_(self.error)
            self.input_shape = [
                self.input_shape.objectAtIndex_(_).intValue()
                for _ in range(self.input_shape.count())
            ]
            self.output_shape = self.interpreter.outputTensorAtIndex_error_(
                0, self.error).shapeWithError_(self.error)
            self.output_shape = [
                self.output_shape.objectAtIndex_(_).intValue()
                for _ in range(self.output_shape.count())
            ]
            self.output_type = self.interpreter.outputTensorAtIndex_error_(
                0, self.error).dataType

        def get_input_shape(self):
            return self.input_shape

        def resize_input(self, shape):
            if self.input_shape != shape:
                # workaround as objc_arr doesn't work as expected on iPhone
                array = NSMutableArray.new()
                for x in shape:
                    array.addObject_(x)
                self.interpreter.resizeInputTensorAtIndex_toShape_error_(
                    0, array, self.error)
                self.allocate_tensors()

        def pred(self, x):
            # assumes one input and one output for now
            bytestr = x.tobytes()
            # must cast to ctype._SimpleCData so that pyobjus passes pointer
            floatbuf = cast(bytestr, POINTER(c_float)).contents
            data = NSData.dataWithBytes_length_(floatbuf, len(bytestr))
            print(dir(self.interpreter))
            self.interpreter.copyData_toInputTensor_error_(
                data, self.interpreter.inputTensorAtIndex_error_(
                    0, self.error), self.error)
            self.interpreter.invokeWithError_(self.error)
            output = self.interpreter.outputTensorAtIndex_error_(
                0, self.error).dataWithError_(self.error).bytes()
            # have to do this to avoid memory leaks...
            while data.retainCount() > 1:
                data.release()
            return np.reshape(
                np.frombuffer(
                    (c_float * np.prod(self.output_shape)).from_address(
                        output.arg_ref), c_float), self.output_shape)

else:
    if platform == 'win':
        import tensorflow as tf
        Interpreter = tf.lite.Interpreter

    else:
        # ai-edege-litert is only available on Linux/WSL and MacOS 
        from ai_edge_litert.interpreter import Interpreter # type: ignore

    class TensorFlowModel:
        def load(self, model_filename, num_threads=None):
            self.interpreter = Interpreter(model_filename,
                                                   num_threads=num_threads)
            self.interpreter.allocate_tensors()

        def resize_input(self, shape):
            if list(self.get_input_shape()) != shape:
                self.interpreter.resize_tensor_input(0, shape)
                self.interpreter.allocate_tensors()

        def get_input_shape(self):
            return self.interpreter.get_input_details()[0]['shape']

        def pred(self, x):
            # assumes one input and one output for now
            self.interpreter.set_tensor(
                self.interpreter.get_input_details()[0]['index'], x)
            self.interpreter.invoke()
            return self.interpreter.get_tensor(
                self.interpreter.get_output_details()[0]['index'])