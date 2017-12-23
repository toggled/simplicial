# Tests of construction of flag complexes in simplicial complex class
#
# Copyright (C) 2017 Simon Dobson
# 
# This file is part of simplicial, simplicial topology in Python.
#
# Simplicial is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Simplicial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Simplicial. If not, see <http://www.gnu.org/licenses/gpl.html>.

import unittest
import numpy
import copy
import itertools
from simplicial import *

class FlagTests(unittest.TestCase):

    def testOneTriangle( self ):
        '''Test creating a single triangle.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = '12', fs = [1, 2])
        c.addSimplex(id = '23', fs = [2, 3])
        c.addSimplex(id = '31', fs = [3, 1])
        flag = c.flagComplex()
        self.assertEqual(flag.maxOrder(), 2)
        ss = flag.numberOfSimplicesOfOrder()
        self.assertEqual(ss[0], 3)
        self.assertEqual(ss[1], 3)
        self.assertEqual(ss[2], 1)
        self.assertItemsEqual(flag.basisOf((list(flag.simplicesOfOrder(2)))[0]), [ 1, 2, 3 ])

    def testOneTriangleAlready( self ):
        '''Test that we don't add a duplicate triangle.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [1, 2])
        c.addSimplex(id = 23, fs = [2, 3])
        c.addSimplex(id = 31, fs = [3, 1])
        c.addSimplex(id = 123, fs = [12, 23, 31 ]) 
        flag = c.flagComplex()
        self.assertEqual(flag.maxOrder(), 2)
        ss = flag.numberOfSimplicesOfOrder()
        self.assertEqual(ss[0], 3)
        self.assertEqual(ss[1], 3)
        self.assertEqual(ss[2], 1)

    def testOneTetrahedron( self ):
        '''Test that we correctly form a tetrahedron.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        for bs in itertools.combinations([ 1, 2, 3, 4 ], 2):
            c.addSimplexWithBasis(bs = bs)
        flag = c.flagComplex()
        self.assertEqual(flag.maxOrder(), 3)
        ss = flag.numberOfSimplicesOfOrder()
        self.assertEqual(ss[0], 4)
        self.assertEqual(ss[1], 6)
        self.assertEqual(ss[2], 4)
        self.assertEqual(ss[3], 1)

    def testTwoTetrahedra( self ):
        '''Test that we correctly form two tetrahedra, connected at a point.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        for bs in itertools.combinations([ 1, 2, 3, 4 ], 2):
            c.addSimplexWithBasis(bs = bs)
        c.addSimplex(id = 5)
        c.addSimplex(id = 6)
        c.addSimplex(id = 7)
        for bs in itertools.combinations([ 1, 5, 6, 7 ], 2):
            c.addSimplexWithBasis(bs = bs)
        flag = c.flagComplex()
        self.assertEqual(flag.maxOrder(), 3)
        ss = flag.numberOfSimplicesOfOrder()
        self.assertEqual(ss[0], 7)
        self.assertEqual(ss[1], 12)
        self.assertEqual(ss[2], 8)
        self.assertEqual(ss[3], 2)
        tbs = set()
        for s in flag.simplicesOfOrder(3):
            tbs |= flag.basisOf(s)
        self.assertItemsEqual(tbs, [ 1, 2, 3, 4, 5, 6, 7 ])
        ibs = set()
        for s in flag.simplicesOfOrder(3):
            if len(ibs) == 0:
                ibs = flag.basisOf(s)
            else:
                ibs &= flag.basisOf(s)
        self.assertItemsEqual(ibs, [ 1 ])
        
