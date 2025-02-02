#!/usr/bin/env python3
# coding: utf-8
"""Test AST representation."""

import unittest

from triton import TritonContext, ARCH, AST_REPRESENTATION


class TestAstRepresentation(unittest.TestCase):

    """Testing the AST Representation."""

    def setUp(self):
        """Define the arch."""
        self.Triton = TritonContext()
        self.Triton.setArchitecture(ARCH.X86_64)
        self.astCtxt = self.Triton.getAstContext()

        self.v1  = self.astCtxt.variable(self.Triton.newSymbolicVariable(8))
        self.v2  = self.astCtxt.variable(self.Triton.newSymbolicVariable(8))
        self.ref = self.Triton.newSymbolicExpression(self.v1 + self.v2, "ref test")

        # Default
        self.assertEqual(self.Triton.getAstRepresentationMode(), AST_REPRESENTATION.SMT)

        self.node = [
            # Overloaded operators                               # SMT                                                           # Python
            ((self.v1 & self.v2),                                "(bvand SymVar_0 SymVar_1)",                                    "(SymVar_0 & SymVar_1)"),
            ((self.v1 + self.v2),                                "(bvadd SymVar_0 SymVar_1)",                                    "((SymVar_0 + SymVar_1) & 0xFF)"),
            ((self.v1 - self.v2),                                "(bvsub SymVar_0 SymVar_1)",                                    "((SymVar_0 - SymVar_1) & 0xFF)"),
            ((self.v1 ^ self.v2),                                "(bvxor SymVar_0 SymVar_1)",                                    "(SymVar_0 ^ SymVar_1)"),
            ((self.v1 | self.v2),                                "(bvor SymVar_0 SymVar_1)",                                     "(SymVar_0 | SymVar_1)"),
            ((self.v1 * self.v2),                                "(bvmul SymVar_0 SymVar_1)",                                    "((SymVar_0 * SymVar_1) & 0xFF)"),
            ((self.v1 / self.v2),                                "(bvudiv SymVar_0 SymVar_1)",                                   "(SymVar_0 / SymVar_1)"),
            ((self.v1 % self.v2),                                "(bvurem SymVar_0 SymVar_1)",                                   "(SymVar_0 % SymVar_1)"),
            ((self.v1 << self.v2),                               "(bvshl SymVar_0 SymVar_1)",                                    "((SymVar_0 << SymVar_1) & 0xFF)"),
            ((self.v1 >> self.v2),                               "(bvlshr SymVar_0 SymVar_1)",                                   "(SymVar_0 >> SymVar_1)"),
            ((~self.v1),                                         "(bvnot SymVar_0)",                                             "(~(SymVar_0) & 0xFF)"),
            ((-self.v1),                                         "(bvneg SymVar_0)",                                             "-SymVar_0"),
            ((self.v1 == self.v2),                               "(= SymVar_0 SymVar_1)",                                        "(SymVar_0 == SymVar_1)"),
            ((self.v1 != self.v2),                               "(not (= SymVar_0 SymVar_1))",                                  "not (SymVar_0 == SymVar_1)"),
            ((self.v1 <= self.v2),                               "(bvule SymVar_0 SymVar_1)",                                    "(SymVar_0 <= SymVar_1)"),
            ((self.v1 >= self.v2),                               "(bvuge SymVar_0 SymVar_1)",                                    "(SymVar_0 >= SymVar_1)"),
            ((self.v1 < self.v2),                                "(bvult SymVar_0 SymVar_1)",                                    "(SymVar_0 < SymVar_1)"),
            ((self.v1 > self.v2),                                "(bvugt SymVar_0 SymVar_1)",                                    "(SymVar_0 > SymVar_1)"),

            # AST api                                            # SMT                                                           # Python
            (self.astCtxt.assert_(self.v1 == 0),                 "(assert (= SymVar_0 (_ bv0 8)))",                              "assert_((SymVar_0 == 0x0))"),
            (self.astCtxt.bv(2, 8),                              "(_ bv2 8)",                                                    "0x2"),
            (self.astCtxt.bvashr(self.v1, self.v2),              "(bvashr SymVar_0 SymVar_1)",                                   "(SymVar_0 >> SymVar_1)"),
            (self.astCtxt.bvfalse(),                             "(_ bv0 1)",                                                    "0x0"),
            (self.astCtxt.bvnand(self.v1, self.v2),              "(bvnand SymVar_0 SymVar_1)",                                   "(~(SymVar_0 & SymVar_1) & 0xFF)"),
            (self.astCtxt.bvnor(self.v1, self.v2),               "(bvnor SymVar_0 SymVar_1)",                                    "(~(SymVar_0 | SymVar_1) & 0xFF)"),
            (self.astCtxt.bvrol(self.v1, self.astCtxt.bv(3, 8)), "((_ rotate_left 3) SymVar_0)",                                 "rol(SymVar_0, 0x3)"),
            (self.astCtxt.bvror(self.v2, self.astCtxt.bv(2, 8)), "((_ rotate_right 2) SymVar_1)",                                "ror(SymVar_1, 0x2)"),
            (self.astCtxt.bvsdiv(self.v1, self.v2),              "(bvsdiv SymVar_0 SymVar_1)",                                   "(SymVar_0 / SymVar_1)"),
            (self.astCtxt.bvsge(self.v1, self.v2),               "(bvsge SymVar_0 SymVar_1)",                                    "(SymVar_0 >= SymVar_1)"),
            (self.astCtxt.bvsgt(self.v1, self.v2),               "(bvsgt SymVar_0 SymVar_1)",                                    "(SymVar_0 > SymVar_1)"),
            (self.astCtxt.bvsle(self.v1, self.v2),               "(bvsle SymVar_0 SymVar_1)",                                    "(SymVar_0 <= SymVar_1)"),
            (self.astCtxt.bvslt(self.v1, self.v2),               "(bvslt SymVar_0 SymVar_1)",                                    "(SymVar_0 < SymVar_1)"),
            (self.astCtxt.bvsmod(self.v1, self.v2),              "(bvsmod SymVar_0 SymVar_1)",                                   "(SymVar_0 % SymVar_1)"),
            (self.astCtxt.bvsrem(self.v1, self.v2),              "(bvsrem SymVar_0 SymVar_1)",                                   "(SymVar_0 % SymVar_1)"),
            (self.astCtxt.bvtrue(),                              "(_ bv1 1)",                                                    "0x1"),
            (self.astCtxt.bvurem(self.v1, self.v2),              "(bvurem SymVar_0 SymVar_1)",                                   "(SymVar_0 % SymVar_1)"),
            (self.astCtxt.bvxnor(self.v1, self.v2),              "(bvxnor SymVar_0 SymVar_1)",                                   "(~(SymVar_0 ^ SymVar_1) & 0xFF)"),
            (self.astCtxt.compound([self.v1, self.v2]),          "SymVar_0\nSymVar_1",                                           "SymVar_0\nSymVar_1"),
            (self.astCtxt.concat([self.v1, self.v2]),            "(concat SymVar_0 SymVar_1)",                                   "((SymVar_0) << 8 | SymVar_1)"),
            (self.astCtxt.declare(self.v1),                      "(declare-fun SymVar_0 () (_ BitVec 8))",                       "SymVar_0 = 0xdeadbeef"),
            (self.astCtxt.distinct(self.v1, self.v2),            "(distinct SymVar_0 SymVar_1)",                                 "(SymVar_0 != SymVar_1)"),
            (self.astCtxt.equal(self.v1, self.v2),               "(= SymVar_0 SymVar_1)",                                        "(SymVar_0 == SymVar_1)"),
            (self.astCtxt.extract(4, 2, self.v1),                "((_ extract 4 2) SymVar_0)",                                   "((SymVar_0 >> 2) & 0x7)"),
            (self.astCtxt.extract(6, 0, self.v1),                "((_ extract 6 0) SymVar_0)",                                   "(SymVar_0 & 0x7F)"),
            (self.astCtxt.extract(7, 0, self.v1),                "SymVar_0",                                                     "SymVar_0"),
            (self.astCtxt.iff(self.v1 == 1, self.v2 == 2),       "(iff (= SymVar_0 (_ bv1 8)) (= SymVar_1 (_ bv2 8)))",          "((SymVar_0 == 0x1) and (SymVar_1 == 0x2)) or (not (SymVar_0 == 0x1) and not (SymVar_1 == 0x2))"),
            (self.astCtxt.ite(self.v1 == 1, self.v1, self.v2),   "(ite (= SymVar_0 (_ bv1 8)) SymVar_0 SymVar_1)",               "(SymVar_0 if (SymVar_0 == 0x1) else SymVar_1)"),
            (self.astCtxt.land([self.v1 == 1, self.v2 == 2]),    "(and (= SymVar_0 (_ bv1 8)) (= SymVar_1 (_ bv2 8)))",          "((SymVar_0 == 0x1) and (SymVar_1 == 0x2))"),
            (self.astCtxt.let("alias", self.v1, self.v2),        "(let ((alias SymVar_0)) SymVar_1)",                            "SymVar_1"),
            (self.astCtxt.lnot(self.v1 == 0),                    "(not (= SymVar_0 (_ bv0 8)))",                                 "not (SymVar_0 == 0x0)"),
            (self.astCtxt.lor([self.v1 >= 0, self.v2 <= 10]),    "(or (bvuge SymVar_0 (_ bv0 8)) (bvule SymVar_1 (_ bv10 8)))",  "((SymVar_0 >= 0x0) or (SymVar_1 <= 0xA))"),
            (self.astCtxt.lxor([self.v1 >= 0, self.v2 <= 10]),   "(xor (bvuge SymVar_0 (_ bv0 8)) (bvule SymVar_1 (_ bv10 8)))", "(bool((SymVar_0 >= 0x0)) != bool((SymVar_1 <= 0xA)))"),
            (self.astCtxt.reference(self.ref),                   "ref!0",                                                        "ref_0"),
            (self.astCtxt.string("test"),                        "test",                                                         "test"),
            (self.astCtxt.sx(8, self.v1),                        "((_ sign_extend 8) SymVar_0)",                                 "sx(0x8, SymVar_0)"),
            (self.astCtxt.zx(8, self.v1),                        "((_ zero_extend 8) SymVar_0)",                                 "SymVar_0"),
            (self.astCtxt.forall([self.v1], 1 == self.v1),       "(forall ((SymVar_0 (_ BitVec 8))) (= SymVar_0 (_ bv1 8)))",    "forall([symvar_0], (symvar_0 == 0x1))"),
        ]

    def test_smt_representation(self):
        self.Triton.setAstRepresentationMode(AST_REPRESENTATION.SMT)
        self.assertEqual(self.Triton.getAstRepresentationMode(), AST_REPRESENTATION.SMT)
        for n in self.node:
            self.assertEqual(str(n[0]), n[1])

    def test_python_representation(self):
        self.Triton.setAstRepresentationMode(AST_REPRESENTATION.PYTHON)
        self.assertEqual(self.Triton.getAstRepresentationMode(), AST_REPRESENTATION.PYTHON)
        for n in self.node:
            # Note: lower() in order to handle boost-1.55 (from travis) and boost-1.71 (from an up-to-date machine)
            self.assertEqual(str(n[0]).lower(), n[2].lower())
