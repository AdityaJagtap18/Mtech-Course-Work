#!/usr/bin/env python3
"""
Huffman Coding - Build Huffman Tree and Generate Codes

Algorithm:
1. Create leaf nodes for each character with its frequency
2. Build a min-heap with all nodes
3. Repeatedly extract two minimum frequency nodes and create parent
4. Assign 0 to left edge, 1 to right edge
5. Generate codes by traversing tree from root to leaves
"""

import heapq
from collections import defaultdict


class Node:
    """Node in Huffman Tree"""
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    # For min-heap comparison
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __repr__(self):
        if self.char:
            return f"Node('{self.char}', {self.freq})"
        return f"Node(Internal, {self.freq})"


def build_huffman_tree(characters, frequencies):
    """
    Build Huffman Tree using greedy method
    
    Args:
        characters: list of characters
        frequencies: list of frequencies
    
    Returns:
        root: root node of Huffman tree
    """
    n = len(characters)
    
    # Create leaf nodes and add to min-heap
    heap = []
    for i in range(n):
        node = Node(characters[i], frequencies[i])
        heapq.heappush(heap, node)
    
    print("\nBuilding Huffman Tree:")
    print("=" * 80)
    step = 1
    
    # Build tree by combining nodes
    while len(heap) > 1:
        # Extract two nodes with minimum frequency
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        # Create internal node with combined frequency
        merged_freq = left.freq + right.freq
        merged = Node(None, merged_freq)
        merged.left = left
        merged.right = right
        
        print(f"Step {step}: Merge {left} + {right} = Node(freq={merged_freq})")
        step += 1
        
        # Add back to heap
        heapq.heappush(heap, merged)
    
    print("=" * 80)
    
    # Return root of tree
    return heap[0]


def generate_huffman_codes(root):
    """
    Generate Huffman codes by traversing tree
    
    Args:
        root: root node of Huffman tree
    
    Returns:
        codes: dictionary mapping character to code
    """
    codes = {}
    
    def traverse(node, code):
        if node is None:
            return
        
        # Leaf node - store code
        if node.char is not None:
            codes[node.char] = code if code else "0"
            return
        
        # Internal node - traverse children
        traverse(node.left, code + "0")
        traverse(node.right, code + "1")
    
    traverse(root, "")
    return codes


def calculate_average_length(codes, frequencies, char_freq_map):
    """
    Calculate average code length
    
    Average length = Σ(frequency * code_length) / total_frequency
    """
    total_freq = sum(frequencies)
    weighted_sum = 0
    
    for char, code in codes.items():
        freq = char_freq_map[char]
        weighted_sum += freq * len(code)
    
    avg_length = weighted_sum / total_freq
    return avg_length


def display_huffman_codes(characters, frequencies, codes):
    """Display Huffman codes in a formatted table"""
    print("\n" + "=" * 80)
    print("HUFFMAN CODES")
    print("=" * 80)
    print(f"{'Character':<15} {'Frequency':<15} {'Huffman Code':<20} {'Code Length':<15}")
    print("-" * 80)
    
    total_freq = sum(frequencies)
    
    for i, char in enumerate(characters):
        freq = frequencies[i]
        code = codes[char]
        code_len = len(code)
        print(f"{char:<15} {freq:<15} {code:<20} {code_len:<15}")
    
    print("-" * 80)
    print(f"{'TOTAL':<15} {total_freq:<15}")
    print("=" * 80)


def display_tree(root, prefix="", is_left=True):
    """Display tree structure"""
    if root is None:
        return
    
    print(prefix + ("|-- " if is_left else "`-- ") + 
          (f"'{root.char}' ({root.freq})" if root.char else f"Internal ({root.freq})"))
    
    if root.left or root.right:
        if root.left:
            display_tree(root.left, prefix + ("|   " if is_left else "    "), True)
        if root.right:
            display_tree(root.right, prefix + ("|   " if is_left else "    "), False)


def display_encoding_example(text, codes):
    """Show how text is encoded using Huffman codes"""
    print("\n" + "=" * 80)
    print("ENCODING EXAMPLE")
    print("=" * 80)
    print(f"Original text: {text}")
    
    encoded = ""
    for char in text:
        if char in codes:
            encoded += codes[char]
    
    print(f"Encoded: {encoded}")
    print(f"Original bits (8-bit ASCII): {len(text) * 8} bits")
    print(f"Huffman encoded bits: {len(encoded)} bits")
    print(f"Compression ratio: {len(encoded) / (len(text) * 8) * 100:.2f}%")
    print(f"Space saved: {(1 - len(encoded) / (len(text) * 8)) * 100:.2f}%")
    print("=" * 80)


def main():
    print("HUFFMAN CODING")
    print("=" * 80)
    
    # Get input
    n = int(input("\nEnter number of characters: "))
    
    characters = []
    frequencies = []
    
    print("\nEnter character and frequency:")
    for i in range(n):
        char = input(f"  Character {i+1}: ")
        freq = int(input(f"  Frequency: "))
        characters.append(char)
        frequencies.append(freq)
    
    # Create character-frequency mapping
    char_freq_map = {characters[i]: frequencies[i] for i in range(n)}
    
    print(f"\nInput Data:")
    print("-" * 40)
    for i in range(n):
        print(f"  '{characters[i]}': {frequencies[i]}")
    print("-" * 40)
    
    # Build Huffman tree
    root = build_huffman_tree(characters, frequencies)
    
    # Display tree structure
    print("\nHuffman Tree Structure:")
    print("=" * 80)
    display_tree(root)
    print("=" * 80)
    
    # Generate Huffman codes
    codes = generate_huffman_codes(root)
    
    # Display codes
    display_huffman_codes(characters, frequencies, codes)
    
    # Calculate and display average code length
    avg_length = calculate_average_length(codes, frequencies, char_freq_map)
    print(f"\nAverage Code Length: {avg_length:.4f} bits/character")
    
    # Calculate efficiency
    import math
    total_freq = sum(frequencies)
    entropy = 0
    for freq in frequencies:
        if freq > 0:
            prob = freq / total_freq
            entropy -= prob * math.log2(prob)
    
    print(f"Theoretical Minimum (Entropy): {entropy:.4f} bits/character")
    print(f"Efficiency: {(entropy / avg_length) * 100:.2f}%")
    
    # Optional: Show encoding example
    try:
        print("\n" + "=" * 80)
        example = input("\nEnter a text to encode (using above characters, or press Enter to skip): ")
        if example:
            display_encoding_example(example, codes)
    except EOFError:
        pass


if __name__ == "__main__":
    main()