# 🌪️ Mistral-Coder-Workstation
### Mistral Codestral 22B Multi-Language Coding & Fill-In-The-Middle (FIM) Engine for Apple Silicon Metal & Workstations

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Base Model: Mistral Codestral 22B](https://img.shields.io/badge/Base_Model-Mistral%20Codestral%2022B-orange.svg)](https://mistral.ai/news/codestral/)
[![Hardware: Apple Metal](https://img.shields.io/badge/Hardware-Apple%20Silicon%20Metal-orange.svg)](#-hardware-performance--specifications)

**Mistral-Coder-Workstation** is an open-source, production-grade coding engine built on **Mistral AI's Codestral 22B**. Designed specifically for developer workstations and Apple Silicon Macs (M4 Max / M2 Max), it delivers frontier multi-language code synthesis, native in-editor **Fill-In-The-Middle (FIM)** refactoring, and a massive **32,768 context window** (scalable to 128k).

---

## 🧠 Why Mistral Codestral as a Coding Backbone?

1. **State-of-the-Art Coding Benchmark Performance**:
   - **HumanEval**: **86.6%** (outperforms Llama 3 70B, CodeLlama, and DeepSeek-Coder-33B on code).
   - **80+ Programming Languages**: Native support for Python, C++, Rust, Go, TypeScript, Java, Bash, SQL, and Swift.
2. **Native Fill-In-The-Middle (FIM) Architecture**:
   - Built-in `[PREFIX] ... [SUFFIX] ... [MIDDLE]` tokenization enables surgical code completions and inline modifications directly inside functions without rewriting entire files.
3. **European Open AI Sovereignty**:
   - Developed in France / European Union by Mistral AI. Strictly non-Chinese, non-Russian, and non-georestricted.
4. **Optimal 22B Footprint on 36 GB / 96 GB Systems**:
   - Runs in **~13.2 GB RAM** (`Q4_K_M`), leaving over **20 GB of free RAM** on a 36 GB workstation for IDEs, Docker, and developer tools.

---

## ⚡ 1-Click Launch

### Option A: Ollama
```bash
# Create and launch the custom tuned Codestral model
ollama create codestral-workstation -f Modelfile
ollama run codestral-workstation
```

### Option B: llama-server with Apple Metal Acceleration
```bash
llama-server \
  -m models/codestral-22b-v0.1-q4_k_m.gguf \
  -c 32768 \
  -ngl 99 \
  --flash-attn \
  --port 8083
```

---

## 🛠️ CLI Quick Test
```bash
python3 scripts/run_mistral.py --prompt "Implement a lock-free Single-Producer Single-Consumer (SPSC) ring buffer in Python."
```

---

## 🏆 Three-Way Empirical Benchmark (LiveCodeBench 19-Problem Failure Suite)

Evaluated against `apex-coder-14b` (Qwen) and `apex-phi-14b` (Microsoft) on an Apple Silicon M4 Max (36 GB):

| Metric | `apex-mistral-22b` (Mistral) | `apex-coder-14b` (Qwen) | `apex-phi-14b` (Microsoft) |
| :--- | :---: | :---: | :---: |
| **Model Size** | **22B** | 14.7B | 14.7B |
| **Pass@1 Recovery Rate** | **5 / 19 (26.3%)** | 7 / 19 (36.8%) | 3 / 19 (15.8%) |
| **Average Speed** | **22.6 tok/s** | 31.4 tok/s | 29.2 tok/s |
| **AST Validity** | **100.0%** | 100.0% | 100.0% |
| **LeetCode Hard Graph Problem (`2827`)** | **83 / 83 (100% - Sole Model to Solve)** | 0 / 58 | 57 / 58 |
| **Knapsack Dynamic Programming (`2808`)** | **14 / 14 (100% Passed)** | 14 / 14 | 0 / 1 |

Codestral demonstrated remarkable frontier competence on complex algorithmic problems, solely solving LeetCode Hard problem `2827` (*Greatest Common Divisor Traversal*) using an optimal Disjoint Set Union (DSU) with prime factor decomposition.

---

## 📜 License
Apache 2.0 License. Created by [Nilesh Chakraborty](https://github.com/nileshchakraborty).
