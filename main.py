import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("💸 共有家計簿")

# Google Sheetsへの接続設定
conn = st.connection("gsheets", type=GSheetsConnection)

# データの読み込み
# (スプレッドシートの一番上の行を見出しとして読み込みます)
df = conn.read()

# サイドバーでの入力（前と同じ）
st.sidebar.header("収支の入力")
date = st.sidebar.date_input("日付")
item = st.sidebar.text_input("項目名")
category = st.sidebar.selectbox("カテゴリ", ["食費", "日用品", "交通費", "娯楽", "その他"])
amount = st.sidebar.number_input("金額", min_value=0)

if st.sidebar.button("追加"):
    # 新しいデータを作成
    new_data = pd.DataFrame([{"日付": str(date), "項目": item, "カテゴリ": category, "金額": amount}])
    
    # 既存のデータに追加
    updated_df = pd.concat([df, new_data], ignore_index=True)
    
    # スプレッドシートを更新
    conn.update(data=updated_df)
    st.sidebar.success("スプレッドシートを更新しました！")

# データの表示
st.dataframe(df)