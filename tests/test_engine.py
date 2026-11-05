import unittest,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from engine import *
class TestEngine(unittest.TestCase):
    def test_canonical_order(self): self.assertEqual(receipt({'a':1,'b':2})['digest'],receipt({'b':2,'a':1})['digest'])
    def test_receipt_verification(self):
        d=receipt({'x':3})['digest'];self.assertTrue(verify_receipt({'x':3},d)['valid']);self.assertFalse(verify_receipt({'x':4},d)['valid'])
    def test_scour(self):
        r=root_scour({'a':1,'b':2},{'a':1,'b':3,'c':4});self.assertEqual(r['stable_keys'],['a']);self.assertEqual(r['added_keys'],['c'])
    def test_velocity(self): self.assertEqual(velocity_splat([0,2],[3,6],2)['speed_norm'],2.5)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): velocity_splat([0],[float('nan')])
    def test_mismatch(self):
        with self.assertRaises(ValueError): velocity_splat([0],[0,1])
    def test_gate(self):
        r=octopus_mode({x:{'v':i} for i,x in enumerate(FACES)},0);self.assertEqual(r['state']['gate'],'CLOSED');self.assertEqual(len(r['state']['six_face_commitments']),6)
    def test_reject_eight_faces(self):
        with self.assertRaises(ValueError): octopus_mode({**{x:0 for x in FACES},'time_axis':0,'foretentacle':0},0)
    def test_negative_tick(self):
        with self.assertRaises(ValueError): octopus_mode({x:0 for x in FACES},-1)
    def test_no_timestamp(self): self.assertFalse(receipt({'a':1})['timestamp_attested'])
if __name__=='__main__': unittest.main()
