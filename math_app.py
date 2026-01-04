import streamlit as st
import random

# 设置网页标题和图标
st.set_page_config(page_title="宝贝的数学冒险", page_icon="🌈")

# 自定义样式：让数字和按钮变大，适合 5 岁小朋友点击
st.markdown("""
    <style>
    .big-font { font-size:60px !important; font-weight: bold; text-align: center; color: #FF4B4B; }
    .stButton>button { width: 100%; height: 80px; font-size: 30px; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 初始化游戏状态
if 'num1' not in st.session_state:
    st.session_state.num1 = random.randint(1, 9)
    st.session_state.num2 = random.randint(1, 9)
    # 确保减法不会出现负数
    st.session_state.op = random.choice(['+', '-'])
    if st.session_state.op == '-':
        if st.session_state.num1 < st.session_state.num2:
            st.session_state.num1, st.session_state.num2 = st.session_state.num2, st.session_state.num1
    st.session_state.answer = st.session_state.num1 + st.session_state.num2 if st.session_state.op == '+' else st.session_state.num1 - st.session_state.num2
    st.session_state.feedback = ""

# 显示题目
st.markdown(f'<p class="big-font">{st.session_state.num1} {st.session_state.op} {st.session_state.num2} = ?</p>', unsafe_allow_html=True)

# 生成 4 个备选答案按钮
cols = st.columns(2)
# 生成干扰项
options = list(set([st.session_state.answer, random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)]))
random.shuffle(options)

for i, opt in enumerate(options):
    with cols[i % 2]:
        if st.button(str(opt)):
            if opt == st.session_state.answer:
                st.session_state.feedback = "correct"
            else:
                st.session_state.feedback = "wrong"

# 显示反馈 Emoji
if st.session_state.feedback == "correct":
    st.markdown("<h1 style='text-align: center;'>🎉 ✨ 🍬</h1>", unsafe_allow_html=True)
    st.balloons()
    if st.button("再来一题！"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

elif st.session_state.feedback == "wrong":
    st.markdown("<h1 style='text-align: center;'>🐥 ❓ 🌈</h1>", unsafe_allow_html=True)
    st.write("<center>没关系，再试一次吧！</center>", unsafe_allow_html=True)