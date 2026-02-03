# ==============================
# CS 216 – UTXO Simulator
# ==============================

# ---------- UTXO MANAGER ----------
class UTXOManager:
    def __init__(self):
        self.utxo_set = {}

    def add_utxo(self, tx_id, index, amount, owner):
        self.utxo_set[(tx_id, index)] = (amount, owner)

    def remove_utxo(self, tx_id, index):
        self.utxo_set.pop((tx_id, index), None)

    def exists(self, tx_id, index):
        return (tx_id, index) in self.utxo_set

    def get_balance(self, owner):
        return sum(a for a, o in self.utxo_set.values() if o == owner)

    def get_utxos_for_owner(self, owner):
        return [
            (tx, idx, amt)
            for (tx, idx), (amt, o) in self.utxo_set.items()
            if o == owner
        ]


# ---------- TRANSACTION VALIDATION ----------
def validate_transaction(tx, utxo_manager, mempool):
    seen = set()
    total_in = 0.0
    total_out = 0.0

    for inp in tx["inputs"]:
        key = (inp["prev_tx"], inp["index"])

        if key in seen:
            return False, "Double-spend inside transaction"

        if not utxo_manager.exists(*key):
            return False, f"UTXO {key} does not exist"

        if key in mempool.spent_utxos:
            return False, f"UTXO {key} already spent by mempool transaction"

        amt, owner = utxo_manager.utxo_set[key]
        if owner != inp["owner"]:
            return False, "Owner mismatch"

        seen.add(key)
        total_in += amt

    for out in tx["outputs"]:
        if out["amount"] < 0:
            return False, "Negative output amount"
        total_out += out["amount"]

    if total_in < total_out:
        return False, "Insufficient funds"

    return True, round(total_in - total_out, 6)


# ---------- MEMPOOL ----------
class Mempool:
    def __init__(self, max_size=50):
        self.transactions = []
        self.spent_utxos = set()
        self.max_size = max_size

    def add_transaction(self, tx, utxo_manager):
        valid, result = validate_transaction(tx, utxo_manager, self)
        if not valid:
            return False, result

        for inp in tx["inputs"]:
            self.spent_utxos.add((inp["prev_tx"], inp["index"]))

        self.transactions.append({"tx": tx, "fee": result})
        return True, f"Transaction valid! Fee: {result} BTC"

    def remove_transaction(self, tx_id):
        for t in self.transactions:
            if t["tx"]["tx_id"] == tx_id:
                for inp in t["tx"]["inputs"]:
                    self.spent_utxos.discard((inp["prev_tx"], inp["index"]))
                self.transactions.remove(t)
                return

    def get_top_transactions(self, n):
        return sorted(self.transactions, key=lambda x: x["fee"], reverse=True)[:n]

    def clear(self):
        self.transactions.clear()
        self.spent_utxos.clear()


# ---------- MINING ----------
def mine_block(miner, mempool, utxo_manager, num_txs=5):
    selected = mempool.get_top_transactions(num_txs)
    total_fees = 0.0

    print(f"Selected {len(selected)} transactions from mempool.")

    for entry in selected:
        tx = entry["tx"]
        fee = entry["fee"]
        total_fees += fee

        for inp in tx["inputs"]:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        for i, out in enumerate(tx["outputs"]):
            utxo_manager.add_utxo(tx["tx_id"], i, out["amount"], out["address"])

        mempool.remove_transaction(tx["tx_id"])

    utxo_manager.add_utxo("coinbase", 0, total_fees, miner)
    print(f"Miner {miner} receives {total_fees} BTC")
    print("Block mined successfully!")


# ---------- TEST SCENARIOS ----------
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


# ---------- MENU ----------
def main():
    utxo_manager = UTXOManager()
    mempool = Mempool()

    # Genesis block
    genesis = [
        ("Alice", 50.0),
        ("Bob", 30.0),
        ("Charlie", 20.0),
        ("David", 10.0),
        ("Eve", 5.0),
    ]

    for i, (owner, amt) in enumerate(genesis):
        utxo_manager.add_utxo("genesis", i, amt, owner)

    while True:
        print("\n=== Bitcoin Transaction Simulator ===")
        print("Initial UTXOs (Genesis Block):")
        for owner, amt in genesis:
            print(f"- {owner} : {amt} BTC")

        print("\nMain Menu:")
        print("1. Create new transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            sender = input("Enter sender: ")
            balance = utxo_manager.get_balance(sender)
            print(f"Available balance: {balance} BTC")

            receiver = input("Enter recipient: ")
            amount = float(input("Enter amount: "))

            utxos = utxo_manager.get_utxos_for_owner(sender)
            inputs = []
            total = 0.0

            for tx, idx, amt in utxos:
                inputs.append({
                    "prev_tx": tx,
                    "index": idx,
                    "owner": sender
                })
                total += amt
                if total >= amount + 0.001:
                    break

            if total < amount:
                print("Insufficient funds")
                continue

            change = round(total - amount - 0.001, 6)

            outputs = [{"amount": amount, "address": receiver}]
            if change > 0:
                outputs.append({"amount": change, "address": sender})

            tx = {
                "tx_id": f"tx_{sender}_{receiver}_{len(mempool.transactions)}",
                "inputs": inputs,
                "outputs": outputs
            }

            ok, msg = mempool.add_transaction(tx, utxo_manager)
            print(msg)

        elif choice == "2":
            print("\nUTXO Set:")
            for k, v in utxo_manager.utxo_set.items():
                print(k, "->", v)

        elif choice == "3":
            print("\nMempool:")
            for t in mempool.transactions:
                print(t)

        elif choice == "4":
            miner = input("Enter miner name: ")
            print("Mining block...")
            mine_block(miner, mempool, utxo_manager)

        elif choice == "5":
            run_tests(utxo_manager, mempool)

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
