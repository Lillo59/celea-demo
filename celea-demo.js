/* Siti di esempio di Celea · scena animata e «Parla ora» (restyling 2026-11).
   La pagina della demo si ridisegna quando si cambia pagina o lingua: per questo le scene si avviano
   ogni volta che compaiono (MutationObserver) e girano solo quando sono visibili. */
(function(){
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var BEATS = [[0,1000],[1,1700],[2,2000],[3,1500],[4,2000],[5,1900],[6,4400]];
  function avvia(stage){
    if(stage.dataset.pronta) return; stage.dataset.pronta = "1";
    if(reduce || !("IntersectionObserver" in window)) return; // resta il fotogramma finale
    var items = [].slice.call(stage.querySelectorAll("[data-at]")), i = 0, t = null, vis = false;
    function show(n){ items.forEach(function(el){ el.classList.toggle("on", +el.dataset.at <= n); }); }
    function next(){ if(!vis || !document.body.contains(stage)) return; var b = BEATS[i]; show(b[0]); i = (i + 1) % BEATS.length; t = setTimeout(next, b[1]); }
    new IntersectionObserver(function(es){ es.forEach(function(e){
      if(e.isIntersecting && !vis){ vis = true; stage.classList.add("playing"); next(); }
      else if(!e.isIntersecting){ vis = false; clearTimeout(t); }
    }); }, { threshold: .35 }).observe(stage);
  }
  // «Parla ora»: carica il widget vocale di Retell solo al clic (chiavi pubbliche, come su www.celea.it).
  var TALK = { key:"public_key_c73e28f264823fa5e478c", recaptcha:"6Lc2O_4tAAAAAMUHuzb58YLXZ14f1q23lMZsPcz4" };
  var caricato = false;
  function parla(btn){
    var msg = btn.parentNode.querySelector(".parla-msg"), T = btn.dataset;
    if(caricato){ if(msg) msg.textContent = T.aperto || ""; return; }
    caricato = true; if(msg) msg.textContent = T.carico || "";
    var rc = document.createElement("script"); rc.async = true; rc.src = "https://www.google.com/recaptcha/api.js?render=" + encodeURIComponent(TALK.recaptcha); document.head.appendChild(rc);
    var w = document.createElement("script"); w.type = "module"; w.id = "retell-widget"; w.src = "https://dashboard.retellai.com/retell-widget-v2.js";
    var a = { "data-voice-public-key":TALK.key, "data-voice-agent-id":T.agente, "data-recaptcha-key":TALK.recaptcha, "data-title":T.titolo, "data-bot-name":T.nome, "data-fab-text":T.fab, "data-color":getComputedStyle(document.documentElement).getPropertyValue("--acc").trim() || "#1C2A30", "data-show-ai-popup":"false", "data-auto-open":"true" };
    // l'assistente si presenta con il nome della demo (Odontèa, Casa Lumèa, Domèa): variabile {{nome_attivita}} su Retell
    var attivita = String(T.titolo || "").split(" · ")[0]; if(attivita) a["data-dynamic"] = JSON.stringify({ nome_attivita: attivita });
    Object.keys(a).forEach(function(k){ w.setAttribute(k, a[k]); });
    w.onerror = function(){ caricato = false; if(msg) msg.textContent = T.errore || ""; };
    document.head.appendChild(w);
  }
  function scan(){
    [].forEach.call(document.querySelectorAll(".sc-stage"), avvia);
    [].forEach.call(document.querySelectorAll("[data-parla]:not([data-pronto])"), function(b){ b.dataset.pronto = "1"; b.addEventListener("click", function(e){ e.preventDefault(); parla(b); }); });
  }
  var main = document.getElementById("main");
  if(main) new MutationObserver(scan).observe(main, { childList: true });
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", scan); else scan();
})();
