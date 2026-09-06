#!/usr/bin/env python3
import sys, argparse, os
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', help='File to process')
    parser.add_argument('--hex', action='store_true', help='Dump file as Hexadecimal')
    args = parser.parse_args()
    
    print("\033[1;34m=== V3 FILE PARSING & COMPILATION ENGINE ===\033[0m")
    
    if not args.file:
        print("Usage: ./start.sh <file> [--hex]")
        sys.exit(1)
        
    if not os.path.exists(args.file):
        print(f"\033[1;31m[Error] File not found: {args.file}\033[0m")
        sys.exit(1)
        
    with open(args.file, 'rb') as f:
        data = f.read()
        
    if args.hex:
        print(f"\033[1;33m[Compiler] Dumping {len(data)} bytes in Hex:\033[0m")
        for i in range(0, min(len(data), 512), 16):
            chunk = data[i:i+16]
            print(f"0x{i:04x} | {' '.join(f'{b:02x}' for b in chunk)}")
        if len(data) > 512: print("... (truncated)")
    else:
        try:
            text = data.decode('utf-8')
            print(f"\033[1;32m[Parser] UTF-8 Decoded ({len(text)} chars):\033[0m\n{text[:500]}")
            if len(text) > 500: print("\n... (truncated)")
        except:
            print("\033[1;31m[Error] Binary file detected. Use --hex to parse.\033[0m")
if __name__ == '__main__': main()
