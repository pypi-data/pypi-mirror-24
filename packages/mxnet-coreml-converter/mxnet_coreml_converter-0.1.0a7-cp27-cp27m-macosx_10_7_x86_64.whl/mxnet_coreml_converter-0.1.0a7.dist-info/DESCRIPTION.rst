MXNET -> CoreML Converter
=========================

This tool helps convert MXNet models into `Apple CoreML <https://developer.apple.com/documentation/coreml>`_ format which can then be run on Apple devices. You can find more information about tool on our `github <https://github.com/apache/incubator-mxnet/tree/master/tools/coreml>`_ page.

Prerequisites
-------------
This package can only be installed on MacOS X since it relies on Apple's CoreML SDK. This tool can be run on MacOS 10.12 or higher though for running inferences on the converted model MacOS 10.13 or higher is needed (or for phones, iOS 11 or above).

Installation
------------
The method for installing this tool follows the `standard python package installation steps <https://packaging.python.org/installing/>`_. Once you have set up a python environment, run::

  pip install mxnet-coreml-converter

The package `documentation <https://github.com/apache/incubator-mxnet/tree/master/tools/coreml>`_ contains more details on how to use coremltools.

Dependencies
------------
This tool has the following dependencies:
* pyyaml (3.12+)
* mxnet (0.10.0+)
* coremltools (0.5.1+)

Sample Usage
------------

In order to convert, say a `Squeezenet model <http://data.mxnet.io/models/imagenet/squeezenet/>`_, with labels from `synset.txt <http://data.mxnet.io/models/imagenet/synset.txt>`_, execute this ::

  mxnet_coreml_converter.py --model-prefix='squeezenet_v1.1' \
  --epoch=0 --input-shape='{"data":"3,227,227"}' \
  --mode=classifier --pre-processing-arguments='{"image_input_names":"data"}' \
  --class-labels synset.txt --output-file="squeezenetv11.mlmodel"

More Information
----------------
* `Github page for this tool <https://github.com/apache/incubator-mxnet/tree/master/tools/coreml>`_
* `MXNet framework documentation <https://github.com/apache/incubator-mxnet>`_
* `Apple CoreML <https://developer.apple.com/documentation/coreml>`_


