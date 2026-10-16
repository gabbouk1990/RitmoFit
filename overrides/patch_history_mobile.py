from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')

def replace_once(old,new,description):
    global s
    hits=s.count(old)
    assert hits==1, f'{description}: attesa una corrispondenza, trovate {hits}'
    s=s.replace(old,new,1)

# Save only hidden IDs: Health workouts remain untouched.
replace_once(
    'await restoreWorkoutRunner();render();}',
    "await restoreWorkoutRunner();state.hiddenHealthWorkouts=await getItem('hiddenHealthWorkouts',[]);if(!Array.isArray(state.hiddenHealthWorkouts))state.hiddenHealthWorkouts=[];render();}",
    'Caricamento esclusioni Salute')

old_helper=s.index('function workoutSessionAction(s){')
end_helper=s.index('function renderWorkouts(){',old_helper)
helper="""function workoutSessionKey(s){
 return String(s?.id||[s?.start,s?.end,s?.source,s?.type,s?.date,s?.duration].join('|'));
}
function workoutSessionAction(s){
 const key=workoutSessionKey(s);
 if(s.manual)return '<button type="button" class="btn session-delete-button" data-act="deleteWorkoutSession" data-id="'+safe(key)+'" aria-label="Elimina sessione manuale '+safe(s.type||s.name||'Allenamento')+'">🗑️ Elimina</button>';
 return '<button type="button" class="btn session-hide-button" data-act="hideHealthWorkout" data-id="'+safe(key)+'" aria-label="Nascondi allenamento importato '+safe(s.type||s.name||'Allenamento')+'" title="Nasconde il record solo nello storico di Ritmo Fit">◉ Nascondi</button>';
}
"""
s=s[:old_helper]+helper+s[end_helper:]

replace_once(
    'function renderWorkouts(){const fromH=state.health?.workouts||[];let content=',
    "function renderWorkouts(){const fromH=(state.health?.workouts||[]).filter(s=>!state.hiddenHealthWorkouts.includes(workoutSessionKey(s)));let content=",
    'Storico Salute filtrato')
replace_once('Sessioni da Salute</h3>','Storico allenamenti</h3>','Titolo storico')
replace_once(
    '<div class="table-wrap"><table class="data-table"><thead><tr><th>Quando',
    '<div class="table-wrap workout-history-scroll"><table class="data-table workout-history-table"><thead><tr><th>Quando',
    'Tabella mobile')
replace_once('<th>FC media</th><th>Azioni</th></tr></thead>','<th>FC media</th></tr></thead>','Colonna rimossa')
replace_once(
    '<td class="session-delete-cell">${workoutSessionAction(s)}</td>',
    '',
    'Azione di fine riga rimossa')
replace_once(
    "</small></td><td>${fmt(s.duration)} min</td>",
    '</small><div class="session-inline-actions">${workoutSessionAction(s)}</div></td><td>${fmt(s.duration)} min</td>',
    'Azione sotto il nome allenamento')
replace_once(
    '</span></div><button class="btn btn-primary" data-act="logWorkout">',
    """</span>${state.hiddenHealthWorkouts.length?'<button class="btn btn-outline session-restore-button" data-act="restoreHiddenHealth">Ripristina nascosti ('+state.hiddenHealthWorkouts.length+')</button>':''}</div><button class="btn btn-primary" data-act="logWorkout">""",
    'Ripristino delle sessioni nascoste')

actions="""case 'hideHealthWorkout':{
 const imported=(state.health?.workouts||[]).find(w=>workoutSessionKey(w)===id);
 if(!imported){toast('Allenamento di Salute non trovato.');break;}
 const description=(imported.type||'Allenamento')+' del '+dateFmt(imported.date,{day:'numeric',month:'short',year:'numeric'});
 if(!confirm('Nascondere "'+description+'" dallo storico di Ritmo Fit?\\n\\nNon cancellerai nulla da Apple Salute e non modificherai i riepiloghi dell’app Salute. Puoi ripristinarlo quando vuoi.'))break;
 const previous=state.hiddenHealthWorkouts;
 state.hiddenHealthWorkouts=[...new Set([...previous,id])];
 try{await setItem('hiddenHealthWorkouts',state.hiddenHealthWorkouts);render();toast('Allenamento nascosto dallo storico di Ritmo Fit.');}
 catch(e){state.hiddenHealthWorkouts=previous;render();toast('Impossibile nascondere l’allenamento: '+e.message);}
 break;
}
case 'restoreHiddenHealth':{
 if(!state.hiddenHealthWorkouts.length)break;
 if(!confirm('Rendere nuovamente visibili nello storico tutti gli allenamenti importati che avevi nascosto?'))break;
 const previous=state.hiddenHealthWorkouts;
 state.hiddenHealthWorkouts=[];
 try{await setItem('hiddenHealthWorkouts',[]);render();toast('Allenamenti importati ripristinati nello storico.');}
 catch(e){state.hiddenHealthWorkouts=previous;render();toast('Impossibile ripristinare: '+e.message);}
 break;
}
"""
replace_once("case 'deleteWorkoutSession':",actions+"case 'deleteWorkoutSession':",'Gestione dei record Salute')

app.write_text(s,encoding='utf-8')
css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/history-mobile.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')
sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v7')==1,'Versione della cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v7','ritmo-fit-static-v8'),encoding='utf-8')
print('Comandi visibili nello storico e filtro Salute reversibile aggiunti.')
