from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.block import mine_block
from tests.test_scenarios import run_tests
import uuid

def main():
    utxo_manager = UTXOManager()
    mempool = Mempool(allow_unconfirmed=True)

    genesis = [
        ("Alice", 50.0),
        ("Bob", 30.0),
        ("Charlie", 20.0),
        ("David", 10.0),
        ("Eve", 5.0),
    ]

    for i, (owner, amt) in enumerate(genesis):
        utxo_manager.add_utxo("genesis", i, amt, owner)

    print("\n=== Bitcoin Transaction Simulator ===")
    print("Initial UTXOs (Genesis Block):")
    for owner, amt in genesis:
        print(f"- {owner} : {amt} BTC")
        
    while True:

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
            if not utxos:
                print("FAIL - No UTXOs available for sender")
                continue

            inputs = []
            total = 0.0

            for txid, idx, amt in utxos:
                inputs.append({"prev_tx": txid, "index": idx, "owner": sender})
                total += amt
                if total >= amount:
                    break

            if total < amount:
                print("FAIL - Insufficient funds")
                continue

            outputs = [{"amount": amount, "address": receiver}]
            change = round(total - amount - 0.001, 6)

            if change < 0:
                print("FAIL - Not enough balance to pay fee")
                continue

            if change > 0:
                outputs.append({"amount": change, "address": sender})

            tx = {"tx_id": str(uuid.uuid4()), "inputs": inputs, "outputs": outputs}

            ok, msg = mempool.add_transaction(tx, utxo_manager)
            print("PASS" if ok else "FAIL", msg)

        elif choice == "2":
            print("\n--- UTXO Set ---")
            for (txid, idx), (amt, owner) in utxo_manager.utxo_set.items():
                print(f"{txid}:{idx} → {owner} : {amt} BTC")

        elif choice == "3":
            print("\n--- Mempool ---")
            if not mempool.transactions:
                print("(empty)")
            for t in mempool.transactions:
                tx = t["tx"]
                print(f"TX {tx['tx_id']} | Fee: {t['fee']} BTC")

        elif choice == "4":
            miner = input("Miner name: ").strip()
            mine_block(miner, mempool, utxo_manager)

        elif choice == "5":
            run_tests()

        elif choice == "6":
            print("Exiting simulator.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
