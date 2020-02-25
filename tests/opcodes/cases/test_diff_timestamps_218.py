from unittest import TestCase

from pytezos.repl.interpreter import Interpreter
from pytezos.michelson.converter import michelson_to_micheline
from pytezos.repl.parser import parse_value


class OpcodeTestdiff_timestamps_218(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.i = Interpreter(debug=True)
        
    def test_opcode_diff_timestamps_218(self):
        res = self.i.execute('INCLUDE "/home/mickey/pytezos/tests/opcodes/contracts/diff_timestamps.tz"')
        self.assertTrue(res['success'])
        
        res = self.i.execute('RUN (Pair 0 0) 111')
        self.assertTrue(res['success'])
        
        type_expr = self.i.ctx.stack[0].type_expr['args'][1]
        expected_expr = michelson_to_micheline('0')
        expected_val = parse_value(expected_expr, type_expr)
        self.assertEqual(expected_val, self.i.ctx.stack[0]._val[1])
