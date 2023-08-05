#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit testing for pyswarms.single.GBestPSO"""

# Import modules
import unittest
import numpy as np

# Import from package
from pyswarms.discrete import BinaryPSO
from pyswarms.utils.functions.single_obj import sphere_func

class Base(unittest.TestCase):
    """Base class for tests

    This class defines a common `setUp` method that defines attributes
    which are used in the various tests.
    """
    def setUp(self):
        """Set up test fixtures"""
        self.options = {'c1':0.5, 'c2':0.7, 'w':0.5, 'k': 2, 'p': 2}

class Instantiation(Base):
    """Tests all aspects of instantiation

    Tests include: instantiation with args of wrong type, instantiation
    with input values outside constraints, etc.
    """
    def test_keyword_check_fail(self):
        """Tests if exceptions are thrown when keywords are missing"""
        check_c1 = {'c2':0.7, 'w':0.5, 'k': 2, 'p': 2}
        check_c2 = {'c1':0.5, 'w':0.5, 'k': 2, 'p': 2}
        check_m = {'c1':0.5, 'c2':0.7, 'k': 2, 'p': 2}
        check_k = {'c1':0.5, 'c2':0.7, 'w':0.5, 'p': 2}
        check_p = {'c1':0.5, 'c2':0.7, 'w':0.5, 'k': 2}
        with self.assertRaises(KeyError):
            optimizer = BinaryPSO(5,2,**check_c1)
        with self.assertRaises(KeyError):
            optimizer = BinaryPSO(5,2,**check_c2)
        with self.assertRaises(KeyError):
            optimizer = BinaryPSO(5,2,**check_m)
        with self.assertRaises(KeyError):
            optimizer = BinaryPSO(5,2,**check_k)
        with self.assertRaises(KeyError):
            optimizer = BinaryPSO(5,2,**check_p)

    def test_k_fail(self):
        """Tests if exception is thrown when feeding an invalid k."""
        k_less_than_min = {'c1':0.5, 'c2':0.7, 'w':0.5, 'k':-1, 'p':2}
        k_more_than_max = {'c1':0.5, 'c2':0.7, 'w':0.5, 'k':6, 'p':2}

        with self.assertRaises(ValueError):
            optimizer = BinaryPSO(5,2,**k_less_than_min)
        with self.assertRaises(ValueError):
            optimizer = BinaryPSO(5,2,**k_more_than_max)

    def test_p_fail(self):
        """Tests if exception is thrown when feeding an invalid p."""
        p_fail = {'c1':0.5, 'c2':0.7, 'w':0.5, 'k':2, 'p':5}
        with self.assertRaises(ValueError):
            optimizer = BinaryPSO(5,2, **p_fail)

    def test_vclamp_type_fail(self):
        """Tests if exception is thrown when v_clamp is not a tuple."""
        v_clamp = [1,3]
        with self.assertRaises(TypeError):
            optimizer = BinaryPSO(5,2,v_clamp=v_clamp, **self.options)

    def test_vclamp_shape_fail(self):
        """Tests if exception is thrown when v_clamp is not equal to 2"""
        v_clamp = (1,1,1)
        with self.assertRaises(IndexError):
            optimizer = BinaryPSO(5,2,v_clamp=v_clamp, **self.options)

    def test_vclamp_minmax_fail(self):
        """Tests if exception is thrown when v_clamp's minmax is wrong"""
        v_clamp = (3,2)
        with self.assertRaises(ValueError):
            optimizer = BinaryPSO(5,2,v_clamp=v_clamp, **self.options)

class Methods(Base):
    """Tests all aspects of the class methods

    Tests include: wrong inputs of methods, wrong return types,
    unexpected attribute setting, and etc.
    """

    def test_reset(self):
        """Tests if the reset method resets the attributes required"""
        # Perform a simple optimization
        optimizer = BinaryPSO(5,2, **self.options)
        optimizer.optimize(sphere_func, 100, verbose=0)
        # Reset the attributes
        optimizer.reset()
        # Perform testing
        self.assertEqual(optimizer.lbest_cost, np.inf)
        self.assertIsNone(optimizer.lbest_pos)

class Run(Base):
    """Perform a single run of the algorithm to see if something breaks."""

    def test_run(self):
        """Perform a single run."""
        optimizer = BinaryPSO(10,2, **self.options)
        try:
            optimizer.optimize(sphere_func, 1000, verbose=0)
            trigger = True
        except:
            print('Execution failed.')
            trigger = False

        self.assertTrue(trigger)

if __name__ == '__main__':
    unittest.main()