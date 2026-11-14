# Widget di qualificazione lead – Ford Interauto

Widget multistep (5 domande) per qualificare i lead delle landing **auto** e **veicoli commerciali (Ford Pro)**.
Calcola un punteggio da 0 a 100, assegna un segmento (hot, warm, cold) e passa i dati al form Umbraco già presente sulla pagina.

- Un solo file JavaScript, nessuna dipendenza.
- Stili isolati con Shadow DOM: il CSS della landing non lo altera.
- Pensato per CMS che non accettano script nella pagina: si inserisce con un iframe.

## Contenuto del repository

| Percorso | A cosa serve |
|---|---|
| `src/ford-lead-widget.js` | Il widget. **È l'unico file da modificare** per cambiare domande, punteggi o grafica. |
| `build.py` | Rigenera `index.html` e `dist/` dal widget. |
| `index.html` | Pagina ospitata (GitHub Pages) da usare in un iframe con `src`. Generata da `build.py`. |
| `dist/ford-lead-srcdoc-auto-qualify.html` | Iframe "tutto dentro" per le landing auto. Generato. |
| `dist/ford-lead-srcdoc-pro-qualify.html` | Iframe "tutto dentro" per le landing veicoli commerciali. Generato. |
| `demo.html` | Pagina di prova locale, con form contatti integrato nel widget. |

## Pubblicare su GitHub

```bash
cd ford-lead-widget
git init
git add .
git commit -m "Widget lead Ford Interauto"
git branch -M main
git remote add origin https://github.com/TUO-UTENTE/ford-lead-widget.git
git push -u origin main
```

Crea prima il repository vuoto su github.com (senza README, `.gitignore` o licenza, che ci sono già).

Per ospitare `index.html` con **GitHub Pages**: *Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save*.
Dopo un minuto la pagina è su `https://TUO-UTENTE.github.io/ford-lead-widget/`.
Con un account gratuito il repository deve essere pubblico: non metterci mai indirizzi di webhook o dati riservati.

## Come inserirlo nella landing

Il widget fa le domande, poi porta l'utente al **form Umbraco sulla stessa pagina**. Ci sono due modi.

### Opzione A: iframe "tutto dentro" (non serve hosting)

Apri `dist/ford-lead-srcdoc-auto-qualify.html` (o `-pro-`), copia tutto e incollalo in un blocco HTML della landing.
L'id del form (`umbraco_form_be2f4f1afda648c4bd1c14cc52ca592f`) è già nel codice.
Se il CMS rifiuta il blocco, usa l'opzione B.

### Opzione B: iframe con indirizzo (GitHub Pages)

```html
<iframe title="Qualificazione auto Ford"
  src="https://TUO-UTENTE.github.io/ford-lead-widget/?product=auto&mode=qualify&form=https://INDIRIZZO-DELLA-LANDING&anchor=umbraco_form_be2f4f1afda648c4bd1c14cc52ca592f"
  style="width:100%;border:0;height:620px" loading="lazy"></iframe>
```

Qui `form` deve essere l'indirizzo completo della landing, perché la pagina ospitata non può leggerlo da sola.

| Parametro | Valori | Note |
|---|---|---|
| `product` | `auto`, `pro` | Versione del widget. Se manca: `auto`. |
| `mode` | `qualify`, `full` | `qualify`: solo domande, poi vai al tuo form. `full`: il widget raccoglie anche i contatti. |
| `form` | indirizzo completo | Pagina che contiene il form (solo con `mode=qualify`). |
| `anchor` | id del form | Per scorrere fino al form dopo il ricaricamento. |
| `endpoint` | indirizzo | Solo con `mode=full`: webhook che riceve il lead in POST JSON. |
| `privacy` | indirizzo | Solo con `mode=full`: informativa privacy. |
| `phone` | numero | Solo con `mode=full`: telefono mostrato a fine flusso. |

## Collegamento al form Umbraco

1. Nel form aggiungi cinque campi **Hidden** (nascosti).
2. Come valore predefinito di ciascuno scrivi:

   | Campo | Valore predefinito |
   |---|---|
   | punteggio | `[@lead_score]` |
   | segmento | `[@lead_segment]` |
   | tag | `[@lead_tags]` |
   | riepilogo risposte | `[@lead_summary]` |
   | prodotto | `[@lead_product]` |

3. Nel workflow del form (invio al CRM) aggiungi questi campi tra quelli inviati.

Cosa succede: a fine domande l'utente clicca "Vai al modulo", la pagina si ricarica con i valori nell'indirizzo e il form li legge. Dopo il ricaricamento il widget mostra "Hai già risposto alle domande" invece di ripartire.

Note:

- La sintassi `[@nome]` è quella di Umbraco Forms per leggere un valore dall'indirizzo. Verifica sempre con un test che i campi si riempiano.
- Non chiamare un campo `model`: in alcuni casi segnalati dalla comunità dà errore.
- Se il CRM non ha campi per punteggio e segmento, manda almeno `lead_summary` nel campo note.
- I consensi privacy e marketing restano nel tuo form: in modalità `qualify` il widget non li raccoglie.

## Domande e punteggi

Punteggio totale massimo 100.

**Auto**

| Domanda | Risposte e punti |
|---|---|
| Quando pensi di acquistare? | Entro 1 mese 30 · 1-3 mesi 20 · 3-6 mesi 10 · Sto solo guardando 0 |
| Budget indicativo | Oltre 40.000 € 20 · 30-40.000 € 15 · 25-30.000 € 8 · Non lo so 5 · Sotto 25.000 € 0 |
| Come preferisci acquistare? | Finanziamento 15 · Contanti 15 · Noleggio a lungo termine 12 · Non lo so 5 |
| Auto da permutare? | Sì 10 (+5 se compili marca e modello) · Prima auto 7 · Tengo l'auto attuale 3 |
| Cosa vuoi fare ora? | Test drive 25 · Preventivo 18 · Parlare con un consulente 15 · Solo informazioni 5 |

**Veicoli commerciali** (prima: tipo di veicolo, poi se hai una P.IVA, senza punteggio)

| Domanda | Risposte e punti |
|---|---|
| Quando ti serve? | Entro 1 mese 25 · 1-3 mesi 17 · 3-6 mesi 8 · Sto solo valutando 0 |
| Quanti veicoli? | Oltre 10: 20 · 6-10: 18 · 2-5: 14 · 1: 8 |
| Come acquisire il mezzo? | Noleggio a lungo termine 15 · Leasing o finanziamento 15 · Contanti 12 · Non lo so 5 |
| Sostituisci un veicolo? | Sì 10 (+5 se compili marca e modello) · Amplio la flotta 8 · Primo mezzo 5 |
| Cosa vuoi fare ora? | Prova su strada 30 · Preventivo 22 · Consulente Ford Pro 18 · Solo informazioni 5 |

**Segmenti**

| Punteggio | Segmento | Messaggio finale |
|---|---|---|
| 70-100 | hot | Ti richiamiamo entro 30 minuti |
| 40-69 | warm | Ti contattiamo entro 24 ore |
| 0-39 | cold | Informazioni e novità |

**Regole speciali**

- Hot a prescindere dal punteggio: acquisto entro 1 mese con test drive o prova su strada richiesti. Per i veicoli commerciali anche una flotta oltre 10 mezzi.
- Cold a prescindere dal punteggio: per le auto, budget sotto 25.000 € senza noleggio. Per i veicoli commerciali, 1 solo veicolo con "sto solo valutando" e "solo informazioni".
- Chi risponde "sto solo guardando" salta le domande su budget e modalità di acquisto (per i veicoli commerciali salta solo la modalità).
- Noleggio a lungo termine: domanda in più su privato/P.IVA (auto) o su durata e km (veicoli commerciali).
- Il punteggio non viene mai mostrato all'utente.

## Eventi per il tracciamento

A fine domande il widget emette sull'elemento l'evento `ford-lead:complete`, con questi dati in `detail`: `score`, `segment`, `tags`, `summary`, `product` e, in modalità `full`, i contatti e i consensi.
Dentro l'iframe viene anche inviato un messaggio alla pagina padre con segmento, punteggio e prodotto (senza dati personali).
Se il CMS non accetta script nella pagina, il tracciamento delle conversioni va fatto sulla pagina di ringraziamento del form.

## Modificare il widget

1. Cambia `src/ford-lead-widget.js`: domande e punteggi sono nell'oggetto `DATA` in cima al file, la grafica nella costante `CSS`.
2. Esegui `python3 build.py` per rigenerare `index.html` e `dist/`.
3. Prova con `demo.html` (aprilo nel browser) e con un test completo sul form reale.
4. Fai il commit e il push. Se usi GitHub Pages, l'aggiornamento è online in un minuto.

Per cambiare l'id del form o l'altezza dell'iframe, modifica le due costanti all'inizio di `build.py`.

## Da verificare prima di andare online

- I testi dei consensi privacy e marketing vanno approvati dal legale o dal DPO.
- Le fasce di budget delle auto sono indicative e vanno allineate al listino.
- Il funzionamento sul form Umbraco e sul CRM va provato con un lead di test.
- Il repository non ha una licenza: aggiungine una (file `LICENSE`) se vuoi definire come può essere riusato il codice.
