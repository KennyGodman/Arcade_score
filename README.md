# ArcadeScoreOracle - GenLayer Intelligent Contract Primitive

`ArcadeScoreOracle` is a **GenLayer Intelligent Contract primitive** built for hackathons and decentralized gaming applications. It solves the challenge of trustless score verification for arcade/retro games by combining GenLayer's **Equivalence Principle** with AI-driven anti-cheat replay log analysis.

---

## 🕹️ Problem & Solution

Traditional smart contracts cannot verify off-chain game replays without centralized oracles or complex ZK-proof circuits for game engines. `ArcadeScoreOracle` leverages GenLayer's non-deterministic AI validators to inspect replay telemetry (timestamps, button press intervals, score progression) on-chain and reach consensus on score legitimacy.

---

## 📐 Architecture & Equivalence Principle

```
[ Game Client ] ---> submit_score(player, score, replay_log)
                             |
                             v
               [ Non-Deterministic LLM Block ]
                             |
                 gl.eq_principle.prompt_non_comparative
                             |
         +-------------------+-------------------+
         |                                       |
  Leader Validator                        Follower Validators
  (Executes anti-cheat prompt)            (Verify against criteria)
         |                                       |
         +-------------------+-------------------+
                             |
                     Consensus Reached
                             |
                             v
               [ Persistent State Updated ]
               - high_scores[player] = score
               - verified_replays[replay_id] = true
```

### Why `prompt_non_comparative`?
- **Efficiency**: The leader validator executes the detailed LLM prompt analyzing input intervals, timestamps, and score scalability.
- **Verification**: Follower validators evaluate the leader's verdict against defined anti-cheat criteria without re-running the full prompt, minimizing latency and gas/token overhead.

---

## 📁 Repository Layout

```text
ARCADE/
├── contracts/
│   └── arcade_score_oracle.py     # Main GenLayer Intelligent Contract (Python)
├── tests/
│   └── direct/
│       └── test_arcade_score_oracle.py # Direct mode unit test suite
├── deploy/
│   └── 001_deploy_oracle.ts       # Deployment script using genlayer-js
├── pyproject.toml                 # Python dependency specifications
├── package.json                   # TypeScript/Node.js specifications
└── README.md                      # Documentation
```

---

## 📜 Contract Overview

- **`submit_score(player: Address, claimed_score: int, replay_log: str) -> bool`**: Main entry point for submitting scores and replay logs for AI anti-cheat validation.
- **`get_high_score(player: Address) -> int`**: View function for retrieving verified personal high score.
- **`is_replay_verified(replay_id: str) -> bool`**: View function to check if a specific replay log was verified.
- **`get_total_replays() -> int`**: View function returning total submitted replays.
- **`get_owner() -> Address`**: View function for contract owner.

---

## 🚀 Getting Started

### Python Contracts & Tests
Contracts are located in [`contracts/arcade_score_oracle.py`](file:///c:/Users/HP/Desktop/ARCADE/contracts/arcade_score_oracle.py).
Unit tests are in [`tests/direct/test_arcade_score_oracle.py`](file:///c:/Users/HP/Desktop/ARCADE/tests/direct/test_arcade_score_oracle.py).

### Deployment
Deploy to the GenLayer Simulator endpoint using [`deploy/001_deploy_oracle.ts`](file:///c:/Users/HP/Desktop/ARCADE/deploy/001_deploy_oracle.ts):
```bash
npm install
npm run deploy
```
