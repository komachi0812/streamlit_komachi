# save as app.py and run: streamlit run app.py
import streamlit as st
from typing import List, Tuple


st.set_page_config(page_title="🧭 超主観行動診断", page_icon="🧭", layout="centered")


# -----------------------
# CSS（ポップ & アニメ）
# -----------------------
st.markdown("""
<style>
.stApp {
    /* 不思議な幻想的グラデーション背景 */
    background: radial-gradient(circle at 20% 30%, #ffdee9 0%, #b5fffc 40%, #ffe5a8 70%, #d4a5ff 100%);
    background-attachment: fixed;
    font-family: 'Segoe UI', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', Meiryo, sans-serif;
    color: #333;
}

/* タイトルカードも浮かせる */
.title-card {
    background: linear-gradient(135deg, #ffd6f0 0%, #a0e7ff 100%);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    text-align: center;
    animation: floaty 6s ease-in-out infinite;
}

@keyframes floaty {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

/* 残りの既存スタイル（質問カードや結果表示など） */
.question-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(250,250,255,0.95));
    padding: 14px;
    border-radius: 12px;
    margin: 10px 0;
    border: 1px solid rgba(200,200,220,0.6);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    box-shadow: 0 6px 18px rgba(20,30,60,0.04);
}
.question-card:hover { transform: translateY(-8px); box-shadow: 0 16px 40px rgba(20,30,60,0.12); }

.q-header { font-weight:700; margin-bottom:6px; }
div[data-baseweb="radio"] > label { display: block; }

.tag-left { display:inline-block; padding:6px 10px; border-radius:999px; font-weight:700; margin-right:8px; }
.tag-bad { background:#ffd6d6; color:#8b1d1d; }
.tag-neutral { background:#fff0cb; color:#7d5b00; }
.tag-good { background:#d6fff0; color:#006644; }

.progress-text { font-size:13px; color:#333; margin-bottom:6px; }

.result-box {
    margin-top: 12px;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 8px 30px rgba(34,99,169,0.06);
    background: linear-gradient(90deg, rgba(255,255,255,0.9), rgba(255,255,255,0.85));
}
.result-emoji { font-size: 48px; display:inline-block; vertical-align: middle; margin-right:12px; }

@keyframes shake {0% { transform: translateX(0px); }20% { transform: translateX(-6px); }40% { transform: translateX(6px); }60% { transform: translateX(-4px); }80% { transform: translateX(4px); }100% { transform: translateX(0px); }}
.shake { animation: shake 0.8s ease; }

@media (max-width: 640px) { .title-main { font-size: 20px; } .result-emoji { font-size:40px; }}
</style>
""", unsafe_allow_html=True)



# -----------------------
# ヘッダー
# -----------------------
st.markdown("""
<div class="title-card">
<div class="title-emoji">🧭</div>
<div class="title-main">超主観行動診断</div>
<div class="title-sub">直感で答えてね。進捗・アニメ・アドバイス付き！</div>
</div>
""", unsafe_allow_html=True)


# -----------------------
# 元の質問10個
# -----------------------
questions: List[Tuple[str, List[str], List[int]]] = [
("今の体の調子はどんな感じですか？", ["— 選択してください —", "悪い", "普通", "良い"], [0, -1, 0, 1]),
("空腹感や食欲の状態はどうですか？", ["— 選択してください —", "腹ペコ", "ちょうどいい", "おなかいっぱい"], [0, -1, 0, 1]),
("今の自分の気持ちはポジティブですか？ネガティブですか？", ["— 選択してください —", "ネガティブ", "どちらでもない", "ポジティブ"], [0, -1, 0, 1]),
("楽しい・ワクワクすることを思い浮かべられますか？", ["— 選択してください —", "できない", "しようと思えば", "できる"], [0, -1, 0, 1]),
("今の自分に「やる気スイッチ」があるとしたら、入っていますか？", ["— 選択してください —", "入ってない", "どちらでもない", "入っている"], [0, -1, 0, 1]),
("外の空気を最近吸いましたか？", ["— 選択してください —", "吸ってない", "一回は吸った", "結構吸った"], [0, -1, 0, 1]),
("頭の中がすっきりしていますか？", ["— 選択してください —", "してない", "どちらともいえない", "してる"], [0, -1, 0, 1]),
("自分を大切にできていると感じますか？", ["— 選択してください —", "できてない", "わからない", "できてる"], [0, -1, 0, 1]),
("他人の意見に左右されすぎていませんか？", ["— 選択してください —", "されてる", "どちらともいえない", "されてない"], [0, 1, 2, 3]),
("今日タバコ吸いましたか？", ["— 選択してください —", "いつも吸うけど吸ってない", "まず吸わない", "吸った"], [0, -100, 0, 100]),
]


# -----------------------
# 質問の表示とスコア取得
# -----------------------
scores = []
answered_count = 0

for i, (q_text, opts, vals) in enumerate(questions, start=1):
    st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="q-header">質問 {i}</div>', unsafe_allow_html=True)
    st.write(q_text)

    # 選択肢のタグ表示
    st.markdown(
        '<div style="margin-bottom:6px;">'
        '<span class="tag-left tag-bad">Bad</span>'
        '<span class="tag-left tag-neutral">So-so</span>'
        '<span class="tag-left tag-good">Good</span>'
        '</div>', 
        unsafe_allow_html=True
    )

    # ラジオボタン（placeholder 0 をデフォルトに）
    choice = st.radio("", opts, index=0, key=f"q{i}")
    idx = opts.index(choice)
    score = vals[idx]
    scores.append(score)

    # placeholder 以外は回答済みカウント
    if idx != 0:
        answered_count += 1

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# プログレスバー
# -----------------------
progress = answered_count / len(questions)
st.markdown(f'<div class="progress-text">回答進捗: {answered_count}/{len(questions)}</div>', unsafe_allow_html=True)
st.progress(progress)



# スコア合計の判定例
# -----------------------
# 結果表示
# -----------------------
# -----------------------
# 結果表示
# -----------------------
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# 「結果を見る」ボタン
if st.button("結果を見る"):
    st.session_state.show_result = True

if st.session_state.show_result:
    total_score = sum(scores)

    # タバコ吸って90以上なら無敵モード
    if abs(total_score) >= 90 and scores[-1] == 100:
        emoji = "💪"
        message = "無敵モード！タバコ吸ってるあなたは今日なんでもできる気分！"
    elif total_score <= -90 and scores[-1] == 100:
        emoji = "😣"
        message = "やばいです！今すぐタバコを吸いましょう！"
    else:
        # スコア帯で結果テキストを決定
        def get_result_text(score):
            if score >= 10:
                return "あなたのコンディションは **超銀河級に良い** と、私の主観的脳内学会で満場一致しました。"
            elif score >= 8:
                return "かなり良い。学術的に言うと『いい感じホルモン』がモリモリ（※全部主観）。"
            elif score >= 5:
                return "そこそこ好調。脳内シミュレーションだと80％成功してます。"
            elif score >= 2:
                return "平均よりちょい上。私の主観基準では優秀です。"
            elif score >= -2:
                return "だいたい普通。学術的にも普通（※学術的とは言ってない）。"
            elif score >= -5:
                return "ちょい不調。主観的に『休め』のサインが出てます。"
            elif score >= -8:
                return "なかなかヤバめ。脳内研究所で赤ランプが点灯しました。"
            else:
                return "深刻レベル。主観だとあなたは今すぐ布団に吸い込まれるべきです。"

        def get_emoji(score):
            if score >= 8: return "🌈✨"
            if score >= 5: return "😎👍"
            if score >= 2: return "🙂"
            if score >= -2: return "😐"
            if score >= -5: return "🥲"
            if score >= -8: return "😣"
            return "💀"

        emoji = get_emoji(total_score)
        message = get_result_text(total_score)

    # 結果表示
    st.markdown(
        f"<div class='result-box result-gradient-2 shake'>"
        f"<span class='result-emoji'>{emoji}</span>"
        f"<strong>合計スコア: {total_score}</strong>"
        f"<p>{message}</p>"
        f"</div>", unsafe_allow_html=True
    )

    # ---------------- ACTION FRAME -----------------
  # ---------------- ACTION FRAME -----------------
st.markdown("### 🚀 簡単アクション（押すと意味がわかる・全部俺の主観）")

# スコア帯ごとにポップなアクションを用意
if total_score >= 8:
    actions = [
        ("全力挑戦ボタン", "学術的に言うと『テンションホルモン』が脳内爆発中。やりたいことを無限ループでやるべし！"),
        ("笑顔バラ撒きボタン", "研究結果（俺調べ）によると、笑顔は周囲の幸福指数を 142% 増幅するらしい。"),
        ("ポジティブ思考ボタン", "脳内観察で『楽しい波動』が増幅中。小さな喜びも取りこぼすな！")
    ]
elif total_score >= 2:
    actions = [
        ("深呼吸ボタン", "呼吸のリズムが心拍とシンクロすると主観的幸福度が 7.3 倍になる（脳内統計）。"),
        ("軽散歩ボタン", "歩行によって足先から『やる気物質』が全身に循環する法則（主観的発見）。"),
        ("水飲むボタン", "体内水分率 70% の理論から、水を飲むと脳が『あ、活動できるぞ』と反応する。")
    ]
elif total_score >= -2:
    actions = [
        ("休憩ボタン", "主観的に言うと、横になることで『集中リセット値』が最大 +42pt。"),
        ("ストレッチボタン", "筋肉の伸縮により『やる気シグナル』が脳内に流れる。科学的根拠は俺の観察。"),
        ("温かい飲み物ボタン", "体温上昇→脳が『生存確認OK』と判断するフロー（全主観）。")
    ]
else:
    actions = [
        ("布団インボタン", "深刻レベルの疲労に対して布団は最強の安全装置。脳内研究所が推奨。"),
        ("深呼吸ボタン", "酸素を取り込むと主観的ストレスレベルが 23% 減少（脳内統計）。"),
        ("お茶ボタン", "温かい液体は心拍と気持ちを安定化させる。学術的には俺の体感。")
    ]

# ボタンと説明を表示（押すと下に表示）
for i, (label, desc) in enumerate(actions):
    key = f"action_{i}"
    if st.button(label, key=key):
        if f"{key}_shown" not in st.session_state:
            st.session_state[f"{key}_shown"] = True
        else:
            st.session_state[f"{key}_shown"] = True

    if st.session_state.get(f"{key}_shown", False):
        st.markdown(f"### {desc}")

st.caption("参照：俺の主観")