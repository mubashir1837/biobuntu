import pytest
from core.engine import Engine

def test_engine():
    engine = Engine()
    assert engine is not None