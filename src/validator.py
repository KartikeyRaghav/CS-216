def validate_transaction(tx, utxo_manager, mempool):
    seen = set()
    total_in = 0.0
    total_out = 0.0

    for inp in tx["inputs"]:
        key = (inp["prev_tx"], inp["index"])

        if key in seen:
            return False, "Double-spend inside transaction"

        if not utxo_manager.exists(*key):
            if not mempool.allow_unconfirmed:
                return False, f"UTXO {key} does not exist"
            if mempool.allow_unconfirmed:
                for t in mempool.transactions:
                    for i, out in enumerate(t["tx"]["outputs"]):
                        if (t["tx"]["tx_id"], i) == key:
                            total_in += out["amount"]
                            seen.add(key)
                            break

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
