from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
def replace_once(old,new,description):
 global s
 assert s.count(old)==1, f'{description}: riferimento non univoco, trovati {s.count(old)}'
 s=s.replace(old,new,1)

extra=Path('overrides/food-alternatives.js.txt').read_text(encoding='utf-8')
replace_once('const FOOD_CATALOG=FOOD_CATALOG_ROWS.map',extra+'\nconst FOOD_CATALOG=FOOD_CATALOG_ROWS.map','Estensione catalogo')

replace_once(
 " if(state.workoutPane==='schede')content=",
 " if(state.workoutPane==='timer')content=renderTrainingTimer();\n else if(state.workoutPane==='schede')content=",
 "Vista timer")
tab_anchor='<button data-act="workoutPane" data-to="storico"'
tab_new="""<button data-act="workoutPane" data-to="timer" class="tab ${state.workoutPane==='timer'?'active':''}">Timer & recuperi</button>"""
replace_once(tab_anchor,tab_new+tab_anchor,"Pulsante timer")

card_button='<button class="btn btn-primary" data-act="openTemplate" data-id="${safe(t.id)}">Apri scheda</button>'
replace_once(card_button,
 '<button class="btn btn-primary" data-act="startWorkout" data-id="${safe(t.id)}">▶ Avvia sessione</button>'+card_button,
 'Avvio schede')
replace_once('Esplora 53 alimenti →','Esplora ${FOOD_CATALOG.length} alimenti →','Catalogo dinamico')
replace_once("await migrateTrainingProgram();if(upgradeDefaultMeals())await persist('meals');render();}",
 "await migrateTrainingProgram();if(upgradeDefaultMeals())await persist('meals');await restoreWorkoutRunner();render();}",
 'Ripristino timer')

insert_at=s.index('async function importHealth(')
extra_js='\n'.join(Path('overrides/'+f).read_text(encoding='utf-8') for f in
 ['workout-alternatives.js.txt','workout-timer.js.txt','food-live.js.txt'])
s=s[:insert_at]+extra_js+'\n'+s[insert_at:]

replace_once(
 'if(foodIngredientClick(act,t))return;',
 'if(foodIngredientClick(act,t))return;if(await handleWorkoutAction(act,t))return;',
 'Dispatcher timer')

app.write_text(s,encoding='utf-8')
css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/interactive-v5.css').read_text(encoding='utf-8'),encoding='utf-8')
sw=Path('_site/sw.js')
v=sw.read_text(encoding='utf-8')
assert v.count('ritmo-fit-static-v4')==1,'Versione cache imprevista'
sw.write_text(v.replace('ritmo-fit-static-v4','ritmo-fit-static-v5'),encoding='utf-8')
print('Patch interattiva alimentazione e allenamenti applicata')
