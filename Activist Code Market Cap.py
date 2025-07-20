# -*- coding: utf-8 -*-
"""
売上減少 vs 純利益・時価総額カーブ / 感応度表 / マルチシナリオ表
"""

import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict

# --- ChatGPT 用リッチ表示ライブラリを“ある時だけ”使う -----------------
try:
    import ace_tools          # ChatGPT UI 専用
    _USE_ACE = True
except ImportError:
    _USE_ACE = False
# ----------------------------------------------------------------

@dataclass
class Impact:
    profit_pct: float
    mcap_pct: float

BASE_MAP   = {10: Impact(20, 15), 20: Impact(40, 30), 30: Impact(60, 45)}
LIGHT_MAP  = {10: Impact(15, 12), 20: Impact(30, 24), 30: Impact(45, 36)}
SEVERE_MAP = {10: Impact(25, 18), 20: Impact(50, 35), 30: Impact(75, 55)}
SCENARIOS = {"Base": BASE_MAP, "Light": LIGHT_MAP, "Severe": SEVERE_MAP}

def _interp(x0, x1, y0, y1, x):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

def get_impact(rev_drop: float, mp: Dict[int, Impact]) -> Impact:
    keys = sorted(mp.keys())
    if rev_drop in mp:
        return mp[rev_drop]
    if rev_drop < keys[0]:
        k0, k1 = keys[0], keys[1]
    elif rev_drop > keys[-1]:
        k0, k1 = keys[-2], keys[-1]
    else:
        for i in range(len(keys) - 1):
            if keys[i] <= rev_drop <= keys[i + 1]:
                k0, k1 = keys[i], keys[i + 1]; break
    p = _interp(k0, k1, mp[k0].profit_pct, mp[k1].profit_pct, rev_drop)
    m = _interp(k0, k1, mp[k0].mcap_pct,   mp[k1].mcap_pct,   rev_drop)
    return Impact(round(p, 2), round(m, 2))

def show_df(name, df):
    if _USE_ACE:
        ace_tools.display_dataframe_to_user(name, df)
    else:
        print(f"\n=== {name} ===")
        print(df.to_string(index=False))

def main():
    sales_range = list(range(0, 51, 5))

    base_tbl = pd.DataFrame(
        [{"Sales Decline (%)": s,
          "Profit Decline (%)": get_impact(s, BASE_MAP).profit_pct,
          "MCap Decline (%)":   get_impact(s, BASE_MAP).mcap_pct}
         for s in sales_range]
    )
    show_df("Base Scenario Sensitivity (0‑50% step5)", base_tbl)

    multi_tbl = pd.DataFrame(
        [{"Scenario": scen,
          "Sales Decline (%)": s,
          "Profit Decline (%)": get_impact(s, mp).profit_pct,
          "MCap Decline (%)":   get_impact(s, mp).mcap_pct}
         for scen, mp in SCENARIOS.items()
         for s in sales_range]
    )
    show_df("Multi‑Scenario Sensitivity", multi_tbl)

    # プロット
    plt.figure()
    for scen, mp in SCENARIOS.items():
        y = [get_impact(s, mp).profit_pct for s in sales_range]
        plt.plot(sales_range, y, label=f"{scen} Profit")
    plt.title("Sales Decline vs Profit Decline")
    plt.xlabel("Sales Decline (%)"); plt.ylabel("Profit Decline (%)")
    plt.legend(); plt.grid(True); plt.tight_layout()
    plt.show()

    plt.figure()
    for scen, mp in SCENARIOS.items():
        y = [get_impact(s, mp).mcap_pct for s in sales_range]
        plt.plot(sales_range, y, label=f"{scen} Market Cap")
    plt.title("Sales Decline vs Market Cap Decline")
    plt.xlabel("Sales Decline (%)"); plt.ylabel("Market Cap Decline (%)")
    plt.legend(); plt.grid(True); plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
