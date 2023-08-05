tensorpack
==========

Neural Network Toolbox on TensorFlow.

|Build Status| |badge|

See some `examples <examples>`__ to learn about the framework:

Vision:
~~~~~~~

-  `DoReFa-Net: train binary / low-bitwidth CNN on
   ImageNet <examples/DoReFa-Net>`__
-  `Train ResNet on ImageNet / Cifar10 / SVHN <examples/ResNet>`__
-  `Generative Adversarial Network(GAN) variants <examples/GAN>`__,
   including DCGAN, InfoGAN, Conditional GAN, WGAN, BEGAN, DiscoGAN,
   Image to Image, CycleGAN.
-  `Fully-convolutional Network for Holistically-Nested Edge
   Detection(HED) <examples/HED>`__
-  `Spatial Transformer Networks on MNIST
   addition <examples/SpatialTransformer>`__
-  `Visualize CNN saliency maps <examples/Saliency>`__
-  `Similarity learning on MNIST <examples/SimilarityLearning>`__

Reinforcement Learning:
~~~~~~~~~~~~~~~~~~~~~~~

-  `Deep Q-Network(DQN) variants on Atari
   games <examples/DeepQNetwork>`__, including DQN, DoubleDQN,
   DuelingDQN.
-  `Asynchronous Advantage Actor-Critic(A3C) with demos on OpenAI
   Gym <examples/A3C-Gym>`__

Speech / NLP:
~~~~~~~~~~~~~

-  `LSTM-CTC for speech recognition <examples/CTC-TIMIT>`__
-  `char-rnn for fun <examples/Char-RNN>`__
-  `LSTM language model on PennTreebank <examples/PennTreebank>`__

The examples are not only for demonstration of the framework -- you can
train them and reproduce the results in papers.

Features:
---------

It's Yet Another TF wrapper, but different in: 1. Not focus on models. +
There are already too many symbolic function wrappers. Tensorpack
includes only a few common models, and helpful tools such as
``LinearWrap`` to simplify large models. But you can use any other
wrappers within tensorpack, such as
sonnet/Keras/slim/tflearn/tensorlayer/....

2. Focus on **training speed**.

   -  Tensorpack trainer is almost always faster than ``feed_dict``
      based wrappers. Even on a tiny CNN example, the training runs `2x
      faster <https://gist.github.com/ppwwyyxx/8d95da79f8d97036a7d67c2416c851b6>`__
      than the equivalent Keras code.

   -  Data-parallel multi-GPU training is off-the-shelf to use. It is as
      fast as Google's `benchmark
      code <https://github.com/tensorflow/benchmarks>`__.

   -  Data-parallel distributed training is off-the-shelf to use. It is
      as slow as Google's `benchmark
      code <https://github.com/tensorflow/benchmarks>`__.

3. Focus on large datasets.

   -  It's painful to read/preprocess data from TF. Use **DataFlow** to
      load large datasets (e.g. ImageNet) in **pure Python** with
      multi-process prefetch.
   -  DataFlow has a unified interface, so you can compose and reuse
      them to perform complex preprocessing.

4. Interface of extensible **Callbacks**. Write a callback to implement
   everything you want to do apart from the training iterations, and
   enable it with one line of code. Common examples include:

   -  Change hyperparameters during training
   -  Print some tensors of interest
   -  Run inference on a test dataset
   -  Run some operations once a while
   -  Send loss to your phone

Install:
--------

Dependencies:

-  Python 2 or 3
-  TensorFlow >= 1.0.0 (>=1.1.0 for Multi-GPU)
-  Python bindings for OpenCV (Optional, but required by a lot of
   features)

   ::

       pip install -U git+https://github.com/ppwwyyxx/tensorpack.git
       # or add `--user` to avoid system-wide installation.

.. |Build Status| image:: https://travis-ci.org/ppwwyyxx/tensorpack.svg?branch=master
   :target: https://travis-ci.org/ppwwyyxx/tensorpack
.. |badge| image:: https://readthedocs.org/projects/pip/badge/?version=latest
   :target: http://tensorpack.readthedocs.io/en/latest/index.html


