import random
import time

def create_512mb_file(filename='test_512mb.txt'):
    """
    Create a 512 MB file with random numbers.
    Each line contains a random integer.
    """
    target_size = 512 * 1024 * 1024  # 512 MB in bytes
    avg_bytes_per_line = 8  # Average: number + newline
    estimated_lines = target_size // avg_bytes_per_line
    
    print("=" * 60)
    print("CREATING 512 MB TEST FILE")
    print("=" * 60)
    print(f"Target size: 512 MB")
    print(f"Estimated lines: {estimated_lines:,}")
    print(f"Output file: {filename}")
    print("=" * 60)
    
    start_time = time.time()
    current_size = 0
    lines_written = 0
    
    with open(filename, 'w') as f:
        while current_size < target_size:
            # Generate random number (1 to 9,999,999)
            number = random.randint(1, 9999999)
            line = f"{number}\n"
            f.write(line)
            
            current_size += len(line)
            lines_written += 1
            
            # Progress update every 5 million lines
            if lines_written % 5_000_000 == 0:
                progress_mb = current_size / (1024 * 1024)
                percent = (current_size / target_size) * 100
                elapsed = time.time() - start_time
                print(f"Progress: {progress_mb:.1f} MB / 512 MB ({percent:.1f}%) | "
                      f"{lines_written:,} lines | {elapsed:.1f}s elapsed")
    
    # Final statistics
    elapsed_time = time.time() - start_time
    actual_size_mb = current_size / (1024 * 1024)
    
    print("\n" + "=" * 60)
    print("✓ FILE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"File: {filename}")
    print(f"Size: {actual_size_mb:.2f} MB")
    print(f"Lines: {lines_written:,}")
    print(f"Time taken: {elapsed_time:.1f} seconds")
    print("=" * 60)
    
    # Show sample of file content
    print("\nSample content (first 10 lines):")
    with open(filename, 'r') as f:
        for i in range(10):
            line = f.readline().strip()
            if line:
                print(f"  {line}")
    
    print("\n✓ Ready to use with merge sort!")

if __name__ == "__main__":
    create_512mb_file()