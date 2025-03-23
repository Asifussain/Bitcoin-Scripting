from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
import sys, json

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def pretty_print(title, data):
    print(f"\n--- {title} ---")
    print(json.dumps(data, indent=4, cls=DecimalEncoder))
    print("-" * 60)

# --- RPC Connection Settings ---
RPC_USER = "sathwik"
RPC_PASSWORD = "btc18"
RPC_HOST = "127.0.0.1"
RPC_PORT = "18443"
WALLET_NAME = "default"

def connect_rpc():
    rpc_url = f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}"
    print("=" * 60)
    print("P2SH-SegWit Transaction (A' -> B')")
    print("=" * 60)
    print(f"Connecting to Bitcoin Core at {rpc_url}")
    try:
        rpc_conn = AuthServiceProxy(rpc_url)
        rpc_conn.getblockchaininfo()
        return rpc_conn
    except Exception as e:
        print("ERROR: Could not connect to Bitcoin Core. Is bitcoind running in regtest mode?")
        print(f"Details: {e}")
        sys.exit(1)

def load_wallet(rpc_conn, wallet_name=WALLET_NAME):
    try:
        wallets = rpc_conn.listwallets()
        if wallet_name not in wallets:
            print(f"Wallet '{wallet_name}' not loaded; attempting to load it...")
            rpc_conn.loadwallet(wallet_name)
        wallet_rpc = AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}/wallet/{wallet_name}")
        return wallet_rpc
    except JSONRPCException as e:
        print("ERROR loading wallet:", e)
        sys.exit(1)

def main():
    rpc_conn = connect_rpc()
    wallet = load_wallet(rpc_conn)

    try:
        balance = wallet.getbalance()
    except Exception as e:
        print("ERROR fetching balance:", e)
        sys.exit(1)
    print(f"Initial Wallet Balance: {balance:.8f} BTC")

    # Generate three P2SH-SegWit addresses: A', B', and C'.
    addr_A = wallet.getnewaddress("addr_A", "p2sh-segwit")
    addr_B = wallet.getnewaddress("addr_B", "p2sh-segwit")
    addr_C = wallet.getnewaddress("addr_C", "p2sh-segwit")
    print("-" * 60)
    print("Generated P2SH-SegWit Addresses:")
    print(f"  Address A' (Sender):   {addr_A}")
    print(f"  Address B' (Receiver): {addr_B}")
    print(f"  Address C' (Extra):      {addr_C}")
    print("-" * 60)

    print("Generating 101 blocks to fund coins...")
    mining_addr = wallet.getnewaddress("mining")
    wallet.generatetoaddress(101, mining_addr)

    try:
        txid_fund = wallet.sendtoaddress(addr_A, 1.0)
        print(f"Funding Transaction: Sent 1.0 BTC to Address A' | TXID: {txid_fund}")
        wallet.generatetoaddress(1, mining_addr)
    except Exception as e:
        print("ERROR funding Address A':", e)
        sys.exit(1)
    print("-" * 60)

    utxos = wallet.listunspent(1, 9999999, [addr_A])
    if not utxos:
        print("ERROR: No UTXOs available for Address A'.")
        sys.exit(1)
    utxo = utxos[0]
    send_amt = Decimal("0.5")
    fee = Decimal("0.0001")
    change_amt = Decimal(utxo["amount"]) - send_amt - fee
    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_B: float(send_amt)}
    if change_amt > 0:
        outputs[addr_A] = float(change_amt)

    try:
        raw_tx = wallet.createrawtransaction(inputs, outputs)
        print("\nRaw Transaction Hex (A' -> B'):")
        print(raw_tx)
        signed_tx = wallet.signrawtransactionwithwallet(raw_tx)
        if not signed_tx.get("complete"):
            print("ERROR: Transaction signing incomplete!")
            sys.exit(1)
        txid_A_B = wallet.sendrawtransaction(signed_tx["hex"])
        print(f"\nTransaction A' -> B' broadcasted. TXID: {txid_A_B}")
    except Exception as e:
        print("ERROR creating transaction A' -> B':", e)
        sys.exit(1)

    wallet.generatetoaddress(1, addr_B)
    print("-" * 60)

    decoded = wallet.decoderawtransaction(signed_tx["hex"])
    pretty_print("Decoded Transaction A' -> B'", decoded)

    lock_script = None
    for out in decoded.get("vout", []):
        spk = out.get("scriptPubKey", {})
        if ("addresses" in spk and addr_B in spk["addresses"]) or (spk.get("address") == addr_B):
            lock_script = spk.get("hex")
            break
    if lock_script:
        print("\nLocking Script for Address B':")
        print(lock_script)
    else:
        print("\nWARNING: Locking script for Address B' not found.")
    print("=" * 60)

if __name__ == "__main__":
    main()
