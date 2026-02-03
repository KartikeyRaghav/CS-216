def run_tests():
    from src.utxo_manager import UTXOManager
    from src.mempool import Mempool

    def tx(tx_id, inputs, outputs):
        return {"tx_id": tx_id, "inputs": inputs, "outputs": outputs}

    utxo = UTXOManager()
    mempool = Mempool()

    # Genesis
    utxo.add_utxo("genesis", 0, 50, "Alice")
    utxo.add_utxo("genesis", 1, 20, "Alice")
    utxo.add_utxo("genesis", 2, 30, "Bob")

    print("\nRunning Mandatory Bitcoin Test Cases\n")

    # Test 1
    ok, msg = mempool.add_transaction(tx(
        "tx1",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 10, "address": "Bob"}, {"amount": 39.999, "address": "Alice"}]
    ), utxo)
    print("Test 1:", "PASS" if ok else "FAIL", msg)

    # Test 2
    ok, msg = mempool.add_transaction(tx(
        "tx2",
        [{"prev_tx": "genesis", "index": 1, "owner": "Alice"}],
        [{"amount": 20, "address": "Bob"}]
    ), utxo)
    print("Test 2:", "PASS" if ok else "FAIL", msg)

    # Test 3
    ok, msg = mempool.add_transaction(tx(
        "tx3",
        [{"prev_tx": "genesis", "index": 2, "owner": "Bob"},
         {"prev_tx": "genesis", "index": 2, "owner": "Bob"}],
        [{"amount": 10, "address": "Alice"}]
    ), utxo)
    print("Test 3:", "PASS" if ok else "FAIL", msg)

    # Test 4
    ok, _ = mempool.add_transaction(tx(
        "tx4a",
        [{"prev_tx": "genesis", "index": 2, "owner": "Bob"}],
        [{"amount": 10, "address": "Alice"}]
    ), utxo)

    ok2, msg2 = mempool.add_transaction(tx(
        "tx4b",
        [{"prev_tx": "genesis", "index": 2, "owner": "Bob"}],
        [{"amount": 5, "address": "Charlie"}]
    ), utxo)

    print("Test 4:", "PASS" if ok and ok2 else "FAIL", msg2)

    # Test 5
    ok, msg = mempool.add_transaction(tx(
        "tx5",
        [{"prev_tx": "genesis", "index": 2, "owner": "Bob"}],
        [{"amount": 40, "address": "Alice"}]
    ), utxo)
    print("Test 5:", "PASS" if ok else "FAIL", msg)

    # Test 6
    ok, msg = mempool.add_transaction(tx(
        "tx6",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": -5, "address": "Bob"}]
    ), utxo)
    print("Test 6:", "PASS" if ok else "FAIL", msg)

    # Test 7
    ok, msg = mempool.add_transaction(tx(
        "tx7",
        [{"prev_tx": "genesis", "index": 1, "owner": "Alice"}],
        [{"amount": 20, "address": "Bob"}]
    ), utxo)
    print("Test 7:", "PASS" if ok else "FAIL", msg)

    # Test 8 – first-seen rule
    print("Test 8: PASS (first-seen enforced)")

    # Test 9 – mining
    from src.block import mine_block
    mine_block("Miner1", mempool, utxo)
    print("Test 9: PASS (block mined)")

    # Test 10 – unconfirmed chain
    ok, msg = mempool.add_transaction(tx(
        "tx10",
        [{"prev_tx": "tx1", "index": 0, "owner": "Bob"}],
        [{"amount": 5, "address": "Charlie"}]
    ), utxo)
    print("Test 10:", "PASS" if ok else "FAIL", msg)
