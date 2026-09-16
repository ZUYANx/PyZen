import argparse
import json
import os
from .model import PyZen

def main():
    p = argparse.ArgumentParser(prog="pyzen")
    p.add_argument("--model", default="models/needle2.cact")
    p.add_argument("--engine", default=None)
    p.add_argument("--prompt")
    p.add_argument("--max", type=int, default=256)
    args = p.parse_args()

    ai = PyZen(args.model, args.engine)
    prompt = args.prompt or input("PyZen> ")
    print(json.dumps(ai(prompt, args.max), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
