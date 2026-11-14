import heapq
from collections import Counter


class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right


def build_tree(freqs):
    if not freqs:
        return None

    heap = []
    order = 0
    for char, freq in sorted(freqs.items()):
        heap.append((freq, order, Node(freq, char)))
        order += 1
    heapq.heapify(heap)

    while len(heap) > 1:
        freq1, _, left = heapq.heappop(heap)
        freq2, _, right = heapq.heappop(heap)
        parent = Node(freq1 + freq2, left=left, right=right)
        heapq.heappush(heap, (parent.freq, order, parent))
        order += 1

    return heap[0][2]


def build_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = prefix or "0"
        return codes

    build_codes(node.left, prefix + "0", codes)
    build_codes(node.right, prefix + "1", codes)
    return codes


def encode(text, codes):
    return "".join(codes[char] for char in text)


def decode(bits, root):
    if root is None:
        return ""
    if root.char is not None:
        return root.char * len(bits)

    result = []
    node = root
    for bit in bits:
        node = node.right if bit == "1" else node.left
        if node.char is not None:
            result.append(node.char)
            node = root
    return "".join(result)


def uniform_length(text):
    bits_per_symbol = max(1, (len(set(text)) - 1).bit_length())
    return bits_per_symbol * len(text)


def show(text):
    freqs = Counter(text)
    root = build_tree(freqs)
    codes = build_codes(root)
    encoded = encode(text, codes)
    uniform = uniform_length(text)
    saved = 100 - 100 * len(encoded) / uniform

    print(f"\nФраза: {text}")
    print(f"Довжина: {len(text)} символів, унікальних: {len(freqs)}")
    print("\nСимвол  Частота  Код")
    for char, code in sorted(codes.items(), key=lambda item: (len(item[1]), item[0])):
        print(f"{char!r:<7} {freqs[char]:<8} {code}")

    print(f"\nЗакодовано: {encoded}")
    print(f"Код Хаффмана: {len(encoded)} біт")
    print(f"Рівномірний код: {uniform} біт")
    print(f"Економія: {saved:.1f}%")
    print(f"Декодування збігається з оригіналом: {decode(encoded, root) == text}")


if __name__ == "__main__":
    show("абабагаламага")

    phrase = input("\nВведіть свою фразу (Enter, щоб пропустити): ")
    if phrase:
        show(phrase)