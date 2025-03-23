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
    print("P2SH-SegWit Transaction (B' -> C')")
    print("=" * 60)
    print(f"Connecting to Bitcoin Core at {rpc_url}")
    try:
        conn = AuthServiceProxy(rpc_url)
        conn.getblockchaininfo()
        return conn
    except Exception as e:
        print("ERROR: Could not connect to Bitcoin Core. Verify that bitcoind is running!")
        print(f"Details: {e}")
        sys.exit(1)

def load_wallet(conn, wallet_name=WALLET_NAME):
    try:
        wallets = conn.listwallets()
        if wallet_name not in wallets:
            print(f"Wallet '{wallet_name}' not loaded; attempting to load it...")
            conn.loadwallet(wallet_name)
        wallet_conn = AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}/wallet/{wallet_name}")
        return wallet_conn
    except JSONRPCException as e:
        print("ERROR loading wallet:", e)
        sys.exit(1)

def main():
    rpc_conn = connect_rpc()
    wallet = load_wallet(rpc_conn)

    print("Enter the actual P2SH-SegWit Address B' (sender from A'->B transaction):")
    addr_B = input().strip()
    print("Enter the P2SH-SegWit Address C' (receiver):")
    addr_C = input().strip()
    print("-" * 60)

    utxos = wallet.listunspent(1, 9999999, [addr_B])
    if not utxos:
        print("ERROR: No UTXOs found for Address B'. Ensure that the A'->B' transaction is confirmed.")
        sys.exit(1)
    utxo = utxos[0]
    available = Decimal(utxo["amount"])
    print("Selected UTXO:")
    print(f"  TXID: {utxo['txid']}")
    print(f"  VOUT: {utxo['vout']}")
    print(f"  Amount: {available:.8f} BTC")
    print("-" * 60)

    send_amt = min(Decimal("0.3"), available - Decimal("0.0001"))
    if send_amt <= 0:
        print("ERROR: Not enough funds available after fees!")
        sys.exit(1)
    fee = Decimal("0.0001")
    change_amt = available - send_amt - fee

    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_C: float(send_amt)}
    if change_amt > 0:
        outputs[addr_B] = float(change_amt)

    try:
        raw_tx = wallet.createrawtransaction(inputs, outputs)
        print("\nRaw Transaction Hex (B' -> C'):")
        print(raw_tx)
        signed_tx = wallet.signrawtransactionwithwallet(raw_tx)
        if not signed_tx.get("complete"):
            print("ERROR: Transaction signing incomplete!")
            sys.exit(1)
        txid_B_C = wallet.sendrawtransaction(signed_tx["hex"])
        print(f"\nTransaction B' -> C' broadcasted. TXID: {txid_B_C}")
    except Exception as e:
        print("ERROR creating transaction B' -> C':", e)
        sys.exit(1)

    wallet.generatetoaddress(1, addr_C)
    print("-" * 60)

    decoded = wallet.decoderawtransaction(signed_tx["hex"])
    pretty_print("Decoded Transaction B' -> C'", decoded)

    for vin in decoded.get("vin", []):
        if "scriptSig" in vin:
            print("\nUnlocking Script for Input:")
            print(vin["scriptSig"])
    print("=" * 60)

if __name__ == "__main__":
    main()
