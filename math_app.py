import streamlit as st
import random
import time

# --- 1. 样式与美化：适配 iPhone 15/S25 的 Apple 风格 ---
st.markdown("""
<style>
/* 背景色：奶黄色 */
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #FFFBE6 !important;
}

/* 顶部成绩单 */
.score-board {
    background-color: white;
    border-radius: 20px;
    padding: 10px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    border: 3px solid #A3D9A5;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.score-box { text-align: center; }
.score-label { font-size: 14px; color: #888; }
.score-num { font-size: 24px; font-weight: bold; color: #FF6F61; }

/* 题目卡片：加厚黄色边框 */
.question-container {
    background: white;
    border: 8px solid #FFB800;
    border-radius: 40px;
    padding: 40px 15px;
    text-align: center;
    margin: 15px auto;
    max-width: 350px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}
.mode-title { font-size: 20px; font-weight: bold; color: #444; margin-bottom: 10px; }
.huge-text { font-size: 65px !important; font-weight: 900; color: #333; margin: 10px 0; letter-spacing: 5px; }

/* 选项按钮：粉红色 */
div[data-testid="stHorizontalBlock"] {
    max-width: 350px;
    margin: 0 auto;
}
.stButton > button {
    background-color: #FF85A1 !important;
    color: white !important;
    border-radius: 15px !important;
    height: 70px !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border: none !important;
    box-shadow: 0 5px 0 #FF477E !important;
    margin-bottom: 12px !important;
}
.stButton > button:active {
    box-shadow: none !important;
    transform: translateY(5px) !important;
}

/* 搞怪表情 */
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    20% { transform: translate(-3px, 0px) rotate(-1deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}
.funny-error { font-size: 100px; text-align: center; animation: shake 0.5s infinite; margin-top: 20px;}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. 500个成语大词库 ---
IDIOM_DB = [
    "自强不息", "坚持不懈", "全力以赴", "一心一意", "五彩缤纷", "半途而废", "大公无私", "画龙点睛", "名落孙山", "胸有成竹",
    "一见如故", "井底之蛙", "拔苗助长", "狐假虎威", "亡羊补牢", "守株待兔", "惊弓之鸟", "画蛇添足", "对牛弹琴", "盲人摸象",
    "杯弓蛇影", "如鱼得水", "龙飞凤舞", "鸟语花香", "千山万水", "千军万马", "四海为家", "五湖四海", "六神无主", "七手八脚",
    "八仙过海", "九牛一毛", "十全十美", "百花齐放", "万马奔腾", "一马当先", "两全其美", "三心二意", "四分五裂", "五谷丰登",
    "六畜兴旺", "七上八下", "八面玲珑", "九死一生", "十指连心", "百发百中", "千变万化", "万众一心", "一日千里", "一表人才",
    "一帆风顺", "一举两得", "一贫如洗", "一事无成", "一意孤行", "一针见血", "一望无际", "一目了然", "一见钟情", "一言为定",
    "二话不说", "三长两短", "三顾茅庐", "三生有幸", "三言两语", "四通八达", "四平八稳", "五大三粗", "五光十色", "五颜六色",
    "六亲不认", "七零八落", "七嘴八舌", "八面威风", "九九归一", "九霄云外", "十拿九稳", "百感交集", "百依百顺", "千辛万苦",
    "千载难逢", "万无一失", "万紫千红", "风和日丽", "风平浪静", "风起云涌", "风调雨顺", "雨过天晴", "大雨滂沱", "电闪雷鸣",
    "春暖花开", "夏日炎炎", "秋高气爽", "冬日里的", "冰天雪地", "山清水秀", "湖光山色", "名山大川", "气势磅礴", "波澜壮阔",
    "欢天喜地", "眉开眼笑", "大喜过望", "兴高采烈", "手舞足蹈", "怒气冲冲", "火冒三丈", "垂头丧气", "愁眉苦脸", "胆战心惊",
    "心惊肉跳", "废寝忘食", "孜孜不倦", "闻鸡起舞", "悬梁刺股", "凿壁偷光", "博学多才", "见多识广", "才华横溢", "学富五车",
    "金榜题名", "旗开得胜", "马到成功", "功成名就", "一鸣惊人", "脱颖而出", "大智若愚", "助人为乐", "舍己为人", "两袖清风",
    "拾金不昧", "尊老爱幼", "尊师重道", "言行一致", "表里如一", "光明磊落", "诚实守信", "坚持不懈", "持之以恒", "锲而不舍",
    "不屈不挠", "坚韧不拔", "自强不息", "奋发图强", "精益求精", "全神贯注", "聚精会神", "专心致志", "一丝不苟", "兢兢业业",
    "任劳任怨", "艰苦奋斗", "克勤克俭", "光明正大", "正大光明", "浩然正气", "舍生取义", "视死如归", "义无反顾", "前赴后继",
    "赴汤蹈火", "冲锋陷阵", "披荆斩棘", "乘风破浪", "一往无前", "勇往直前", "所向披靡", "势如破竹", "万众一心", "众志成城",
    "同舟共济", "患难与共", "风雨同舟", "志同道合", "同甘共苦", "团结友爱", "互助互利", "精诚团结", "齐心协力", "群策群力",
    "集思广益", "众目睽睽", "人山人海", "万人空巷", "座无虚席", "摩肩接踵", "熙熙攘攘", "车水马龙", "热闹非凡", "繁荣昌盛",
    "欣欣向荣", "蒸蒸日上", "日新月异", "翻天覆地", "沧海桑田", "白驹过隙", "光阴似箭", "岁月如流", "斗转星移", "千变万化",
    "瞬息万变", "变化莫测", "捉摸不透", "出神入化", "巧夺天工", "鬼斧神工", "琳琅满目", "目不暇接", "美不胜收", "赏心悦目",
    "心旷神怡", "悠然自得", "自由自在", "无忧无虑", "天真烂漫", "活泼可爱", "聪明伶俐", "伶牙俐齿", "口若悬河", "滔滔不绝",
    "侃侃而谈", "出口成章", "妙笔生花", "文思敏捷", "博览群书", "见识广博", "学识渊博", "才气过人", "德才兼备", "名扬天下",
    "举世闻名", "家喻户晓", "众所周知", "声名显赫", "如雷贯耳", "名副其实", "实至名归", "名不虚传", "名副其实", "大名鼎鼎",
    "赫赫有名", "不可一世", "自以为是", "骄傲自满", "狂妄自大", "目中无人", "趾高气扬", "得意忘形", "得意洋洋", "沾沾自喜",
    "自鸣得意", "摇头摆尾", "大摇大摆", "昂首挺胸", "神气十足", "气宇轩昂", "威风凛凛", "雄心壮志", "雄心勃勃", "壮志凌云",
    "豪情壮志", "志向远大", "抱负不凡", "志气不凡", "不甘落后", "力争上游", "奋起直追", "突飞猛进", "青出于蓝", "后生可畏",
    "后来居上", "大器晚成", "少年老成", "老当益壮", "老骥伏枥", "生龙活虎", "龙精虎猛", "精气神十足", "精神焕发", "容光焕发",
    "神采奕奕", "神采飞扬", "喜笑颜开", "喜出望外", "喜从天降", "欢呼雀跃", "欢聚一堂", "阖家欢乐", "团团圆圆", "幸福美满",
    "吉祥如意", "万事大吉", "心想事成", "平平安安", "健康长寿", "延年益寿", "长命百岁", "岁岁平安", "年年有余", "五谷丰登",
    "六畜兴旺", "风调雨顺", "国泰民安", "繁荣富强", "太平盛世", "锦绣河山", "壮丽多姿", "风景如画", "美轮美奂", "金碧辉煌",
    "富丽堂皇", "古色古香", "别具一格", "独具匠心", "独树一帜", "匠心独运", "巧立名目", "别出心裁", "推陈出新", "革故鼎新",
    "自力更生", "艰苦创业", "白手起家", "奋发有为", "大显身手", "大展宏图", "大有作为", "前途无量", "前程似锦", "鹏程万里",
    "平步青云", "步步高升", "官运亨通", "财源滚滚", "生意兴隆", "开张大吉", "马到成功", "旗开得胜", "凯旋而归", "得胜回朝",
    "满载而归", "不虚此行", "获益匪浅", "受益良多", "铭记在心", "永志不忘", "感人至深", "动人心弦", "扣人心弦", "引人入胜",
    "引人注目", "惹人喜爱", "爱不释手", "如获至宝", "视如珍宝", "掌上明珠", "心头肉", "命根子", "患难夫妻", "青梅竹马",
    "两小无猜", "情深意重", "情深似海", "深情厚谊", "手足之情", "血浓于水", "同胞兄弟", "形影不离", "亲密无间", "推心置腹",
    "肝胆相照", "情同手足", "志趣相投", "臭味相投", "一拍即合", "一见倾心", "心有灵犀", "心心相印", "志同道合", "同仇敌忾",
    "众志成城", "团结协作", "分工合作", "密切配合", "通力合作", "齐心合力", "并肩作战", "休戚相关", "休戚与共", "生死与共",
    "肝脑涂地", "赴汤蹈火", "出生入死", "舍生忘死", "前仆后继", "视死如归", "大义凛然", "慷慨就义", "英勇牺牲", "永垂不朽",
    "名垂青史", "流芳百世", "流芳千古", "万古长存", "历久弥新", "经久不衰", "长盛不衰", "延绵不断", "源远流长", "博大精深",
    "深奥莫测", "妙趣横生", "趣味无穷", "耐人寻味", "意味深长", "话里有话", "言外之意", "弦外之音", "意犹未尽", "回味无穷",
    "爱屋及乌", "半信半疑", "变幻莫测", "别有洞天", "不耻下问", "不可思议", "不劳而获", "不约而同", "沧海一粟", "草木皆兵",
    "朝气蓬勃", "唇亡齿寒", "粗制滥造", "得意忘形", "东山再起", "对症下药", "耳濡目染", "反其道而行", "防微杜渐", "负荆请罪",
    "隔岸观火", "各有千秋", "孤注一掷", "归心似箭", "各抒己见", "和蔼可亲", "后继有人", "呼风唤雨", "画地为牢", "挥金如土",
    "豁然开朗", "鸡犬不宁", "急功近利", "家常便饭", "见义勇为", "娇生惯养", "津津有味", "井井有条", "斤斤计较", "精打细算",
    "开门见山", "看风使舵", "空前绝后", "苦心经营", "老少皆宜", "理直气壮", "力不从心", "两全其美", "流离失所", "炉火纯青",
    "路不拾遗", "落花流水", "满载而归", "慢条斯理", "毛遂自荐", "门庭若市", "面目一新", "明目张胆", "目光如炬", "南辕北辙",
    "宁死不屈", "抛砖引玉", "平易近人", "迫不及待", "齐头并进", "杞人忧天", "前所未有", "轻而易举", "情不自禁", "全力以赴",
    "全力支持", "全神贯注", "拳不离手", "惹是生非", "人云亦云", "忍俊不禁", "如愿以求", "三思而后行", "杀鸡儆猴", "深谋远虑",
    "神机妙算", "事半功倍", "事与愿违", "守口如瓶", "水到渠成", "水涨船高", "四面楚歌", "肆无忌惮", "随波逐流", "随心所欲",
    "谈笑风生", "叹为观止", "提心胆战", "天经地义", "天衣无缝", "挑拨离间", "挺身而出", "同心协力", "推陈出新", "脱口而出",
    "微不足道", "危言耸听", "唯利是图", "温故知新", "无微不至", "无懈可击", "洗心革面", "鲜为人知", "相提并论", "小心翼翼",
    "心悦诚服", "欣欣向荣", "新陈代谢", "兴致勃勃", "胸怀大志", "袖手旁观", "悬崖勒马", "循序渐进", "鸦雀无声", "言简意赅",
    "奄奄一息", "眼见为实", "扬长避短", "摇摇欲坠", "一败涂地", "一尘不染", "一鼓作气", "一劳永逸", "一鸣惊人",
    "一目十行", "一窍不通", "一如既往", "一丝不苟", "一塌糊涂", "一针见血", "怡然自得", "义不容辞", "异口同声",
    "因材施教", "饮水思源", "迎刃而解", "勇往直前", "优胜劣汰", "由浅入深", "与众不同", "再接再厉", "斩钉截铁", "朝气蓬勃",
    "争先恐后", "知难而退", "纸上谈兵", "志在四方", "众目睽睽", "助人为乐", "自给自足", "自取灭亡", "自私自利", "自相矛盾"
]

# --- 3. 游戏核心逻辑 ---

if 'score' not in st.session_state: st.session_state.score = 0
if 'high_score' not in st.session_state: st.session_state.high_score = 0

def generate_question():
    st.session_state.show_error = False
    st.session_state.answered = False
    
    # 随机选成语
    idiom = random.choice(IDIOM_DB)
    # 随机选一个位置挖空
    blank_idx = random.randint(0, 3)
    answer = idiom[blank_idx]
    
    # 题目文本
    display_text = list(idiom)
    display_text[blank_idx] = "_"
    st.session_state.current_idiom = "".join(display_text)
    st.session_state.answer = answer
    
    # 生成选项
    all_chars = "".join(IDIOM_DB)
    options = {answer}
    while len(options) < 4:
        rand_char = random.choice(all_chars)
        if rand_char != answer:
            options.add(rand_char)
    
    opt_list = list(options)
    random.shuffle(opt_list)
    st.session_state.options = opt_list

# 初始化题目
if 'current_idiom' not in st.session_state:
    generate_question()

# --- 4. 界面绘制 ---

# 成绩单
st.markdown(f'''
<div class="score-board">
    <div class="score-box">
        <div class="score-label">⭐ 连对分数</div>
        <div class="score-num">{st.session_state.score}</div>
    </div>
    <div style="width: 2px; height: 30px; background-color: #EEE;"></div>
    <div class="score-box">
        <div class="score-label">🏆 最高纪录</div>
        <div class="score-num">{st.session_state.high_score}</div>
    </div>
</div>
''', unsafe_allow_html=True)

# 搞怪表情
if st.session_state.get('show_error'):
    st.markdown(f'<p class="funny-error">{random.choice(["🤪", "👻", "🙊", "👽", "💩"])}</p>', unsafe_allow_html=True)

# 题目区域
st.markdown(f'''
<div class="question-container">
    <div class="mode-title">✨ 成语填空挑战 ✨</div>
    <div class="huge-text">{st.session_state.current_idiom}</div>
    <div style="color:#AAA; font-size:14px; margin-top:10px;">请选出正确的字补全成语</div>
</div>
''', unsafe_allow_html=True)

# 按钮区域
col1, col2 = st.columns(2)
for i, opt in enumerate(st.session_state.options):
    target_col = col1 if i < 2 else col2
    if target_col.button(opt, key=f"btn_{i}", use_container_width=True):
        if opt == st.session_state.answer:
            # 答对了
            st.session_state.score += 1
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
            st.balloons()
            time.sleep(1.2)
            generate_question()
            st.rerun()
        else:
            # 答错了
            st.session_state.score = 0
            st.session_state.show_error = True
            st.rerun()

# 侧边栏重置
if st.sidebar.button("🏆 清空最高纪录"):
    st.session_state.high_score = 0
    st.rerun()
