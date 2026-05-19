from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>大骨班培训手册</title>
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
            overflow-x: hidden;
        }
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
        .header {
            text-align: center;
            padding: 40px 0 8px 0;
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
            font-size: 26px;
            font-weight: 700;
            color: var(--text-dark);
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        .header-title .highlight {
            color: var(--primary-red);
        }
        .header-subtitle {
            font-size: 14px;
            color: var(--text-gray);
            letter-spacing: 2px;
        }
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
        }
        .option-card:active {
            transform: scale(0.97);
        }
        .option-card:hover {
            box-shadow: var(--shadow-hover);
            border-color: var(--border-light);
            transform: translateY(-2px);
        }
        .option-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 20%;
            bottom: 20%;
            width: 4px;
            background: var(--primary-red);
            border-radius: 0 3px 3px 0;
        }
        .card-decoration {
            position: absolute;
            top: -30px;
            right: -30px;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: var(--light-red);
            opacity: 0.5;
            pointer-events: none;
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
        }
        .card-icon {
            font-size: 26px;
        }
        .card-label {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 6px;
        }
        .card-desc {
            font-size: 13px;
            color: var(--text-gray);
            line-height: 1.5;
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
        }
        .card-arrow svg {
            width: 16px;
            height: 16px;
            fill: white;
        }
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
            justify-content: center;
        }
        .overlay.bottom {
            align-items: flex-end;
        }
        .overlay.center {
            align-items: center;
        }
        .overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
        .detail-panel {
            background: var(--white);
            width: 100%;
            max-width: 520px;
            transition: transform 0.4s cubic-bezier(0.32, 0.72, 0, 1);
            position: relative;
            box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.2);
        }
        .overlay.bottom .detail-panel {
            border-radius: 24px 24px 0 0;
            transform: translateY(100%);
            max-height: 85vh;
            overflow-y: auto;
        }
        .overlay.bottom.active .detail-panel {
            transform: translateY(0);
        }
        .overlay.center .detail-panel {
            border-radius: 24px;
            transform: scale(0.9);
            opacity: 0;
            max-width: 90vw;
            width: auto;
            min-width: 280px;
            max-height: 85vh;
            overflow-y: auto;
            transition: transform 0.25s ease, opacity 0.25s ease;
        }
        .overlay.center.active .detail-panel {
            transform: scale(1);
            opacity: 1;
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
        }
        .overlay.bottom .panel-header {
            border-radius: 24px 24px 0 0;
        }
        .overlay.center .panel-header {
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
            color: #666;
        }
        .panel-close:active {
            background: #E8E8E8;
            transform: scale(0.93);
        }
        .panel-body {
            padding: 20px 24px 40px;
        }
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
        }
        .section-title-text {
            font-size: 16px;
            font-weight: 700;
            color: var(--text-dark);
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
        .table-container {
            overflow-x: auto;
            margin: 12px 0;
            border-radius: 12px;
            border: 1px solid #FFF0F2;
            width: 100%;
        }
        .info-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 15px;
        }
        .info-table th, .info-table td {
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid #FFF0F2;
            white-space: normal;
            vertical-align: top;
        }
        .info-table th {
            background: var(--light-red);
            color: var(--primary-red);
            font-weight: 600;
            position: sticky;
            top: 0;
        }
        .info-table tbody tr:nth-child(even) {
            background-color: #FFE9EC;
        }
        .info-table tr:last-child td {
            border-bottom: none;
        }
        .footer {
            text-align: center;
            padding: 16px 0 30px;
            font-size: 12px;
            color: #CCC;
        }
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
        @media (max-width: 380px) {
            .header-title { font-size: 22px; }
            .option-card { padding: 22px 18px; }
            .card-label { font-size: 18px; }
            .card-arrow { right: 14px; bottom: 22px; width: 30px; height: 30px; }
            .info-table th, .info-table td { padding: 10px 12px; font-size: 13px; }
        }
    </style>
</head>
<body>
    <div class="top-accent"></div>
    <div class="page-container">
        <div class="header">
            <div class="header-badge">青马工程</div>
            <h1 class="header-title">
                西藏民族大学<span class="highlight">2026大骨班</span>
            </h1>
            <p class="header-subtitle">大学生骨干培训班培训手册</p>
            <div class="divider-ornament">
                <span class="line"></span>
                <span class="dot"></span>
                <span class="line"></span>
            </div>
        </div>
        <div class="cards-section">
            <div class="option-card" id="cardManual" onclick="openDetail('manual')">
                <div class="card-decoration"></div>
                <div class="card-content">
                    <div class="card-icon-wrapper"><span class="card-icon">📋</span></div>
                    <div class="card-label">培训手册</div>
                    <div class="card-desc">培养目标、培训内容、培养要求、考勤制度</div>
                </div>
                <div class="card-arrow"><svg viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg></div>
            </div>
            <div class="option-card" id="cardSchedule" onclick="openDetail('schedule')">
                <div class="card-decoration"></div>
                <div class="card-content">
                    <div class="card-icon-wrapper"><span class="card-icon">📅</span></div>
                    <div class="card-label">课程表</div>
                    <div class="card-desc">本周培训课程安排</div>
                </div>
                <div class="card-arrow"><svg viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg></div>
            </div>
            <div class="option-card" id="cardClass" onclick="openDetail('class')">
                <div class="card-decoration"></div>
                <div class="card-content">
                    <div class="card-icon-wrapper"><span class="card-icon">👥</span></div>
                    <div class="card-label">分班表</div>
                    <div class="card-desc">班级名单</div>
                </div>
                <div class="card-arrow"><svg viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg></div>
            </div>
        </div>
        <div class="footer">
            <p>共青团西藏民族大学委员会 2026年5月</p>
        </div>
    </div>

    <div class="overlay bottom" id="overlay" onclick="closeDetail(event)">
        <div class="detail-panel" id="detailPanel" onclick="event.stopPropagation()">
            <div class="panel-handle"></div>
            <div class="panel-header">
                <div class="panel-title"><span class="panel-title-dot"></span><span id="panelTitle">培训手册</span></div>
                <button class="panel-close" onclick="closeDetailDirect()">✕</button>
            </div>
            <div class="panel-body" id="panelBody"></div>
        </div>
    </div>

    <script>
        const manualData = {
            title: '培训手册',
            sections: [
                { icon: '📍', title: '基本信息', items: [{ label: '开班时间', value: '2026年5月9日' }, { label: '开班地点', value: '秦汉校区学术报告厅' }, { label: '培训时间', value: '5月9日、16日、17日、23日、30日、6月6日' }, { label: '培训形式', value: '知识培训+实践基地研学' }, { label: '学员人数', value: '共计87名' }] },
                { icon: '👤', title: '学员组成', items: [{ label: '校团委', value: '专兼职团干部' }, { label: '校级组织', value: '校学生会、研究生会、青年志愿者协会部长及以上学生干部' }, { label: '学院', value: '各学院学生分会、研究生分会主席各1名' }, { label: '社团', value: '部分校级社团社长1名' }] },
                { icon: '🎯', title: '培养目标', items: [{ label: '政治品格', value: '信念坚定，拥护党的领导' }, { label: '家国情怀', value: '扎根西藏，服务边疆建设' }, { label: '理论素养', value: '掌握马克思主义中国化最新成果' }, { label: '综合能力', value: '具备组织协调、服务基层的实践本领' }] },
                { icon: '📚', title: '培训内容', items: [{ label: '理论学习', value: '时政政策解读、藏传佛教实践、党的青年工作' }, { label: '能力培养', value: '公文写作、社区服务策划、田野调查' }, { label: '专题研学', value: '延安革命纪念馆、杨家岭、枣园、梁家河村史馆' }] },
                { icon: '⚠️', title: '培训要求', items: [{ label: '组织要求', value: '各单位做好学员遴选和监督工作' }, { label: '学员要求', value: '不迟到早退，不无故请假缺席' }, { label: '考核要求', value: '学习实效作为评优奖励重要依据' }] },
                { icon: '✅', title: '考勤制度', items: [{ label: '签到', value: '提前15分钟签到，本人亲自签到，禁止代签' }, { label: '请假', value: '事假需学院团委公章，病假需医院证明' }, { label: '纪律', value: '关闭通讯设备，保持会场秩序' }, { label: '结业', value: '缺课两节以上不予结业，取消年度青马资格' }] }
            ]
        };
        const scheduleData = {
            title: '课程表',
            headers: ['日期', '上课时间', '课程内容', '主讲人', '主持人', '地点'],
            rows: [
                ['5.30', '08:30-10:00', '铸牢中华民族共同体意识', '达宝次仁（西藏党委党校）', '--', '学术报告厅（秦汉校区）'],
                ['5.30', '10:20-11:50', '共青团社区青少年服务策划与实施', '王渭巍（中央团校）', '--', '学术报告厅（秦汉校区）'],
                ['5.30', '14:50-16:20', '依法治理藏传佛教的实践与启示', '达宝次仁（西藏党委党校）', '--', '学术报告厅（秦汉校区）'],
                ['5.30', '16:40-18:10', '青年学生干部综合素养提升与发展规划', '马天祥', '--', '学术报告厅（秦汉校区）']
            ]
        };
        const classData = {
            title: '分班表',
            classes: [
                { name: '一班', monitor: '德吉措姆', viceMonitor: '刘倩', members: ['曹宇彤', '李芬芬', '张瀚予', '刘佳烨', '周梦雨', '益西尼玛', '刘佳雨', '珠吉江措', '李泓成', '何沁薇', '佘诗琦', '时馨怡', '白玛旺姆', '解树群', '次仁央吉', '扎西次吉', '余瑞东', '戴槟'] },
                { name: '二班', monitor: '高果露', viceMonitor: '胡小亮', members: ['李佳璇', '申畑恬', '高梓亮', '张宇航', '张海明', '郝晓华', '谭雨晨', '庞星源', '土登美久', '龙娟', '周悦颖', '谢恬', '吕豪雨', '洛松次仁', '格桑扎西', '陈贝妮', '次旺白玛', '扎西伦珠', '康嘎措姆'] },
                { name: '三班', monitor: '闹布', viceMonitor: '罗爽', members: ['达娃', '肖雅倩', '王佳卉', '常江', '王俊谚', '张雪松', '李子昂', '许妍蓓', '赵晶', '郭小凯', '谢雅欣', '李露', '朱敏', '格桑玉珍', '郭江波', '高奕博', '逯如意', '尼玛仓木拉', '杨佳晔'] },
                { name: '四班（秦汉校区）', monitor: '强巴扎西', viceMonitor: '白玛群措', members: ['平措南加', '巴桑仓决', '王恩宁', '白玛央珍', '旦增索朗', '李烁', '肖楼', '多吉占堆', '齐天宇', '周文杰', '次旺欧珠', '黄宏方', '王渤涵', '赵艺航', '赤列罗布', '王雅菲', '曹卓颖', '刘馨蓓', '席仲远', '王思晨', '旦增次央', '丹智白萨', '戴同欣'] }
            ]
        };

        const overlay = document.getElementById('overlay');
        const panelTitle = document.getElementById('panelTitle');
        const panelBody = document.getElementById('panelBody');
        const detailPanel = document.getElementById('detailPanel');

        function openDetail(type) {
            overlay.classList.remove('bottom', 'center');
            if (type === 'manual') {
                overlay.classList.add('bottom');
                panelTitle.textContent = manualData.title;
                panelBody.innerHTML = renderManualContent();
            } else if (type === 'schedule') {
                overlay.classList.add('center');
                panelTitle.textContent = scheduleData.title;
                panelBody.innerHTML = renderScheduleContent();
            } else if (type === 'class') {
                overlay.classList.add('bottom');
                panelTitle.textContent = classData.title;
                panelBody.innerHTML = renderClassContent();
            }
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function renderManualContent() {
            let html = '';
            for (let s of manualData.sections) {
                html += `<div class="manual-section"><div class="section-title-bar"><div class="section-icon-tag">${s.icon}</div><div class="section-title-text">${s.title}</div></div>`;
                for (let item of s.items) {
                    html += `<div class="info-item"><span class="info-label-tag">${item.label}</span><span>${escapeHtml(item.value)}</span></div>`;
                }
                html += `</div>`;
            }
            return html;
        }

        function renderScheduleContent() {
            let html = '<div class="table-container"><table class="info-table"><thead><tr>';
            for (let h of scheduleData.headers) html += `<th>${h}</th>`;
            html += '</tr></thead><tbody>';
            for (let row of scheduleData.rows) {
                html += '<tr>';
                for (let cell of row) {
                    let display = (cell === undefined || cell === null || cell === '') ? '--' : cell;
                    html += `<td>${escapeHtml(display)}</td>`;
                }
                html += '</tr>';
            }
            html += '</tbody></table></div>';
            return html;
        }

        function renderClassContent() {
            let html = '';
            for (let cls of classData.classes) {
                html += `<div class="manual-section"><div class="section-title-bar"><div class="section-icon-tag">👥</div><div class="section-title-text">${cls.name}</div></div>`;
                html += `<div class="info-item"><span class="info-label-tag">班长</span><span>${escapeHtml(cls.monitor)}</span></div>`;
                html += `<div class="info-item"><span class="info-label-tag">副班长</span><span>${escapeHtml(cls.viceMonitor)}</span></div>`;
                html += `<div class="info-item"><span class="info-label-tag">成员</span><span class="class-members">${escapeHtml(cls.members.join('、'))}</span></div>`;
                html += `</div>`;
            }
            return html;
        }

        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }

        function closeDetail(e) {
            if (e.target === overlay) closeDetailDirect();
        }
        function closeDetailDirect() {
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        document.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = (e.clientX - rect.left - size/2) + 'px';
                ripple.style.top = (e.clientY - rect.top - size/2) + 'px';
                this.appendChild(ripple);
                ripple.addEventListener('animationend', () => ripple.remove());
            });
        });

        let touchStartY = 0;
        detailPanel.addEventListener('touchstart', function(e) {
            if (overlay.classList.contains('bottom') && this.scrollTop <= 0) {
                touchStartY = e.touches[0].clientY;
            }
        });
        detailPanel.addEventListener('touchmove', function(e) {
            if (overlay.classList.contains('bottom') && this.scrollTop <= 0 && e.touches[0].clientY - touchStartY > 60) {
                closeDetailDirect();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/manual')
def api_manual():
    data = {
        'title': '培训手册',
        'sections': [
            {
                'icon': '📍',
                'title': '基本信息',
                'items': [
                    {'label': '开班时间', 'value': '2026年5月9日'},
                    {'label': '开班地点', 'value': '秦汉校区学术报告厅'},
                    {'label': '培训时间', 'value': '5月9日、5月16日、5月17日、5月23日、5月30日、6月6日'},
                ]
            }
        ]
    }
    return jsonify(data)

@app.route('/api/schedule')
def api_schedule():
    data = {
        'title': '课程表',
        'headers': ['日期', '上课时间', '课程内容', '主讲人', '主持人', '地点'],
        'rows': [
            {'date': '5.30', 'time': '08:30-10:00', 'content': '铸牢中华民族共同体意识', 'speaker': '达宝次仁（西藏党委党校）', 'host': '--', 'location': '学术报告厅（秦汉校区）'}
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('=' * 50)
    print('  🎉  西藏民族大学2026大骨班培训手册已启动')
    print(f'  📱  请在浏览器中打开: http://127.0.0.1:{port}')
    print(f'  🌐  局域网访问: http://0.0.0.0:{port}')
    print('  📋  按 Ctrl+C 停止服务')
    print('=' * 50)
    app.run(host='0.0.0.0', port=port, debug=True)
