import json
import os
import struct
import sys
from collections import Counter

from huffman import build_tree, build_codes, encode, decode


def compress(src, dst):
    with open(src, encoding="utf-8", newline="") as file:
        text = file.read()

    freqs = Counter(text)
    codes = build_codes(build_tree(freqs))
    bits = encode(text, codes)

    padded = bits + "0" * (-len(bits) % 8)
    body = int(padded, 2).to_bytes(len(padded) // 8, "big") if padded else b""
    header = json.dumps({"freq": freqs, "bits": len(bits)}, ensure_ascii=False).encode("utf-8")

    with open(dst, "wb") as file:
        file.write(struct.pack(">I", len(header)))
        file.write(header)
        file.write(body)


def decompress(src, dst):
    with open(src, "rb") as file:
        header_length = struct.unpack(">I", file.read(4))[0]
        header = json.loads(file.read(header_length).decode("utf-8"))
        body = file.read()

    bits = ""
    if body:
        bits = bin(int.from_bytes(body, "big"))[2:].zfill(len(body) * 8)[:header["bits"]]

    text = decode(bits, build_tree(header["freq"]))

    with open(dst, "w", encoding="utf-8", newline="") as file:
        file.write(text)


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("compress", "decompress"):
        print("Використання:")
        print("  python archiver.py compress файл.txt файл.huf")
        print("  python archiver.py decompress файл.huf файл.txt")
        sys.exit(1)

    action, src, dst = sys.argv[1:]
    if action == "compress":
        compress(src, dst)
    else:
        decompress(src, dst)

    print(f"{src}: {os.path.getsize(src)} байт -> {dst}: {os.path.getsize(dst)} байт")