from src.validator import validate_transaction

class Mempool:
    def __init__(self, max_size=50, allow_unconfirmed=False):
        self.transactions = []
        self.spent_utxos = set()
        self.max_size = max_size
        self.allow_unconfirmed = allow_unconfirmed

    def add_transaction(self, tx, utxo_manager):
        valid, result = validate_transaction(tx, utxo_manager, self)
        if not valid:
            return False, result
        
        for i, out in enumerate(tx["outputs"]):
            self.spent_utxos.discard((tx["tx_id"], i))


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
