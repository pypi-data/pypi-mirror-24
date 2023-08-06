"""
Provides common loss functions.

Losses
---------

.. autosummary::
   :nosignatures:

   CrossEntropyLoss

Base class
----------

To implement a new loss, subclass the :class:`Loss` class.

.. autosummary::
   :nosignatures:

   Loss

"""
from __future__ import division
import sys
import abc
abstractmethod = abc.abstractmethod

if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:  # pragma: no cover
    ABC = abc.ABCMeta('ABC', (), {})

import numpy as np
from utils import one_hot_like


class Loss(ABC):
    """Base class for losses.

    """

    def __init__(self, model):
        pass

    @abstractmethod
    def _fallback(self):
        raise NotImplementedError

    def name(self):
        return self.__class__.__name__


class LogitLoss(Loss):
    # TODO: Logit or Negative Logit

    def _fallback(self, logits, label):
        loss = logits[label]
        gradient = one_hot_like(logits, label)
        return loss, gradient

    def _tensorflow(self, logits, label):
        loss = logits[label]
        return loss


class CrossEntropyLoss(Loss):
    """Sparse softmax cross-entropy loss calculates the cross-entropy
    using logits and a single ground-truth label.

    """

    def _fallback(self, logits, label):
        logits = logits - np.max(logits)
        e = np.exp(logits)
        s = np.sum(e)
        loss = np.log(s) - logits[label]
        gradient = e / s - one_hot_like(logits, label)
        return loss, gradient

    def _tensorflow(self, logits, label):
        import tensorflow as tf
        loss = tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels=label[tf.newaxis],
            logits=logits[tf.newaxis])
        loss = tf.squeeze(loss, axis=0)
        return loss


class CarlinieLoss(Loss):

    def _tensorflow(self, logits, label):
        import tensorflow as tf
        loss = tf.reduce_max(logits) - logits[label]
        # TODO: why does wieland add relu?
        return loss
