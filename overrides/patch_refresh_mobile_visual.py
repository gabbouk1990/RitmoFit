"""Production visual refresh: preserve all latest RitmoFit functions/data."""
from pathlib import Path
app=Path('_site/app.js')
js=app.read_text(encoding='utf-8')
anchor='async function importHealth('
assert js.count(anchor)==1,'App integration point missing'
for token in ['function sup2026Source(d)','function secure2026ImportDialog()',
              'function rf5CustomControls(ex)','function rf4ExerciseScreen()',
              'function foodCatalogView()','function proCompleteSet()',
              'function proSessionFinish()','function renderToday()',
              'function renderNav()']:
 assert token in js,f'Expected prior feature missing: {token}'
overlay=Path('overrides/refresh-mobile-visual.js.txt').read_text(encoding='utf-8')
assert 'renderToday=function()' in overlay
assert 'renderNav=function()' in overlay
assert "rf6TodayShift()" in overlay
assert "proWeekProgress()" in overlay
assert "proWeeklySessions(inputDate())" in overlay
assert "data-act=\\"rf5GoWorkouts\\"" in overlay
assert "data-act=\\"nav\\" data-to=\\"alimentazione\\"" in overlay
assert "data-act=\\"nav\\" data-to=\\"turni\\"" in overlay
js=js.replace(anchor,overlay+'\n'+anchor,1)
app.write_text(js,encoding='utf-8')

css=Path('_site/style.css')
current=css.read_text(encoding='utf-8')
visual=Path('overrides/refresh-mobile-visual.css').read_text(encoding='utf-8')
assert '.rf6-mountain-hero' in visual
assert '.rf5-activity-photo' in visual
assert '.rf5-template-line' in visual
assert '.pro-timer-ring' in visual
css.write_text(current+'\n'+visual+'\n',encoding='utf-8')

sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v18')==1,'Service worker cache unexpected'
sw.write_text(cache.replace('ritmo-fit-static-v18','ritmo-fit-static-v19'),encoding='utf-8')
print('Restyling 2026 completato sulla versione aggiornata, senza cancellare dati locali.')
