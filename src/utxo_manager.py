class UTXOManager:
    def __init__(self):
        self.utxo_set = {}
        self.block_height = 0

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
