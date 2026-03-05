import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ページの設定
st.set_page_config(page_title="マイ家計簿", page_icon="💸")

st.title("💸 Google Sheets 連携家計簿")
st.write("スマホから入力したデータは、即座にスプレッドシートに保存されます。")

# 1. Google Sheetsへの接続作成
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. データの読み込み
# ttl="0" とすることで、キャッシュを無効化し常に最新の状態を取得します
df = conn.read(ttl="0")

# --- サイドバー：入力フォーム ---
st.sidebar.header("新しい収支を入力")
date = st.sidebar.date_input("日付")
item = st.sidebar.text_input("項目名 (例: 柏駅でのランチ)")
category = st.sidebar.selectbox("カテゴリ", ["食費", "日用品", "交通費", "娯楽", "固定費", "その他"])
amount = st.sidebar.number_input("金額 (円)", min_value=0, step=100)

if st.sidebar.button("スプレッドシートに追加"):
    if item and amount > 0:
        # 新しい行の作成
        new_row = pd.DataFrame([{
            "日付": str(date),
            "項目": item,
            "カテゴリ": category,
            "金額": amount
        }])

        # 既存データと結合して更新
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
        
        st.sidebar.success("保存しました！")
        # 画面を更新して最新の表を表示させる
        st.rerun()
    else:
        st.sidebar.error("項目名と金額を入力してください。")

# --- メイン画面：データの表示 ---
st.header("📊 現在の支出状況")

if not df.empty:
    # A. 合計金額の表示
    total_amount = df["金額"].sum()
    st.metric("今までの合計支出", f"{total_amount:,} 円")

    # B. データテーブルの表示
    st.subheader("履歴一覧")
    # 日付の新しい順に並び替えて表示
    st.dataframe(df.sort_values("日付", ascending=False), use_container_width=True)

    # C. カテゴリ別の集計グラフ
    st.subheader("カテゴリ別支出")
    category_summary = df.groupby("カテゴリ")["金額"].sum()
    st.bar_chart(category_summary)

else:
    st.info("データがまだありません。サイドバーから入力してください。")