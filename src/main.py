from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.block import mine_block
from tests.test_scenarios import run_tests

def main():
    utxo_manager = UTXOManager()
    mempool = Mempool()

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

        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            sender = input("Enter sender: ")
            balance = utxo_manager.get_balance(sender)
            print(f"Available balance: {balance} BTC")

            receiver = input("Enter recipient: ")
            amount = float(input("Enter amount: "))

            utxos = utxo_manager.get_utxos_for_owner(sender)
            inputs = []
            total = 0.0

            for tx_id, idx, amt in utxos:
                inputs.append({
                    "prev_tx": tx_id,
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
            for (tx_id, idx), (amt, owner) in utxo_manager.utxo_set.items():
                print(f"{tx_id}:{idx} -> {amt} BTC ({owner})")

        elif choice == "3":
            print("\nMempool:")
            if not mempool.transactions:
                print("Mempool empty")
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

