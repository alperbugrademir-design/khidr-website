import os
import sys
import base64
import pathlib
import webbrowser

calisma_klasoru = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, calisma_klasoru)





def mobil_uyumlu_yap(ham_html, panel_class, canvas_id):
    css_yamasi = f"""
    <style>
      @media (max-width: 900px) {{
        canvas#{canvas_id} {{ 
          flex: none !important; 
          height: 55vh !important; 
          width: 100% !important; 
        }}
        .{panel_class} {{ 
          position: fixed !important; 
          top: 0 !important; 
          left: 0 !important;
          transform: translateX(-100%) !important;
          width: 80% !important; 
          height: 100vh !important; 
          z-index: 20000 !important; 
          background: var(--bg, #08090d) !important;
          border-right: 1px solid var(--border, #2a2f3a) !important;
          transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
          padding-bottom: 100px !important;
          overflow-y: auto !important;
          -webkit-overflow-scrolling: touch !important;
          will-change: transform !important;
        }}
        .{panel_class}.open {{ 
          transform: translateX(0) !important;
        }}
        .evrensel-mobil-btn {{
          display: flex !important;
          align-items: center !important;
          justify-content: center !important;
          position: fixed !important;
          bottom: 25px !important;
          right: 25px !important;
          z-index: 20001 !important;
          width: 56px !important;
          height: 56px !important;
          border-radius: 50% !important;
          background: var(--accent, var(--cyan, #4fc3f7)) !important;
          color: #000 !important;
          font-size: 22px !important;
          border: none !important;
          box-shadow: 0 8px 25px rgba(0,0,0,0.6) !important;
          transition: all 0.2s !important;
          cursor: pointer !important;
        }}
        .evrensel-mobil-btn:active {{ transform: scale(0.9) !important; }}
        .main-container, .main-layout, .diagram-wrapper {{ 
          display: block !important; 
          flex-direction: column !important;
        }}
        .diagram-box, .diagram-area, .canvas-wrapper {{ 
          width: 100% !important; 
          padding: 4px !important; 
        }}
      }}
      @media (min-width: 901px) {{
        .evrensel-mobil-btn {{ display: none !important; }}
      }}
    </style>
    """
    js_yamasi = f"""
    <script>
      document.addEventListener("DOMContentLoaded", function() {{
        const btn = document.createElement("button");
        btn.className = "evrensel-mobil-btn";
        btn.setAttribute("aria-label", "Kontrol Paneli");
        btn.innerHTML = "&#9881;";
        document.body.appendChild(btn);
        
        const panel = document.querySelector(".{panel_class}");
        if (panel) {{
          btn.addEventListener("click", function(e) {{
            e.stopPropagation();
            const isOpen = panel.classList.toggle("open");
            btn.innerHTML = isOpen ? "&#10005;" : "&#9881;";
            btn.style.background = isOpen 
              ? "#ff1744" 
              : "var(--accent, var(--cyan, #4fc3f7))";
          }});
          document.addEventListener("click", function(e) {{
            if (panel.classList.contains("open") 
                && !panel.contains(e.target) 
                && e.target !== btn) {{
              panel.classList.remove("open");
              btn.innerHTML = "&#9881;";
              btn.style.background = "var(--accent, var(--cyan, #4fc3f7))";
            }}
          }});
        }}
      }});
    </script>
    """
    if "</head>" in ham_html:
        ham_html = ham_html.replace("</head>", css_yamasi + "</head>")
    if "</body>" in ham_html:
        ham_html = ham_html.replace("</body>", js_yamasi + "</body>")
    return ham_html

def modulu_hazirla(modul_adi, import_adi, html_degisken, panel_class, canvas_id, cikti_dosya):
    try:
        mod = __import__(modul_adi)
        kod = getattr(mod, html_degisken)
        kod = mobil_uyumlu_yap(kod, panel_class=panel_class, canvas_id=canvas_id)
        dosya = os.path.abspath(cikti_dosya)
        with open(dosya, 'w', encoding='utf-8') as f:
            f.write(kod)
        return pathlib.Path(dosya).as_uri()
    except ImportError:
        print(f"HATA: {modul_adi}.py bulunamadi!")
        return ""
    except Exception as ex:
        print(f"HATA ({modul_adi}): {ex}")
        return ""

ellingham_uri = modulu_hazirla(
    modul_adi    = "el_modul",
    import_adi   = "el_modul",
    html_degisken= "html_kodu",
    panel_class  = "left-panel",
    canvas_id    = "ellinghamCanvas",
    cikti_dosya  = "ellingham_mobil.html"
)

fec_uri = modulu_hazirla(
    modul_adi    = "demir_celik_faz",
    import_adi   = "demir_celik_faz",
    html_degisken= "html_kodu",
    panel_class  = "alloy-panel",
    canvas_id    = "fecCanvas",
    cikti_dosya  = "fec_mobil.html"
)

try:
    from ehph import html_kodu as ehph_kodu
    dosya = os.path.abspath("ehph_mobil.html")
    with open(dosya, 'w', encoding='utf-8') as f:
        f.write(ehph_kodu)
    ehph_uri = pathlib.Path(dosya).as_uri()
except ImportError:
    print("HATA: ehph.py bulunamadi!")
    ehph_uri = ""

try:
    from hizli_okuma import rsvp_html, rsvp_js
except ImportError:
    print("HATA: hizli_okuma.py bulunamadi!")
    rsvp_html = ""
    rsvp_js   = ""

html_kodu = r"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>Mühendislik Portalı</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow+Condensed:wght@300;400;600;700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0c10;
    --panel: #111318;
    --border: #2a2f3a;
    --accent: #e8a020;
    --accent2: #4fc3f7;
    --green: #4caf82;
    --red: #e05555;
    --text: #dde2ec;
    --dim: #6b7280;
    --mono: 'Share Tech Mono', monospace;
    --sans: 'Barlow Condensed', sans-serif;
  }

  * { margin:0; padding:0; box-sizing:border-box;
      -webkit-touch-callout:none; -webkit-user-select:none; user-select:none; }

  body {
    background:var(--bg); color:var(--text);
    font-family:var(--sans); min-height:100vh;
    display:flex; flex-direction:column; align-items:center;
    overflow-x:hidden;
  }

  body::before {
    content:''; position:fixed; inset:0;
    background-image:
      linear-gradient(rgba(78,195,247,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(78,195,247,0.03) 1px, transparent 1px);
    background-size:40px 40px; pointer-events:none; z-index:0;
  }

  .view-section {
    display:none; width:100%; max-width:820px;
    padding:24px 16px 60px; position:relative; z-index:1;
    animation:fadeIn 0.35s ease forwards;
  }
  .view-section.active { display:block; }

  @keyframes fadeIn   { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
  @keyframes slideIn  { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:translateX(0)} }
  @keyframes pop      { 0%{transform:scale(0.92)} 60%{transform:scale(1.04)} 100%{transform:scale(1)} }
  @keyframes shake    { 10%,90%{transform:translate3d(-1px,0,0)} 20%,80%{transform:translate3d(2px,0,0)} 30%,50%,70%{transform:translate3d(-4px,0,0)} 40%,60%{transform:translate3d(4px,0,0)} }
  @keyframes shakeTile{ 0%,100%{transform:translateX(0)} 25%{transform:translateX(-5px)} 75%{transform:translateX(5px)} }
  @keyframes swipeLeft { to{transform:translate(-200px,50px) rotate(-20deg);opacity:0} }
  @keyframes swipeRight{ to{transform:translate(200px,50px)  rotate(20deg); opacity:0} }

  .hero-header { text-align:center; margin-bottom:40px; padding-top:20px; }
  .hero-header h1 { font-size:clamp(40px,8vw,64px); font-weight:900; letter-spacing:-1px; line-height:1; color:#fff; }
  .hero-header h1 span { color:var(--accent2); }
  .hero-subtitle { margin-top:10px; font-size:16px; color:var(--dim); letter-spacing:2px; text-transform:uppercase; font-family:var(--mono); }

  .dashboard-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:20px; }

  .module-card {
    background:var(--panel); border:1px solid var(--border); border-radius:8px;
    padding:24px; transition:all 0.3s ease; display:flex; flex-direction:column;
    position:relative; overflow:hidden;
  }
  .module-card:hover { border-color:var(--accent); transform:translateY(-4px); box-shadow:0 10px 30px rgba(232,160,32,0.1); }
  .module-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,var(--accent),var(--accent2)); opacity:0; transition:opacity 0.3s; }
  .module-card:hover::before { opacity:1; }

  .module-tag { font-family:var(--mono); font-size:11px; color:var(--accent); letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
  .module-title { font-size:24px; font-weight:700; color:#fff; margin-bottom:12px; line-height:1.1; }
  .module-desc { font-size:14px; color:var(--dim); margin-bottom:24px; flex-grow:1; line-height:1.5; }

  .play-btn {
    background:var(--accent); color:#000; font-family:var(--sans); font-size:15px;
    font-weight:700; letter-spacing:2px; padding:12px; border:none; border-radius:4px;
    cursor:pointer; text-transform:uppercase; transition:filter 0.2s; width:100%;
  }
  .play-btn:active { filter:brightness(1.15); }

  .nav-bar { display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; }
  .back-btn {
    background:transparent; border:1px solid var(--border); color:var(--text);
    padding:8px 16px; border-radius:4px; cursor:pointer; font-family:var(--sans);
    font-weight:600; letter-spacing:1px; transition:background 0.2s;
  }
  .back-btn:hover { background:rgba(255,255,255,0.05); }

  .btn-primary {
    background:var(--accent); color:#000; font-family:var(--sans); font-size:15px;
    font-weight:700; letter-spacing:2px; text-transform:uppercase; padding:12px 28px;
    border-radius:4px; border:none; cursor:pointer; transition:all 0.2s;
  }
  .btn-primary:hover:not(:disabled) { filter:brightness(1.1); transform:translateY(-1px); }
  .btn-primary:disabled { background:var(--dim); cursor:not-allowed; opacity:0.7; }

  .lives-bar { text-align:center; font-size:22px; letter-spacing:4px; margin-bottom:24px; }
  .stat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:20px; }
  .stat-box { background:var(--panel); border:1px solid var(--border); border-radius:4px; padding:12px; text-align:center; }
  .stat-val { font-family:var(--mono); font-size:26px; color:var(--accent); display:block; }
  .stat-lbl { font-size:11px; color:var(--dim); letter-spacing:1px; text-transform:uppercase; margin-top:2px; }
  .high-score { color:var(--accent2); }

  .card {
    background:var(--panel); border:1px solid var(--border); border-radius:6px;
    padding:28px 28px 24px; margin-bottom:16px; position:relative; overflow:hidden;
  }
  .card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,transparent,var(--accent),transparent); }

  .shake { animation:shake 0.4s cubic-bezier(.36,.07,.19,.97) both; border-color:var(--red); }
  .shake::before { background:var(--red); }

  .timer-container { height:4px; background:rgba(255,255,255,0.05); border-radius:2px; margin-bottom:20px; overflow:hidden; }
  .timer-fill { height:100%; background:var(--green); transition:width 0.1s linear, background-color 0.4s ease; }
  .timer-fill.warning { background:var(--accent); }
  .timer-fill.danger  { background:var(--red); }

  .steel-label { font-family:var(--mono); font-size:11px; letter-spacing:3px; color:var(--dim); text-transform:uppercase; margin-bottom:12px; }
  .steel-name { font-family:var(--mono); font-size:clamp(36px,8vw,68px); font-weight:700; color:var(--accent); letter-spacing:2px; line-height:1; margin-bottom:6px; text-shadow:0 0 40px rgba(232,160,32,0.3); }
  .steel-name.new { animation:pop 0.4s ease; }

  .hint-row { display:flex; gap:8px; flex-wrap:wrap; margin-top:14px; }
  .hint-chip {
    background:rgba(78,195,247,0.08); border:1px solid rgba(78,195,247,0.2);
    border-radius:3px; padding:4px 10px; font-size:12px; font-family:var(--mono);
    color:var(--accent2); cursor:pointer;
  }

  .checklist { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:16px; margin-top:20px; }
  @media (max-width:520px) { .checklist { grid-template-columns:1fr; } }
  .check-item {
    display:flex; align-items:center; gap:10px; background:var(--bg);
    border:1px solid var(--border); border-radius:4px; padding:10px 14px;
    cursor:pointer; transition:border-color 0.2s, background 0.2s;
  }
  .check-item.selected { border-color:var(--accent2); background:rgba(78,195,247,0.06); }
  .check-item.correct  { border-color:var(--green); background:rgba(76,175,130,0.1); }
  .check-item.wrong    { border-color:var(--red);   background:rgba(224,85,85,0.08); }
  .check-box {
    width:18px; height:18px; border:1.5px solid var(--border); border-radius:3px;
    flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:11px;
  }
  .check-item.selected .check-box { border-color:var(--accent2); background:var(--accent2); color:#000; }
  .check-item.correct  .check-box { border-color:var(--green); background:var(--green); color:#000; }
  .check-item.wrong    .check-box { border-color:var(--red);   background:var(--red);   color:#fff; }

  .feedback { margin-top:16px; padding:16px 18px; border-radius:4px; border-left:3px solid; font-size:14px; line-height:1.7; display:none; }
  .feedback.show { display:block; animation:slideIn 0.3s ease; }
  .feedback.correct-fb { border-color:var(--green); background:rgba(76,175,130,0.07); }
  .feedback.partial-fb { border-color:var(--accent); background:rgba(232,160,32,0.07); }
  .feedback.wrong-fb, .feedback.timeout-fb { border-color:var(--red); background:rgba(224,85,85,0.07); }
  .feedback-title { font-size:16px; font-weight:700; letter-spacing:1px; margin-bottom:8px; }

  .breakdown { display:none; margin-top:20px; background:var(--bg); border:1px solid var(--border); border-radius:4px; overflow:hidden; }
  .breakdown.show { display:block; }
  .breakdown-title { padding:10px 16px; font-size:11px; letter-spacing:3px; color:var(--dim); font-family:var(--mono); border-bottom:1px solid var(--border); text-transform:uppercase; }
  .breakdown-row { display:flex; align-items:center; gap:10px; padding:9px 16px; border-bottom:1px solid rgba(42,47,58,0.5); font-size:13px; }
  .bd-token { font-family:var(--mono); color:var(--accent); min-width:80px; font-size:14px; }
  .bd-meaning { color:var(--text); flex:1; }
  .bd-category { font-size:11px; padding:2px 8px; border-radius:2px; background:rgba(78,195,247,0.1); color:var(--accent2); font-family:var(--mono); }

  .modal-overlay {
    position:fixed; inset:0; background:rgba(10,12,16,0.95);
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    z-index:9999; opacity:0; pointer-events:none; transition:opacity 0.3s ease;
    backdrop-filter:blur(5px);
  }
  .modal-overlay.show { opacity:1; pointer-events:auto; }
  .modal-content { text-align:center; max-width:400px; padding:30px; }
  .modal-title { font-size:64px; font-weight:900; color:var(--red); letter-spacing:2px; line-height:1; margin-bottom:10px; }
  .modal-score { font-family:var(--mono); font-size:48px; color:var(--accent); margin:20px 0; }
  .modal-record { font-size:18px; color:var(--accent2); margin-bottom:30px; font-weight:600; display:none; animation:slideIn 0.5s ease; }

  .dt-header { text-align:center; margin-bottom:30px; }
  .dt-scenario {
    background:rgba(78,195,247,0.05); border:1px solid rgba(78,195,247,0.2);
    padding:16px; border-radius:6px; color:var(--accent2); font-family:var(--mono);
    font-size:14px; line-height:1.5; margin-bottom:24px; border-left:4px solid var(--accent2);
  }
  .dt-question-box { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:30px 20px; text-align:center; margin-bottom:20px; }
  .dt-question-text { font-size:22px; font-weight:600; color:#fff; margin-bottom:30px; line-height:1.4; }
  .dt-options { display:flex; flex-direction:column; gap:12px; }
  .dt-btn {
    background:var(--bg); border:1px solid var(--border); color:var(--text);
    padding:16px 20px; font-size:16px; font-family:var(--sans); border-radius:6px;
    cursor:pointer; transition:all 0.2s ease; text-align:left;
    display:flex; align-items:center; gap:15px;
  }
  .dt-btn:hover { border-color:var(--accent); background:rgba(232,160,32,0.05); transform:translateX(5px); }
  .dt-btn-icon {
    background:var(--panel); color:var(--accent); width:30px; height:30px;
    display:flex; justify-content:center; align-items:center; border-radius:4px;
    font-weight:900; font-family:var(--mono); flex-shrink:0; border:1px solid var(--border);
  }
  .dt-result-box {
    display:none; background:var(--panel); border:1px solid var(--green);
    border-radius:6px; padding:30px; text-align:center; border-top:4px solid var(--green);
  }
  .dt-result-title { font-size:32px; font-weight:900; color:var(--green); letter-spacing:1px; margin-bottom:10px; text-transform:uppercase; }
  .dt-result-desc { font-size:16px; color:var(--text); line-height:1.6; margin-bottom:24px; }

  .fc-container { position:relative; width:100%; max-width:360px; height:420px; margin:0 auto 30px; perspective:1000px; }
  .fc-card {
    position:absolute; width:100%; height:100%; transform-style:preserve-3d;
    transition:transform 0.4s cubic-bezier(0.175,0.885,0.32,1.275);
    cursor:grab; border-radius:12px; box-shadow:0 15px 35px rgba(0,0,0,0.4);
  }
  .fc-card.is-flipped { transform:rotateY(180deg); }
  .fc-face {
    position:absolute; width:100%; height:100%; backface-visibility:hidden;
    display:flex; flex-direction:column; justify-content:center; align-items:center;
    padding:30px; border-radius:12px; border:1px solid var(--border); text-align:center;
  }
  .fc-front { background:var(--panel); color:var(--accent2); }
  .fc-back  { background:var(--bg); color:var(--text); transform:rotateY(180deg); border-color:var(--green); }
  .fc-title { font-family:var(--mono); font-size:14px; letter-spacing:2px; color:var(--dim); margin-bottom:20px; text-transform:uppercase; }
  .fc-content { font-size:28px; font-weight:700; line-height:1.3; }
  .fc-back .fc-content { font-size:18px; font-weight:400; color:#fff; line-height:1.6; }
  .fc-controls { display:flex; justify-content:center; gap:20px; margin-top:20px; }
  .fc-btn { width:60px; height:60px; border-radius:50%; border:none; font-size:24px; cursor:pointer; display:flex; justify-content:center; align-items:center; transition:transform 0.2s; box-shadow:0 5px 15px rgba(0,0,0,0.3); }
  .fc-btn:active { transform:scale(0.9); }
  .fc-btn-wrong   { background:rgba(224,85,85,0.1);  color:var(--red);   border:2px solid var(--red); }
  .fc-btn-flip    { background:var(--panel); color:var(--text); border:2px solid var(--border); width:auto; padding:0 30px; border-radius:30px; font-family:var(--sans); font-weight:700; letter-spacing:1px; }
  .fc-btn-correct { background:rgba(76,175,130,0.1); color:var(--green); border:2px solid var(--green); }
  .swipe-left  { animation:swipeLeft  0.5s forwards; }
  .swipe-right { animation:swipeRight 0.5s forwards; }
  .fc-progress { text-align:center; font-family:var(--mono); color:var(--dim); margin-bottom:20px; letter-spacing:2px; }

  .wordle-clue {
    background:rgba(78,195,247,0.08); border:1px solid rgba(78,195,247,0.2);
    padding:15px; border-radius:8px; color:var(--accent2); font-family:var(--mono);
    font-size:14px; line-height:1.4; margin-bottom:20px; text-align:center;
  }
  .wordle-board { width:100%; max-width:450px; margin:0 auto 20px; }
  .wordle-row { display:grid; gap:4px; width:100%; justify-content:center; margin-bottom:4px; }
  .wordle-tile {
    width:100%; aspect-ratio:1/1; min-height:36px;
    border:2px solid var(--border); border-radius:4px;
    display:flex; justify-content:center; align-items:center;
    font-size:clamp(13px,5vw,24px); font-weight:700; color:#fff;
    text-transform:uppercase; background:var(--bg);
    touch-action:manipulation; user-select:none;
  }
  .wordle-tile.filled  { border-color:var(--dim); }
  .wordle-tile.correct { background:var(--green); border-color:var(--green); color:#000; }
  .wordle-tile.present { background:var(--accent); border-color:var(--accent); color:#000; }
  .wordle-tile.absent  { background:var(--panel); border-color:var(--panel); color:var(--dim); }
  .flip-anim { animation: flipTile 0.5s ease forwards; }
  .shake-anim { animation:shakeTile 0.4s ease; }

  .keyboard { display:flex; flex-direction:column; gap:6px; width:100%; max-width:500px; margin:0 auto; }
  .key-row  { display:flex; justify-content:center; gap:4px; }
  .key {
    background:var(--panel); border:1px solid var(--border); color:var(--text);
    font-family:var(--sans); font-weight:600; font-size:clamp(11px,3.2vw,16px);
    border-radius:4px; padding:14px 0; min-width:0; flex:1;
    cursor:pointer; display:flex; justify-content:center; align-items:center;
    text-transform:uppercase; touch-action:manipulation; user-select:none;
    min-height:44px; -webkit-tap-highlight-color:transparent;
  }
  .key:active { opacity:0.6; }
  .key.wide { flex:1.5; font-size:11px; letter-spacing:1px; }
  .key.correct { background:var(--green); border-color:var(--green); color:#000; }
  .key.present { background:var(--accent); border-color:var(--accent); color:#000; }
  .key.absent  { background:rgba(255,255,255,0.05); border-color:transparent; color:var(--dim); opacity:0.5; }

  .iframe-wrap {
    position:relative; width:100%; height:80vh; min-height:500px;
    border-radius:8px; border:1px solid var(--border); overflow:hidden;
    -webkit-overflow-scrolling:touch;
  }
  .iframe-wrap iframe {
    position:absolute; top:0; left:0; width:100%; height:100%;
    border:none; background:var(--bg);
  }
</style>
</head>
<body>

<div class="modal-overlay" id="gameOverModal">
  <div class="modal-content">
    <div class="modal-title">GAME OVER</div>
    <div style="color:var(--dim);font-size:16px;letter-spacing:2px;">TOPLAM PUAN</div>
    <div class="modal-score" id="finalScoreDisplay">0</div>
    <div class="modal-record" id="newRecordAlert">🏆 YENİ REKOR! 🏆</div>
    <button class="btn-primary" onclick="restartGame()" style="width:100%;margin-bottom:10px;">TEKRAR OYNA</button>
    <button class="back-btn" onclick="document.getElementById('gameOverModal').classList.remove('show');goHome();" style="width:100%;">ANA MENÜYE DÖN</button>
  </div>
</div>

<div id="homeView" class="view-section active">
  <div class="hero-header">
    <h1>MÜHENDİSLİK <span>PORTALI</span></h1>
    <div class="hero-subtitle">// İnteraktif Eğitim & Pratik Modülleri //</div>
  </div>
  <div class="dashboard-grid">
    <div class="module-card">
      <div class="module-tag">HIZLI OKUMA</div>
      <div class="module-title">RSVP E-Kitap Okuyucu</div>
      <div class="module-desc">Kelimeleri tek bir odak noktasında sabitleyerek zaman kaybını önle.</div>
      <button class="play-btn" onclick="openView('fastReadView')">OKUMAYA BAŞLA</button>
    </div>
    <div class="module-card">
      <div class="module-tag">EN 10020 & AISI</div>
      <div class="module-title">Çelik İsimlendirme Quizi</div>
      <div class="module-desc">Standartlara göre çeliklerin harf ve rakam analizini yaparak malzeme bilgisini test et. Hıza dayalı hayatta kalma modu.</div>
      <button class="play-btn" onclick="openView('quizView')">MODÜLÜ BAŞLAT</button>
    </div>
    <div class="module-card">
      <div class="module-tag">FRAKTOGRAFİ & NDT</div>
      <div class="module-title">Hasar Analizi Simülatörü</div>
      <div class="module-desc">Kırılan bir parçanın yüzeyini incele. Adım adım kırılma türünü ve kök nedeni tespit et.</div>
      <button class="play-btn" style="background:var(--accent2);" onclick="openView('decisionView')">VAKAYI İNCELE</button>
    </div>
    <div class="module-card">
      <div class="module-tag">MET344</div>
      <div class="module-title">Kavram Kartları</div>
      <div class="module-desc">Mekanik ve malzeme tanımlarını sağa/sola kaydırarak ezberle. Yanlış bildiklerin desteye geri döner.</div>
      <button class="play-btn" style="background:var(--green);" onclick="openView('flashcardView')">DESTEYİ AÇ</button>
    </div>
    <div class="module-card">
      <div class="module-tag">KAVRAM BULMACA</div>
      <div class="module-title">MET-WORDLE</div>
      <div class="module-desc">İpuçlarını oku ve gizli metalurji terimini tahmin et. Yeşil doğru yer, Sarı yanlış yer, Gri yok demektir.</div>
      <button class="play-btn" style="background:var(--accent2);" onclick="openView('wordleView')">ŞİFREYİ ÇÖZ</button>
    </div>
    <div class="module-card">
      <div class="module-tag">TERMODİNAMİK</div>
      <div class="module-title">Ellingham Diyagramı</div>
      <div class="module-desc">Metal oksitlerin Gibbs enerjisini ve indirgenme sıcaklıklarını interaktif grafik üzerinde analiz et.</div>
      <button class="play-btn" style="background:#e74c3c;" onclick="openView('ellinghamView')">LABORATUVARA GİR</button>
    </div>
    <div class="module-card">
      <div class="module-tag">MET211 & MET344</div>
      <div class="module-title">Fe-C Faz Diyagramı</div>
      <div class="module-desc">Demir-Karbon denge diyagramında gezin. Faz bölgelerini, kritik sıcaklıkları ve mikroyapıları analiz et.</div>
      <button class="play-btn" style="background:#a29bfe;" onclick="openView('feCView')">DİYAGRAMI AÇ</button>
    </div>
    <div class="module-card">
      <div class="module-tag">ELEKTROKİMYA</div>
      <div class="module-title">Eh-pH Pourbaix Diyagramı</div>
      <div class="module-desc">10 metal için termodinamik kararlılık bölgelerini analiz et. Sıcaklık, konsantrasyon kontrolü ve sementasyon tespiti.</div>
      <button class="play-btn" style="background:linear-gradient(135deg,#0077b6,#00b4d8);" onclick="openView('ehphView')">DİYAGRAMI AÇ</button>
    </div>
  </div>
</div>

<div id="fastReadView" class="view-section">
  RSVP_HTML_BURAYA
</div>

<div id="quizView" class="view-section">
  <div class="nav-bar">
    <button class="back-btn" onclick="goHome()">← Ana Menü</button>
    <span style="font-family:var(--mono);font-size:12px;color:var(--dim);">EN 10020</span>
  </div>
  <div class="lives-bar" id="livesBar">❤️❤️❤️</div>
  <div class="stat-grid">
    <div class="stat-box"><span class="stat-val" id="totalScore">0</span><div class="stat-lbl">Puan</div></div>
    <div class="stat-box"><span class="stat-val" id="streakVal">0</span><div class="stat-lbl">Seri 🔥</div></div>
    <div class="stat-box"><span class="stat-val high-score" id="highScoreVal">0</span><div class="stat-lbl">Rekor 🏆</div></div>
  </div>
  <div class="card" id="mainCard">
    <div class="timer-container"><div class="timer-fill" id="timerFill"></div></div>
    <div class="steel-label">Bu çeliğin tüm özelliklerini belirleyin:</div>
    <div class="steel-name" id="steelDisplay">—</div>
    <div class="hint-row" id="hintRow"></div>
    <div>
      <label style="font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:2px;">// Doğru olan tüm özellikleri seçin</label>
      <div class="checklist" id="checklist"></div>
      <button class="btn-primary" id="submitBtn" onclick="submitAnswer()" style="width:100%;margin-top:15px;">CEVAPLA</button>
    </div>
    <div class="feedback" id="feedback">
      <div class="feedback-title" id="fbTitle"></div>
      <div id="fbBody"></div>
    </div>
  </div>
  <div class="breakdown" id="breakdown">
    <div class="breakdown-title">// Detaylı Analiz</div>
    <div id="breakdownRows"></div>
  </div>
</div>

<div id="decisionView" class="view-section">
  <div class="nav-bar">
    <button class="back-btn" onclick="goHome()">← Ana Menü</button>
    <span style="font-family:var(--mono);font-size:12px;color:var(--accent2);">Root Cause Analysis</span>
  </div>
  <div class="dt-header">
    <h1 style="font-size:36px;font-weight:900;margin-bottom:8px;">DEDEKTİF <span style="color:var(--accent2);">MODU</span></h1>
    <div style="color:var(--dim);font-size:14px;letter-spacing:1px;">Adım Adım Kırılma Teşhisi</div>
  </div>
  <div class="dt-scenario" id="dtScenario">
    <strong>VAKA #001:</strong> Şanzımandaki 42CrMo4 dişli, makine devreye alındıktan 6 ay sonra aniden kırılmış. Parça laboratuvara geldi. Mikroskobu açtın...
  </div>
  <div class="dt-question-box" id="dtQuestionBox">
    <div class="dt-question-text" id="dtQuestionText">Yükleniyor...</div>
    <div class="dt-options" id="dtOptions"></div>
  </div>
  <div class="dt-result-box" id="dtResultBox">
    <div class="module-tag" style="color:var(--green);margin-bottom:10px;">TEŞHİS TAMAMLANDI</div>
    <div class="dt-result-title" id="dtResultTitle"></div>
    <div class="dt-result-desc" id="dtResultDesc"></div>
    <button class="btn-primary" onclick="startDecisionTree()" style="width:100%;margin-bottom:10px;">YENİ VAKA İNCELE</button>
    <button class="back-btn" onclick="goHome()" style="width:100%;">ANA MENÜYE DÖN</button>
  </div>
</div>

<div id="flashcardView" class="view-section">
  <div class="nav-bar">
    <button class="back-btn" onclick="goHome()">← Ana Menü</button>
    <span style="font-family:var(--mono);font-size:12px;color:var(--green);">MET344</span>
  </div>
  <h1 style="font-size:36px;font-weight:900;text-align:center;margin-bottom:20px;">KAVRAM <span style="color:var(--green);">KARTLARI</span></h1>
  <div class="fc-progress" id="fcProgress">Kalan Kart: 0</div>
  <div class="fc-container" id="fcContainer"></div>
  <div class="fc-controls" id="fcControls">
    <button class="fc-btn fc-btn-wrong"   onclick="swipeCard('left')">✗</button>
    <button class="fc-btn fc-btn-flip"    onclick="flipCard()">ÇEVİR</button>
    <button class="fc-btn fc-btn-correct" onclick="swipeCard('right')">✓</button>
  </div>
  <div class="dt-result-box" id="fcResultBox" style="display:none;border-color:var(--green);">
    <div class="dt-result-title" style="color:var(--green);">MÜKEMMEL!</div>
    <div class="dt-result-desc">Tüm MET344 destesini başarıyla ezberledin!</div>
    <button class="btn-primary" onclick="startFlashcards()" style="width:100%;margin-bottom:10px;background:var(--green);">TEKRAR ÇALIŞ</button>
    <button class="back-btn" onclick="goHome()" style="width:100%;">ANA MENÜYE DÖN</button>
  </div>
</div>

<div id="wordleView" class="view-section">
  <div class="nav-bar">
    <button class="back-btn" onclick="goHome()">← Ana Menü</button>
    <span style="font-family:var(--mono);font-size:12px;color:var(--accent2);">Met-Wordle</span>
  </div>
  <h1 style="font-size:36px;font-weight:900;text-align:center;margin-bottom:16px;">GİZLİ <span style="color:var(--accent2);">TERİM</span></h1>
  <div class="wordle-clue" id="wordleClue">İpucu yükleniyor...</div>
  <div class="wordle-board" id="wordleBoard"></div>
  <input type="text" id="gizliInput"
    autocapitalize="off" autocomplete="off" autocorrect="off" spellcheck="false"
    style="position:fixed;opacity:0;pointer-events:none;top:-100px;left:0;width:1px;height:1px;">
  <div style="text-align:center;margin-bottom:12px;">
    <button class="back-btn" style="color:var(--accent2);border-color:var(--accent2);font-size:12px;border-radius:20px;"
      onclick="document.getElementById('gizliInput').focus()">📱 Sistem Klavyesi</button>
  </div>
  <div class="keyboard" id="keyboard"></div>
  <div class="dt-result-box" id="wordleResultBox" style="display:none;margin-top:20px;">
    <div class="dt-result-title" id="wordleResultTitle">TEBRİKLER!</div>
    <div class="dt-result-desc"  id="wordleResultDesc"></div>
    <button class="btn-primary" onclick="startWordle()" style="width:100%;margin-bottom:10px;background:var(--accent2);">YENİ KELİME</button>
    <button class="back-btn" onclick="goHome()" style="width:100%;">ANA MENÜYE DÖN</button>
  </div>
</div>

<div id="ellinghamView" class="view-section" style="max-width:1200px;">
  <div class="nav-bar">
    <button class="back-btn" onclick="goHome()">← Ana Menü</button>
    <span style="font-family:var(--mono);font-size:12px;color:#e74c3c;">Simülasyon</span>
  </div>
  <div class="iframe-wrap">
    <iframe id="ellinghamFrame" src="ELLINGHAM_URI_BURAYA" allowfullscreen></iframe>
  </div>
</div>

<div id="feCView" class="view-section" style="max-width:1200px;">
  <div class="nav-bar">
    <button class="back-btn" onclick="goHome()">← Ana Menü</button>
    <span style="font-family:var(--mono);font-size:12px;color:#a29bfe;">Termodinamik Denge</span>
  </div>
  <div class="iframe-wrap">
    <iframe id="fecFrame" src="FEC_URI_BURAYA" allowfullscreen></iframe>
  </div>
</div>

<div id="ehphView" class="view-section" style="max-width:1200px;">
  <div class="nav-bar">
    <button class="back-btn" onclick="goHome()">← Ana Menü</button>
    <span style="font-family:var(--mono);font-size:12px;color:#00b4d8;">Elektrokimya</span>
  </div>
  <div class="iframe-wrap">
    <iframe id="ehphFrame" src="EHPH_URI_BURAYA" allowfullscreen></iframe>
  </div>
</div>

<script>
function openView(viewId) {
  document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
  document.getElementById(viewId).classList.add('active');
  window.scrollTo(0, 0);
  if (viewId === 'quizView')           { if (state.total === 0) initQuiz(); else startTimer(); }
  else if (viewId === 'decisionView')  { startDecisionTree(); }
  else if (viewId === 'flashcardView') { startFlashcards(); }
  else if (viewId === 'wordleView')    { startWordle(); }
  else if (viewId === 'fastReadView')  { if (typeof rsvpIndex !== 'undefined' && rsvpIndex === 0) displayRSVPWord(rsvpWords[0]); }
}

function goHome() {
  document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
  document.getElementById('homeView').classList.add('active');
  clearInterval(timerInterval);
  if (typeof stopRSVP === 'function') stopRSVP();
}

RSVP_JS_BURAYA

// ═══════════════════ MODÜL 1: ÇELİK QUİZİ ═══════════════════
const STEELS = [
  { name: "S235JR", category: "structural", correct: ["Yapı Çeliği (S)", "Min. 235 MPa akma dayanımı", "27J darbe dayanımı (20°C)", "Genel yapı amaçlı"], distractors: ["Min. 355 MPa akma", "Paslanmaz çelik", "Takım çeliği", "-20°C'de test"], breakdown: [ { token: "S", meaning: "Structural – Yapı/İnşaat çeliği", cat: "TİP" }, { token: "235", meaning: "Min. akma dayanımı: 235 MPa", cat: "DAYANIM" }, { token: "J", meaning: "Charpy V-çentik (27J)", cat: "DARBE" }, { token: "R", meaning: "Oda sıcaklığı (+20°C)", cat: "SICAKLIK" } ], explanation: "En yaygın yapı çeliği. İnşaatlarda, köprülerde, genel mühendislik uygulamalarında kullanılır." },
  { name: "S355J2", category: "structural", correct: ["Yapı Çeliği (S)", "Min. 355 MPa akma dayanımı", "27J darbe dayanımı (-20°C)", "Yüksek dayanımlı yapı çeliği"], distractors: ["Min. 235 MPa akma", "+20°C'de darbe testi", "Otomasyon çeliği", "Paslanmaz çelik"], breakdown: [ { token: "S", meaning: "Structural – Yapı çeliği", cat: "TİP" }, { token: "355", meaning: "Min. akma dayanımı: 355 MPa", cat: "DAYANIM" }, { token: "J", meaning: "Charpy V-çentik (27J)", cat: "DARBE" }, { token: "2", meaning: "-20°C'de Charpy testi", cat: "SICAKLIK" } ], explanation: "Yüksek dayanımlı yapı çeliği. Ağır çelik konstrüksiyonlar, vinçler için tercih edilir." },
  { name: "C45", category: "special", correct: ["Kaliteli karbonlu çelik", "Alaşımsız çelik", "%0,45 C karbon içeriği", "Orta karbonlu, sertleştirilebilir"], distractors: ["Alaşımlı çelik", "Paslanmaz çelik", "Yapı çeliği (S)", "Düşük karbonlu"], breakdown: [ { token: "C", meaning: "Carbon steel – Kaliteli alaşımsız çelik", cat: "TİP" }, { token: "45", meaning: "Ortalama karbon: 0,45% C", cat: "KARBON" } ], explanation: "En çok kullanılan mühendislik çeliği. Mil, dişli ve bağlantı elemanları için idealdir." },
  { name: "42CrMo4", category: "special", correct: ["Islah çeliği", "Krom-Molibden alaşımlı", "%0,42 C karbon içeriği", "Su verme + temperlenebilir"], distractors: ["Sementasyon çeliği", "Paslanmaz çelik", "Yapı çeliği (S)", "Düşük karbonlu"], breakdown: [ { token: "42", meaning: "Karbon: 0,42% C", cat: "KARBON" }, { token: "Cr", meaning: "Krom (Cr)", cat: "ALAŞIM" }, { token: "Mo", meaning: "Molibden (Mo)", cat: "ALAŞIM" }, { token: "4", meaning: "Cr içeriği: 4/4 = %1,0 Cr", cat: "ORAN" } ], explanation: "Yüksek dayanım ve tokluk sunar (4140). Krank mili, akslar, dişliler için." },
  { name: "X155CrVMo12-1", category: "tool", correct: ["Takım çeliği", "Paslanmaz yüksek alaşımlı (X)", "Yüksek karbon: %1,55 C", "D2 soğuk iş takım çeliği"], distractors: ["Yapı çeliği", "Düşük karbonlu", "Min. 355 MPa akma", "Östenitik paslanmaz"], breakdown: [ { token: "X", meaning: "Yüksek alaşımlı çelik", cat: "TİP" }, { token: "155", meaning: "Karbon: 1,55% C (Çok yüksek)", cat: "KARBON" }, { token: "CrVMo", meaning: "Krom, Vanadyum, Molibden", cat: "ALAŞIM" }, { token: "12-1", meaning: "%12 Cr, %1 Mo/V", cat: "ORAN" } ], explanation: "D2 çeliği. Mükemmel aşınma direnci. Soğuk kesme kalıplarında kullanılır." },
  { name: "34CrNiMo6", category: "special", correct: ["Alaşımlı ıslah çeliği", "%0,34 C karbon içeriği", "Cr-Ni-Mo alaşımlı", "Yüksek tokluk ve mukavemet"], distractors: ["Paslanmaz çelik (X)", "Yapı çeliği (S)", "%3,4 Karbon", "Sementasyon çeliği"], breakdown: [ { token: "34", meaning: "Ortalama karbon: %0,34 C", cat: "KARBON" }, { token: "CrNiMo", meaning: "Krom, Nikel, Molibden", cat: "ALAŞIM" }, { token: "6", meaning: "Cr içeriği: 6/4 = %1,5 Cr", cat: "ORAN" } ], explanation: "Ağır sanayide yüksek mukavemet/tokluk gerektiren rüzgar türbini milleri, kranklar için kullanılan ıslah çeliğidir." },
  { name: "X2CrNiMo18-14-3", category: "stainless", correct: ["Paslanmaz çelik (X)", "Max %0,02 C (Ekstra düşük karbon)", "%18 Cr - %14 Ni - %3 Mo", "Klorür korozyonuna dirençli"], distractors: ["Yapı çeliği (S)", "Martensitik paslanmaz", "Yüksek karbonlu takım çeliği", "Molibden içermez"], breakdown: [ { token: "X", meaning: "Paslanmaz / Yüksek Alaşımlı", cat: "TİP" }, { token: "2", meaning: "Max karbon: %0,02 C", cat: "KARBON" }, { token: "CrNiMo", meaning: "Krom, Nikel, Molibden", cat: "ALAŞIM" }, { token: "18-14-3", meaning: "%18 Cr, %14 Ni, %3 Mo", cat: "ORAN" } ], explanation: "316L ailesinden yüksek korozyon dirençli östenitik paslanmaz çelik. Medikal ve kimya endüstrisinde kullanılır." },
  { name: "11SMnPbTe30", category: "special", correct: ["Otomat çeliği (Serbest kesim)", "Kükürt (S) ve Kurşun (Pb) içerir", "%0,11 C karbon", "Tellür (Te) ilaveli"], distractors: ["Paslanmaz çelik", "Yüksek tokluklu yapı çeliği", "Kaynak kabiliyeti çok yüksek", "Islah çeliği"], breakdown: [ { token: "11", meaning: "Karbon: %0,11 C (Düşük karbon)", cat: "KARBON" }, { token: "S", meaning: "Kükürt (S) - Talaş kırıcı", cat: "ALAŞIM" }, { token: "MnPbTe", meaning: "Mangan, Kurşun, Tellür", cat: "ALAŞIM" }, { token: "30", meaning: "Kükürt içeriği: %0,30 S", cat: "ORAN" } ], explanation: "CNC tezgahlarında hızlı işlenebilmesi için kükürt, kurşun ve tellür ilave edilen otomat çeliğidir." },
  { name: "H13", category: "tool", correct: ["Amerikan (AISI/SAE) standardı", "Sıcak iş takım çeliği", "Yüksek ısıl yorulma direnci", "EN karşılığı: X40CrMoV5-1"], distractors: ["EN 10020 standardı", "Paslanmaz çelik", "Yapı çeliği (S)", "Soğuk iş takım çeliği"], breakdown: [ { token: "H", meaning: "Hot Work - Sıcak iş takım çeliği (AISI)", cat: "TİP" }, { token: "13", meaning: "Alaşım sınıflandırma numarası", cat: "KOD" } ], explanation: "TUZAK SORU! H13, EN 10020 değil AISI standardıdır. En yaygın sıcak iş kalıp çeliğidir." },
  { name: "S355K2G2W+NT", category: "structural", correct: ["Yapı Çeliği (S)", "Atmosferik korozyon direnci (W)", "Min. 355 MPa akma dayanımı", "Normalize ve Meneviş (+NT)"], distractors: ["Paslanmaz çelik", "Sıcak haddelenmiş teslim (+AR)", "-40°C'de test edilmiş", "Yüksek alaşımlı çelik"], breakdown: [ { token: "S", meaning: "Structural - Yapı çeliği", cat: "TİP" }, { token: "355", meaning: "Min. akma dayanımı: 355 MPa", cat: "DAYANIM" }, { token: "K2", meaning: "Charpy V-çentik: 40J (-20°C)", cat: "DARBE" }, { token: "W", meaning: "Weathering - Atmosferik korozyon direnci", cat: "ÖZELLİK" }, { token: "+NT", meaning: "Normalized and Tempered", cat: "DURUM" } ], explanation: "'Corten çeliği' olarak bilinen, boya gerektirmeyen atmosferik korozyon dirençli yapı çeliğidir." },
  { name: "R320Cr", category: "special", correct: ["Ray Çeliği (R)", "Min. 320 HBW Sertlik", "Krom (Cr) alaşımlı", "Aşınma direnci yüksek"], distractors: ["Rulman çeliği (R)", "Min. 320 MPa akma dayanımı", "Soğuk şekillendirme çeliği", "Paslanmaz çelik"], breakdown: [ { token: "R", meaning: "Rail - Ray çeliği", cat: "TİP" }, { token: "320", meaning: "Minimum sertlik: 320 HBW", cat: "DAYANIM" }, { token: "Cr", meaning: "Krom ilaveli", cat: "ALAŞIM" } ], explanation: "Demiryollarında aşınma direnci için krom ilave edilmiş, min. 320 HBW sertliğe sahip ray çeliğidir." },
  { name: "HC260LA", category: "special", correct: ["Soğuk şekillendirmeye uygun (H)", "Soğuk haddelenmiş (C)", "Min. 260 MPa akma dayanımı", "Mikro alaşımlı (LA)"], distractors: ["Sıcak haddelenmiş (D)", "Min. 260 HBW sertlik", "Yüksek karbonlu çelik", "Sıcak iş takım çeliği"], breakdown: [ { token: "H", meaning: "High strength - Soğuk şekillendirmeye uygun", cat: "TİP" }, { token: "C", meaning: "Cold rolled - Soğuk haddelenmiş", cat: "ÜRETİM" }, { token: "260", meaning: "Min. akma dayanımı: 260 MPa", cat: "DAYANIM" }, { token: "LA", meaning: "Low Alloy - Mikro alaşımlı", cat: "ALAŞIM" } ], explanation: "Otomotiv gövde parçalarında kullanılan yüksek şekillendirilebilir mikro alaşımlı çeliktir." }
];

const HINTS = { structural: ["S yapı çeliğidir"], stainless: ["X ≥5% alaşım içeriğidir"], tool: ["Yüksek C ve X içerir"], special: ["Alaşımsızlar C ile başlar"] };

let _hs = 0;
try { _hs = parseInt(localStorage.getItem('steelHS') || '0') || 0; } catch(e) {}
let state = { current: null, options: [], answered: false, score: 0, streak: 0, lives: 3, hintsUsed: 0, total: 0, highScore: _hs };
const TIME_LIMIT = 20;
let timeLeft = TIME_LIMIT;
let timerInterval = null;

function initQuiz() { document.getElementById('highScoreVal').textContent = state.highScore; updateLivesUI(); nextQuestion(); }

function startTimer() {
  clearInterval(timerInterval);
  timeLeft = TIME_LIMIT;
  updateTimerUI();
  timerInterval = setInterval(() => {
    timeLeft = Math.max(0, timeLeft - 0.1);
    updateTimerUI();
    if (timeLeft <= 0) { clearInterval(timerInterval); handleTimeout(); }
  }, 100);
}

function updateTimerUI() {
  const fill = document.getElementById('timerFill');
  fill.style.width = ((timeLeft / TIME_LIMIT) * 100) + '%';
  fill.className = 'timer-fill' + (timeLeft <= 5 ? ' danger' : timeLeft <= 10 ? ' warning' : '');
}

function updateLivesUI() {
  document.getElementById('livesBar').textContent =
    Array(3).fill(0).map((_, i) => i < state.lives ? '❤️' : '🖤').join('');
}

function loseLife() {
  state.lives--;
  updateLivesUI();
  triggerShake();
  state.streak = 0;
  if (state.lives <= 0) setTimeout(showGameOver, 1500);
}

function triggerShake() {
  const c = document.getElementById('mainCard');
  c.classList.remove('shake');
  void c.offsetWidth;
  c.classList.add('shake');
}

function handleTimeout() {
  if (state.answered) return;
  state.answered = true;
  loseLife();
  document.querySelectorAll('.check-item').forEach(i => {
    if (state.current.correct.includes(i.dataset.val)) {
      i.classList.add('correct');
      i.querySelector('.check-box').textContent = '✓';
    }
  });
  showFeedback(false, false, 0, state.current.correct.length, 0, state.current.correct, [], 0, true);
  showBreakdown();
  disableButtons();
}

function shuffle(arr) { return [...arr].sort(() => Math.random() - 0.5); }

function nextQuestion() {
  state.answered = false;
  state.hintsUsed = 0;
  state.total++;
  const cands = STEELS.filter(s => !state.current || s.name !== state.current.name);
  state.current = cands[Math.floor(Math.random() * cands.length)];
  state.options = shuffle([...state.current.correct, ...shuffle(state.current.distractors).slice(0, Math.max(2, 6 - state.current.correct.length))]);
  renderQuestion();
  hideFeedback();
  hideBreakdown();
  startTimer();
}

function renderQuestion() {
  const el = document.getElementById('steelDisplay');
  el.textContent = state.current.name;
  el.classList.remove('new');
  void el.offsetWidth;
  el.classList.add('new');
  const cl = document.getElementById('checklist');
  cl.innerHTML = '';
  state.options.forEach(opt => {
    const d = document.createElement('div');
    d.className = 'check-item';
    d.dataset.val = opt;
    d.innerHTML = `<div class="check-box"></div><div>${opt}</div>`;
    d.onclick = () => toggleCheck(d);
    cl.appendChild(d);
  });
  document.getElementById('hintRow').innerHTML =
    (HINTS[state.current.category] || []).map((h, i) =>
      `<button class="hint-chip" onclick="showHint(this,'${h}')">💡 İpucu ${i+1}</button>`
    ).join('');
  document.getElementById('submitBtn').disabled = false;
}

function showHint(btn, text) { btn.textContent = text; state.hintsUsed++; }

function toggleCheck(el) {
  if (state.answered) return;
  el.classList.toggle('selected');
  el.querySelector('.check-box').textContent = el.classList.contains('selected') ? '✓' : '';
}

function disableButtons() { document.getElementById('submitBtn').disabled = true; }

function submitAnswer() {
  if (state.answered) return;
  clearInterval(timerInterval);
  state.answered = true;
  const items = document.querySelectorAll('.check-item');
  const sel = [];
  items.forEach(i => { if (i.classList.contains('selected')) sel.push(i.dataset.val); });
  let hits = 0;
  items.forEach(i => {
    const v = i.dataset.val;
    const isC = state.current.correct.includes(v);
    const isS = sel.includes(v);
    if (isC) { i.classList.add('correct'); i.querySelector('.check-box').textContent = '✓'; if (isS) hits++; }
    else if (isS) { i.classList.add('wrong'); i.querySelector('.check-box').textContent = '✗'; }
  });
  const missed = state.current.correct.filter(c => !sel.includes(c));
  const wrong  = sel.filter(s => !state.current.correct.includes(s));
  const full   = hits === state.current.correct.length && wrong.length === 0;
  const part   = hits > 0 && !full;
  let pts = 0;
  if (full) {
    pts = Math.max(10, 10 - state.hintsUsed * 2) + Math.floor((timeLeft / TIME_LIMIT) * 5);
    state.streak++;
    if (state.streak > 1) pts += Math.min(state.streak * 2, 10);
    state.score += pts;
  } else if (part) {
    pts = Math.floor((hits / state.current.correct.length) * 5);
    state.streak = 0;
    state.score += pts;
  } else {
    loseLife();
  }
  document.getElementById('totalScore').textContent = state.score;
  document.getElementById('streakVal').textContent   = state.streak;
  showFeedback(full, part, hits, state.current.correct.length, wrong.length, missed, wrong, pts, false);
  showBreakdown();
  disableButtons();
}

function showFeedback(f, p, h, t, wc, m, w, pts, to) {
  const fb = document.getElementById('feedback');
  fb.className = 'feedback show';
  const ti = document.getElementById('fbTitle');
  const body = document.getElementById('fbBody');
  if (to) {
    fb.classList.add('timeout-fb');
    ti.textContent = '⏰ SÜRE DOLDU! -1 Can 🖤';
    body.innerHTML = `Doğru: ${state.current.correct.join(', ')}<br><br>${state.current.explanation}`;
  } else if (f) {
    fb.classList.add('correct-fb');
    ti.textContent = `✅ Mükemmel! +${pts} Puan`;
    body.textContent = state.current.explanation;
  } else if (p) {
    fb.classList.add('partial-fb');
    ti.textContent = `⚡ Kısmi Doğru! +${pts} Puan`;
    body.innerHTML = `Eksik: ${m.join(', ')}<br>Hatalı: ${w.join(', ')}<br><br>${state.current.explanation}`;
  } else {
    fb.classList.add('wrong-fb');
    ti.textContent = '❌ Tamamen Yanlış! -1 Can 🖤';
    body.innerHTML = `Olması gereken: ${state.current.correct.join(', ')}<br><br>${state.current.explanation}`;
  }
  if (state.lives > 0) {
    setTimeout(() => {
      const b = document.createElement('button');
      b.className = 'btn-primary';
      b.style.marginTop = '14px';
      b.textContent = 'SIRADAKİ →';
      b.onclick = nextQuestion;
      fb.appendChild(b);
    }, 400);
  }
}

function hideFeedback() {
  const fb = document.getElementById('feedback');
  fb.className = 'feedback';
  fb.innerHTML = '<div class="feedback-title" id="fbTitle"></div><div id="fbBody"></div>';
}

function showBreakdown() {
  document.getElementById('breakdown').classList.add('show');
  document.getElementById('breakdownRows').innerHTML =
    state.current.breakdown.map(r =>
      `<div class="breakdown-row"><div class="bd-token">${r.token}</div><div class="bd-meaning">${r.meaning}</div><div class="bd-category">${r.cat}</div></div>`
    ).join('');
}
function hideBreakdown() { document.getElementById('breakdown').classList.remove('show'); }

function showGameOver() {
  document.getElementById('finalScoreDisplay').textContent = state.score;
  if (state.score > state.highScore) {
    state.highScore = state.score;
    try { localStorage.setItem('steelHS', state.score); } catch(e) {}
    document.getElementById('highScoreVal').textContent = state.score;
    document.getElementById('newRecordAlert').style.display = 'block';
  } else {
    document.getElementById('newRecordAlert').style.display = 'none';
  }
  document.getElementById('gameOverModal').classList.add('show');
}

function restartGame() {
  state.score = 0; state.streak = 0; state.lives = 3; state.total = 0;
  document.getElementById('totalScore').textContent = 0;
  document.getElementById('streakVal').textContent   = 0;
  updateLivesUI();
  document.getElementById('gameOverModal').classList.remove('show');
  nextQuestion();
}

// ═══════════════════ MODÜL 2: KARAR AĞACI ═══════════════════
const DECISION_TREE = {
  start: { question: "Mikroskoptaki ilk izlenimin nedir? Kırık yüzeyin genel görünümü nasıl?", options: [ { text: "Parlak, düzgün — plastik deformasyon yok.", icon: "A", next: "gevrek_dal" }, { text: "Mat, pürüzlü, lifli — boyun verme var.", icon: "B", next: "sunek_dal" } ] },
  gevrek_dal: { question: "Kırık yüzeyinde 'midye kabuğu' izleri (beach marks) var mı?", options: [ { text: "Evet, yüzeyden içe doğru yayılan belirgin çizgiler var.", icon: "A", next: "res_fatigue" }, { text: "Hayır, yüzey tamamen kristalin (şeker kırığı gibi).", icon: "B", next: "res_brittle" } ] },
  sunek_dal: { question: "Parçanın kopma şekli nasıl?", options: [ { text: "Koni-çanak (cup and cone) şeklinde uzayarak kopmuş.", icon: "A", next: "res_ductile" }, { text: "45° açıyla veya çapraz yırtılmış.", icon: "B", next: "res_shear" } ] },
  res_fatigue: { isResult: true, title: "YORULMA HASARI", color: "var(--accent)", desc: "Parça, akma dayanımının altındaki tekrarlayan yüklerle kırılmış.<br><br><strong>Çözüm:</strong> Keskin köşelerden kaçın, yüzey kalitesini artır, nitrürleme uygula." },
  res_brittle: { isResult: true, title: "GEVREK KIRILMA", color: "var(--red)", desc: "Plastik deformasyon olmadan aniden kırılmış.<br><br><strong>Nedenler:</strong> Düşük sıcaklık, yüksek deformasyon hızı, hatalı ısıl işlem." },
  res_ductile: { isResult: true, title: "SÜNEK KIRILMA (Aşırı Yük)", color: "var(--green)", desc: "Malzeme kapasitesi aşılmış. Kırılmadan önce uyarı vermiş.<br><br><strong>Çözüm:</strong> Kesit artır veya daha yüksek dayanımlı malzeme seç." },
  res_shear: { isResult: true, title: "KESME / BURULMA HASARI", color: "var(--accent2)", desc: "Kayma kuvvetleri veya aşırı burulma momenti sonucu kırılmış.<br><br><strong>Çözüm:</strong> Mil çapını ve kama kanallarını yeniden hesapla." }
};
let currentDecisionNode = 'start';

function startDecisionTree() {
  currentDecisionNode = 'start';
  document.getElementById('dtResultBox').style.display   = 'none';
  document.getElementById('dtQuestionBox').style.display = 'block';
  renderDecisionNode();
}

function renderDecisionNode() {
  const node = DECISION_TREE[currentDecisionNode];
  if (node.isResult) {
    document.getElementById('dtQuestionBox').style.display = 'none';
    const resBox = document.getElementById('dtResultBox');
    resBox.style.display = 'block';
    const titleEl = document.getElementById('dtResultTitle');
    titleEl.textContent = node.title;
    titleEl.style.color = node.color;
    resBox.style.borderColor = node.color;
    document.getElementById('dtResultDesc').innerHTML = node.desc;
    return;
  }
  document.getElementById('dtQuestionText').textContent = node.question;
  const optDiv = document.getElementById('dtOptions');
  optDiv.innerHTML = '';
  node.options.forEach(opt => {
    const btn = document.createElement('button');
    btn.className = 'dt-btn';
    btn.innerHTML = `<div class="dt-btn-icon">${opt.icon}</div><div>${opt.text}</div>`;
    btn.onclick = () => { currentDecisionNode = opt.next; renderDecisionNode(); };
    optDiv.appendChild(btn);
  });
}

// ═══════════════════ MODÜL 3: FLASHCARDS ═══════════════════
const FLASHCARD_DATA = [
  { front: "Normal Stress<br><span style='font-size:13px;color:var(--dim);'>(Normal Gerilme)</span>", back: "Yüzeye dik olarak etki eden kuvvetin birim alana düşen miktarıdır." },
  { front: "Shear Stress<br><span style='font-size:13px;color:var(--dim);'>(Kayma Gerilmesi)</span>", back: "Yüzeye paralel (teğet) olarak etki eden kuvvetin birim alana düşen miktarıdır." },
  { front: "Normal Strain<br><span style='font-size:13px;color:var(--dim);'>(Normal Uzama)</span>", back: "Malzemenin başlangıç boyuna göre eksenel yönde gösterdiği oransal uzama veya kısalmadır." },
  { front: "Shear Strain<br><span style='font-size:13px;color:var(--dim);'>(Kayma Birim Şekil Değ.)</span>", back: "Malzemenin kesme kuvvetleri altında uğradığı açısal değiştirmedir." },
  { front: "Elastic Modulus<br><span style='font-size:13px;color:var(--dim);'>(Young Modülü)</span>", back: "Malzemenin elastik şekil değiştirmeye karşı direnci (σ/ε oranı)." },
  { front: "Poisson's Ratio<br><span style='font-size:13px;color:var(--dim);'>(Poisson Oranı)</span>", back: "Eksenel yükleme altında enine birim şekil değiştirmenin boyuna olana oranının negatifi." },
  { front: "Hardness<br><span style='font-size:13px;color:var(--dim);'>(Sertlik)</span>", back: "Malzemenin yüzeyine batan sert bir cisme, çizilmeye veya aşınmaya karşı gösterdiği lokal direnç." },
  { front: "Toughness<br><span style='font-size:13px;color:var(--dim);'>(Tokluk)</span>", back: "Malzemenin kırılana kadar absorbe ettiği toplam enerji (gerilme-uzama eğrisi altındaki alan)." },
  { front: "Ductility<br><span style='font-size:13px;color:var(--dim);'>(Süneklik)</span>", back: "Malzemenin kopmadan önce ne kadar kalıcı şekil değiştirebildiğinin ölçüsü." },
  { front: "Strength<br><span style='font-size:13px;color:var(--dim);'>(Mukavemet)</span>", back: "Malzemenin kırılmadan veya kalıcı deformasyon olmadan taşıyabileceği maksimum kuvvet kapasitesi." }
];
let currentDeck = [];
let currentCardEl = null;

function startFlashcards() {
  currentDeck = [...FLASHCARD_DATA].sort(() => Math.random() - 0.5);
  document.getElementById('fcResultBox').style.display  = 'none';
  document.getElementById('fcControls').style.display   = 'flex';
  document.getElementById('fcContainer').style.display  = 'block';
  nextFlashcard();
}

function nextFlashcard() {
  const container = document.getElementById('fcContainer');
  container.innerHTML = '';
  document.getElementById('fcProgress').textContent = `Kalan Kart: ${currentDeck.length}`;
  if (currentDeck.length === 0) {
    document.getElementById('fcContainer').style.display = 'none';
    document.getElementById('fcControls').style.display  = 'none';
    document.getElementById('fcResultBox').style.display = 'block';
    return;
  }
  const cardData = currentDeck[0];
  const cardEl = document.createElement('div');
  cardEl.className = 'fc-card';
  cardEl.innerHTML = `
    <div class="fc-face fc-front">
      <div class="fc-title">MET344 TERİM</div>
      <div class="fc-content">${cardData.front}</div>
    </div>
    <div class="fc-face fc-back">
      <div class="fc-title" style="color:var(--green);">TANIM</div>
      <div class="fc-content">${cardData.back}</div>
    </div>`;

  let startX = 0, startTime = 0, moved = false;
  cardEl.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX; startTime = Date.now(); moved = false;
    cardEl.style.transition = 'none';
  }, { passive: true });
  cardEl.addEventListener('touchmove', (e) => {
    const dx = e.touches[0].clientX - startX;
    if (Math.abs(dx) > 8) moved = true;
    if (!moved) return;
    cardEl.style.transform = `translateX(${dx}px) rotate(${dx * 0.04}deg)`;
  }, { passive: true });
  cardEl.addEventListener('touchend', (e) => {
    cardEl.style.transition = 'transform 0.4s cubic-bezier(0.175,0.885,0.32,1.275)';
    const dx = e.changedTouches[0].clientX - startX;
    const dt = Date.now() - startTime;
    if (!moved && dt < 300) { flipCard(); cardEl.style.transform = ''; }
    else if (dx > 80)  { swipeCard('right'); }
    else if (dx < -80) { swipeCard('left'); }
    else { cardEl.style.transform = cardEl.classList.contains('is-flipped') ? 'rotateY(180deg)' : ''; }
  }, { passive: true });

  currentCardEl = cardEl;
  container.appendChild(cardEl);
}

function flipCard() { if (currentCardEl) currentCardEl.classList.toggle('is-flipped'); }

function swipeCard(direction) {
  if (!currentCardEl) return;
  currentCardEl.style.transition = 'transform 0.4s ease, opacity 0.4s ease';
  currentCardEl.classList.add(direction === 'right' ? 'swipe-right' : 'swipe-left');
  setTimeout(() => {
    const card = currentDeck.shift();
    if (direction === 'left') currentDeck.push(card);
    nextFlashcard();
  }, 300);
}

// ═══════════════════ MODÜL 4: MET-WORDLE ═══════════════════
const HAM_VERI = `ÖSTENİT:Demirin YMK kafes yapısına sahip yüksek sıcaklık fazı.
MARTENZİT:Çeliğin ani soğutulmasıyla oluşan difüzyonsuz ve aşırı sert faz.
SEMENTİT:Çeliklerde bulunan Fe3C formülündeki sert demir karbür bileşiği.
FERRİT:Demirin oda sıcaklığındaki HMK kafes yapısına sahip fazı.
PERLİT:Ferrit ve sementitin tabakalı (lamelli) mikroyapı karışımı.
BEYNİT:Perlit ile martenzit arasında oluşan iğnesel mikroyapı.
LEDEBURİT:Dökme demirlerde görülen ötektik sıvı-katı karışımı.
ÖTEKTİK:Sıvı fazın aynı anda iki farklı katı faza dönüştüğü reaksiyon.
ÖTEKTOİD:Bir katı fazın iki farklı katı faza dönüştüğü izotermal reaksiyon.
PERİTEKTİK:Sıvı ve katı fazın birleşerek yeni bir katı faz oluşturduğu reaksiyon.
SÜNEKLİK:Malzemenin kopmadan önce kalıcı şekil değiştirebilme yeteneği.
TOKLUK:Malzemenin kırılana kadar sönümlediği toplam enerji miktarı.
AKMA:Plastik deformasyonun başladığı kritik gerilme eşiği.
ÇEKME:Malzemenin dayanabileceği maksimum mühendislik gerilmesi.
GEVREKLİK:Malzemenin plastik şekil değiştirmeden aniden kırılma eğilimi.
REZİLYANS:Malzemenin elastik enerji depolama ve geri verme yeteneği.
SERTLİK:Malzemenin yüzeyine batan sert bir cisme karşı gösterdiği direnç.
YORULMA:Tekrarlı yükler altında malzemenin zamanla hasara uğraması.
SÜNME:Yüksek sıcaklık ve sabit yük altında zamanla oluşan kalıcı uzama.
DİSLOKASYON:Kristal yapıdaki plastik deformasyonu sağlayan çizgisel kusur.
VAKANS:Kristal kafes yapısındaki atom boşluğu veya noktasal kusur.
İNTERSTİSYEL:Atomların kafes boşlukları arasına yerleşmesiyle oluşan yapı.
SUBSTİTÜSYONEL:Yabancı atomların ana atomların yerini aldığı alaşım türü.
ANİZOTROPİ:Özelliklerin ölçüldüğü yöne göre değişiklik göstermesi durumu.
İZOTROPİK:Malzeme özelliklerinin her yönde aynı olması durumu.
TAVLAMA:İç gerilmeleri gidermek veya yumuşatmak için yapılan ısıtma işlemi.
TEMPERLEME:Martenzitik çeliklerin gevrekliğini azaltmak için yapılan ısıl işlem.
NORMALİZASYON:Tane yapısını inceltmek için havada soğutma ile yapılan işlem.
SEMENTASYON:Düşük karbonlu çelik yüzeyine karbon emdirilmesi işlemi.
NİTRÜRLEME:Aşınma direnci için çelik yüzeyine azot emdirilmesi.
YAŞLANDIRMA:Çökelme sertleşmesi yoluyla alaşımı kuvvetlendirme yöntemi.
KOROZYON:Metallerin çevreleriyle elektrokimyasal etkileşimi sonucu bozunması.
OKSİDASYON:Metalin elektron kaybederek oksijenle tepkimeye girmesi.
PASLANMA:Demir ve alaşımlarının nemli ortamda oksitlenmesi.
GALVANİZ:Çeliğin korozyondan korunması için çinko ile kaplanması.
ANODİZASYON:Alüminyum yüzeyinde koruyucu oksit tabakası oluşturma işlemi.
DÖKÜM:Ergimiş metalin bir kalıba dökülerek katılaştırılması yöntemi.
HADDELEME:Metalin merdaneler arasından geçirilerek inceltilmesi işlemi.
EKSTRÜZYON:Metalin bir kovan içinden basınçla itilerek şekillendirilmesi.
SİNTERLEME:Toz metal parçaların ergime derecesi altında birleştirilmesi.
KAYNAK:İki parçanın ısı veya basınç yardımıyla birleştirilmesi tekniği.
DENDRİT:Katılaşma sırasında oluşan ağaçsı kristal büyüme yapısı.
ALAŞIM:En az biri metal olan elementlerin oluşturduğu metalik malzeme.
PİRİNÇ:Bakır ve çinko elementlerinden oluşan temel alaşım.
BRONZ:Bakır ve kalay elementlerinden oluşan tarihi alaşım.
METALURJİ:Metallerin cevherden eldesi ve özelliklerinin incelenmesi bilimi.
SERAMİK:Metal ve ametal elementlerin bileşiği olan inorganik malzeme.
KOMPOZİT:En az iki farklı malzemenin makro düzeyde birleşimi.
XRD:Kristal yapı analizi için kullanılan X-ışını kırınımı yöntemi.
SEM:Yüksek çözünürlüklü görüntüleme sağlayan taramalı elektron mikroskobu.
TEM:Elektronların numune içinden geçtiği transmisyon mikroskobu.
İNKONEL:Nikel esaslı yüksek sıcaklığa dayanıklı süper alaşım.
NİTİNOL:Şekil hatırlama özelliğine sahip nikel-titanyum alaşımı.
VICKERS:Elmas piramit uç kullanılarak yapılan hassas sertlik testi.
ROCKWELL:İz derinliğine göre ölçüm yapan yaygın sertlik test yöntemi.
CHARPY:Darbeli yükler altında tokluk ölçen çentikli test cihazı.
KAVİTASYON:Sıvı içindeki kabarcık patlamalarının yüzeyde açtığı mikro oyuklar.
DİFÜZYON:Atomların konsantrasyon farkı nedeniyle yer değiştirmesi.
ALLOTROPİ:Bir elementin farklı kristal yapılarda bulunabilme özelliği.
SİGMA:Paslanmaz çeliklerde görülen istenmeyen gevrek ara faz.`.trim();

const WORDLE_DATA = HAM_VERI.split('\n').map(s => {
  const [word, clue] = s.split(':');
  return { word: word.trim(), clue: clue.trim() };
});

const KB_LAYOUT = [
  ['E','R','T','Y','U','I','O','P','Ğ','Ü'],
  ['A','S','D','F','G','H','J','K','L','Ş','İ'],
  ['ENTER','Z','C','V','B','N','M','Ö','Ç','DEL']
];

let targetWord = '', currentGuess = '', currentRow = 0, maxAttempts = 6, gameOver = false;

function startWordle() {
  const rd = WORDLE_DATA[Math.floor(Math.random() * WORDLE_DATA.length)];
  targetWord   = rd.word.normalize('NFC').toLocaleUpperCase('tr-TR');
  currentGuess = ''; currentRow = 0; gameOver = false;
  maxAttempts  = Math.max(6, Math.ceil(targetWord.length * 0.85));
  document.getElementById('wordleClue').textContent        = `// İPUCU: ${rd.clue}`;
  document.getElementById('wordleResultBox').style.display = 'none';
  document.getElementById('keyboard').style.display        = 'flex';
  renderWordleBoard();
  renderKeyboard();
}

function renderWordleBoard() {
  const board = document.getElementById('wordleBoard');
  board.innerHTML = '';
  for (let i = 0; i < maxAttempts; i++) {
    const row = document.createElement('div');
    row.className = 'wordle-row';
    row.style.gridTemplateColumns = `repeat(${targetWord.length},1fr)`;
    row.id = `w-row-${i}`;
    for (let j = 0; j < targetWord.length; j++) {
      const tile = document.createElement('div');
      tile.className = 'wordle-tile';
      tile.id = `w-tile-${i}-${j}`;
      row.appendChild(tile);
    }
    board.appendChild(row);
  }
}

function renderKeyboard() {
  const kb = document.getElementById('keyboard');
  kb.innerHTML = '';
  KB_LAYOUT.forEach(row => {
    const rowEl = document.createElement('div');
    rowEl.className = 'key-row';
    row.forEach(key => {
      const k = document.createElement('button');
      k.className = `key${key.length > 1 ? ' wide' : ''}`;
      k.textContent = key === 'DEL' ? '⌫' : key;
      k.id = `key-${key}`;
      k.onclick = () => handleKeyPress(key);
      rowEl.appendChild(k);
    });
    kb.appendChild(rowEl);
  });
}

function handleKeyPress(key) {
  if (gameOver) return;
  key = key.normalize ? key.normalize('NFC') : key;
  if (key === 'DEL' || key === 'BACKSPACE') {
    currentGuess = currentGuess.slice(0, -1);
  } else if (key === 'ENTER') {
    if (currentGuess.length === targetWord.length) submitGuess();
    else triggerWordleShake();
    return;
  } else if (currentGuess.length < targetWord.length) {
    currentGuess += key;
  }
  updateWordleRow();
}

function updateWordleRow() {
  const tiles = document.getElementById(`w-row-${currentRow}`).children;
  for (let i = 0; i < targetWord.length; i++) {
    const tile = tiles[i];
    const ch = currentGuess[i] || '';
    if (tile.textContent !== ch) {
      tile.textContent = ch;
      if (ch) tile.classList.add('filled');
      else tile.classList.remove('filled');
    }
  }
}

function triggerWordleShake() {
  const row = document.getElementById(`w-row-${currentRow}`);
  row.classList.remove('shake-anim');
  void row.offsetWidth;
  row.classList.add('shake-anim');
}

// ★ TEK VE TEMİZ submitGuess — 3 kez çalışan bug giderildi ★
function submitGuess() {
  const guessArr = currentGuess.split('');
  const targetArr = targetWord.split('');
  const rowTiles = document.getElementById(`w-row-${currentRow}`).children;
  let letterCounts = {};
  targetArr.forEach(l => letterCounts[l] = (letterCounts[l] || 0) + 1);
  let statuses = Array(targetWord.length).fill('absent');

  guessArr.forEach((letter, i) => {
    if (letter === targetArr[i]) { statuses[i] = 'correct'; letterCounts[letter] -= 1; }
  });
  guessArr.forEach((letter, i) => {
    if (statuses[i] !== 'correct' && letterCounts[letter] > 0) { statuses[i] = 'present'; letterCounts[letter] -= 1; }
  });

  guessArr.forEach((letter, i) => {
    setTimeout(() => {
      rowTiles[i].classList.add('flip-anim', statuses[i]);
      const keyBtn = document.getElementById(`key-${letter}`);
      if (keyBtn) {
        if (statuses[i] === 'correct') { keyBtn.classList.remove('present','absent'); keyBtn.classList.add('correct'); }
        else if (statuses[i] === 'present' && !keyBtn.classList.contains('correct')) { keyBtn.classList.remove('absent'); keyBtn.classList.add('present'); }
        else if (statuses[i] === 'absent' && !keyBtn.classList.contains('correct') && !keyBtn.classList.contains('present')) { keyBtn.classList.add('absent'); }
      }
    }, i * 150);
  });

  setTimeout(() => {
    if (currentGuess === targetWord) { endWordle(true); }
    else { currentRow++; currentGuess = ''; if (currentRow >= maxAttempts) endWordle(false); }
  }, targetWord.length * 150 + 100);
}

function endWordle(isWin) {
  gameOver = true;
  document.getElementById('keyboard').style.display = 'none';
  const resBox = document.getElementById('wordleResultBox');
  const title  = document.getElementById('wordleResultTitle');
  if (isWin) {
    resBox.style.borderColor = 'var(--green)'; title.style.color = 'var(--green)';
    title.textContent = 'MÜKEMMEL!';
    document.getElementById('wordleResultDesc').innerHTML = `<strong>${targetWord}</strong> kelimesini ${currentRow+1}. denemede buldun.`;
  } else {
    resBox.style.borderColor = 'var(--red)'; title.style.color = 'var(--red)';
    title.textContent = 'MAALESEF!';
    document.getElementById('wordleResultDesc').innerHTML = `Doğru kelime: <strong>${targetWord}</strong>`;
  }
  resBox.style.display = 'block';
}

document.addEventListener('keydown', (e) => {
  if (!document.getElementById('wordleView').classList.contains('active') || gameOver) return;
  if (e.target.id === 'gizliInput') return;
  const trMap = { 'i':'İ','ı':'I','ş':'Ş','ğ':'Ğ','ü':'Ü','ö':'Ö','ç':'Ç' };
  let key = trMap[e.key] || e.key.toUpperCase();
  const valid = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ';
  if (valid.includes(key)) handleKeyPress(key);
  else if (e.key === 'Enter') handleKeyPress('ENTER');
  else if (e.key === 'Backspace') handleKeyPress('DEL');
});

const gizliInput = document.getElementById('gizliInput');
gizliInput.value = 'A';

gizliInput.addEventListener('focus', () => {
  gizliInput.value = 'A';
  gizliInput.setSelectionRange(1, 1);
});

gizliInput.addEventListener('keydown', (e) => {
  if (e.key === 'Backspace') { e.preventDefault(); handleKeyPress('DEL'); }
  if (e.key === 'Enter')     { e.preventDefault(); handleKeyPress('ENTER'); }
});

gizliInput.addEventListener('input', () => {
  if (gameOver) return;
  const val = gizliInput.value;
  if (val.length < 2) { handleKeyPress('DEL'); gizliInput.value = 'A'; gizliInput.setSelectionRange(1,1); return; }
  const code = val.charCodeAt(1);
  const codeMap = { 351:'Ş',350:'Ş',287:'Ğ',286:'Ğ',252:'Ü',220:'Ü',246:'Ö',214:'Ö',231:'Ç',199:'Ç',305:'I',73:'I',105:'İ',304:'İ' };
  const key = codeMap[code] || String.fromCharCode(code).toUpperCase();
  const valid = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ';
  if (valid.includes(key)) handleKeyPress(key);
  gizliInput.value = 'A';
  gizliInput.setSelectionRange(1, 1);
});
</script>
</body>
</html>
"""

html_kodu = html_kodu.replace("ELLINGHAM_URI_BURAYA", ellingham_uri)
html_kodu = html_kodu.replace("FEC_URI_BURAYA",       fec_uri)
html_kodu = html_kodu.replace("EHPH_URI_BURAYA",      ehph_uri)
html_kodu = html_kodu.replace("RSVP_HTML_BURAYA",     rsvp_html)
html_kodu = html_kodu.replace("RSVP_JS_BURAYA",       rsvp_js)






dosya_yolu = os.path.abspath('portal_motoru.html')
with open(dosya_yolu, 'w', encoding='utf-8') as f:
    f.write(html_kodu)

dosya_uri = pathlib.Path(dosya_yolu).as_uri()


print("Mühendislik Portalı hazırlanıyor...")
print(f"Tarayıcıda açılıyor: {dosya_uri}")
webbrowser.open(dosya_uri)
