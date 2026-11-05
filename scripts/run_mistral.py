#!/usr/bin/env python3
"""
Mistral Codestral 22B Interactive CLI & Benchmark Runner.
Supports standard code generation and Fill-In-The-Middle (FIM) code refactoring.
"""

import os
import sys
import time
import json
import ast
import argparse
import urllib.request
from typing import Dict, Any

MODEL_NAME = os.getenv("MISTRAL_MODEL", "codestral")
OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434")


def query_mistral(
    prompt: str,
    prefix: str = "",
    suffix: str = "",
    temperature: float = 0.0
) -> Dict[str, Any]:
    url = f"{OLLAMA_API.rstrip('/')}/api/generate"
    
    # Handle FIM format if prefix and suffix provided
    if prefix and suffix:
        final_prompt = f"[PREFIX]{prefix}[SUFFIX]{suffix}[MIDDLE]"
    else:
        final_prompt = prompt

    payload = {
        "model": MODEL_NAME,
        "prompt": final_prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 1024,
            "num_ctx": 32768
        }
    }
    
    t0 = time.perf_counter()
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    t1 = time.perf_counter()
    
    total_time = round(t1 - t0, 3)
    response_text = data.get("response", "")
    eval_count = data.get("eval_count", len(response_text.split()))
    eval_dur = data.get("eval_duration", 0) / 1e9
    speed = round(eval_count / eval_dur, 1) if eval_dur > 0 else round(eval_count / total_time, 1)
    
    # Extract code
    code = response_text
    if "```python" in response_text:
        code = response_text.split("```python")[1].split("```")[0].strip()
    elif "```" in response_text:
        code = response_text.split("```")[1].split("```")[0].strip()
        
    try:
        ast.parse(code)
        ast_valid = True
    except SyntaxError:
        ast_valid = False
        
    return {
        "model": MODEL_NAME,
        "latency_sec": total_time,
        "tokens": eval_count,
        "tok_per_sec": speed,
        "ast_valid": ast_valid,
        "code": code,
        "raw_response": response_text
    }


def main():
    parser = argparse.ArgumentParser(description="Codestral 22B CLI")
    parser.add_argument("--prompt", default="Implement an Augmented Interval Tree with point overlap search in Python 3. Output only typed code.", help="Prompt to run")
    parser.add_argument("--prefix", default="", help="FIM prefix code")
    parser.add_argument("--suffix", default="", help="FIM suffix code")
    args = parser.parse_args()
    
    print(f"🚀 Running Codestral 22B ({MODEL_NAME})...")
    if args.prefix and args.suffix:
        print("Mode: Fill-In-The-Middle (FIM)")
    res = query_mistral(args.prompt, prefix=args.prefix, suffix=args.suffix)
    print("=" * 72)
    print(f"⚡ Latency: {res['latency_sec']}s | Tokens: {res['tokens']} | Speed: {res['tok_per_sec']} tok/s | AST Valid: {res['ast_valid']}")
    print("=" * 72)
    print(res["code"])


if __name__ == "__main__":
    main()
