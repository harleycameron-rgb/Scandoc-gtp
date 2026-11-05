"""Adversarial checks for the SCANDOC public research preview."""
import pathlib, sys, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from engine import root_scour, velocity_splat, double_snapshot, receipt, verify_receipt, octopus_mode, FACES

class PublicBoundaryTests(unittest.TestCase):
    def test_zero_interval_rejected(self):
        with self.assertRaises(ValueError): velocity_splat([1],[2],0)
    def test_negative_interval_rejected(self):
        with self.assertRaises(ValueError): velocity_splat([1],[2],-1)
    def test_infinite_interval_rejected(self):
        with self.assertRaises(ValueError): velocity_splat([1],[2],float('inf'))
    def test_bool_vector_rejected(self):
        with self.assertRaises(ValueError): velocity_splat([True],[1])
    def test_empty_vector_rejected(self):
        with self.assertRaises(ValueError): velocity_splat([],[])
    def test_large_vector_rejected(self):
        with self.assertRaises(ValueError): velocity_splat([0]*513,[0]*513)
    def test_non_dict_scour_rejected(self):
        with self.assertRaises(ValueError): root_scour('potato',{})
    def test_mixed_snapshots_rejected(self):
        with self.assertRaises(ValueError): double_snapshot({'x':1},[1])
    def test_nan_receipt_rejected(self):
        with self.assertRaises(ValueError): receipt({'x':float('nan')})
    def test_digest_mismatch(self):
        self.assertFalse(verify_receipt({'x':1},'0'*128)['valid'])
    def test_missing_face_rejected(self):
        with self.assertRaises(ValueError): octopus_mode({x:1 for x in FACES[:-1]},0)
    def test_boolean_tick_rejected(self):
        with self.assertRaises(ValueError): octopus_mode({x:1 for x in FACES},True)
    def test_invalid_genesis_rejected(self):
        with self.assertRaises(ValueError): octopus_mode({x:1 for x in FACES},0,'fake')
    def test_gate_stays_closed_even_with_genesis(self):
        state=octopus_mode({x:1 for x in FACES},1,'a'*128)['state']
        self.assertEqual(state['gate'],'CLOSED')
        self.assertFalse(state['writes_permitted'])
    def test_no_attested_timestamp(self):
        self.assertFalse(receipt({'subject':'trex'})['timestamp_attested'])

if __name__ == '__main__': unittest.main()
