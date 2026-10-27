#!/usr/bin/env python3
"""Generates the Chaos Table press kit page (white document layout).
Languages: English (default), Thai, Japanese, Simplified Chinese — same set as the game UI.
Usage: gen.py <out.html>          -> full site page (GitHub Pages)
       gen.py <out.html> preview  -> artifact body (no <html>/<head>/<body>, trailer as link, no download attrs)
"""
import sys, html as H

OUT = sys.argv[1]
PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"

SIZES = {"all": "25 MB", "shots": "11 MB", "store": "4 MB", "cards": "12 MB", "logo": "1 MB"}
LANGS = [("en", "English"), ("th", "ไทย"), ("ja", "日本語"), ("zh-Hans", "简体中文")]

def t(en, th, ja, zh):
    return (f'<span lang="en">{en}</span><span lang="th">{th}</span>'
            f'<span lang="ja">{ja}</span><span lang="zh-Hans">{zh}</span>')

def dl(href, en, th, ja, zh):
    if PREVIEW:
        if href.endswith((".zip", ".txt")):
            # ZIPs are not uploaded to the preview; a link would navigate the frame to a missing file.
            return (f'<span class="na">{t(en, th, ja, zh)}</span> <span class="na-note">'
                    + t("(on the live site)", "(ดาวน์โหลดได้บนเว็บจริง)", "（公開サイトでダウンロード可）", "（可在正式网站下载）") + '</span>')
        return f'<a href="{href}" target="_blank" rel="noopener">{t(en, th, ja, zh)}</a>'
    return f'<a href="{href}" download>{t(en, th, ja, zh)}</a>'

def dl_all(href, size):
    return dl(href, f"Download all (ZIP, {size})", f"ดาวน์โหลดทั้งหมด (ZIP, {size})",
              f"すべてダウンロード (ZIP, {size})", f"全部下载 (ZIP, {size})")

PNG_ATTR = ' target="_blank" rel="noopener"' if PREVIEW else " download"

shots = [
    ("shot-01-hero", "The table at your turn", "โต๊ะเกมตอนถึงเทิร์นของเรา", "自分のターンのテーブル", "轮到你时的牌桌"),
    ("shot-02-discussion", "Discussion phase", "ช่วงพูดคุย", "議論フェーズ", "讨论阶段"),
    ("shot-03-voting", "Choose who to vote out", "เลือกคนที่จะโหวตออก", "追放する人を投票で選ぶ", "投票选出要淘汰的人"),
    ("shot-04-card", "Action card: Banned", "การ์ดแอคชั่น: Banned", "アクションカード：Banned", "行动卡：Banned"),
    ("shot-05-seller", "Card seller and Tactic cards", "พ่อค้าการ์ดและการ์ดแท็กติก", "カード商人とタクティクスカード", "卡牌商人与战术卡"),
    ("shot-06-war", "War Event: hold the tower", "War Event: ป้องกันหอคอย", "戦争イベント：塔を守り抜け", "战争事件：守住高塔"),
    ("shot-07-guest", "Special guest: Muscle Cat", "แขกพิเศษ: แมวกล้าม", "特別ゲスト：マッスルキャット", "特别访客：肌肉猫"),
    ("shot-08-reveal", "Final reveal: Skull side wins", "ผลจบเกม: ฝ่ายกะโหลกชนะ", "最終結果：スカル陣営の勝利", "最终揭晓：骷髅阵营胜利"),
    ("shot-09-ghost", "Ghost world: predict the next death", "โลกผี: ทายว่าใครจะตายต่อ", "幽霊の世界：次に死ぬ人を予想", "幽灵世界：预测下一个死者"),
    ("shot-10-rps", "Rock-paper-scissors tie-break", "เป่ายิ้งฉุบตัดสินโหวตเสมอ", "同票時のじゃんけん決着", "平票时的石头剪刀布决胜"),
    ("shot-11-mainmenu", "Main menu", "เมนูหลัก", "メインメニュー", "主菜单"),
    ("shot-12-lobby", "Lobby", "ล็อบบี้", "ロビー", "大厅"),
]
card_groups = [
    ("Character", ("Role cards", "การ์ดบทบาท", "役職カード", "身份卡"), ["king", "knight", "nurse", "people", "skull", "skull_king", "skull_predator"]),
    ("Action", ("Action cards", "การ์ดแอคชั่น", "アクションカード", "行动卡"), ["banned", "bomb", "choose", "free_time", "get_out", "revive", "salt", "switch", "whoru"]),
    ("Tactic", ("Tactic cards", "การ์ดแท็กติก", "タクティクスカード", "战术卡"), ["counter", "discard", "myturn", "plusone", "shield", "steal", "swap"]),
    ("Rps", ("Tie-break cards", "การ์ดเป่ายิ้งฉุบ", "じゃんけんカード", "石头剪刀布卡"), ["rock", "paper", "scissors"]),
]
# Card faces are English-only in every language (owner decision 2026-10-16), so names stay English here.
CARD_NAMES = {"king": "King", "knight": "Knight", "nurse": "Nurse", "people": "People", "skull": "Skull",
              "skull_king": "Skull King", "skull_predator": "Skull Predator", "banned": "Banned", "bomb": "Bomb",
              "choose": "Choose", "free_time": "Free Time", "get_out": "Get Out", "revive": "Revive", "salt": "Salt",
              "switch": "Switch", "whoru": "Who R U?", "counter": "Counter", "discard": "Discard", "myturn": "My Turn",
              "plusone": "Plus One", "shield": "Shield", "steal": "Steal", "swap": "Swap", "rock": "Rock",
              "paper": "Paper", "scissors": "Scissors"}
logos = [
    ("ChaosTable_Logo_Transparent_2000x1200", ("Logo", "โลโก้", "ロゴ", "标志"),
     ("2000×1200, transparent", "2000×1200 พื้นโปร่งใส", "2000×1200・透過", "2000×1200，透明背景")),
    ("ChaosTable_Logo_Transparent_1280x720", ("Logo (16:9 canvas)", "โลโก้ (กรอบ 16:9)", "ロゴ（16:9 キャンバス）", "标志（16:9 画布）"),
     ("1280×720, transparent", "1280×720 พื้นโปร่งใส", "1280×720・透過", "1280×720，透明背景")),
    ("ChaosTable_Icon_1024", ("Game icon", "ไอคอนเกม", "ゲームアイコン", "游戏图标"), ("1024×1024",) * 4),
    ("ChaosTable_Icon_512", ("Game icon", "ไอคอนเกม", "ゲームアイコン", "游戏图标"), ("512×512",) * 4),
]

nav = [("factsheet", ("Factsheet", "ข้อมูลเกม", "ファクトシート", "游戏资料")),
       ("description", ("Description", "คำอธิบาย", "ゲーム紹介", "游戏介绍")),
       ("features", ("Features", "จุดเด่น", "特徴", "游戏特色")),
       ("trailer", ("Trailer", "ตัวอย่างเกม", "トレーラー", "预告片")),
       ("screenshots", ("Screenshots", "ภาพหน้าจอ", "スクリーンショット", "游戏截图")),
       ("store-art", ("Main art", "ภาพหลัก", "メインアート", "主视觉")),
       ("cards", ("Cards", "การ์ด", "カード", "卡牌")),
       ("logo", ("Logo &amp; icons", "โลโก้และไอคอน", "ロゴ・アイコン", "标志与图标")),
       ("about", ("About", "เกี่ยวกับผู้พัฒนา", "開発者について", "关于开发者")),
       ("contact", ("Contact", "ติดต่อ", "お問い合わせ", "联系方式"))]

css = r"""
/* Layout: a plain white document. Left rail = contents + download-all; right = the kit in the order
   press people look for things: facts, words, media, files, contact. */
:root{
  --bg:#ffffff; --fg:#1d1b20; --muted:#68636e; --line:#e3e0e6; --soft:#f5f4f6;
  --link:#9c4a00; --link-hover:#5f2c00; --banner:#2a1d30;
  --font:'Kanit',system-ui,-apple-system,'Segoe UI',sans-serif;
  color-scheme:light;
}
html[data-lang=ja]{--font:'Kanit','Noto Sans JP','Hiragino Sans','Yu Gothic',system-ui,sans-serif}
html[data-lang=zh-Hans]{--font:'Kanit','Noto Sans SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:16px;background:var(--bg)}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--font);font-weight:300;font-size:17px;line-height:1.7;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 64px}
html[data-lang=ja] body,html[data-lang=zh-Hans] body{font-weight:400;line-break:strict}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}
/* Only the active language's text is shown. English shows if the script has not run yet. */
body [lang]{display:none}
html:not([data-lang]) body [lang=en],
html[data-lang=en] body [lang=en],html[data-lang=th] body [lang=th],
html[data-lang=ja] body [lang=ja],html[data-lang=zh-Hans] body [lang=zh-Hans]{display:revert}
body .langs [lang]{display:revert}
a{color:var(--link);text-underline-offset:2px}
a:hover{color:var(--link-hover)}
a:focus-visible,button:focus-visible{outline:2px solid var(--link);outline-offset:2px}
img{max-width:100%}
h1,h2,h3{font-weight:500;line-height:1.25;margin:0;text-wrap:balance}
h2{font-size:26px;margin:0 0 14px}
h3{font-size:18px;margin:22px 0 8px}
p{margin:0 0 14px;max-width:44em}
.page{max-width:1100px;margin:0 auto}

.banner{position:relative;margin-top:16px;width:100%;aspect-ratio:3.1/1;overflow:hidden;background:var(--banner)}
.banner img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.banner img.logo{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:82%;width:auto;max-width:70%;filter:drop-shadow(0 6px 16px rgba(0,0,0,.45))}
@media(max-width:560px){.banner{aspect-ratio:auto;height:150px}}

.frame{display:grid;grid-template-columns:210px minmax(0,1fr);gap:48px;margin-top:30px}
@media(max-width:860px){.frame{grid-template-columns:1fr;gap:14px}}

.rail{position:sticky;top:20px;align-self:start;font-size:15px}
.rail .name{font-size:24px;font-weight:600;line-height:1.15}
.rail .sub{color:var(--muted);margin:2px 0 14px}
.rail ul{list-style:none;margin:0;padding:0;display:grid;gap:1px}
.rail li a{display:block;padding:3px 0;color:var(--fg);text-decoration:none}
.rail li a:hover{color:var(--link);text-decoration:underline}
.rail .all{display:block;margin-top:16px;padding-top:12px;border-top:1px solid var(--line);font-weight:400}
.langs{margin-top:14px;display:flex;flex-wrap:wrap;gap:4px 14px;font-size:14px}
.langs button{all:unset;cursor:pointer;color:var(--muted);border-bottom:1px solid transparent}
.langs button[aria-pressed=true]{color:var(--fg);border-bottom-color:var(--fg)}
@media(max-width:860px){
  .rail{position:static}
  .rail .name,.rail .sub{display:none}
  .rail ul{display:flex;flex-wrap:wrap;gap:2px 16px}
  .rail .all{margin-top:8px}
}

.main h1{font-size:40px;font-weight:600}
.byline{color:var(--muted);font-size:15px;margin:4px 0 18px}
.lead{font-size:18px}
.getall{border:1px solid var(--line);padding:14px 18px;margin:6px 0 4px;max-width:44em}
.getall p{margin:0}
.getall .files{margin-top:4px;font-size:15px;color:var(--muted)}
section{padding-top:30px;border-top:1px solid var(--line);margin-top:30px}
section.first{border-top:0;margin-top:14px;padding-top:6px}
.zip{font-size:15px;margin:-4px 0 16px;color:var(--muted)}

dl.facts{margin:0;display:grid;grid-template-columns:minmax(120px,190px) minmax(0,1fr)}
dl.facts dt,dl.facts dd{margin:0;padding:8px 0;border-bottom:1px solid var(--line)}
dl.facts dt{color:var(--muted);font-weight:400}
dl.facts dd{overflow-wrap:anywhere}
@media(max-width:560px){dl.facts{grid-template-columns:1fr}dl.facts dt{border-bottom:0;padding-bottom:0}}

.copyrow{margin:-6px 0 18px}
.na{color:var(--muted);text-decoration:underline dotted}.na-note{font-size:13px;color:var(--muted)}
.copy{all:unset;cursor:pointer;color:var(--link);font-size:14px;text-decoration:underline}

ul.bullets{margin:0 0 14px;padding-left:22px;max-width:44em}
ul.bullets li{margin-bottom:6px}

.video{position:relative;aspect-ratio:16/9;background:#000;overflow:hidden;max-width:760px}
.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.video .alt{position:absolute;inset:0;display:grid;place-items:center;color:#fff;font-size:18px}
.video .alt img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.45}
.video .alt span{position:relative}

.grid{display:grid;gap:20px 16px}
.g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.g7{grid-template-columns:repeat(7,minmax(0,1fr));gap:14px 10px}
.g9{grid-template-columns:repeat(9,minmax(0,1fr));gap:14px 8px}
@media(max-width:860px){.g3{grid-template-columns:repeat(2,minmax(0,1fr))}.g7,.g9{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:480px){.g3{grid-template-columns:1fr}.g7,.g9{grid-template-columns:repeat(3,minmax(0,1fr))}}
figure{margin:0;min-width:0}
figure .thumb{display:block;background:var(--soft);overflow:hidden}
figure .thumb img{display:block;width:100%;height:auto}
.shot .thumb{aspect-ratio:16/9;cursor:zoom-in}
.shot .thumb img{height:100%;object-fit:cover}
figcaption{font-size:14px;color:var(--muted);margin-top:5px;line-height:1.45}
figcaption b{font-weight:400;color:var(--fg)}
figcaption a{white-space:nowrap}

.store{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 20px}
@media(max-width:560px){.store{grid-template-columns:1fr}}
.store.one{grid-template-columns:minmax(0,640px)}
.store.one .thumb{aspect-ratio:1232/706}
.store.one .thumb img{inset:0;width:100%;height:100%;object-fit:cover}
.store figure.wide{grid-column:1/-1}
.store figure.wide .thumb{aspect-ratio:3.4/1}
.store .thumb{position:relative;aspect-ratio:16/10;background:var(--soft)}
.store .thumb img{position:absolute;inset:6%;width:88%;height:88%;object-fit:contain}

.card .thumb{background:none}
.card figcaption{text-align:center}

.logos{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px 16px}
@media(max-width:860px){.logos{grid-template-columns:repeat(2,minmax(0,1fr))}}
.logos .thumb{display:grid;place-items:center;aspect-ratio:4/3;background:#1d1720}
.logos .thumb img{max-height:80%;max-width:80%;width:auto}

dialog{border:0;background:transparent;padding:0;max-width:96vw;max-height:96vh}
dialog::backdrop{background:rgba(10,8,12,.92)}
dialog img{max-width:96vw;max-height:92vh;display:block}

.contact{background:var(--soft);padding:18px 22px;max-width:44em}
.contact p{margin:0 0 6px}
.contact .lbl{font-weight:500}
footer{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
"""

parts = []
a = parts.append
a('<div class="page">')
a('<div class="banner"><img class="bg" src="assets/banner.jpg" alt=""><img class="logo" src="assets/logo.png" alt="Chaos Table"></div>')
a('<div class="frame">')
# rail
a('<aside class="rail" aria-label="Contents"><div class="name">Chaos Table</div><div class="sub">Press Kit</div><ul>')
for i, labels in nav:
    li_id = ' id="navTrailer"' if i == "trailer" else ""
    a(f'<li{li_id}><a href="#{i}">{t(*labels)}</a></li>')
a('</ul>')
_rail_label = t("Download everything", "ดาวน์โหลดทั้งหมด", "すべてダウンロード", "下载全部") + f' <span style="color:var(--muted);font-weight:300">(ZIP, {SIZES["all"]})</span>'
a(f'<span class="all na">{_rail_label}</span>' if PREVIEW else f'<a class="all" href="downloads/ChaosTable_PressKit_All.zip" download>{_rail_label}</a>')
a('<div class="langs" role="group" aria-label="Language">' + "".join(
    f'<button type="button" data-set="{code}" lang="{code}" aria-pressed="{"true" if code == "en" else "false"}">{name}</button>'
    for code, name in LANGS) + '</div>')
a('</aside>')

a('<main class="main">')
a('<h1>Chaos Table Press Kit</h1>')
a('<div class="byline">' + t("By Viberzix&#39;s Lab · updated 27 Oct 2026", "โดย Viberzix&#39;s Lab · อัปเดต 27 ต.ค. 2026",
                             "開発：Viberzix&#39;s Lab ・ 更新日 2026年10月27日", "开发：Viberzix&#39;s Lab · 更新于 2026年10月27日") + '</div>')
a('<p class="lead">' + t("Everything you need to write about Chaos Table or put it in a video is on this page. If you need something in another format, or a review key, email us.",
                         "ข้อมูลทั้งหมดสำหรับเขียนข่าวหรือทำคลิปเกี่ยวกับ Chaos Table อยู่ในหน้านี้ หากต้องการไฟล์รูปแบบอื่นหรือคีย์รีวิว อีเมลมาได้เลยครับ",
                         "Chaos Table の記事や動画の制作に必要な素材は、すべてこのページにそろっています。別の形式のファイルやレビュー用キーが必要な場合は、お気軽にメールでご連絡ください。",
                         "撰写 Chaos Table 相关报道或制作视频所需的素材都在本页。如需其他格式的文件或评测激活码，欢迎发邮件联系我们。") + '</p>')
a('<div class="getall"><p>' + dl("downloads/ChaosTable_PressKit_All.zip",
                                 f"Download the full press kit (ZIP, {SIZES['all']})", f"ดาวน์โหลด Press Kit ทั้งชุด (ZIP, {SIZES['all']})",
                                 f"プレスキット一式をダウンロード (ZIP, {SIZES['all']})", f"下载完整媒体资料包 (ZIP, {SIZES['all']})") + '</p>'
  '<p class="files">' + t("12 screenshots, main art, 26 cards, logo and icons.", "ภาพหน้าจอ 12 ภาพ, ภาพหลัก, การ์ด 26 ใบ, โลโก้และไอคอน",
                          "スクリーンショット12枚、メインアート、カード26枚、ロゴ・アイコン", "12 张截图、主视觉、26 张卡牌、标志与图标") + '</p></div>')

# factsheet
facts = [
    (("Developer", "ผู้พัฒนา", "開発", "开发商"), "Viberzix&#39;s Lab"),
    (("Publisher", "ผู้จัดจำหน่าย", "販売", "发行商"), "Viberzix&#39;s Lab"),
    (("Release date", "วันวางจำหน่าย", "発売日", "发售日期"), '<span id="factRelease"></span>'),
    (("Platform", "แพลตฟอร์ม", "プラットフォーム", "平台"), "Windows PC (Steam)"),
    (("Genre", "แนวเกม", "ジャンル", "类型"), t("Social deduction, multiplayer", "Social Deduction, Multiplayer",
                                                 "正体隠匿（ソーシャルディダクション）・マルチプレイ", "社交推理、多人游戏")),
    (("Players", "จำนวนผู้เล่น", "プレイ人数", "玩家人数"), t("6–10", "6–10 คน", "6〜10人", "6–10 人")),
    (("Match length", "ความยาวหนึ่งแมตช์", "1試合の時間", "单局时长"), t("About 15–30 minutes", "ประมาณ 15–30 นาที", "約15〜30分", "约 15–30 分钟")),
    (("Languages", "ภาษา", "対応言語", "支持语言"), t("Interface in English, Thai, Japanese and Simplified Chinese", "อินเทอร์เฟซ: อังกฤษ ไทย ญี่ปุ่น จีนตัวย่อ",
                                                  "インターフェース：英語・タイ語・日本語・簡体字中国語", "界面：英语、泰语、日语、简体中文")),
    (("Price", "ราคา", "価格", "价格"), '<span id="factPrice"></span>'),
    (("Steam", "Steam", "Steam", "Steam"), '<a href="https://store.steampowered.com/app/5294070/" target="_blank" rel="noopener">store.steampowered.com/app/5294070</a>'),
    (("Social", "ช่องทางติดตาม", "SNS", "社交媒体"), '<a href="https://www.youtube.com/@ChaosTable" target="_blank" rel="noopener">YouTube</a> · <a href="https://x.com/ChaosTableGame" target="_blank" rel="noopener">X</a> · <a href="https://www.facebook.com/ChaosTableGame" target="_blank" rel="noopener">Facebook</a>'),
    (("Press contact", "ติดต่อสื่อ", "取材窓口", "媒体联系"), '<a href="mailto:viberzixlab@outlook.co.th">viberzixlab@outlook.co.th</a>'),
]
a('<section id="factsheet" class="first"><h2>' + t("Factsheet", "ข้อมูลเกม", "ファクトシート", "游戏资料") + '</h2><dl class="facts">')
for labels, v in facts:
    a(f'<dt>{t(*labels)}</dt><dd>{v}</dd>')
a('</dl></section>')

# description
def block(bid, heading, paras):
    """paras: dict lang -> list of paragraphs (same count in every language)."""
    a(f'<h3>{t(*heading)}</h3><div id="{bid}">' + "".join(
        f'<p lang="{code}">{p}</p>' for code, _ in LANGS for p in paras[code]) + '</div>')
    a('<div class="copyrow"><button class="copy" data-copy="' + bid + '" type="button">'
      + t("Copy text", "คัดลอกข้อความ", "テキストをコピー", "复制文本") + '</button></div>')

a('<section id="description"><h2>' + t("Description", "คำอธิบาย", "ゲーム紹介", "游戏介绍") + '</h2>')
block("oneliner", ("In one line", "หนึ่งบรรทัด", "ひとことで", "一句话简介"), {
    "en": ["A social deduction party game where roles can change at any time. Talk, spot the liars, eliminate other players, and scheme your way to survival."],
    "th": ["เกมแนวปาร์ตี้สวมบทบาทที่สามารถเปลี่ยนได้เสมอ แนวพูดคุย จับผิด กำจัดผู้เล่นออก และเหลี่ยมให้สุดเพื่อเอาตัวรอด"],
    "ja": ["役職がいつでも入れ替わる、正体隠匿系パーティーゲーム。話し合い、嘘を見抜き、ほかのプレイヤーを脱落させ、策略を尽くして生き残れ。"],
    "zh-Hans": ["一款身份随时可能改变的社交推理派对游戏。交谈、识破谎言、淘汰其他玩家，用尽心机活到最后。"],
})
block("short", ("Short description", "คำอธิบายสั้น", "短い紹介文", "简短介绍"), {
    "en": ["Chaos Table is a talking-and-deduction party game for 6–10 players. Roles are never guaranteed to stay the same and can change at any time, so you can never be sure who is on your side. Talk, build trust, catch the lies, dig up other players&#8217; secrets and guard your own, all without being eliminated first. Or choose to betray, and do whatever it takes to survive until you are the winner."],
    "th": ["Chaos Table คือเกมปาร์ตี้ พูดคุย จับผิด สำหรับผู้เล่น 6–10 คน โดยบทบาทจะไม่การันตีว่าจะเหมือนเดิมตลอดไป มีการเปลี่ยนแปลงได้เสมอ ไม่มีทางรู้ว่าใครเป็นพวกของตัวเอง คุณต้องพูดคุย สร้างความไว้วางใจ จับผิดคำโกหก สืบความลับของพวกเขา และปกป้องความลับที่คุณมี โดยไม่ให้ถูกกำจัดออกไปซะก่อน หรือเลือกที่จะหักหลัง เพื่อความเอาตัวรอดจนกว่าคุณจะเป็นผู้ชนะซะเอง"],
    "ja": ["Chaos Table は、6〜10人で遊ぶ会話と推理のパーティーゲームです。役職がずっと同じとは限らず、いつでも変わる可能性があるため、誰が味方なのか確信することはできません。話し合って信頼を築き、嘘を見抜き、ほかのプレイヤーの秘密を探りながら自分の秘密を守り、先に脱落しないよう立ち回りましょう。あるいは裏切りを選び、最後に勝者となるまで手段を選ばず生き残るのもあなた次第です。"],
    "zh-Hans": ["Chaos Table 是一款供 6–10 名玩家游玩的交谈推理派对游戏。身份并不保证一成不变，随时都可能改变，所以你永远无法确定谁才是自己的同伴。你需要交谈、建立信任、揭穿谎言、打探其他玩家的秘密并守住自己的秘密，同时避免被提前淘汰。你也可以选择背叛，不择手段地活下去，直到成为最后的赢家。"],
})
block("long", ("Long description", "คำอธิบายแบบยาว", "詳しい紹介文", "详细介绍"), {
    "en": ["No one at this table can be trusted.",
           "In Chaos Table, 6–10 players receive secret roles, and nobody knows for sure who is on their side. The game is played in turns, and each turn gives you tools to investigate other players, eliminate them, or ban them to restrict what they can do. Roles can be swapped as well.",
           "Dying is not always the end. A player can be revived at any time in a new role, on either side.",
           "You will also run into special events and mysterious guests who keep shaking up the situation."],
    "th": ["บนโต๊ะแห่งนี้ไม่มีใครไว้ใจได้",
           "ใน Chaos Table ผู้เล่น 6–10 คน จะได้รับบทบาทลับ โดยที่ไม่มีใครรู้เลยว่าใครเป็นพวกของตัวเองก็ตาม รูปแบบการเล่นจะเป็นแบบเทิร์น และแต่ละเทิร์นจะมีตัวช่วยคอยช่วยสืบข้อมูลของผู้เล่น กำจัดผู้เล่นออก หรือแบนเพื่อจำกัดสิทธิ์ได้ รวมถึงการสับเปลี่ยนบทบาทก็ตาม",
           "การตายภายในเกมนั้นถือว่ายังไม่ใช่จุดจบเสมอไป เพราะว่าผู้เล่นสามารถถูกชุบกลับมาได้เสมอในบทบาทใหม่ไม่ว่าจะเป็นฝั่งไหนก็ตาม",
           "นอกจากนี้ก็สามารถพบกับเหตุการณ์พิเศษที่จะเกิดขึ้น หรือแขกปริศนาเพื่อคอยสร้างสถานการณ์ให้เปลี่ยนแปลงได้เสมอ"],
    "ja": ["このテーブルに、信じられる者はいない。",
           "Chaos Table では、6〜10人のプレイヤーにそれぞれ秘密の役職が配られ、誰が味方なのかは誰にもはっきりわかりません。ゲームはターン制で進み、ターンごとにほかのプレイヤーを調べたり、脱落させたり、行動を制限するために封じたりする手段が手に入ります。役職そのものを入れ替えることもできます。",
           "死んでも、それで終わりとは限りません。プレイヤーはいつでも新たな役職で復活する可能性があり、それがどちらの陣営になるかはわかりません。",
           "さらに、特別なイベントや謎の来訪者が次々と現れ、状況をかき乱していきます。"],
    "zh-Hans": ["这张桌上，没有人值得信任。",
                "在 Chaos Table 中，6–10 名玩家各自获得秘密身份，没有人能确定谁是自己的同伴。游戏采用回合制，每个回合都会提供调查其他玩家、淘汰他们，或是封禁对方以限制其行动的手段，甚至还能交换身份。",
                "死亡并不一定是终点。玩家随时可能以新的身份复活，而且可能属于任意一方阵营。",
                "此外，你还会遇到各种特殊事件和神秘访客，让局势不断发生变化。"],
})
a('</section>')

feats = [("Roles can change at any time, and may not stay the same from game to game.",
          "เกมนี้บทบาทมีการเปลี่ยนแปลงได้ตลอดเวลา บางครั้งอาจจะไม่ใช่บทบาทเดิมเสมอไปของทุกการเล่น",
          "役職はいつでも変わる可能性があり、毎回同じ役職のままとは限りません。",
          "身份随时可能改变，每局游戏中都不一定保持原样。"),
         ("No player knows for certain who the rest of their own side are.",
          "ไม่มีผู้เล่นฝ่ายไหนรู้ตัวจริงหรือบทบาทของพวกตัวเองทั้งหมด",
          "どちらの陣営のプレイヤーも、味方全員の正体を確実には知りません。",
          "无论哪一方的玩家，都无法确定自己所有同伴的真实身份。"),
         ("Tactics let you build a plan of your own to win.",
          "มีแท็คติคในการสร้างแบบแผนในการเล่น เพื่อสร้างชัยชนะของตัวเอง",
          "タクティクスカードで自分だけの作戦を組み立て、勝利をつかみましょう。",
          "利用战术卡制定属于自己的计划，赢得胜利。"),
         ("Some roles keep special abilities after death, to help other players or to eliminate others faster.",
          "บทบาทบางบทนั้นมีความสามารถพิเศษหลังตายไปแล้ว เพื่อช่วยเหลือผู้เล่นอื่น หรือกำจัดผู้เล่นออกไวขึ้น",
          "一部の役職は死亡後にも特殊能力を発揮でき、ほかのプレイヤーを助けたり、より早く誰かを脱落させたりできます。",
          "部分身份在死亡后仍能发动特殊能力，可以帮助其他玩家，或更快地淘汰他人。")]
a('<section id="features"><h2>' + t("Features", "จุดเด่น", "特徴", "游戏特色") + '</h2><ul class="bullets">' + "".join(f'<li>{t(*f)}</li>' for f in feats) + '</ul></section>')

a('<section id="trailer"><h2>' + t("Trailer", "ตัวอย่างเกม", "トレーラー", "预告片") + '</h2><div class="video" id="trailerBox"></div>'
  '<p style="margin-top:10px;font-size:15px"><a id="trailerLink" target="_blank" rel="noopener" href="#">'
  + t("Open on YouTube", "เปิดบน YouTube", "YouTube で見る", "在 YouTube 上观看") + '</a></p></section>')

# screenshots
a('<section id="screenshots"><h2>' + t("Screenshots", "ภาพหน้าจอ", "スクリーンショット", "游戏截图") + '</h2>')
a('<p class="zip">' + t("1920×1080 PNG, captured in game. Click an image to enlarge it.", "PNG 1920×1080 แคปจากในเกม คลิกภาพเพื่อขยาย",
                        "1920×1080 の PNG、ゲーム内で撮影。画像をクリックすると拡大します。", "1920×1080 PNG，游戏内截取。点击图片可放大。")
  + ' · ' + dl_all("downloads/ChaosTable_Screenshots.zip", SIZES['shots']) + '</p>')
a('<div class="grid g3">')
for f, en, th, ja, zh in shots:
    a(f'<figure class="shot"><a class="thumb" href="assets/screenshots/{f}.png" data-full="assets/screenshots/{f}.png"><img src="assets/thumbs/screenshots/{f}.jpg" alt="{H.escape(en)}" loading="lazy"></a>'
      f'<figcaption>{t(en, th, ja, zh)} · <a href="assets/screenshots/{f}.png"{PNG_ATTR}>PNG</a></figcaption></figure>')
a('</div></section>')

# store art (single main capsule)
a('<section id="store-art"><h2>' + t("Main art", "ภาพหลักหน้าร้าน", "メインアート", "主视觉") + '</h2>')
a('<p class="zip">' + t("The main capsule from our Steam page, for headers, thumbnails and video edits.",
                        "ภาพหลักจากหน้าร้าน Steam ใช้ทำภาพหัวข่าว ปกคลิป หรือตัดต่อได้",
                        "Steam ストアページのメインカプセル画像です。記事のヘッダー、サムネイル、動画編集にご利用ください。",
                        "Steam 商店页面的主胶囊图，可用于文章头图、缩略图和视频剪辑。") + '</p>')
_f = "ChaosTable_MainCapsule_1232x706"
a('<div class="store one">')
a(f'<figure><a class="thumb" href="assets/store/{_f}.png" target="_blank" rel="noopener"><img src="assets/thumbs/store/{_f}.jpg" alt="Main capsule" loading="lazy"></a>'
  f'<figcaption><b>{t("Main capsule", "ภาพหลัก", "メインカプセル", "主胶囊图")}</b> · 1232×706 · <a href="assets/store/{_f}.png"{PNG_ATTR}>PNG</a></figcaption></figure>')
a('</div></section>')

# cards
a('<section id="cards"><h2>' + t("Cards", "การ์ด", "カード", "卡牌") + '</h2>')
a('<p class="zip">' + t("Every card in the game as a transparent PNG at 1600×2240, ready to drop into thumbnails or edits.",
                        "การ์ดทุกใบในเกม PNG พื้นโปร่งใส 1600×2240 พร้อมใช้ทำปกคลิปหรือตัดต่อ",
                        "ゲーム内の全カードを 1600×2240 の透過 PNG で収録。サムネイルや動画編集にそのまま使えます。",
                        "游戏中全部卡牌，1600×2240 透明背景 PNG，可直接用于缩略图或视频剪辑。")
  + ' · ' + dl("downloads/ChaosTable_Cards.zip", f"Download all 26 (ZIP, {SIZES['cards']})", f"ดาวน์โหลดทั้ง 26 ใบ (ZIP, {SIZES['cards']})",
               f"26枚すべてダウンロード (ZIP, {SIZES['cards']})", f"下载全部 26 张 (ZIP, {SIZES['cards']})") + '</p>')
for cat, labels, items in card_groups:
    a(f'<h3>{t(*labels)}</h3><div class="grid {"g9" if len(items) > 7 else "g7"}">')
    for it in items:
        fn = f"ChaosTable_Card_{cat}_{it}"
        nm = CARD_NAMES[it]
        a(f'<figure class="card"><a class="thumb" href="assets/cards/{fn}.png" target="_blank" rel="noopener"><img src="assets/thumbs/cards/{fn}.png" alt="{H.escape(nm)} card" loading="lazy"></a><figcaption>{nm}</figcaption></figure>')
    a('</div>')
a('</section>')

# logo
a('<section id="logo"><h2>' + t("Logo &amp; icons", "โลโก้และไอคอน", "ロゴ・アイコン", "标志与图标") + '</h2>')
a('<p class="zip">' + dl_all("downloads/ChaosTable_Logo_Icons.zip", SIZES['logo']) + '</p>')
a('<div class="logos">')
for f, name, size in logos:
    a(f'<figure><a class="thumb" href="assets/logo/{f}.png" target="_blank" rel="noopener"><img src="assets/thumbs/logo/{f}.png" alt="{H.escape(name[0])}" loading="lazy"></a><figcaption><b>{t(*name)}</b><br>{t(*size)} · <a href="assets/logo/{f}.png"{PNG_ATTR}>PNG</a></figcaption></figure>')
a('</div></section>')

a('<section id="about"><h2>' + t("About the developer", "เกี่ยวกับผู้พัฒนา", "開発者について", "关于开发者") + '</h2>'
  '<p>' + t("Chaos Table is an indie game made by one developer under the name Viberzix&#8217;s Lab.",
            "Chaos Table เป็นเกมอินดี้ที่พัฒนาโดยคนเดียว ภายใต้ชื่อ Viberzix&#8217;s Lab",
            "Chaos Table は、Viberzix&#8217;s Lab の名義で活動する開発者が一人で制作したインディーゲームです。",
            "Chaos Table 是一款由开发者以 Viberzix&#8217;s Lab 之名独自制作的独立游戏。") + '</p>'
  '<h3>' + t("AI disclosure", "การใช้ AI", "AI の使用について", "AI 使用说明") + '</h3><p>'
  + t("AI tools were used only for programming and for the English, Simplified Chinese and Japanese translations. No generative AI was used for art, animation or audio.",
      "ใช้ AI เฉพาะงานเขียนโค้ดและการแปลภาษาอังกฤษ จีนตัวย่อ และญี่ปุ่น ไม่ใช้ Generative AI กับงานภาพ แอนิเมชัน หรือเสียง",
      "AI ツールはプログラミングと、英語・簡体字中国語・日本語への翻訳にのみ使用しています。アート、アニメーション、サウンドには生成 AI を使用していません。",
      "AI 工具仅用于编程以及英语、简体中文和日语的翻译。美术、动画和音频均未使用生成式 AI。") + '</p></section>')

a('<section id="contact"><h2>' + t("Contact", "ติดต่อ", "お問い合わせ", "联系方式") + '</h2><div class="contact">'
  '<p><span class="lbl">' + t("Email:", "อีเมล:", "メール：", "邮箱：") + '</span> <a href="mailto:viberzixlab@outlook.co.th">viberzixlab@outlook.co.th</a></p></div></section>')
a('<footer>© Viberzix&#39;s Lab · Chaos Table</footer>')
a('</main></div></div>')
a('<dialog id="lightbox"><img alt=""></dialog>')

js = r"""
/* ====== EDIT ME ====== */
const CONFIG = {
  trailerYouTubeId: "ggFYxW_-1vo",
  embedTrailer: EMBED,
  release: { "en": "12 November 2026", "th": "12 พฤศจิกายน 2026", "ja": "2026年11月12日", "zh-Hans": "2026年11月12日" },
  price:   { "en": "4.99 USD", "th": "99 บาท", "ja": "655円（Steam 日本ストア価格）", "zh-Hans": "22 元人民币（Steam 国区价格）" }
};
const LANGS = ["en", "th", "ja", "zh-Hans"];
const UI = {
  copied:   { "en": "Copied", "th": "คัดลอกแล้ว", "ja": "コピーしました", "zh-Hans": "已复制" },
  selected: { "en": "Text selected, press Ctrl+C", "th": "เลือกข้อความแล้ว กด Ctrl+C", "ja": "テキストを選択しました。Ctrl+C でコピー", "zh-Hans": "已选中文本，请按 Ctrl+C" },
  watch:    { "en": "Watch the trailer on YouTube", "th": "ดูตัวอย่างเกมบน YouTube", "ja": "YouTube でトレーラーを見る", "zh-Hans": "在 YouTube 上观看预告片" }
};
const html = document.documentElement;
function setLang(l){
  html.dataset.lang = l; html.lang = l;
  document.querySelectorAll('.langs button').forEach(b => b.setAttribute('aria-pressed', b.dataset.set === l));
  try { localStorage.setItem('ct-lang', l); } catch(e){}
  document.getElementById('factRelease').textContent = CONFIG.release[l];
  document.getElementById('factPrice').textContent   = CONFIG.price[l];
  const w = document.getElementById('watchLabel'); if (w) w.textContent = '▶ ' + UI.watch[l];
}
document.querySelectorAll('.langs button').forEach(b => b.addEventListener('click', () => setLang(b.dataset.set)));
/* A visitor's own choice wins; otherwise follow the browser language; otherwise English. */
function guessLang(){
  const list = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || 'en'];
  for (const raw of list){
    const c = String(raw).toLowerCase();
    if (c.startsWith('ja')) return 'ja';
    if (c.startsWith('th')) return 'th';
    if (c === 'zh' || c.startsWith('zh-cn') || c.startsWith('zh-sg') || c.startsWith('zh-hans')) return 'zh-Hans';
    if (c.startsWith('en')) return 'en';
  }
  return 'en';
}
let start = guessLang();
try { const s = localStorage.getItem('ct-lang'); if (LANGS.includes(s)) start = s; } catch(e){}

(function(){
  const id = CONFIG.trailerYouTubeId.trim();
  if (!id){ document.getElementById('trailer').hidden = true; document.getElementById('navTrailer').hidden = true; return; }
  const url = 'https://www.youtube.com/watch?v=' + encodeURIComponent(id);
  document.getElementById('trailerLink').href = url;
  const box = document.getElementById('trailerBox');
  box.innerHTML = CONFIG.embedTrailer
    ? '<iframe src="https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'" title="Chaos Table trailer" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe>'
    : '<a class="alt" target="_blank" rel="noopener" href="'+url+'"><img src="assets/thumbs/screenshots/shot-01-hero.jpg" alt=""><span id="watchLabel"></span></a>';
})();

const lb = document.getElementById('lightbox');
document.querySelectorAll('.shot a.thumb').forEach(a => a.addEventListener('click', e => {
  e.preventDefault(); lb.querySelector('img').src = a.dataset.full; lb.showModal();
}));
lb.addEventListener('click', () => lb.close());

document.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', async () => {
  const el = document.getElementById(b.dataset.copy), l = html.dataset.lang;
  const text = Array.from(el.querySelectorAll('[lang="'+l+'"]')).map(n => n.textContent.trim()).join('\n\n');
  const old = b.innerHTML;
  try { await navigator.clipboard.writeText(text); b.textContent = UI.copied[l]; }
  catch(e){ const r = document.createRange(); r.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = UI.selected[l]; }
  setTimeout(() => b.innerHTML = old, 1600);
}));
setLang(start);
""".replace("EMBED", "false" if PREVIEW else "true")

head = ('<meta name="claude:viewport-fit-sides" content="cover">\n<title>Chaos Table Press Kit</title>\n'
        '<meta name="description" content="Press kit for Chaos Table, an online social deduction party game for 6–10 players by Viberzix&#39;s Lab.">\n'
        '<meta property="og:title" content="Chaos Table Press Kit">\n<meta property="og:image" content="assets/store/ChaosTable_MainCapsule_1232x706.png">\n'
        '<link rel="icon" href="assets/logo/ChaosTable_Icon_512.png">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&family=Noto+Sans+JP:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600&display=swap" rel="stylesheet">\n'
        f'<style>{css}</style>\n')
body = "\n".join(parts) + f"\n<script>{js}</script>\n"

if PREVIEW:
    doc = head + body
else:
    doc = ('<!doctype html>\n<html lang="en" data-lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           + head + '</head>\n<body>\n' + body + '</body>\n</html>\n')
open(OUT, "w", encoding="utf-8").write(doc)
print("wrote", OUT, len(doc))
