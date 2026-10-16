from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
start=s.index(" if(state.workoutPane==='timer')content=",s.index("function renderWorkouts(){"))
end=s.index("\n else content=",start)
replacement=""" if(state.workoutPane==='timer')content=renderTrainingTimerPro();
 else if(state.workoutPane==='statistiche')content=renderWorkoutStatsPro();
 else if(state.workoutPane==='schede')content=renderWorkoutCardsPro();"""
s=s[:start]+replacement+s[end:]

tab='<button data-act="workoutPane" data-to="storico"'
assert s.count(tab)==1,'Scheda Storico non individuata'
s=s.replace(tab, """<button data-act="workoutPane" data-to="statistiche" class="tab ${state.workoutPane==='statistiche'?'active':''}">Statistiche</button>"""+tab,1)

click='if(await handleWorkoutAction(act,t))return;'
assert s.count(click)==1,'Gestore clic allenamenti non trovato'
s=s.replace(click,'if(await handleWorkoutProAction(act,t))return;'+click,1)

manual="""if(s.manual)return '<button type="button" class="btn session-delete-button" """
assert s.count(manual)==1,'Comando eliminazione manuale modificato'
s=s.replace(manual, """if(s.manual)return '<button type="button" class="btn btn-outline" data-act="proSessionDetails" data-id="'+safe(s.id)+'">Dettagli</button> <button type="button" class="btn session-delete-button" """,1)

inject=s.index('async function importHealth(')
extra=Path('overrides/workout-experience.js.txt').read_text(encoding='utf-8')
s=s[:inject]+extra+'\n'+s[inject:]
app.write_text(s,encoding='utf-8')

css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/workout-experience.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')

sw=Path('_site/sw.js')
old=sw.read_text(encoding='utf-8')
assert old.count('ritmo-fit-static-v8')==1,'Versione cache inattesa'
sw.write_text(old.replace('ritmo-fit-static-v8','ritmo-fit-static-v9'),encoding='utf-8')
print('Esperienza Allenamenti migliorata e dati locali conservati')
