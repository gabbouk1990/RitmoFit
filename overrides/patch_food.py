from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
assert "const MEALS=[" in s and "function renderFood()" in s

catalog=Path('overrides/food-catalog.js.txt').read_text(encoding='utf-8')
editor=Path('overrides/food-editor.js.txt').read_text(encoding='utf-8')
view=Path('overrides/food-view.js.txt').read_text(encoding='utf-8')
# Il pattern data in regex deve usare \d, non il backslash doppio.
editor=editor.replace(r'/^\\d{4}-\\d{2}-\\d{2}$/',r'/^\d{4}-\d{2}-\d{2}$/')

s=s.replace("foodPane:'piano',","foodPane:'piano',foodCategory:'proteine',",1)
state_start=s.index('let state={')
s=s[:state_start]+catalog+'\n'+s[state_start:]

startup='await migrateTrainingProgram();render();}'
assert startup in s,'Inizializzazione schema schede cambiata'
s=s.replace(startup,"await migrateTrainingProgram();if(upgradeDefaultMeals())await persist('meals');render();}",1)

render_start=s.index('function renderFood(){')
render_end=s.index('function metricSeries(',render_start)
s=s[:render_start]+view+'\n'+s[render_end:]

editor_start=s.index('function editMeal(')
editor_end=s.index('function editTemplate(',editor_start)
s=s[:editor_start]+editor+'\n'+s[editor_end:]

act_anchor="const act=t.dataset.act,id=t.dataset.id;"
assert act_anchor in s,'Dispatcher azioni non individuato'
s=s.replace(act_anchor,act_anchor+"if(foodIngredientClick(act,t))return;",1)
pane_anchor="case 'foodPane':state.foodPane=t.dataset.to;render();break;"
assert pane_anchor in s,'Selezione scheda Alimentazione non trovata'
s=s.replace(pane_anchor,pane_anchor+"case 'foodCategory':state.foodCategory=t.dataset.to;render();break;",1)
remove_anchor="case 'removeFoodLog':"
assert remove_anchor in s
s=s.replace(remove_anchor,"case 'editFoodLog':editFoodLog(id);break;"+remove_anchor,1)

listeners="$('#healthFile').addEventListener('change',"
assert listeners in s
s=s.replace(listeners,
 """document.addEventListener('change',e=>{foodIngredientChange(e);});
document.addEventListener('input',e=>{if(e.target.closest('#foodIngredients'))foodUpdatePreview();});
""" + listeners,1)

app.write_text(s,encoding='utf-8')
css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/food.css').read_text(encoding='utf-8'),encoding='utf-8')
sw=Path('_site/sw.js')
source=sw.read_text(encoding='utf-8')
assert 'ritmo-fit-static-v3' in source,'Cache versione inattesa'
sw.write_text(source.replace('ritmo-fit-static-v3','ritmo-fit-static-v4'),encoding='utf-8')
