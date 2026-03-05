import streamlit as st
import pandas as pd
import datetime
import os

# データの保存先ファイル名
DATA_FILE = "kakeibo.csv"

# --- データの読み込み関数 ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # ファイルがない場合は空のデータフレームを作成
        return pd.DataFrame(columns=["日付", "項目", "カテゴリ", "金額"])

# --- アプリのメイン画面 ---
st.title("💸 シンプル家計簿")

# サイドバーに入力フォームを作成
st.sidebar.header("収支の入力")
date = st.sidebar.date_input("日付", datetime.date.today())
item = st.sidebar.text_input("項目名 (例: ランチ)")
category = st.sidebar.selectbox("カテゴリ", ["食費", "日用品", "交通費", "娯楽", "その他"])
amount = st.sidebar.number_input("金額 (円)", min_value=0, step=100)

if st.sidebar.button("追加"):
    # 新しいデータをデータフレームに追加
    new_data = pd.DataFrame([[date, item, category, amount]], columns=["日付", "項目", "カテゴリ", "金額"])
    df = load_data()
    df = pd.concat([df, new_data], ignore_index=True)
    
    # CSVに保存
    df.to_csv(DATA_FILE, index=False)
    st.sidebar.success("保存しました！")

# --- データの表示 ---
st.header("履歴一覧")
df = load_data()

if not df.empty:
    # 表を表示
    st.dataframe(df.sort_values("日付", ascending=False), use_container_width=True)
    
    # 合計金額を表示
    total = df["金額"].sum()
    st.metric("合計支出", f"{total:,} 円")
else:
    st.info("データがまだありません。サイドバーから追加してください。")