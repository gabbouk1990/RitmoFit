"""Turni MP/F, priorità correzioni manuali, Supershift e recupero."""
from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
def once(old,new,label):
 global s
 count=s.count(old)
 assert count==1,f'{label}: attesa una corrispondenza, trovate {count}'
 s=s.replace(old,new,1)

once(
 'function shiftFor(d){const events=state.shifts.filter(s=>s.date===d);if(events.length)return events[0];',
 "function shiftFor(d){const events=state.shifts.filter(s=>s.date===d);if(events.length)return events.find(s=>s.source==='manual')||events[0];",
 'Priorità turni manuali')

once(
 "if(s&&s.type!=='Riposo'&&s.type!=='Smonto')return s;",
 "if(s&&s.type!=='Riposo'&&s.type!=='Smonto'&&s.type!=='Ferie')return s;",
 'Esclusione ferie dai prossimi servizi')

once(
 "function shiftTime(shift){if(!shift)return '';if(shift.source==='pattern')",
 """function shiftTime(shift){if(!shift)return '';
 if(shift.source==='manual')return {Mattina:'06:50–14:22',Pomeriggio:'13:50–21:22',Notte:'20:50–07:22',Smonto:'Dopo notte',Riposo:'Giornata libera',MP:'06:50–21:22',Ferie:'Giornata libera'}[shift.type]||'';
 if(shift.type==='MP'&&!shift.displayStart&&!shift.displayEnd)return '06:50–21:22';
 if(shift.type==='Ferie'&&!shift.displayStart&&!shift.displayEnd)return 'Giornata libera';
 if(shift.source==='pattern')""",
 'Orario specifico MP e ferie')

once(
 "function recommended(d){const s=shiftFor(d),day=new Date(d+'T12:00:00').getDay();if(state.settings.weekendsOff",
 """function recommended(d){const s=shiftFor(d),day=new Date(d+'T12:00:00').getDay();
 if(s?.type==='MP')return {name:'Riposo dagli allenamenti',why:'Turno MP 06:50–21:22: giornata dedicata al lavoro e al recupero. Nessuna sessione proposta.',key:null,icon:'🛌'};
 if(s?.type==='Ferie')return {name:'Allenamento facoltativo',why:'Ferie: giornata libera. Puoi scegliere una sessione di forza o nuoto, oppure recuperare; non è un obbligo.',key:'forza-a',icon:'🌴'};
 if(state.settings.weekendsOff""",
 'Suggerimenti MP e F anche nel weekend')

once(
 "state.shifts=events;await persist('shifts');",
 "state.shifts=[...state.shifts.filter(e=>e.source==='manual'),...events];await persist('shifts');",
 'Conserva modifiche manuali quando reimporti Supershift')

manual="""case 'saveManualShift':{
 const date=state.date,type=document.querySelector('#manualShiftType')?.value;
 const allowed=['Mattina','Pomeriggio','Notte','Smonto','Riposo','MP','Ferie'];
 if(!allowed.includes(type)){toast('Seleziona un turno valido.');break;}
 const original=state.shifts;
 state.shifts=[...original.filter(e=>!(e.date===date&&e.source==='manual')),{id:'manual|'+date,date,type,label:type==='MP'?'MP':type==='Ferie'?'Ferie':type,source:'manual'}];
 try{await persist('shifts');render();toast('Turno '+(type==='Ferie'?'F':type)+' salvato per il '+date+'.');}
 catch(err){state.shifts=original;render();toast('Salvataggio turno non riuscito: '+err.message);}
 break;
}
case 'removeManualShift':{
 const date=state.date,original=state.shifts;
 if(!original.some(e=>e.date===date&&e.source==='manual'))break;
 state.shifts=original.filter(e=>!(e.date===date&&e.source==='manual'));
 try{await persist('shifts');render();toast('Modifica rimossa: ripristinato il calendario importato o la rotazione.');}
 catch(err){state.shifts=original;render();toast('Ripristino turno non riuscito: '+err.message);}
 break;
}
"""
once("case 'savePattern':{",manual+"case 'savePattern':{",'Comandi turni manuali')

app.write_text(s,encoding='utf-8')

ics=Path('_site/ics.js')
it=ics.read_text(encoding='utf-8')
needle=" const s=String(summary||'').toLowerCase().trim();"
assert it.count(needle)==1,'Classificazione ICS modificata'
classification=""" const s=String(summary||'').toLowerCase().trim();
 // Il controllo MP deve precedere i singoli turni M e P.
 if(/\\bmp\\b|\\bm\\s*[-/+&]\\s*p\\b|\\bmattina\\s*(?:e|[-/+&])\\s*pomeriggio\\b|\\bturno\\s+lungo\\b|\\bdoppio\\s+turno\\b|06[.:]50\\s*[-–—]\\s*21[.:]22/.test(s))return 'MP';
 // Nel calendario Supershift F significa ferie, non il generico 'fuori turno'.
 if(s==='f'||/\\bturno\\s+f\\b/.test(s))return 'Ferie';"""
it=it.replace(needle,classification,1)
ics.write_text(it,encoding='utf-8')

css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\\n'+Path('overrides/shift-mp-ferie.css').read_text(encoding='utf-8')+'\\n',encoding='utf-8')

sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v14')==1,'Versione cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v14','ritmo-fit-static-v15'),encoding='utf-8')

assert "type==='MP'" in s and "type==='Ferie'" in s
assert 'saveManualShift' in s and 'removeManualShift' in s
assert "source==='manual'" in s
print('MP (06:50–21:22) e F (ferie) integrati: calendario, recupero, modifiche e ICS.')
