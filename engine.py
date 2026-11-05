"""SCANDOC deterministic research primitives. Standard library only."""
from __future__ import annotations
import hashlib, json, math, hmac
from typing import Any

VERSION = '0.1.0'
ORIGIN = [1024, 1024, 0]
FACES = ('tap','surface','gain','habitat','engine','business')

def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')

def receipt(payload: Any) -> dict:
    data = canonical(payload)
    return {'algorithm':'SHA-512','digest':hashlib.sha512(data).hexdigest(),'canonical_bytes':len(data),'verification':'CONTENT_COMMITMENT_ONLY','timestamp_attested':False}

def verify_receipt(payload: Any, digest: str) -> dict:
    actual = receipt(payload)['digest']
    return {'valid':hmac.compare_digest(actual, digest.lower()),'computed_digest':actual,'timestamp_attested':False}

def _vector(v: Any, name: str) -> list[float]:
    if not isinstance(v,list) or not v or len(v)>512:
        raise ValueError(f'{name} must be a nonempty list of up to 512 finite numbers')
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in v):
        raise ValueError(f'{name} contains non-finite or non-numeric values')
    return [float(x) for x in v]

def velocity_splat(before: list, after: list, dt: float=1.0) -> dict:
    a,b = _vector(before,'before'),_vector(after,'after')
    if len(a)!=len(b): raise ValueError('Vectors must have identical dimensions')
    if isinstance(dt,bool) or not isinstance(dt,(int,float)) or not math.isfinite(dt) or dt<=0:
        raise ValueError('dt must be finite and > 0')
    delta = [y-x for x,y in zip(a,b)]
    velocity = [v/dt for v in delta]
    norm = math.hypot(*delta)
    return {'dimension':len(a),'delta':delta,'velocity':velocity,'displacement_norm':norm,'speed_norm':norm/dt,'dt':dt,'method':'FINITE_DIFFERENCE_NOT_PHYSICAL_MOTION','verified':False}

def root_scour(before: dict, after: dict) -> dict:
    if not isinstance(before,dict) or not isinstance(after,dict):
        raise ValueError('Both inputs must be feature dictionaries')
    common = sorted(set(before)&set(after))
    stable = [k for k in common if before[k]==after[k]]
    changed = [{'key':k,'before':before[k],'after':after[k]} for k in common if before[k]!=after[k]]
    return {'stable_keys':stable,'changed':changed,'removed_keys':sorted(set(before)-set(after)),'added_keys':sorted(set(after)-set(before)),'status':'STRUCTURAL_COMPARISON_ONLY','invariance_not_proven':True}

def double_snapshot(before: Any, after: Any, dt: float=1.0) -> dict:
    if isinstance(before,dict) and isinstance(after,dict):
        comparison = root_scour(before,after)
    elif isinstance(before,list) and isinstance(after,list):
        comparison = velocity_splat(before,after,dt)
    else:
        raise ValueError('Both snapshots must be feature dictionaries or numeric vectors of the same kind')
    return {'before_receipt':receipt(before),'after_receipt':receipt(after),'comparison':comparison,'source_authenticity':'NOT_ASSESSED','capture_time':'NOT_ATTESTED'}

def octopus_mode(faces: dict, tick: int, genesis_digest: str|None=None) -> dict:
    if not isinstance(faces,dict) or set(faces)!=set(FACES):
        raise ValueError('Exactly six named launch faces required')
    if isinstance(tick,bool) or not isinstance(tick,int) or tick<0:
        raise ValueError('tick must be a nonnegative integer')
    if genesis_digest is not None and (not isinstance(genesis_digest,str) or len(genesis_digest)!=128 or any(c not in '0123456789abcdefABCDEF' for c in genesis_digest)):
        raise ValueError('genesis_digest must be a 128-character SHA-512 hex digest')
    commitments = {name:receipt(faces[name])['digest'] for name in FACES}
    state = {'origin':ORIGIN,'tick':tick,'six_face_commitments':commitments,'time_axis':{'genesis_digest':genesis_digest,'status':'LINK_UNVERIFIED' if genesis_digest else 'ABSENT'},'foretentacle':{'status':'NO_FORWARD_OF_NOW'},'gate':'CLOSED','writes_permitted':False}
    return {'state':state,'state_receipt':receipt(state),'status':'SIMULATION_UNVERIFIED','visualisation_hints':{'arms':list(FACES)+['time_axis','foretentacle'],'geometry':'six launch legs plus two temporal arms'}}
