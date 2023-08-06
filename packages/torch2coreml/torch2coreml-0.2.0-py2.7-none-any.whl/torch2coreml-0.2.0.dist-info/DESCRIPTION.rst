Convert Torch7 models into Apple CoreML format.
===============================================

This tool helps convert Torch7 models into `Apple
CoreML <https://developer.apple.com/documentation/coreml>`__ format
which can then be run on Apple devices.

.. figure:: https://github.com/prisma-ai/torch2coreml/raw/master/screenshot.jpg
   :alt: fast-neural-style example app

   fast-neural-style example app screenshot

Installation
------------

.. code:: bash

    pip install -U torch2coreml

In order to use this tool you need to have these installed: \* Xcode 9
\* python 2.7

If you want to run tests, you need MacOS High Sierra 10.13 installed.

Dependencies
------------

-  coremltools (0.6.2+)
-  PyTorch

How to use
----------

Using this library you can implement converter for your own model types.
An example of such a converter is located at
"example/fast-neural-style/convert-fast-neural-style.py". To implement
converters you should use single function "convert" from torch2coreml:

.. code:: python

    from torch2coreml import convert

This function is simple enough to be self-describing:

.. code:: python

    def convert(model,
                input_shapes,
                input_names=['input'],
                output_names=['output'],
                mode=None,
                image_input_names=[],
                preprocessing_args={},
                image_output_names=[],
                deprocessing_args={},
                class_labels=None,
                predicted_feature_name='classLabel',
                unknown_layer_converter_fn=None)

Parameters
~~~~~~~~~~

| **model**: Torch7 model (loaded with PyTorch) \| str
| A trained Torch7 model loaded in python using PyTorch or path to file
  with model (\*.t7).

**input\_shapes**: list of tuples Shapes of the input tensors.

| **mode**: str ('classifier', 'regressor' or None)
| Mode of the converted coreml model:
| 'classifier', a NeuralNetworkClassifier spec will be constructed.
| 'regressor', a NeuralNetworkRegressor spec will be constructed.

| **preprocessing\_args**: dict
| 'is\_bgr', 'red\_bias', 'green\_bias', 'blue\_bias', 'gray\_bias',
  'image\_scale' keys with the same meaning as
  https://apple.github.io/coremltools/generated/coremltools.models.neural\_network.html#coremltools.models.neural\_network.NeuralNetworkBuilder.set\_pre\_processing\_parameters

| **deprocessing\_args**: dict
| Same as 'preprocessing\_args' but for deprocessing.

| **class\_labels**: A string or list of strings.
| As a string it represents the name of the file which contains the
  classification labels (one per line). As a list of strings it
  represents a list of categories that map the index of the output of a
  neural network to labels in a classifier.

| **predicted\_feature\_name**: str
| Name of the output feature for the class labels exposed in the Core ML
  model (applies to classifiers only). Defaults to 'classLabel'

| **unknown\_layer\_converter\_fn**: function with signature:
| (builder, name, layer, input\_names, output\_names)
| builder: object - instance of NeuralNetworkBuilder class
| name: str - generated layer name
| layer: object - PyTorch (python) object for corresponding layer
| input\_names: list of strings
| output\_names: list of strings
| Returns: list of strings for layer output names
| Callback function to handle unknown for torch2coreml layers

Returns
~~~~~~~

model: A coreml model.

Currently supported
-------------------

Models
~~~~~~

Only Torch7 "nn" module is supported now.

Layers
~~~~~~

List of Torch7 layers that can be converted into their CoreML
equivalent:

1.  Sequential
2.  ConcatTable
3.  SpatialConvolution
4.  ELU
5.  ReLU
6.  SpatialBatchNormalization
7.  Identity
8.  CAddTable
9.  SpatialFullConvolution
10. SpatialSoftMax
11. SpatialMaxPooling
12. SpatialAveragePooling
13. View
14. Linear
15. Tanh
16. MulConstant
17. SpatialZeroPadding
18. SpatialReflectionPadding
19. Narrow
20. SpatialUpSamplingNearest
21. SplitTable

License
-------

Copyright (c) 2017 Prisma Labs, Inc. All rights reserved.

Use of this source code is governed by the `MIT
License <https://opensource.org/licenses/MIT>`__ that can be found in
the LICENSE.txt file.


