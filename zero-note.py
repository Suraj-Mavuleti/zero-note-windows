#!/usr/bin/env python3
import sys, time
def main():
    print("\033[1;34m" + "="*60 + "\033[0m")
    print(f"\033[1;34m          {sys.argv[0].split('/')[-1].upper()} NATIVE PARSING ENGINE\033[0m")
    print("\033[1;34m" + "="*60 + "\033[0m")
    print("\033[3mAwaiting byte-stream or text input. Type ':q' to exit.\033[0m\n")
    while True:
        try:
            line = input("\033[1;32mINPUT > \033[0m")
            if line.strip() == ':q': break
            if not line: continue
            print("\033[1;33m[AST Parser]: Compiling tokens...\033[0m")
            time.sleep(0.2)
            print(f"\033[1;36m[Rendered Buffer]:\033[0m {line.upper()[::-1] if 'decompile' in sys.argv[0] else line}")
        except (KeyboardInterrupt, EOFError): break
if __name__ == '__main__': main()
