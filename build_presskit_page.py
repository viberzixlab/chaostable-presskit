#!/usr/bin/env python3
"""Generates the Chaos Table press kit page (white document layout).
Usage: gen.py <out.html>          -> full site page (GitHub Pages)
       gen.py <out.html> preview  -> artifact body (no <html>/<head>/<body>, trailer as link, no download attrs)
"""
import sys, html as H

OUT = sys.argv[1]
PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"

SIZES = {"all": "25 MB", "shots": "11 MB", "store": "4 MB", "cards": "12 MB", "logo": "1 MB"}

def t(en, th):
    return f'<span lang="en">{en}</span><span lang="th">{th}</span>'

def dl(href, label_en, label_th):
    if PREVIEW:
        if href.endswith((".zip", ".txt")):
            # ZIPs are not uploaded to the preview; a link would navigate the frame to a missing file.
            return f'<span class="na">{t(label_en, label_th)}</span> <span class="na-note">{t("(on the live site)", "(ดาวน์โหลดได้บนเว็บจริง)")}</span>'
        return f'<a href="{href}" target="_blank" rel="noopener">{t(label_en, label_th)}</a>'
    return f'<a href="{href}" download>{t(label_en, label_th)}</a>'

PNG_ATTR = ' target="_blank" rel="noopener"' if PREVIEW else " download"

shots = [
    ("shot-01-hero", "The table at your turn", "โต๊ะเกมตอนถึงเทิร์นของเรา"),
    ("shot-02-discussion", "Discussion phase", "ช่วงพูดคุย"),
    ("shot-03-voting", "Choose who to vote out", "เลือกคนที่จะโหวตออก"),
    ("shot-04-card", "Action card: Banned", "การ์ดแอคชั่น: Banned"),
    ("shot-05-seller", "Card seller and Tactic cards", "พ่อค้าการ์ดและการ์ดแท็กติก"),
    ("shot-06-war", "War Event: hold the tower", "War Event: ป้องกันหอคอย"),
    ("shot-07-guest", "Special guest: Muscle Cat", "แขกพิเศษ: แมวกล้าม"),
    ("shot-08-reveal", "Final reveal: Skull side wins", "ผลจบเกม: ฝ่ายกะโหลกชนะ"),
    ("shot-09-ghost", "Ghost world: predict the next death", "โลกผี: ทายว่าใครจะตายต่อ"),
    ("shot-10-rps", "Rock-paper-scissors tie-break", "เป่ายิ้งฉุบตัดสินโหวตเสมอ"),
    ("shot-11-mainmenu", "Main menu", "เมนูหลัก"),
    ("shot-12-lobby", "Lobby", "ล็อบบี้"),
]
store = [
    ("ChaosTable_HeaderCapsule_920x430", "Header capsule", "Header capsule", "920×430", "Article header or link preview", "ใช้เป็นภาพหัวข่าวหรือภาพลิงก์"),
    ("ChaosTable_MainCapsule_1232x706", "Main capsule", "Main capsule", "1232×706", "Large feature image", "ภาพหลักขนาดใหญ่"),
    ("ChaosTable_SmallCapsule_462x174", "Small capsule", "Small capsule", "462×174", "Lists and small slots", "ใช้ในรายการหรือช่องเล็ก"),
    ("ChaosTable_VerticalCapsule_748x896", "Vertical capsule", "Vertical capsule", "748×896", "Portrait posts", "โพสต์แนวตั้ง"),
    ("ChaosTable_LibraryCapsule_600x900", "Library capsule", "Library capsule", "600×900", "Cover / box art", "ภาพปกแนวตั้ง"),
    ("ChaosTable_Banner_Lineup_1640x720", "Character lineup banner", "แบนเนอร์ตัวละคร", "1640×720", "Social banner with logo", "แบนเนอร์โซเชียลพร้อมโลโก้"),
    ("ChaosTable_KeyArt_NoLogo_3840x1240", "Key art, no logo", "Key Art ไม่มีโลโก้", "3840×1240", "Background for thumbnails and edits", "พื้นหลังสำหรับทำปกคลิปหรือตัดต่อ"),
]
card_groups = [
    ("Character", "Role cards", "การ์ดบทบาท", ["king", "knight", "nurse", "people", "skull", "skull_king", "skull_predator"]),
    ("Action", "Action cards", "การ์ดแอคชั่น", ["banned", "bomb", "choose", "free_time", "get_out", "revive", "salt", "switch", "whoru"]),
    ("Tactic", "Tactic cards", "การ์ดแท็กติก", ["counter", "discard", "myturn", "plusone", "shield", "steal", "swap"]),
    ("Rps", "Tie-break cards", "การ์ดเป่ายิ้งฉุบ", ["rock", "paper", "scissors"]),
]
CARD_NAMES = {"king": "King", "knight": "Knight", "nurse": "Nurse", "people": "People", "skull": "Skull",
              "skull_king": "Skull King", "skull_predator": "Skull Predator", "banned": "Banned", "bomb": "Bomb",
              "choose": "Choose", "free_time": "Free Time", "get_out": "Get Out", "revive": "Revive", "salt": "Salt",
              "switch": "Switch", "whoru": "Who R U?", "counter": "Counter", "discard": "Discard", "myturn": "My Turn",
              "plusone": "Plus One", "shield": "Shield", "steal": "Steal", "swap": "Swap", "rock": "Rock",
              "paper": "Paper", "scissors": "Scissors"}
logos = [
    ("ChaosTable_Logo_Transparent_2000x1200", "Logo", "โลโก้", "2000×1200, transparent", "2000×1200 พื้นโปร่งใส"),
    ("ChaosTable_Logo_Transparent_1280x720", "Logo (16:9 canvas)", "โลโก้ (กรอบ 16:9)", "1280×720, transparent", "1280×720 พื้นโปร่งใส"),
    ("ChaosTable_Icon_1024", "Game icon", "ไอคอนเกม", "1024×1024", "1024×1024"),
    ("ChaosTable_Icon_512", "Game icon", "ไอคอนเกม", "512×512", "512×512"),
]

nav = [("factsheet", "Factsheet", "ข้อมูลเกม"), ("description", "Description", "คำอธิบาย"),
       ("features", "Features", "จุดเด่น"), ("trailer", "Trailer", "ตัวอย่างเกม"),
       ("screenshots", "Screenshots", "ภาพหน้าจอ"), ("store-art", "Main art", "ภาพหลัก"),
       ("cards", "Cards", "การ์ด"), ("logo", "Logo & icons", "โลโก้และไอคอน"),
       ("about", "About", "เกี่ยวกับผู้พัฒนา"), ("contact", "Contact", "ติดต่อ")]

css = r"""
/* Layout: a plain white document. Left rail = contents + download-all; right = the kit in the order
   press people look for things: facts, words, media, files, contact. */
:root{
  --bg:#ffffff; --fg:#1d1b20; --muted:#68636e; --line:#e3e0e6; --soft:#f5f4f6;
  --link:#9c4a00; --link-hover:#5f2c00; --banner:#2a1d30;
  --font:'Kanit',system-ui,-apple-system,'Segoe UI',sans-serif;
  color-scheme:light;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:16px;background:var(--bg)}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--font);font-weight:300;font-size:17px;line-height:1.7;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 64px}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}
body [lang=th]{display:none}
html[data-lang=th] body [lang=en]{display:none}
html[data-lang=th] body [lang=th]{display:revert}
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
.langs{margin-top:14px;display:flex;gap:14px;font-size:14px}
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
for i, en, th in nav:
    li_id = ' id="navTrailer"' if i == "trailer" else ""
    a(f'<li{li_id}><a href="#{i}">{t(en, th)}</a></li>')
a('</ul>')
_rail_label = t("Download everything", "ดาวน์โหลดทั้งหมด") + f' <span style="color:var(--muted);font-weight:300">(ZIP, {SIZES["all"]})</span>'
a(f'<span class="all na">{_rail_label}</span>' if PREVIEW else f'<a class="all" href="downloads/ChaosTable_PressKit_All.zip" download>{_rail_label}</a>')
a('<div class="langs" role="group" aria-label="Language"><button type="button" data-set="en" aria-pressed="true">English</button><button type="button" data-set="th" aria-pressed="false">ไทย</button></div>')
a('</aside>')

a('<main class="main">')
a(f'<h1>Chaos Table Press Kit</h1>')
a(f'<div class="byline">{t("By Viberzix&#39;s Lab · updated", "โดย Viberzix&#39;s Lab · อัปเดต")} 18 Oct 2026</div>')
a('<p class="lead">' + t("Everything you need to write about Chaos Table or put it in a video is on this page. If you need something in another format, or a review key, email us.",
                         "ข้อมูลทั้งหมดสำหรับเขียนข่าวหรือทำคลิปเกี่ยวกับ Chaos Table อยู่ในหน้านี้ หากต้องการไฟล์รูปแบบอื่นหรือคีย์รีวิว อีเมลมาได้เลยครับ") + '</p>')
a('<div class="getall"><p>' + dl("downloads/ChaosTable_PressKit_All.zip", f"Download the full press kit (ZIP, {SIZES['all']})", f"ดาวน์โหลด Press Kit ทั้งชุด (ZIP, {SIZES['all']})") + '</p>'
  '<p class="files">' + t("Factsheet text, 12 screenshots, main art, 26 cards, logo and icons. Or get the ",
                          "มีข้อความ Factsheet, ภาพหน้าจอ 12 ภาพ, ภาพหลัก, การ์ด 26 ใบ, โลโก้และไอคอน หรือดาวน์โหลด") + ' ' +
  dl("downloads/ChaosTable_Factsheet.txt", "factsheet only (TXT)", "เฉพาะ Factsheet (TXT)") + '.</p></div>')

# factsheet
facts = [
    (("Developer", "ผู้พัฒนา"), "Viberzix&#39;s Lab"),
    (("Publisher", "ผู้จัดจำหน่าย"), "Viberzix&#39;s Lab"),
    (("Release date", "วันวางจำหน่าย"), '<span id="factRelease"></span>'),
    (("Platform", "แพลตฟอร์ม"), "Windows PC (Steam)"),
    (("Genre", "แนวเกม"), t("Social deduction, multiplayer", "Social Deduction, Multiplayer")),
    (("Players", "จำนวนผู้เล่น"), t("6–10", "6–10 คน")),
    (("Match length", "ความยาวหนึ่งแมตช์"), t("About 15–30 minutes", "ประมาณ 15–30 นาที")),
    (("Languages", "ภาษา"), t("Interface in English, Thai, Japanese and Simplified Chinese", "อินเทอร์เฟซ: อังกฤษ ไทย ญี่ปุ่น จีนตัวย่อ")),
    (("Price", "ราคา"), '<span id="factPrice"></span>'),
    (("Steam", "Steam"), '<a href="https://store.steampowered.com/app/5294070/" target="_blank" rel="noopener">store.steampowered.com/app/5294070</a>'),
    (("Social", "ช่องทางติดตาม"), '<a href="https://www.youtube.com/@ChaosTable" target="_blank" rel="noopener">YouTube</a> · <a href="https://x.com/ChaosTableGame" target="_blank" rel="noopener">X</a> · <a href="https://www.facebook.com/ChaosTableGame" target="_blank" rel="noopener">Facebook</a>'),
    (("Press contact", "ติดต่อสื่อ"), '<a href="mailto:viberzixlab@outlook.co.th">viberzixlab@outlook.co.th</a>'),
]
a('<section id="factsheet" class="first"><h2>' + t("Factsheet", "ข้อมูลเกม") + '</h2><dl class="facts">')
for (en, th), v in facts:
    a(f'<dt>{t(en, th)}</dt><dd>{v}</dd>')
a('</dl></section>')

# description
def block(bid, h_en, h_th, en_paras, th_paras):
    a(f'<h3>{t(h_en, h_th)}</h3><div id="{bid}">' + "".join(f'<p lang="en">{p}</p>' for p in en_paras) + "".join(f'<p lang="th">{p}</p>' for p in th_paras) + '</div>')
    a(f'<div class="copyrow"><button class="copy" data-copy="{bid}" type="button">{t("Copy text", "คัดลอกข้อความ")}</button></div>')
a('<section id="description"><h2>' + t("Description", "คำอธิบาย") + '</h2>')
block("oneliner", "In one line", "หนึ่งบรรทัด",
      ["A social deduction party game where roles can change at any time. Talk, spot the liars, eliminate other players, and scheme your way to survival."],
      ["เกมแนวปาร์ตี้สวมบทบาทที่สามารถเปลี่ยนได้เสมอ แนวพูดคุย จับผิด กำจัดผู้เล่นออก และเหลี่ยมให้สุดเพื่อเอาตัวรอด"])
block("short", "Short description", "คำอธิบายสั้น",
      ["Chaos Table is a talking-and-deduction party game for 6–10 players. Roles are never guaranteed to stay the same and can change at any time, so you can never be sure who is on your side. Talk, build trust, catch the lies, dig up other players&#8217; secrets and guard your own, all without being eliminated first. Or choose to betray, and do whatever it takes to survive until you are the winner."],
      ["Chaos Table คือเกมปาร์ตี้ พูดคุย จับผิด สำหรับผู้เล่น 6–10 คน โดยบทบาทจะไม่การันตีว่าจะเหมือนเดิมตลอดไป มีการเปลี่ยนแปลงได้เสมอ ไม่มีทางรู้ว่าใครเป็นพวกของตัวเอง คุณต้องพูดคุย สร้างความไว้วางใจ จับผิดคำโกหก สืบความลับของพวกเขา และปกป้องความลับที่คุณมี โดยไม่ให้ถูกกำจัดออกไปซะก่อน หรือเลือกที่จะหักหลัง เพื่อความเอาตัวรอดจนกว่าคุณจะเป็นผู้ชนะซะเอง"])
block("long", "Long description", "คำอธิบายแบบยาว",
      ["No one at this table can be trusted.",
       "In Chaos Table, 6–10 players receive secret roles, and nobody knows for sure who is on their side. The game is played in turns, and each turn gives you tools to investigate other players, eliminate them, or ban them to restrict what they can do. Roles can be swapped as well.",
       "Dying is not always the end. A player can be revived at any time in a new role, on either side.",
       "You will also run into special events and mysterious guests who keep shaking up the situation."],
      ["บนโต๊ะแห่งนี้ไม่มีใครไว้ใจได้",
       "ใน Chaos Table ผู้เล่น 6–10 คน จะได้รับบทบาทลับ โดยที่ไม่มีใครรู้เลยว่าใครเป็นพวกของตัวเองก็ตาม รูปแบบการเล่นจะเป็นแบบเทิร์น และแต่ละเทิร์นจะมีตัวช่วยคอยช่วยสืบข้อมูลของผู้เล่น กำจัดผู้เล่นออก หรือแบนเพื่อจำกัดสิทธิ์ได้ รวมถึงการสับเปลี่ยนบทบาทก็ตาม",
       "การตายภายในเกมนั้นถือว่ายังไม่ใช่จุดจบเสมอไป เพราะว่าผู้เล่นสามารถถูกชุบกลับมาได้เสมอในบทบาทใหม่ไม่ว่าจะเป็นฝั่งไหนก็ตาม",
       "นอกจากนี้ก็สามารถพบกับเหตุการณ์พิเศษที่จะเกิดขึ้น หรือแขกปริศนาเพื่อคอยสร้างสถานการณ์ให้เปลี่ยนแปลงได้เสมอ"])
a('</section>')

feats = [("Roles can change at any time, and may not stay the same from game to game.", "เกมนี้บทบาทมีการเปลี่ยนแปลงได้ตลอดเวลา บางครั้งอาจจะไม่ใช่บทบาทเดิมเสมอไปของทุกการเล่น"),
         ("No player knows for certain who the rest of their own side are.", "ไม่มีผู้เล่นฝ่ายไหนรู้ตัวจริงหรือบทบาทของพวกตัวเองทั้งหมด"),
         ("Tactics let you build a plan of your own to win.", "มีแท็คติคในการสร้างแบบแผนในการเล่น เพื่อสร้างชัยชนะของตัวเอง"),
         ("Some roles keep special abilities after death, to help other players or to eliminate others faster.", "บทบาทบางบทนั้นมีความสามารถพิเศษหลังตายไปแล้ว เพื่อช่วยเหลือผู้เล่นอื่น หรือกำจัดผู้เล่นออกไวขึ้น")]
a('<section id="features"><h2>' + t("Features", "จุดเด่น") + '</h2><ul class="bullets">' + "".join(f'<li>{t(e, th)}</li>' for e, th in feats) + '</ul></section>')

a('<section id="trailer"><h2>' + t("Trailer", "ตัวอย่างเกม") + '</h2><div class="video" id="trailerBox"></div>'
  '<p style="margin-top:10px;font-size:15px"><a id="trailerLink" target="_blank" rel="noopener" href="#">' + t("Open on YouTube", "เปิดบน YouTube") + '</a></p></section>')

# screenshots
a('<section id="screenshots"><h2>' + t("Screenshots", "ภาพหน้าจอ") + '</h2>')
a('<p class="zip">' + t("1920×1080 PNG, captured in game. Click an image to enlarge it.", "PNG 1920×1080 แคปจากในเกม คลิกภาพเพื่อขยาย") + ' · ' + dl("downloads/ChaosTable_Screenshots.zip", f"Download all (ZIP, {SIZES['shots']})", f"ดาวน์โหลดทั้งหมด (ZIP, {SIZES['shots']})") + '</p>')
a('<div class="grid g3">')
for f, en, th in shots:
    a(f'<figure class="shot"><a class="thumb" href="assets/screenshots/{f}.png" data-full="assets/screenshots/{f}.png"><img src="assets/thumbs/screenshots/{f}.jpg" alt="{H.escape(en)}" loading="lazy"></a>'
      f'<figcaption>{t(en, th)} · <a href="assets/screenshots/{f}.png"{PNG_ATTR}>PNG</a></figcaption></figure>')
a('</div></section>')

# store art (single main capsule)
a('<section id="store-art"><h2>' + t("Main art", "ภาพหลักหน้าร้าน") + '</h2>')
a('<p class="zip">' + t("The main capsule from our Steam page, for headers, thumbnails and video edits.", "ภาพหลักจากหน้าร้าน Steam ใช้ทำภาพหัวข่าว ปกคลิป หรือตัดต่อได้") + '</p>')
_f = "ChaosTable_MainCapsule_1232x706"
a('<div class="store one">')
a(f'<figure><a class="thumb" href="assets/store/{_f}.png" target="_blank" rel="noopener"><img src="assets/thumbs/store/{_f}.jpg" alt="Main capsule" loading="lazy"></a>'
  f'<figcaption><b>{t("Main capsule", "ภาพหลัก")}</b> · 1232×706 · <a href="assets/store/{_f}.png"{PNG_ATTR}>PNG</a></figcaption></figure>')
a('</div></section>')

# cards
a('<section id="cards"><h2>' + t("Cards", "การ์ด") + '</h2>')
a('<p class="zip">' + t("Every card in the game as a transparent PNG at 1600×2240, ready to drop into thumbnails or edits.", "การ์ดทุกใบในเกม PNG พื้นโปร่งใส 1600×2240 พร้อมใช้ทำปกคลิปหรือตัดต่อ") + ' · ' + dl("downloads/ChaosTable_Cards.zip", f"Download all 26 (ZIP, {SIZES['cards']})", f"ดาวน์โหลดทั้ง 26 ใบ (ZIP, {SIZES['cards']})") + '</p>')
for cat, en, th, items in card_groups:
    a(f'<h3>{t(en, th)}</h3><div class="grid {"g9" if len(items) > 7 else "g7"}">')
    for it in items:
        fn = f"ChaosTable_Card_{cat}_{it}"
        nm = CARD_NAMES[it]
        a(f'<figure class="card"><a class="thumb" href="assets/cards/{fn}.png" target="_blank" rel="noopener"><img src="assets/thumbs/cards/{fn}.png" alt="{H.escape(nm)} card" loading="lazy"></a><figcaption>{nm}</figcaption></figure>')
    a('</div>')
a('</section>')

# logo
a('<section id="logo"><h2>' + t("Logo &amp; icons", "โลโก้และไอคอน") + '</h2>')
a('<p class="zip">' + dl("downloads/ChaosTable_Logo_Icons.zip", f"Download all (ZIP, {SIZES['logo']})", f"ดาวน์โหลดทั้งหมด (ZIP, {SIZES['logo']})") + '</p>')
a('<div class="logos">')
for f, en, th, sz_en, sz_th in logos:
    a(f'<figure><a class="thumb" href="assets/logo/{f}.png" target="_blank" rel="noopener"><img src="assets/thumbs/logo/{f}.png" alt="{H.escape(en)}" loading="lazy"></a><figcaption><b>{t(en, th)}</b><br>{t(sz_en, sz_th)} · <a href="assets/logo/{f}.png"{PNG_ATTR}>PNG</a></figcaption></figure>')
a('</div></section>')

a('<section id="about"><h2>' + t("About the developer", "เกี่ยวกับผู้พัฒนา") + '</h2>'
  '<p>' + t("Chaos Table is an indie game made by one developer under the name Viberzix&#8217;s Lab.",
            "Chaos Table เป็นเกมอินดี้ที่พัฒนาโดยคนเดียว ภายใต้ชื่อ Viberzix&#8217;s Lab") + '</p>'
  '<h3>' + t("AI disclosure", "การใช้ AI") + '</h3><p>' + t("AI tools were used only for programming and for the English, Simplified Chinese and Japanese translations. No generative AI was used for art, animation or audio.",
            "ใช้ AI เฉพาะงานเขียนโค้ดและการแปลภาษาอังกฤษ จีนตัวย่อ และญี่ปุ่น ไม่ใช้ Generative AI กับงานภาพ แอนิเมชัน หรือเสียง") + '</p></section>')

a('<section id="contact"><h2>' + t("Contact", "ติดต่อ") + '</h2><div class="contact">'
  '<p><span class="lbl">' + t("Email:", "อีเมล:") + '</span> <a href="mailto:viberzixlab@outlook.co.th">viberzixlab@outlook.co.th</a></p></div></section>')
a('<footer>© Viberzix&#39;s Lab · Chaos Table</footer>')
a('</main></div></div>')
a('<dialog id="lightbox"><img alt=""></dialog>')

js = r"""
/* ====== EDIT ME ====== */
const CONFIG = {
  trailerYouTubeId: "ggFYxW_-1vo",
  embedTrailer: EMBED,
  releaseEN: "November 2026", releaseTH: "พฤศจิกายน 2026",
  priceEN: "4.99 USD", priceTH: "99 บาท"
};
const html = document.documentElement;
function setLang(l){
  html.dataset.lang = l; html.lang = l;
  document.querySelectorAll('.langs button').forEach(b => b.setAttribute('aria-pressed', b.dataset.set === l));
  try { localStorage.setItem('ct-lang', l); } catch(e){}
  document.getElementById('factRelease').textContent = l==='th' ? CONFIG.releaseTH : CONFIG.releaseEN;
  document.getElementById('factPrice').textContent   = l==='th' ? CONFIG.priceTH   : CONFIG.priceEN;
}
document.querySelectorAll('.langs button').forEach(b => b.addEventListener('click', () => setLang(b.dataset.set)));
let start = 'en'; /* English by default for a global audience; a visitor's own choice is remembered below */
try { const s = localStorage.getItem('ct-lang'); if (s === 'en' || s === 'th') start = s; } catch(e){}

(function(){
  const id = CONFIG.trailerYouTubeId.trim();
  if (!id){ document.getElementById('trailer').hidden = true; document.getElementById('navTrailer').hidden = true; return; }
  const url = 'https://www.youtube.com/watch?v=' + encodeURIComponent(id);
  document.getElementById('trailerLink').href = url;
  const box = document.getElementById('trailerBox');
  box.innerHTML = CONFIG.embedTrailer
    ? '<iframe src="https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'" title="Chaos Table trailer" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe>'
    : '<a class="alt" target="_blank" rel="noopener" href="'+url+'"><img src="assets/thumbs/screenshots/shot-01-hero.jpg" alt=""><span>&#9654; Watch the trailer on YouTube</span></a>';
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
  try { await navigator.clipboard.writeText(text); b.textContent = l==='th' ? 'คัดลอกแล้ว' : 'Copied'; }
  catch(e){ const r = document.createRange(); r.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = l==='th' ? 'เลือกข้อความแล้ว กด Ctrl+C' : 'Text selected, press Ctrl+C'; }
  setTimeout(() => b.innerHTML = old, 1600);
}));
setLang(start);
""".replace("EMBED", "false" if PREVIEW else "true")

head = ('<meta name="claude:viewport-fit-sides" content="cover">\n<title>Chaos Table Press Kit</title>\n'
        '<meta name="description" content="Press kit for Chaos Table, an online social deduction party game for 6–10 players by Viberzix&#39;s Lab.">\n'
        '<meta property="og:title" content="Chaos Table Press Kit">\n<meta property="og:image" content="assets/store/ChaosTable_MainCapsule_1232x706.png">\n'
        '<link rel="icon" href="assets/logo/ChaosTable_Icon_512.png">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap" rel="stylesheet">\n'
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
