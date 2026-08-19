"""
Direct mode unit test suite for ArcadeScoreOracle GenLayer Intelligent Contract.
"""
import pytest
from unittest.mock import MagicMock, patch

# Mock genlayer module for direct mode testing if py-genlayer package is imported
try:
    import genlayer as gl
except ImportError:
    class MockAddress(str):
        pass

    class MockContract:
        pass

    class MockPublic:
        @staticmethod
        def view(func):
            return func
        
        @staticmethod
        def write(func):
            return func

    class MockEqPrinciple:
        @staticmethod
        def prompt_non_comparative(fn, task, criteria):
            return fn()

    class MockTreeMap(dict):
        pass

    class MockU256(int):
        pass

    class MockMessage:
        sender_address = MockAddress("0x1111111111111111111111111111111111111111")

    class MockGl:
        Contract = MockContract
        Address = MockAddress
        TreeMap = MockTreeMap
        u256 = MockU256
        public = MockPublic
        eq_principle = MockEqPrinciple
        message = MockMessage()
        
        @staticmethod
        def exec_prompt(prompt: str) -> dict:
            if "IMPOSSIBLE_CHEATING_LOG" in prompt:
                return {
                    "is_legitimate": False,
                    "verified_score": 0,
                    "reasoning": "Detected 0ms input intervals and impossible score jump."
                }
            return {
                "is_legitimate": True,
                "verified_score": 15000,
                "reasoning": "Telemetry checks out. Timestamps match standard human play."
            }

    import sys
    gl = MockGl()
    sys.modules['genlayer'] = gl

from contracts.arcade_score_oracle import ArcadeScoreOracle

def test_contract_initialization():
    owner_addr = "0x1111111111111111111111111111111111111111"
    player_addr = "0x2222222222222222222222222222222222222222"
    
    oracle = ArcadeScoreOracle(owner=owner_addr)
    
    assert oracle.get_owner() == owner_addr
    assert oracle.get_high_score(player_addr) == 0
    assert oracle.get_total_replays() == 0

def test_submit_valid_score():
    owner_addr = "0x1111111111111111111111111111111111111111"
    player_addr = "0x2222222222222222222222222222222222222222"
    
    oracle = ArcadeScoreOracle(owner=owner_addr)
    
    valid_log = "FRAME 0: START; FRAME 60: MOVE_RIGHT; FRAME 120: SHOOT; SCORE: 15000"
    
    success = oracle.submit_score(player=player_addr, claimed_score=15000, replay_log=valid_log)
    
    assert success is True
    assert oracle.get_high_score(player_addr) == 15000
    assert oracle.get_total_replays() == 1
    assert oracle.is_replay_verified(f"replay_{player_addr}_0") is True
    assert oracle.get_replay_score(f"replay_{player_addr}_0") == 15000

def test_submit_cheated_score():
    owner_addr = "0x1111111111111111111111111111111111111111"
    player_addr = "0x3333333333333333333333333333333333333333"
    
    oracle = ArcadeScoreOracle(owner=owner_addr)
    
    cheated_log = "IMPOSSIBLE_CHEATING_LOG: FRAME 0: SCORE 99999999"
    
    success = oracle.submit_score(player=player_addr, claimed_score=99999999, replay_log=cheated_log)
    
    assert success is False
    assert oracle.get_high_score(player_addr) == 0
    assert oracle.get_total_replays() == 1
    assert oracle.is_replay_verified(f"replay_{player_addr}_0") is False

def test_high_score_updates_only_on_improvement():
    owner_addr = "0x1111111111111111111111111111111111111111"
    player_addr = "0x4444444444444444444444444444444444444444"
    
    oracle = ArcadeScoreOracle(owner=owner_addr)
    
    # First submit score 15000
    valid_log_1 = "LOG 1"
    oracle.submit_score(player=player_addr, claimed_score=15000, replay_log=valid_log_1)
    assert oracle.get_high_score(player_addr) == 15000
    
    # Second submission with lower score should not downgrade high score
    def mock_lower_score():
        return {"is_legitimate": True, "verified_score": 8000, "reasoning": "Valid but lower"}
    
    with patch.object(gl.eq_principle, 'prompt_non_comparative', side_effect=lambda fn, task, criteria: mock_lower_score()):
        oracle.submit_score(player=player_addr, claimed_score=8000, replay_log="LOG 2")
        assert oracle.get_high_score(player_addr) == 15000

if __name__ == "__main__":
    pytest.main([__file__])
