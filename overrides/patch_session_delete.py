from pathlib import Path
app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
def only(old,new,description):
 global s
 hits=s.count(old)
 assert hits==1, f'{description}: expected 1, found {hits}'
 s=s.replace(old,new,1)

helper="""function workoutSessionAction(s){
 if(!s.manual)return '<span class="session-import-label" title="Registrazione importata da Apple Salute">Da Salute</span>';
 return '<button type="button" class="btn session-delete-button" data-act="deleteWorkoutSession" data-id="'+safe(s.id)+'" aria-label="Elimina allenamento '+safe(s.type||s.name||'registrato')+'" title="Elimina solo questa sessione manuale">🗑️ Elimina</button>';
}
"""
only('function renderWorkouts(){',helper+'function renderWorkouts(){','Render session helper')
only('<th>FC media</th></tr></thead>','<th>FC media</th><th>Azioni</th></tr></thead>','Header azioni')
only('<td>${fmt(s.heartRate?.avg)} bpm</td></tr>','<td>${fmt(s.heartRate?.avg)} bpm</td><td class="session-delete-cell">${workoutSessionAction(s)}</td></tr>','Manual delete button')

handler="""case 'deleteWorkoutSession':{
 const session=state.sessions.find(s=>s.id===id);
 if(!session){toast('Allenamento manuale non trovato.');break;}
 const label=(session.type||session.name||'Allenamento')+' del '+dateFmt(session.date,{day:'numeric',month:'short',year:'numeric'});
 if(!confirm('Eliminare definitivamente "'+label+'" dallo storico?\\n\\nQuesta operazione non modifica gli allenamenti importati da Apple Salute.'))break;
 const previous=state.sessions;
 state.sessions=previous.filter(s=>s.id!==id);
 try{
  await persist('sessions');
  render();
  toast('Allenamento eliminato dallo storico.');
 }catch(e){
  state.sessions=previous;
  render();
  toast('Impossibile eliminare la sessione: '+e.message);
 }
 break;
}
"""
only("case 'logWorkout':logWorkout();break;",handler+"case 'logWorkout':logWorkout();break;",'Azioni eliminazione')
app.write_text(s,encoding='utf-8')
css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/session-delete.css').read_text(encoding='utf-8'),encoding='utf-8')
sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v5')==1,'Versione cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v5','ritmo-fit-static-v6'),encoding='utf-8')
print('Eliminazione protetta delle sessioni manuali: patch applicata')
