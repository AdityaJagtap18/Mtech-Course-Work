import threading
import time
from enum import Enum
from collections import defaultdict
from typing import Set, Dict, Optional

class LockType(Enum):
    """Types of locks"""
    SHARED = "S"      # Read lock
    EXCLUSIVE = "X"   # Write lock

class LockMode(Enum):
    """Lock compatibility modes"""
    COMPATIBLE = "compatible"
    INCOMPATIBLE = "incompatible"

class Transaction:
    """Represents a database transaction"""
    def __init__(self, tid: int):
        self.tid = tid
        self.locks_held: Set[tuple] = set()  # (item, lock_type)
        self.waiting_for: Optional[str] = None
        self.start_time = time.time()
    
    def __repr__(self):
        return f"T{self.tid}"

class LockManager:
    """
    Implements lock-based concurrency control protocols.
    Supports:
    - Two-Phase Locking (2PL)
    - Strict Two-Phase Locking (Strict 2PL)
    - Deadlock detection
    """
    
    def __init__(self, strict_2pl=True):
        """
        Initialize lock manager.
        
        Args:
            strict_2pl: If True, use Strict 2PL (hold locks until commit/abort)
                       If False, use basic 2PL (can release locks before commit)
        """
        self.strict_2pl = strict_2pl
        
        # Lock table: item -> {lock_type: set of transaction_ids}
        self.lock_table: Dict[str, Dict[LockType, Set[int]]] = defaultdict(
            lambda: {LockType.SHARED: set(), LockType.EXCLUSIVE: set()}
        )
        
        # Transaction registry
        self.transactions: Dict[int, Transaction] = {}
        
        # Lock to protect lock manager operations
        self.manager_lock = threading.Lock()
        
        # Statistics
        self.stats = {
            'locks_granted': 0,
            'locks_waited': 0,
            'transactions_aborted': 0
        }
    
    def begin_transaction(self, tid: int):
        """Start a new transaction."""
        with self.manager_lock:
            if tid in self.transactions:
                print(f"WARNING: Transaction T{tid} already exists!")
                return False
            
            self.transactions[tid] = Transaction(tid)
            print(f"SUCCESS: Transaction T{tid} started")
            return True
    
    def lock(self, tid: int, item: str, lock_type: LockType) -> bool:
        """
        Acquire a lock on an item.
        
        Args:
            tid: Transaction ID
            item: Data item to lock
            lock_type: Type of lock (SHARED or EXCLUSIVE)
        
        Returns:
            True if lock granted, False if deadlock detected
        """
        with self.manager_lock:
            if tid not in self.transactions:
                print(f"ERROR: Transaction T{tid} not found!")
                return False
            
            txn = self.transactions[tid]
            
            # Check if already holding this lock
            if (item, lock_type) in txn.locks_held:
                print(f"  T{tid} already holds {lock_type.value} lock on {item}")
                return True
            
            # Check for lock upgrade (S -> X)
            if (item, LockType.SHARED) in txn.locks_held and lock_type == LockType.EXCLUSIVE:
                return self._upgrade_lock(tid, item)
            
            # Check if lock can be granted
            if self._can_grant_lock(tid, item, lock_type):
                self._grant_lock(tid, item, lock_type)
                self.stats['locks_granted'] += 1
                return True
            else:
                # Need to wait
                print(f"WAITING: T{tid} waiting for {lock_type.value} lock on {item}")
                self.stats['locks_waited'] += 1
                return False
    
    def unlock(self, tid: int, item: str):
        """
        Release lock on an item.
        Only allowed in basic 2PL, not in Strict 2PL.
        """
        with self.manager_lock:
            if self.strict_2pl:
                print(f"WARNING: Cannot unlock in Strict 2PL mode. Use commit/abort.")
                return False
            
            if tid not in self.transactions:
                return False
            
            txn = self.transactions[tid]
            
            # Remove locks
            for lock_type in [LockType.SHARED, LockType.EXCLUSIVE]:
                if (item, lock_type) in txn.locks_held:
                    self.lock_table[item][lock_type].discard(tid)
                    txn.locks_held.discard((item, lock_type))
                    print(f"UNLOCK: T{tid} released {lock_type.value} lock on {item}")
            
            return True
    
    def commit(self, tid: int):
        """Commit transaction and release all locks."""
        with self.manager_lock:
            if tid not in self.transactions:
                print(f"ERROR: Transaction T{tid} not found!")
                return False
            
            txn = self.transactions[tid]
            
            # Release all locks
            for item, lock_type in txn.locks_held:
                self.lock_table[item][lock_type].discard(tid)
            
            del self.transactions[tid]
            
            duration = time.time() - txn.start_time
            print(f"COMMIT: T{tid} COMMITTED (duration: {duration:.3f}s)")
            return True
    
    def abort(self, tid: int):
        """Abort transaction and release all locks."""
        with self.manager_lock:
            self._abort_transaction(tid)
    
    def _abort_transaction(self, tid: int):
        """Internal abort implementation."""
        if tid not in self.transactions:
            return
        
        txn = self.transactions[tid]
        
        # Release all locks
        for item, lock_type in txn.locks_held:
            self.lock_table[item][lock_type].discard(tid)
        
        del self.transactions[tid]
        self.stats['transactions_aborted'] += 1
        
        print(f"ABORT: T{tid} ABORTED")
    
    def _can_grant_lock(self, tid: int, item: str, lock_type: LockType) -> bool:
        """Check if lock can be granted."""
        locks = self.lock_table[item]
        
        if lock_type == LockType.SHARED:
            # Shared lock compatible with other shared locks
            # Not compatible with exclusive locks
            if locks[LockType.EXCLUSIVE]:
                # Check if this transaction holds the exclusive lock
                if tid in locks[LockType.EXCLUSIVE]:
                    return True
                return False
            return True
        
        else:  # EXCLUSIVE lock
            # Exclusive lock not compatible with any other locks
            # Check if any locks held by other transactions
            for lt in [LockType.SHARED, LockType.EXCLUSIVE]:
                if locks[lt]:
                    # Check if all locks are held by this transaction
                    if locks[lt] != {tid}:
                        return False
            return True
    
    def _grant_lock(self, tid: int, item: str, lock_type: LockType):
        """Grant lock to transaction."""
        self.lock_table[item][lock_type].add(tid)
        self.transactions[tid].locks_held.add((item, lock_type))
        print(f"LOCK GRANTED: T{tid} acquired {lock_type.value} lock on {item}")
    
    def _upgrade_lock(self, tid: int, item: str) -> bool:
        """Upgrade lock from SHARED to EXCLUSIVE."""
        locks = self.lock_table[item]
        
        # Check if only this transaction holds shared lock
        if locks[LockType.SHARED] == {tid} and not locks[LockType.EXCLUSIVE]:
            locks[LockType.SHARED].discard(tid)
            locks[LockType.EXCLUSIVE].add(tid)
            
            txn = self.transactions[tid]
            txn.locks_held.discard((item, LockType.SHARED))
            txn.locks_held.add((item, LockType.EXCLUSIVE))
            
            print(f"UPGRADE: T{tid} upgraded lock on {item} (S -> X)")
            return True
        
        return False
    
    def _get_lock_holders(self, item: str) -> Set[int]:
        """Get all transactions holding locks on item."""
        holders = set()
        for lock_type in [LockType.SHARED, LockType.EXCLUSIVE]:
            holders.update(self.lock_table[item][lock_type])
        return holders
    
    def print_lock_table(self):
        """Print current state of lock table."""
        print("\n" + "=" * 60)
        print("LOCK TABLE")
        print("=" * 60)
        
        if not any(self.lock_table.values()):
            print("(empty)")
        else:
            for item, locks in sorted(self.lock_table.items()):
                if locks[LockType.SHARED] or locks[LockType.EXCLUSIVE]:
                    print(f"\nItem: {item}")
                    if locks[LockType.SHARED]:
                        holders = [f"T{tid}" for tid in sorted(locks[LockType.SHARED])]
                        print(f"  Shared: {', '.join(holders)}")
                    if locks[LockType.EXCLUSIVE]:
                        holders = [f"T{tid}" for tid in sorted(locks[LockType.EXCLUSIVE])]
                        print(f"  Exclusive: {', '.join(holders)}")
        
        print("=" * 60)
    
    def print_statistics(self):
        """Print lock manager statistics."""
        print("\n" + "=" * 60)
        print("STATISTICS")
        print("=" * 60)
        print(f"Locks granted: {self.stats['locks_granted']}")
        print(f"Locks waited: {self.stats['locks_waited']}")
        print(f"Transactions aborted: {self.stats['transactions_aborted']}")
        print("=" * 60)


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("LOCK-BASED CONCURRENCY CONTROL DEMONSTRATION")
    print("=" * 60)
    
    # Create lock manager with Strict 2PL
    lm = LockManager(strict_2pl=True)
    

    lm.begin_transaction(1)
    lm.begin_transaction(2)
    
    lm.lock(1, "A", LockType.SHARED)
    lm.lock(2, "A", LockType.SHARED)  # Compatible
    lm.lock(2, "B", LockType.EXCLUSIVE)
    
    lm.print_lock_table()
    
    lm.commit(1)
    lm.commit(2)
        
    lm.print_statistics()
    
    print("=" * 60)
    print("DEADLOCK PATTERN DEMO")
    print("=" * 60)

    lm = LockManager(strict_2pl=True)

    lm.begin_transaction(1)
    lm.begin_transaction(2)

    # Step 1: T1 gets X lock on A
    lm.lock(1, "A", LockType.EXCLUSIVE)

    # Step 2: T2 gets X lock on B
    lm.lock(2, "B", LockType.EXCLUSIVE)

    # Step 3: T1 tries X lock on B (held by T2) -> WAITING
    lm.lock(1, "B", LockType.EXCLUSIVE)

    # Step 4: T2 tries X lock on A (held by T1) -> WAITING
    lm.lock(2, "A", LockType.EXCLUSIVE)

    lm.print_lock_table()

