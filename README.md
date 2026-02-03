# Bitcoin Transaction & UTXO Simulator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Course](https://img.shields.io/badge/Course-CS%20216-orange.svg)

A simplified simulation of Bitcoin's transaction system developed for **CS 216: Introduction to Blockchain**. This project demonstrates the core mechanics of the UTXO (Unspent Transaction Output) model, mempool management, transaction validation, and mining without the complexity of networking or cryptographic signatures.

---

## Team Kryptonite

| Name | Roll Number |
|:--- |:--- |
| **Aarush Bindod** | 240051001 |
| **Abhiroop Gohar** | 240051002 |
| **Kartikey Raghav** | 240021008 |
| **Tanishq Dhari** | 240001072 |

---

## Project Overview

This simulator provides a local, single-node implementation of a blockchain transaction system. It focuses on the logic of how bitcoins are spent and tracked.

**Key Concepts Implemented:**
* **UTXO Model:** Tracking unspent outputs as the global state.
* **Transaction Lifecycle:** Creation -> Validation -> Mempool -> Mining.
* **Double-Spending Prevention:** Ensuring an input cannot be referenced twice.
* **Mining Simulation:** Fee-based transaction selection and coinbase rewards.

**Note:** This is a logic simulator. It does not implement P2P networking, SHA-256 PoW, or Elliptic Curve Cryptography.

---

## Project Structure

```bash
CS216-TeamKryptonite-UTXO-Simulator/
│
├── src/
│   ├── main.py          # Entry point for the CLI application
│   ├── utxo_manager.py  # Manages the global state of unspent outputs
│   ├── transaction.py   # Transaction data structure and logic
│   ├── validator.py     # Rules for validating transactions
│   ├── mempool.py       # Temporary storage for unconfirmed transactions
│   └── block.py         # Block structure for mining
│
├── tests/
│   └── test_scenarios.py # Automated test cases (Valid/Invalid/Double-Spend)
│
├── README.md            # Project documentation
└── requirements.txt     # Dependencies
```
## How to Run

### Prerequisites
* Python 3.8 or higher
* pip (Python Package Installer)

### Execution Steps
1.  Clone this repository or download the source code.
2.  Open a terminal in the project directory.
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Navigate to the source folder and run the interactive menu:
    ```bash
    python -m src.main
    ```

## System Architecture

The system is designed around a modular architecture where the `UTXOManager` serves as the central source of truth.

### 1. UTXO Manager
The `UTXOManager` acts as the distributed ledger state. Instead of tracking user balances (Account Model), it tracks specific unspent outputs.
* **Data Structure:** A dictionary mapping `(tx_id, output_index)` to `(amount, owner)`.
* **Role:** It provides the data necessary to validate inputs and is updated atomically when a block is mined.


### 2. Transaction Validation
Before a transaction enters the mempool, the `Validator` module enforces consensus rules:
* **Input Existence:** Checks if the referenced UTXO exists in the `UTXOManager`.
* **Double-Spend Check:** Verifies that the UTXO has not already been consumed by a transaction in the mempool or the blockchain.
* **Solvency:** Ensures `Sum(Inputs) >= Sum(Outputs)`.
* **Fee Calculation:** The difference between inputs and outputs is implicitly calculated as the mining fee.

### 3. Mempool (Memory Pool)
The mempool acts as a holding area for unconfirmed transactions.
* **Conflict Resolution:** It enforces a "First-Seen" rule. If a transaction attempts to spend a UTXO that is already referenced by another transaction in the pool, it is rejected immediately.
* **Mining Selection:** Transactions remain here until a miner selects them for a block.

### 4. Mining Simulation
The mining process simulates the creation of a new block:
1.  **Selection:** The miner selects transactions from the mempool, prioritizing those with the highest fees.
2.  **Coinbase:** A special transaction is created to reward the miner with the block reward plus the sum of all transaction fees.
3.  **State Update:** The `UTXOManager` removes the spent inputs and adds the new outputs from the block to the global set.

---

## Test Scenarios

The simulator includes a suite of test scenarios to verify the integrity of the system. These can be executed via the main menu.

| Scenario | Description | Expected Outcome |
|:--- |:--- |:--- |
| **1. Valid Transaction** | User A sends coins to User B using valid UTXOs. | Transaction enters mempool and is mined successfully. |
| **2. Double-Spend** | User A tries to spend the exact same UTXO in two different transactions. | The second transaction is rejected by the Validator. |
| **3. Mempool Conflict** | Two conflicting transactions are sent rapidly. | The first transaction is accepted; the second is rejected based on the "First-Seen" rule. |
| **4. Insufficient Funds** | User tries to send more coins than the referenced UTXOs contain. | Transaction is rejected due to insolvency. |

---

## References

1.  **Nakamoto, S. (2008).** *Bitcoin: A Peer-to-Peer Electronic Cash System.*
2.  **Antonopoulos, A. M. (2014).** *Mastering Bitcoin: Unlocking Digital Cryptocurrencies.* O'Reilly Media.
3.  **Course Materials:** CS 216 Introduction to Blockchain, IIT Indore (Spring 2026).

---

**Authored by _Team KRYPTONITE_**
