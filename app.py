from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# 主页面HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>会议信息</title>
    <style>
        :root {
            --primary-red: #C41E3A;
            --dark-red: #8B0000;
            --light-red: #FFE9EC;
            --white: #FFFFFF;
            --off-white: #FFF5F5;
            --text-dark: #2C2C2C;
            --text-gray: #666666;
            --shadow: 0 4px 20px rgba(196, 30, 58, 0.12);
            --shadow-hover: 0 8px 32px rgba(196, 30, 58, 0.22);
            --border-light: #F5D5DB;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
            background: linear-gradient(180deg, #FFF5F5 0%, #FFFFFF 30%, #FFFFFF 100%);
            min-height: 100vh;
            -webkit-tap-highlight-color: transparent;
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
        }

        /* 顶部红色装饰条 */
        .top-accent {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--dark-red), var(--primary-red), #E8485E, var(--primary-red), var(--dark-red));
            z-index: 1000;
            animation: shimmer 3s ease-in-out infinite;
        }

        @keyframes shimmer {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .page-container {
            max-width: 520px;
            margin: 0 auto;
            padding: 0 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* 头部区域 */
        .header {
            text-align: center;
            padding: 40px 0 8px 0;
            position: relative;
        }

        .header-badge {
            display: inline-block;
            background: var(--primary-red);
            color: var(--white);
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 3px;
            padding: 6px 18px;
            border-radius: 20px;
            margin-bottom: 16px;
            text-transform: uppercase;
        }

        .header-title {
            font-size: 28px;
            font-weight: 700;
            color: var(--text-dark);
            letter-spacing: 1px;
            margin-bottom: 6px;
        }

        .header-title .highlight {
            color: var(--primary-red);
            position: relative;
        }

        .header-subtitle {
            font-size: 14px;
            color: var(--text-gray);
            letter-spacing: 2px;
            font-weight: 400;
        }

        /* 红色分隔装饰 */
        .divider-ornament {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin: 10px 0;
        }

        .divider-ornament .line {
            width: 35px;
            height: 1.5px;
            background: var(--primary-red);
            opacity: 0.5;
            border-radius: 1px;
        }

        .divider-ornament .dot {
            width: 7px;
            height: 7px;
            background: var(--primary-red);
            border-radius: 50%;
        }

        /* 卡片区域 */
        .cards-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 20px;
            padding: 20px 0;
        }

        .option-card {
            position: relative;
            background: var(--white);
            border-radius: 20px;
            padding: 28px 24px;
            cursor: pointer;
            transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: var(--shadow);
            border: 1.5px solid transparent;
            overflow: hidden;
            user-select: none;
            -webkit-user-select: none;
            -webkit-tap-highlight-color: transparent;
        }

        .option-card:active {
            transform: scale(0.97);
            transition: transform 0.15s ease;
        }

        .option-card:hover {
            box-shadow: var(--shadow-hover);
            border-color: var(--border-light);
            transform: translateY(-2px);
        }

        /* 卡片左侧红色竖条 */
        .option-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 20%;
            bottom: 20%;
            width: 4px;
            background: var(--primary-red);
            border-radius: 0 3px 3px 0;
            transition: all 0.35s ease;
        }

        .option-card:hover::before {
            top: 12%;
            bottom: 12%;
            width: 5px;
        }

        /* 卡片右上角装饰 */
        .card-decoration {
            position: absolute;
            top: -30px;
            right: -30px;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: var(--light-red);
            opacity: 0.5;
            transition: all 0.4s ease;
            pointer-events: none;
        }

        .option-card:hover .card-decoration {
            transform: scale(1.3);
            opacity: 0.7;
        }

        .card-content {
            position: relative;
            z-index: 1;
        }

        .card-icon-wrapper {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 52px;
            height: 52px;
            background: linear-gradient(135deg, var(--light-red), #FFF0F2);
            border-radius: 14px;
            margin-bottom: 16px;
            transition: all 0.3s ease;
        }

        .option-card:hover .card-icon-wrapper {
            background: linear-gradient(135deg, #FFD4DC, var(--light-red));
        }

        .card-icon {
            font-size: 26px;
        }

        .card-label {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }

        .card-desc {
            font-size: 13px;
            color: var(--text-gray);
            line-height: 1.5;
            letter-spacing: 0.3px;
        }

        .card-arrow {
            position: absolute;
            right: 20px;
            bottom: 28px;
            width: 36px;
            height: 36px;
            background: var(--primary-red);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            z-index: 1;
        }

        .option-card:hover .card-arrow {
            transform: translateX(4px);
            background: var(--dark-red);
        }

        .card-arrow svg {
            width: 16px;
            height: 16px;
            fill: white;
        }

        /* 弹窗/详情面板 */
        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.55);
            z-index: 2000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.35s ease;
            display: flex;
            align-items: flex-end;
            justify-content: center;
        }

        .overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .detail-panel {
            background: var(--white);
            width: 100%;
            max-width: 520px;
            max-height: 85vh;
            border-radius: 24px 24px 0 0;
            overflow-y: auto;
            transform: translateY(100%);
            transition: transform 0.4s cubic-bezier(0.32, 0.72, 0, 1);
            position: relative;
            box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.2);
        }

        .overlay.active .detail-panel {
            transform: translateY(0);
        }

        .panel-handle {
            width: 40px;
            height: 4px;
            background: #DDD;
            border-radius: 2px;
            margin: 12px auto 0;
        }

        .panel-header {
            position: sticky;
            top: 0;
            background: var(--white);
            padding: 16px 24px;
            border-bottom: 1px solid #F0F0F0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 10;
            border-radius: 24px 24px 0 0;
        }

        .panel-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-dark);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .panel-title-dot {
            width: 8px;
            height: 8px;
            background: var(--primary-red);
            border-radius: 50%;
            flex-shrink: 0;
        }

        .panel-close {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #F5F5F5;
            border: none;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            color: #666;
            flex-shrink: 0;
        }

        .panel-close:active {
            background: #E8E8E8;
            transform: scale(0.93);
        }

        .panel-body {
            padding: 20px 24px 40px;
        }

        /* 会务手册内容样式 */
        .manual-section {
            margin-bottom: 24px;
        }

        .manual-section:last-child {
            margin-bottom: 0;
        }

        .section-title-bar {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }

        .section-icon-tag {
            width: 32px;
            height: 32px;
            background: var(--primary-red);
            color: var(--white);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
            font-weight: 700;
            flex-shrink: 0;
        }

        .section-title-text {
            font-size: 16px;
            font-weight: 700;
            color: var(--text-dark);
            letter-spacing: 0.5px;
        }

        .info-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 10px 0;
            border-bottom: 1px solid #FFF0F2;
            font-size: 14px;
            color: #444;
            line-height: 1.6;
        }

        .info-item:last-child {
            border-bottom: none;
        }

        .info-label-tag {
            background: var(--light-red);
            color: var(--primary-red);
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            white-space: nowrap;
            flex-shrink: 0;
            margin-top: 2px;
        }

        /* 研学安排 - 时间线样式 */
        .timeline-item {
            position: relative;
            padding-left: 28px;
            padding-bottom: 24px;
            border-left: 2px solid #FFD4DC;
            margin-left: 8px;
        }

        .timeline-item:last-child {
            border-left-color: transparent;
            padding-bottom: 0;
        }

        .timeline-dot {
            position: absolute;
            left: -8px;
            top: 2px;
            width: 14px;
            height: 14px;
            background: var(--primary-red);
            border-radius: 50%;
            border: 3px solid var(--white);
            box-shadow: 0 0 0 3px #FFD4DC;
        }

        .timeline-time {
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-red);
            letter-spacing: 1px;
            margin-bottom: 4px;
        }

        .timeline-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-dark);
            margin-bottom: 4px;
        }

        .timeline-desc {
            font-size: 13px;
            color: var(--text-gray);
            line-height: 1.5;
        }

        .timeline-location {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 12px;
            color: #999;
            margin-top: 4px;
        }

        /* 底部 */
        .footer {
            text-align: center;
            padding: 16px 0 30px;
            font-size: 12px;
            color: #CCC;
            letter-spacing: 1px;
        }

        /* 点击波纹效果 */
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(196, 30, 58, 0.15);
            transform: scale(0);
            animation: ripple-anim 0.6s ease-out;
            pointer-events: none;
        }

        @keyframes ripple-anim {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }

        /* 滚动条美化 */
        .detail-panel::-webkit-scrollbar {
            width: 4px;
        }
        .detail-panel::-webkit-scrollbar-track {
            background: transparent;
        }
        .detail-panel::-webkit-scrollbar-thumb {
            background: #DDD;
            border-radius: 2px;
        }

        /* 响应式 */
        @media (max-width: 380px) {
            .header-title {
                font-size: 24px;
            }
            .option-card {
                padding: 22px 18px;
            }
            .card-label {
                font-size: 18px;
            }
            .card-arrow {
                right: 14px;
                bottom: 22px;
                width: 30px;
                height: 30px;
            }
        }
    </style>
</head>
<body>
    <!-- 顶部红色装饰条 -->
    <div class="top-accent"></div>

    <div class="page-container">
        <!-- 头部 -->
        <div class="header">
            <div class="header-badge">CONFERENCE</div>
            <h1 class="header-title">
                西藏民族大学<span class="highlight">研究生会</span>
            </h1>
            <p class="header-subtitle">请选择您要查看的内容</p>
            <div class="divider-ornament">
                <span class="line"></span>
                <span class="dot"></span>
                <span class="line"></span>
            </div>
        </div>

        <!-- 两个选项卡片 -->
        <div class="cards-section">
            <!-- 会务手册卡片 -->
            <div class="option-card" id="cardManual" onclick="openDetail('manual')">
                <div class="card-decoration"></div>
                <div class="card-content">
                    <div class="card-icon-wrapper">
                        <span class="card-icon">📋</span>
                    </div>
                    <div class="card-label">会务手册</div>
                    <div class="card-desc">查看会议日程、场地信息、参会须知等详细信息</div>
                </div>
                <div class="card-arrow">
                    <svg viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg>
                </div>
            </div>

            <!-- 研学安排卡片 -->
            <div class="option-card" id="cardStudy" onclick="openDetail('study')">
                <div class="card-decoration"></div>
                <div class="card-content">
                    <div class="card-icon-wrapper">
                        <span class="card-icon">🎓</span>
                    </div>
                    <div class="card-label">研学安排</div>
                    <div class="card-desc">查看研学行程、活动内容、时间安排等详细计划</div>
                </div>
                <div class="card-arrow">
                    <svg viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg>
                </div>
            </div>
        </div>

        <!-- 底部 -->
        <div class="footer">
            <p>如有疑问请联系会务组</p>
        </div>
    </div>

    <!-- 详情弹窗 -->
    <div class="overlay" id="overlay" onclick="closeDetail(event)">
        <div class="detail-panel" id="detailPanel" onclick="event.stopPropagation()">
            <div class="panel-handle"></div>
            <div class="panel-header">
                <div class="panel-title">
                    <span class="panel-title-dot"></span>
                    <span id="panelTitle">会务手册</span>
                </div>
                <button class="panel-close" onclick="closeDetailDirect()">✕</button>
            </div>
            <div class="panel-body" id="panelBody">
                <!-- 动态填充 -->
            </div>
        </div>
    </div>

    <script>
        // 会务手册数据
        const manualData = {
            title: '会务手册',
            sections: [
                {
                    icon: '📅',
                    title: '会议日程',
                    items: [
                        { label: '日期', value: '2026年5月15日 - 5月17日' },
                        { label: '报到时间', value: '5月15日 09:00 - 18:00' },
                        { label: '开幕式', value: '5月16日 09:00 - 10:30' },
                        { label: '主题报告', value: '5月16日 10:45 - 17:00' },
                        { label: '闭幕总结', value: '5月17日 14:00 - 16:00' },
                    ]
                },
                {
                    icon: '📍',
                    title: '场地信息',
                    items: [
                        { label: '主会场', value: '国际会议中心 · 三层大宴会厅' },
                        { label: '分会场A', value: '国际会议中心 · 二层201会议室' },
                        { label: '分会场B', value: '国际会议中心 · 二层202会议室' },
                        { label: '用餐地点', value: '国际会议中心 · 一层自助餐厅' },
                    ]
                },
                {
                    icon: '📝',
                    title: '参会须知',
                    items: [
                        { label: '签到', value: '请携带身份证件及参会凭证签到入场' },
                        { label: '着装', value: '建议商务休闲着装，开幕式请着正装' },
                        { label: '网络', value: '会场提供免费Wi-Fi，账号及密码见胸牌' },
                        { label: '停车', value: '凭参会证可免费停车于B2层嘉宾停车区' },
                    ]
                },
                {
                    icon: '📞',
                    title: '联系方式',
                    items: [
                        { label: '会务组', value: '138-0000-1234 / conf@example.com' },
                        { label: '酒店前台', value: '010-8888-6666（24小时）' },
                        { label: '紧急联络', value: '139-0000-5678（王秘书）' },
                    ]
                },
            ]
        };

        // 研学安排数据
        const studyData = {
            title: '研学安排',
            timeline: [
                {
                    time: '5月15日 · 下午',
                    title: '抵达与入住',
                    desc: '抵达会议酒店，办理入住手续，领取研学资料包及分组手环。',
                    location: '国际会议中心 · 大堂'
                },
                {
                    time: '5月16日 · 上午',
                    title: '开幕式 & 主旨演讲',
                    desc: '参加大会开幕式，聆听行业专家主旨演讲，了解最新发展趋势与前沿动态。',
                    location: '三层大宴会厅'
                },
                {
                    time: '5月16日 · 下午',
                    title: '分组研讨 WorkShop',
                    desc: '按研究方向分组进行深度研讨，每组配备导师引导，产出研讨纪要。',
                    location: '二层会议室'
                },
                {
                    time: '5月17日 · 上午',
                    title: '实地考察参访',
                    desc: '前往本地标杆企业/机构进行实地考察，与一线从业者交流实践经验。',
                    location: '统一乘车前往（详见分组通知）'
                },
                {
                    time: '5月17日 · 下午',
                    title: '成果汇报 & 闭幕',
                    desc: '各组汇报研学成果，颁发研学证书，合影留念，会议闭幕。',
                    location: '三层大宴会厅'
                },
            ]
        };

        function openDetail(type) {
            const overlay = document.getElementById('overlay');
            const panelTitle = document.getElementById('panelTitle');
            const panelBody = document.getElementById('panelBody');

            if (type === 'manual') {
                panelTitle.textContent = manualData.title;
                panelBody.innerHTML = renderManualContent();
            } else if (type === 'study') {
                panelTitle.textContent = studyData.title;
                panelBody.innerHTML = renderStudyContent();
            }

            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function renderManualContent() {
            let html = '';
            manualData.sections.forEach(section => {
                html += `
                    <div class="manual-section">
                        <div class="section-title-bar">
                            <div class="section-icon-tag">${section.icon}</div>
                            <div class="section-title-text">${section.title}</div>
                        </div>
                `;
                section.items.forEach(item => {
                    html += `
                        <div class="info-item">
                            <span class="info-label-tag">${item.label}</span>
                            <span>${item.value}</span>
                        </div>
                    `;
                });
                html += '</div>';
            });
            return html;
        }

        function renderStudyContent() {
            let html = '';
            studyData.timeline.forEach((item, index) => {
                html += `
                    <div class="timeline-item">
                        <div class="timeline-dot"></div>
                        <div class="timeline-time">${item.time}</div>
                        <div class="timeline-title">${item.title}</div>
                        <div class="timeline-desc">${item.desc}</div>
                        <div class="timeline-location">
                            <span>📍</span> ${item.location}
                        </div>
                    </div>
                `;
            });
            return html;
        }

        function closeDetail(e) {
            if (e.target === document.getElementById('overlay')) {
                closeDetailDirect();
            }
        }

        function closeDetailDirect() {
            const overlay = document.getElementById('overlay');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        // 点击卡片波纹效果
        document.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
                ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
                this.appendChild(ripple);
                ripple.addEventListener('animationend', () => ripple.remove());
            });
        });

        // 触摸滑动关闭弹窗（简单实现）
        let touchStartY = 0;
        const detailPanel = document.getElementById('detailPanel');
        detailPanel.addEventListener('touchstart', function(e) {
            if (this.scrollTop <= 0) {
                touchStartY = e.touches[0].clientY;
            }
        });
        detailPanel.addEventListener('touchmove', function(e) {
            if (this.scrollTop <= 0 && e.touches[0].clientY - touchStartY > 60) {
                closeDetailDirect();
            }
        });
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    """主页面"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/manual')
def api_manual():
    """会务手册API（可选）"""
    data = {
        'title': '会务手册',
        'sections': [
            {
                'icon': '📅',
                'title': '会议日程',
                'items': [
                    {'label': '日期', 'value': '2026年5月15日 - 5月17日'},
                    {'label': '报到时间', 'value': '5月15日 09:00 - 18:00'},
                    {'label': '开幕式', 'value': '5月16日 09:00 - 10:30'},
                    {'label': '主题报告', 'value': '5月16日 10:45 - 17:00'},
                    {'label': '闭幕总结', 'value': '5月17日 14:00 - 16:00'},
                ]
            },
            {
                'icon': '📍',
                'title': '场地信息',
                'items': [
                    {'label': '主会场', 'value': '国际会议中心 · 三层大宴会厅'},
                    {'label': '分会场A', 'value': '国际会议中心 · 二层201会议室'},
                    {'label': '分会场B', 'value': '国际会议中心 · 二层202会议室'},
                    {'label': '用餐地点', 'value': '国际会议中心 · 一层自助餐厅'},
                ]
            }
        ]
    }
    return jsonify(data)


@app.route('/api/study')
def api_study():
    """研学安排API（可选）"""
    data = {
        'title': '研学安排',
        'timeline': [
            {'time': '5月15日 下午', 'title': '抵达与入住', 'desc': '抵达酒店，办理入住，领取资料包'},
            {'time': '5月16日 上午', 'title': '开幕式', 'desc': '参加开幕式及主旨演讲'},
            {'time': '5月16日 下午', 'title': '分组研讨', 'desc': '分组深度研讨与交流'},
            {'time': '5月17日 上午', 'title': '实地考察', 'desc': '标杆企业/机构参访'},
            {'time': '5月17日 下午', 'title': '成果汇报', 'desc': '汇报成果，颁发证书'},
        ]
    }
    return jsonify(data)


if __name__ == '__main__':
    # 获取端口，默认使用5000
    port = int(os.environ.get('PORT', 5000))
    print('=' * 50)
    print('  🎉  会议信息H5页面已启动')
    print(f'  📱  请在浏览器中打开: http://127.0.0.1:{port}')
    print(f'  🌐  局域网访问: http://0.0.0.0:{port}')
    print('  📋  按 Ctrl+C 停止服务')
    print('=' * 50)
    app.run(host='0.0.0.0', port=port, debug=True)