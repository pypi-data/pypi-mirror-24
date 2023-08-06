import unittest
import inferno.utils.model_utils as mu
from inferno.utils.exceptions import ShapeError
import torch
import torch.nn as nn


class ModelUtilTester(unittest.TestCase):
    def test_model_tester(self):
        model = mu.ModelTester((1, 10, 32, 32), (1, 20, 32, 32))(nn.Conv2d(10, 20, 3, padding=1))
        with self.assertRaises(ShapeError):
            mu.ModelTester((1, 10, 32, 32), (1, 30, 32, 32))(model)

    def test_model_tester_cuda(self):
        if not torch.cuda.is_available():
            return
        model = \
            mu.ModelTester((1, 10, 32, 32), (1, 20, 32, 32))(nn.Conv2d(10, 20, 3, padding=1).cuda())
        with self.assertRaises(ShapeError):
            mu.ModelTester((1, 10, 32, 32), (1, 30, 32, 32))(model)

if __name__ == '__main__':
    unittest.main()