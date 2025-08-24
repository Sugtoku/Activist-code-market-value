# 売上減少 vs 純利益・時価総額カーブ

## プロジェクト概要

本リポジトリは、**売上減少率 → 純利益減少率・時価総額減少率** を線形補間で結び付ける簡易モデルです。  
- 感応度表（単一シナリオ／マルチシナリオ）の生成  
- 売上減少と純利益・時価総額の関係をプロット  

を自動化し、政策分析や経営層向けのシナリオ提示を支援します。  

デフォルトでは以下の **3つのシナリオ** を内蔵しています。  
- Base（ベースライン）  
- Light（軽度ショック）  
- Severe（深刻ショック）  

## 特徴

- 売上減少率 0〜50%（5%刻み）のレンジを一括評価  
- Base / Light / Severe のマルチシナリオ比較  
- 表は ChatGPT UI 上ではリッチ表示（`ace_tools`）、通常環境では標準出力  
- Matplotlib による折れ線グラフ描画  
- シナリオマップを書き換えるだけで業界別・企業別にカスタマイズ可能  

## 依存環境

- Python 3.9+ 推奨  
- 必要ライブラリ  
  - pandas  
  - matplotlib  
- （任意）`ace_tools`：ChatGPT 専用のリッチ表示用。通常環境では未インストールで問題ありません。  

インストール例：
```bash
pip install pandas matplotlib
```

## 実行方法

```bash
python impact_curves.py
```

実行すると以下を出力します：  
- **Base Scenario Sensitivity (0-50% step5)**  
- **Multi-Scenario Sensitivity**  
- 2種類のプロット（売上減少 vs 純利益減少、売上減少 vs 時価総額減少）  

## 出力例（列定義）

### Base Scenario Sensitivity
- Sales Decline (%)  
- Profit Decline (%)  
- MCap Decline (%)  

### Multi-Scenario Sensitivity
- Scenario（Base / Light / Severe）  
- Sales Decline (%)  
- Profit Decline (%)  
- MCap Decline (%)  

## シナリオの拡張方法

`BASE_MAP` / `LIGHT_MAP` / `SEVERE_MAP` のアンカーポイントを変更して利用できます。  
例：
```python
BASE_MAP = {
    5:  Impact(8,  6),
    10: Impact(16, 12),
    20: Impact(35, 26),
    30: Impact(55, 40),
    40: Impact(75, 58),
}
```

## ファイル保存（任意）

感応度表や図をファイルに保存する場合は、以下を追記してください。

```python
# CSV 保存
base_tbl.to_csv("base_sensitivity.csv", index=False)
multi_tbl.to_csv("multi_sensitivity.csv", index=False)

# 画像保存
plt.savefig("profit_curve.png", dpi=300, bbox_inches="tight")
plt.savefig("mcap_curve.png", dpi=300, bbox_inches="tight")
```

## よくある質問

**Q1. `ace_tools` の ImportError が出ます**  
A. 仕様通りです。通常環境では無視して問題ありません。標準出力で自動的に表示されます。  

**Q2. 画像ウィンドウが出ない**  
A. サーバや WSL 環境ではバックエンド設定が必要です。保存専用なら冒頭に `matplotlib.use("Agg")` を追記してください。  

## リポジトリ構成（推奨）

```
.
├─ impact_curves.py          # 本スクリプト
├─ requirements.txt          # pandas, matplotlib
├─ LICENSE                   # ライセンスファイル
└─ README.md
```

---

## ライセンスについて

- 一般公開して自由に使ってもらいたい → **MIT License** が最もシンプルで実務向きです。  
- 商用利用や改変を制限したい → **GPL** や **Apache-2.0** などを検討してください。  
- 日本語での発表資料・研究用の共有が主目的 → **MIT** が推奨です。  

最も使いやすく一般的なのは **MIT License** ですので、このリポジトリも **MIT** をおすすめします。  

## ライセンス

このプロジェクトは [MIT License](./LICENSE) の下で公開されています。
