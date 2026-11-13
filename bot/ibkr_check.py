#!/usr/bin/env python3
"""Read-only IBKR PAPER connection check. Places NO orders.

Run on the machine where IB Gateway / TWS (paper) is running:
    pip install ib_async
    python ibkr_check.py            # Gateway paper port 4002 (default)
    python ibkr_check.py --port 7497   # TWS paper

Safety: refuses to continue unless the connected account is a paper account
(IBKR paper account IDs start with "DU"). Stores no credentials: the login
happens inside IB Gateway, not in this script.
"""
import argparse
import sys

from ib_async import IB

PAPER_PORTS = {4002, 7497}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=4002)
    p.add_argument("--client-id", type=int, default=101)
    a = p.parse_args()

    if a.port not in PAPER_PORTS:
        print(f"Refusing: port {a.port} is not a known paper port {sorted(PAPER_PORTS)}.")
        return 2

    ib = IB()
    ib.connect(a.host, a.port, clientId=a.client_id, readonly=True, timeout=15)
    try:
        accounts = ib.managedAccounts()
        print("Accounts:", accounts)
        if not accounts or not all(x.startswith("DU") for x in accounts):
            print("Refusing: connected account is not a paper (DU...) account.")
            return 3
        for row in ib.accountSummary():
            if row.tag in {"NetLiquidation", "TotalCashValue", "BuyingPower"}:
                print(f"{row.tag}: {row.value} {row.currency}")
        positions = ib.positions()
        print(f"Open positions: {len(positions)}")
        for pos in positions:
            print(f"  {pos.contract.symbol}: {pos.position} @ {pos.avgCost}")
        print("OK: read-only paper connection works.")
        return 0
    finally:
        ib.disconnect()


if __name__ == "__main__":
    sys.exit(main())
