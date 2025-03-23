# Bitcoin-Scripting

## Team Members
| Team Member Name | GitHub Profile | Roll Number |
|------------------|----------------|-------------|
| Asif Hussain     | [Asif](https://github.com/Asifussain)      | 230041021 |
| Sathwik          | [Sathwik](https://github.com/Sathwik-18) | 230041024 |
| Sai Prakul       | [Prakul](https://github.com/SaiPrakul) | 230041031 |

A repository for learning and experimenting with Bitcoin scripting through practical examples. This project demonstrates how to create and analyze different types of Bitcoin transactions (Legacy P2PKH and SegWit) in a regtest environment.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Installing Bitcoin Core](#installing-bitcoin-core)
  - [Configuring Bitcoin Core](#configuring-bitcoin-core)
  - [Setting Up Python Environment](#setting-up-python-environment)
- [Running the Examples](#running-the-examples)
  - [Legacy P2PKH Transactions](#legacy-p2pkh-transactions)
  - [P2SH-SegWit Transactions](#p2sh-segwit-transactions)
- [Understanding the Code](#understanding-the-code)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Overview

This repository contains Python scripts that demonstrate how to create, sign, and broadcast Bitcoin transactions using the Bitcoin Core RPC interface. The examples cover:

1. Legacy P2PKH (Pay-to-Public-Key-Hash) transactions
2. P2SH-SegWit (Pay-to-Script-Hash Segregated Witness) transactions

Each transaction type has two scripts:
- A script to send from Address A to Address B
- A script to send from Address B to Address C

These examples provide hands-on experience with different Bitcoin address formats and transaction types.

## Prerequisites

- Windows, macOS, or Linux operating system
- Python 3.7+
- Bitcoin Core v0.21.0 or newer
- Basic understanding of Bitcoin transactions

## Installation

### Installing Bitcoin Core

1. Download Bitcoin Core from the [official website](https://bitcoincore.org/en/download/).

2. Install Bitcoin Core following the installation instructions for your operating system.

   ![Bitcoin Core Installation](placeholder_for_bitcoin_core_installation_image.png)

### Configuring Bitcoin Core

1. Create or edit the Bitcoin configuration file:

   **Location of bitcoin.conf:**
   - Windows: `C:\Users\{USERNAME}\AppData\Roaming\Bitcoin\bitcoin.conf`
   - macOS: `~/Library/Application Support/Bitcoin/bitcoin.conf`
   - Linux: `~/.bitcoin/bitcoin.conf`

2. Add the following configuration to your `bitcoin.conf` file:

```
[regtest]
regtest=1
rpcuser=your_username
rpcpassword=your_password
rpcport=18443
paytxfee=0.0001
fallbackfee=0.0002
mintxfee=0.00001
txconfirmtarget=6
server=1
```

Make sure to replace `your_username` and `your_password` with your preferred values.

3. Start Bitcoin Core in regtest mode:

   **Windows:**
   ```
   bitcoind -regtest -conf="C:\Users\{USERNAME}\AppData\Roaming\Bitcoin\bitcoin.conf"
   ```

   **macOS/Linux:**
   ```
   bitcoind -regtest -conf="$HOME/.bitcoin/bitcoin.conf"
   ```

4. Verify that Bitcoin Core is running correctly:

   **Windows:**
   ```
   bitcoin-cli -regtest -rpcuser=your_username -rpcpassword=your_password getblockchaininfo
   ```

   **macOS/Linux:**
   ```
   bitcoin-cli -regtest -rpcuser=your_username -rpcpassword=your_password getblockchaininfo
   ```

   You should see blockchain information in JSON format.

   ![Bitcoin Core Running](placeholder_for_bitcoin_core_running_image.png)

### Setting Up Python Environment

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Bitcoin-Scripting.git
   cd Bitcoin-Scripting
   ```

2. Create a virtual environment:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not available, install the necessary packages manually:
   ```
   pip install python-bitcoinrpc
   ```

4. Update the RPC connection settings in each script to match your configuration:
   ```python
   # --- RPC Connection Settings ---
   RPC_USER = "your_username"
   RPC_PASSWORD = "your_password"
   RPC_HOST = "127.0.0.1"
   RPC_PORT = "18443"
   WALLET_NAME = "default"
   ```

## Running the Examples

Make sure Bitcoin Core is running in regtest mode and your virtual environment is activated before running the scripts.

### Legacy P2PKH Transactions

1. First, run the script to create a transaction from Address A to Address B:
   ```
   python legacy_A_to_B.py
   ```

   This script will:
   - Generate three legacy addresses (A, B, and C)
   - Fund Address A with 1 BTC
   - Create a transaction that sends 0.5 BTC from A to B
   - Mine a block to confirm the transaction
   - Display the transaction details and locking script

   ![Legacy A to B Transaction](placeholder_for_legacy_A_to_B_image.png)

   **Make note of the addresses displayed in the output, as you'll need them for the next step.**

2. Next, run the script to create a transaction from Address B to Address C:
   ```
   python legacy_B_to_C.py
   ```

   When prompted:
   - Enter the Address B (displayed in the output of the previous script)
   - Enter the Address C (displayed in the output of the previous script)

   This script will:
   - Create a transaction sending approximately 0.3 BTC from B to C
   - Mine a block to confirm the transaction
   - Display the transaction details and unlocking script

   ![Legacy B to C Transaction](placeholder_for_legacy_B_to_C_image.png)

### P2SH-SegWit Transactions

1. First, run the script to create a transaction from Address A' to Address B':
   ```
   python segwit_A_to_B.py
   ```

   This script will:
   - Generate three P2SH-SegWit addresses (A', B', and C')
   - Fund Address A' with 1 BTC
   - Create a transaction that sends 0.5 BTC from A' to B'
   - Mine a block to confirm the transaction
   - Display the transaction details and locking script

   ![SegWit A to B Transaction](placeholder_for_segwit_A_to_B_image.png)

   **Make note of the addresses displayed in the output, as you'll need them for the next step.**

2. Next, run the script to create a transaction from Address B' to Address C':
   ```
   python segwit_B_to_C.py
   ```

   When prompted:
   - Enter the Address B' (displayed in the output of the previous script)
   - Enter the Address C' (displayed in the output of the previous script)

   This script will:
   - Create a transaction sending approximately 0.3 BTC from B' to C'
   - Mine a block to confirm the transaction
   - Display the transaction details and unlocking script

   ![SegWit B to C Transaction](placeholder_for_segwit_B_to_C_image.png)

## Understanding the Code

Each script follows a similar structure:

1. **Connection Setup**: Establishes connection to the Bitcoin Core RPC interface
2. **Wallet Loading**: Loads the default wallet or creates one if needed
3. **Address Generation/Input**: Creates or requests Bitcoin addresses
4. **Transaction Creation**: Constructs a transaction with inputs, outputs, and change
5. **Transaction Signing**: Signs the transaction with the appropriate private keys
6. **Transaction Broadcasting**: Sends the transaction to the Bitcoin network
7. **Transaction Analysis**: Decodes and displays the transaction details

Key differences between the transaction types:

- **Legacy P2PKH**: Uses traditional Bitcoin addresses with simple locking/unlocking scripts
- **P2SH-SegWit**: Uses Segregated Witness wrapped in a Pay-to-Script-Hash, which offers reduced transaction fees and malleability fixes

## Troubleshooting

### Bitcoin Core Connection Issues

- Ensure Bitcoin Core is running in regtest mode
- Verify your bitcoin.conf file has the correct settings
- Check that the RPC credentials in your scripts match those in bitcoin.conf

### Transaction Errors

- Make sure you have sufficient funds in the sending address
- Verify that previous transactions are confirmed (mined into a block)
- Check that the addresses are entered correctly

### Script Execution Problems

- Ensure your Python virtual environment is activated
- Verify all dependencies are installed
- Check that Python 3.7+ is being used

## References

- [Bitcoin Developer Documentation](https://developer.bitcoin.org/)
- [Bitcoin Core RPC API Reference](https://developer.bitcoin.org/reference/rpc/)
- [Bitcoin Wiki - Script](https://en.bitcoin.it/wiki/Script)
- [Bitcoin Improvement Proposals (BIPs)](https://github.com/bitcoin/bips)
