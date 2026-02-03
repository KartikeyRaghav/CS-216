def run_tests(utxo_manager, mempool):
    print("\nRunning Test: Double Spend\n")

    tx1 = {
        "tx_id": "tx1",
        "inputs": [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        "outputs": [
            {"amount": 10, "address": "Bob"},
            {"amount": 39.999, "address": "Alice"}
        ]
    }

    tx2 = {
        "tx_id": "tx2",
        "inputs": [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        "outputs": [
            {"amount": 10, "address": "Charlie"},
            {"amount": 39.999, "address": "Alice"}
        ]
    }

    print("TX1:", mempool.add_transaction(tx1, utxo_manager))
    print("TX2:", mempool.add_transaction(tx2, utxo_manager))
