# Restyling 2026-11 dei siti di esempio: caratteri inclusi, scena animata del settore e «Parla ora» con l'assistente.
# Idempotente: se una demo ha già le aggiunte (marcatore RESTYLING-2026-11), non le rimette.
import re, os, shutil
RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTPKG = '/tmp/claude-0/-home-user/b8f1de3a-802e-5932-8880-36798cbf7d66/scratchpad/fontpkg'
LAT = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
EXT = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"
# famiglia → (pacchetto, prefisso file, [pesi]); 'wght' = carattere variabile
FONT = {
  'Bricolage Grotesque': ('x-fontsource-variable-bricolage-grotesque-5.3.0', 'bricolage-grotesque', ['wght'], '200 800'),
  'Atkinson Hyperlegible': ('x-fontsource-atkinson-hyperlegible-5.3.0', 'atkinson-hyperlegible', ['400', '700'], None),
  'Young Serif': ('x-fontsource-young-serif-5.3.0', 'young-serif', ['400'], None),
  'Nunito Sans': ('x-fontsource-variable-nunito-sans-5.3.0', 'nunito-sans', ['wght'], '200 1000'),
  'Instrument Serif': ('x-fontsource-instrument-serif-5.3.0', 'instrument-serif', ['400'], None),
  'Figtree': ('x-fontsource-variable-figtree-5.3.0', 'figtree', ['wght'], '300 900'),
}
def font_face(fam):
    pkg, pre, pesi, rng = FONT[fam]; out = []
    os.makedirs(os.path.join(RADICE, 'fonts'), exist_ok=True)
    for p in pesi:
        for sub, ur in (('latin', LAT), ('latin-ext', EXT)):
            nome = f'{pre}-{sub}-{"wght" if p == "wght" else p}-normal.woff2'
            shutil.copy(os.path.join(FONTPKG, pkg, 'package', 'files', nome), os.path.join(RADICE, 'fonts', nome))
            w = rng if p == 'wght' else p
            out.append(f'@font-face{{font-family:"{fam}";src:url("../fonts/{nome}") format("woff2");font-weight:{w};font-style:normal;font-display:optional;unicode-range:{ur}}}')
    return '\n'.join(out)

TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'

DEMO = {
 'odontea': {
  'font': ['Bricolage Grotesque', 'Atkinson Hyperlegible'], 'iniziale': 'O', 'agente': 'agent_d707460b8b0bc2d50382aa3aa9', 'nome': 'Sofia',
  'it': dict(eti='Una sera, dopo la chiusura', h='Un paziente sposta la pulizia. L\'agenda si aggiorna.', lead='Esempio con dati inventati: l\'assistente AI dello studio propone due orari liberi, sposta l\'appuntamento e offre il posto liberato a chi è in lista d\'attesa.',
     chi='Odontèa', sub='assistente AI · esempio', m1='Devo spostare la pulizia di giovedì.', m2='Certo. Ho venerdì alle 9:00 o lunedì alle 17:30. Quale preferisce?', m3='Venerdì alle 9, grazie.', m4='Fatto: venerdì alle 9:00. Il giorno prima Le mando il promemoria.',
     k='Agenda dello studio · venerdì', ev='Pulizia · M. Rossi', evs='spostata dall\'assistente', chip='Giovedì 17:30 offerto alla lista d\'attesa', nota='Esempio illustrativo: pazienti, orari e studio sono inventati.',
     btn='Parla ora con Sofia', pnota='Chiamata di prova dal browser con Sofia, l\'assistente AI dimostrativo di Celea: nome dello studio e dati sono d\'esempio. Serve il microfono; al massimo 3 minuti.', carico='Collegamento in corso…', aperto='La chiamata è già aperta in basso a destra.', errore='Non riesco ad aprire la chiamata: ricarichi la pagina e riprovi.', fab='Parla con Sofia'),
  'en': dict(eti='One evening, after closing', h='A patient moves their cleaning. The diary updates itself.', lead='Example with made-up data: the practice\'s AI assistant offers two free slots, moves the appointment and offers the freed slot to the waiting list.',
     chi='Odontèa', sub='AI assistant · example', m1='I need to move Thursday\'s cleaning.', m2='Of course. I have Friday at 9:00 or Monday at 17:30. Which do you prefer?', m3='Friday at 9, thanks.', m4='Done: Friday at 9:00. I\'ll send you a reminder the day before.',
     k='Practice diary · Friday', ev='Cleaning · M. Rossi', evs='moved by the assistant', chip='Thursday 17:30 offered to the waiting list', nota='Illustrative example: patients, times and practice are made up.',
     btn='Talk now with Sofia', pnota='Test call from your browser with Sofia, Celea\'s demo AI assistant: the practice name and data are examples. You need a microphone; 3 minutes at most.', carico='Connecting…', aperto='The call is already open at the bottom right.', errore='The call can\'t open: please reload the page and try again.', fab='Talk to Sofia'),
  'de': dict(eti='Ein Abend, nach Praxisschluss', h='Ein Patient verschiebt die Reinigung. Der Kalender aktualisiert sich.', lead='Beispiel mit erfundenen Daten: Der KI-Assistent der Praxis schlägt zwei freie Termine vor, verschiebt den Termin und bietet den frei gewordenen Platz der Warteliste an.',
     chi='Odontèa', sub='KI-Assistent · Beispiel', m1='Ich muss die Reinigung am Donnerstag verschieben.', m2='Gern. Ich habe Freitag um 9:00 oder Montag um 17:30. Was passt Ihnen?', m3='Freitag um 9, danke.', m4='Erledigt: Freitag um 9:00. Am Vortag schicke ich Ihnen eine Erinnerung.',
     k='Praxiskalender · Freitag', ev='Reinigung · M. Rossi', evs='vom Assistenten verschoben', chip='Donnerstag 17:30 der Warteliste angeboten', nota='Beispiel: Patienten, Zeiten und Praxis sind erfunden.',
     btn='Jetzt mit Sofia sprechen', pnota='Testanruf im Browser mit Sofia, der Demo-KI-Assistentin von Celea: Praxisname und Daten sind Beispiele. Sie brauchen ein Mikrofon; höchstens 3 Minuten.', carico='Verbindung wird hergestellt…', aperto='Der Anruf ist unten rechts schon geöffnet.', errore='Der Anruf lässt sich nicht öffnen: Bitte laden Sie die Seite neu.', fab='Mit Sofia sprechen'),
 },
 'casa-lumea': {
  'font': ['Young Serif', 'Nunito Sans'], 'iniziale': 'L', 'agente': 'agent_9f88879b0f2fd82c7a074dd2e6', 'nome': 'Elena',
  'it': dict(eti='Un arrivo in ritardo', h='Un ospite straniero arriva tardi. Le istruzioni sono già pronte.', lead='Esempio con dati inventati: l\'assistente AI risponde nella lingua dell\'ospite, spiega il self check-in e avvisa il titolare.',
     chi='Casa Lumèa', sub='assistente AI · esempio', m1='Hi! Our flight lands late, we\'ll arrive around 23:30. How do we get in?', m2='No problem! After 20:00 there\'s self check-in: on the day you\'ll receive the door code here. Your room is Ulivo, ground floor.', m3='Perfect, thank you!', m4='Have a good trip! I\'ve let the owner know you\'re arriving late.',
     k='Arrivi di oggi', ev='Camera Ulivo · famiglia Smith', evs='arrivo previsto 23:30 · istruzioni inviate', chip='Titolare avvisato', nota='Esempio illustrativo: ospiti, orari e struttura sono inventati.',
     btn='Parla ora con Elena', pnota='Chiamata di prova dal browser con Elena, l\'assistente AI dimostrativo di Celea: nome della struttura e dati sono d\'esempio. Serve il microfono; al massimo 3 minuti.', carico='Collegamento in corso…', aperto='La chiamata è già aperta in basso a destra.', errore='Non riesco ad aprire la chiamata: ricarichi la pagina e riprovi.', fab='Parla con Elena'),
  'en': dict(eti='A late arrival', h='A guest from abroad arrives late. The instructions are ready.', lead='Example with made-up data: the AI assistant replies in the guest\'s language, explains self check-in and lets the owner know.',
     chi='Casa Lumèa', sub='AI assistant · example', m1='Hi! Our flight lands late, we\'ll arrive around 23:30. How do we get in?', m2='No problem! After 20:00 there\'s self check-in: on the day you\'ll receive the door code here. Your room is Ulivo, ground floor.', m3='Perfect, thank you!', m4='Have a good trip! I\'ve let the owner know you\'re arriving late.',
     k='Today\'s arrivals', ev='Ulivo room · Smith family', evs='expected 23:30 · instructions sent', chip='Owner notified', nota='Illustrative example: guests, times and property are made up.',
     btn='Talk now with Elena', pnota='Test call from your browser with Elena, Celea\'s demo AI assistant: the property name and data are examples. You need a microphone; 3 minutes at most.', carico='Connecting…', aperto='The call is already open at the bottom right.', errore='The call can\'t open: please reload the page and try again.', fab='Talk to Elena'),
  'de': dict(eti='Eine späte Anreise', h='Ein Gast aus dem Ausland kommt spät an. Die Anleitung ist schon da.', lead='Beispiel mit erfundenen Daten: Der KI-Assistent antwortet in der Sprache des Gastes, erklärt den Self-Check-in und informiert den Inhaber.',
     chi='Casa Lumèa', sub='KI-Assistent · Beispiel', m1='Hi! Our flight lands late, we\'ll arrive around 23:30. How do we get in?', m2='No problem! After 20:00 there\'s self check-in: on the day you\'ll receive the door code here. Your room is Ulivo, ground floor.', m3='Perfect, thank you!', m4='Have a good trip! I\'ve let the owner know you\'re arriving late.',
     k='Anreisen heute', ev='Zimmer Ulivo · Familie Smith', evs='Ankunft gegen 23:30 · Anleitung verschickt', chip='Inhaber informiert', nota='Beispiel: Gäste, Zeiten und Unterkunft sind erfunden.',
     btn='Jetzt mit Elena sprechen', pnota='Testanruf im Browser mit Elena, der Demo-KI-Assistentin von Celea: Name der Unterkunft und Daten sind Beispiele. Sie brauchen ein Mikrofon; höchstens 3 Minuten.', carico='Verbindung wird hergestellt…', aperto='Der Anruf ist unten rechts schon geöffnet.', errore='Der Anruf lässt sich nicht öffnen: Bitte laden Sie die Seite neu.', fab='Mit Elena sprechen'),
 },
 'domea': {
  'font': ['Instrument Serif', 'Figtree'], 'iniziale': 'D', 'agente': 'agent_665333f44ade1c0d48ed000a7d', 'nome': 'Marco',
  'it': dict(eti='Una richiesta da un annuncio', h='Un contatto dall\'annuncio diventa una visita fissata.', lead='Esempio con dati inventati: l\'assistente AI risponde, fa due domande per capire cosa cerca la persona e fissa la visita nell\'agenda dell\'agente.',
     chi='Domèa', sub='assistente AI · esempio', m1='Il trilocale in zona Libertà è ancora disponibile? Posso vederlo sabato?', m2='Sì, è disponibile. Per proporLe la visita giusta: acquisto o affitto, e con quale budget?', m3='Acquisto, fino a 300.000 €.', m4='Perfetto: sabato ho le 10:30 o le 12:00. Le mando la conferma qui.',
     k='Agenda dell\'agente · sabato', ev='Visita trilocale zona Libertà', evs='contatto qualificato: acquisto, fino a 300.000 €', chip='Promemoria il giorno prima', nota='Esempio illustrativo: persone, immobili e prezzi sono inventati.',
     btn='Parla ora con Marco', pnota='Chiamata di prova dal browser con Marco, l\'assistente AI dimostrativo di Celea: nome dell\'agenzia e dati sono d\'esempio. Serve il microfono; al massimo 3 minuti.', carico='Collegamento in corso…', aperto='La chiamata è già aperta in basso a destra.', errore='Non riesco ad aprire la chiamata: ricarichi la pagina e riprovi.', fab='Parla con Marco'),
  'en': dict(eti='An enquiry from a listing', h='A contact from a listing becomes a booked viewing.', lead='Example with made-up data: the AI assistant replies, asks two questions to understand what the person is looking for and books the viewing in the agent\'s diary.',
     chi='Domèa', sub='AI assistant · example', m1='Is the three-room flat in the Libertà area still available? Can I see it on Saturday?', m2='Yes, it\'s available. To suggest the right viewing: buying or renting, and what\'s your budget?', m3='Buying, up to €300,000.', m4='Perfect: on Saturday I have 10:30 or 12:00. I\'ll send the confirmation here.',
     k='Agent\'s diary · Saturday', ev='Viewing: flat in the Libertà area', evs='qualified lead: buying, up to €300,000', chip='Reminder the day before', nota='Illustrative example: people, properties and prices are made up.',
     btn='Talk now with Marco', pnota='Test call from your browser with Marco, Celea\'s demo AI assistant: the agency name and data are examples. You need a microphone; 3 minutes at most.', carico='Connecting…', aperto='The call is already open at the bottom right.', errore='The call can\'t open: please reload the page and try again.', fab='Talk to Marco'),
  'de': dict(eti='Eine Anfrage zu einem Inserat', h='Aus einer Anfrage wird eine vereinbarte Besichtigung.', lead='Beispiel mit erfundenen Daten: Der KI-Assistent antwortet, stellt zwei Fragen und trägt die Besichtigung in den Kalender des Maklers ein.',
     chi='Domèa', sub='KI-Assistent · Beispiel', m1='Ist die Dreizimmerwohnung im Viertel Libertà noch frei? Kann ich sie am Samstag sehen?', m2='Ja, sie ist frei. Damit ich die passende Besichtigung vorschlage: Kauf oder Miete, und mit welchem Budget?', m3='Kauf, bis 300.000 €.', m4='Perfekt: Am Samstag habe ich 10:30 oder 12:00. Die Bestätigung schicke ich Ihnen hier.',
     k='Kalender des Maklers · Samstag', ev='Besichtigung Wohnung Libertà', evs='qualifizierter Kontakt: Kauf, bis 300.000 €', chip='Erinnerung am Vortag', nota='Beispiel: Personen, Immobilien und Preise sind erfunden.',
     btn='Jetzt mit Marco sprechen', pnota='Testanruf im Browser mit Marco, dem Demo-KI-Assistenten von Celea: Name der Agentur und Daten sind Beispiele. Sie brauchen ein Mikrofon; höchstens 3 Minuten.', carico='Verbindung wird hergestellt…', aperto='Der Anruf ist unten rechts schon geöffnet.', errore='Der Anruf lässt sich nicht öffnen: Bitte laden Sie die Seite neu.', fab='Mit Marco sprechen'),
 },
}
def scena(d, t):
    D = DEMO[d]
    return (f'<section class="scena-demo"><div class="wrap scena-grid"><div class="head"><p class="label">{t["eti"]}</p><h2>{t["h"]}</h2><p class="lead">{t["lead"]}</p><p class="sc-nota">{t["nota"]}</p></div>'
            f'<div class="sc-stage" aria-hidden="true"><div class="sc-phone"><div class="sc-screen"><div class="sc-bar"><span class="sc-av">{D["iniziale"]}</span><span><b>{t["chi"]}</b><small>{t["sub"]}</small></span></div>'
            f'<ol class="sc-msgs"><li class="me" data-at="1">{t["m1"]}</li><li class="ai" data-at="2"><b>AI</b>{t["m2"]}</li><li class="me" data-at="3">{t["m3"]}</li><li class="ai" data-at="4"><b>AI</b>{t["m4"]}</li></ol></div></div>'
            f'<div class="sc-card" data-at="5"><p class="sc-k">{t["k"]}</p><div class="sc-row"><time>{"9:00" if d=="odontea" else ("23:30" if d=="casa-lumea" else "10:30")}</time><span class="sc-ev">{t["ev"]}<small>{t["evs"]}</small></span></div><div class="sc-row"><time>{"10:00" if d=="odontea" else ("—" if d=="casa-lumea" else "12:00")}</time><i></i></div></div>'
            f'<div class="sc-chip" data-at="6">{t["chip"]}</div></div></div></section>')
def parla(d, t):
    D = DEMO[d]
    att = f'data-parla data-agente="{D["agente"]}" data-nome="{D["nome"]}" data-titolo="{t["chi"]} · {D["nome"]}" data-fab="{t["fab"]}" data-carico="{t["carico"]}" data-aperto="{t["aperto"]}" data-errore="{t["errore"]}"'
    return f'<div class="parla-box"><a class="btn line parla" href="#" {att}>{TEL}{t["btn"]}</a><p class="parla-msg small" role="status" aria-live="polite"></p><p class="small muted">{t["pnota"]}</p></div>'

for d in DEMO:
    p = os.path.join(RADICE, d, 'index.html'); s = open(p, encoding='utf-8').read()
    if 'RESTYLING-2026-11' in s: print(d, 'già fatto'); continue
    ff = '\n'.join(font_face(f) for f in DEMO[d]['font'])
    s = s.replace('<style>', '<style>\n/* RESTYLING-2026-11: caratteri inclusi nel sito (licenza OFL), prima non venivano caricati */\n' + ff + '\n', 1)
    s = s.replace('</style>', '</style>\n<link rel="stylesheet" href="../celea-demo.css">\n<script src="../celea-demo.js" defer></script>', 1)
    slot = '<div data-chat-slot></div></div></section>'
    pezzi = s.split(slot); assert len(pezzi) == 4, (d, len(pezzi))
    s = pezzi[0]
    for lingua, resto in zip(['it', 'en', 'de'], pezzi[1:]):
        s += slot + '\n' + scena(d, DEMO[d][lingua]) + resto
    # «Parla ora» dentro l'apertura, dopo i pulsanti principali (una volta per lingua)
    n = 0
    def metti(m):
        global n
        lingua = ['it', 'en', 'de'][n]; n += 1
        return m.group(0) + parla(d, DEMO[d][lingua])
    s, k = re.subn(r'(<section class="hero">.*?<div class="cta">.*?</div>)', metti, s, count=3, flags=re.S)
    assert k == 3, (d, k)
    open(p, 'w', encoding='utf-8').write(s); print(d, 'ok')
