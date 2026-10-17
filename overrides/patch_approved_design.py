from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
anchor='async function importHealth('
assert s.count(anchor)==1,'Inserimento design non univoco'
assert 'function rf4ExerciseScreen()' in s
assert 'function secure2026ImportDialog()' in s
assert "renderShifts=renderSupershift2026;" in s
assert 'function proExerciseIllustration(ex' in s
assert 'function proMuscleDetails(ex)' in s
assert 'function thirdExerciseHistory(ex)' in s
assert 'function rf4ActivityScreen()' in s
approved=Path('overrides/approved-design-ritmofit.js.txt').read_text(encoding='utf-8')
assert 'rf4ExerciseScreen=function()' in approved
assert 'async function rf5SaveDraft(' in approved
assert 'renderToday=function()' in approved
assert 'rf4TemplateScreen=function()' in approved
assert 'renderTrainingTimerPro=function()' in approved
s=s.replace(anchor,approved+'\n'+anchor,1)
app.write_text(s,encoding='utf-8')
css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/approved-design-ritmofit.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')
sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v17')==1,'Versione cache imprevista'
sw.write_text(cache.replace('ritmo-fit-static-v17','ritmo-fit-static-v18'),encoding='utf-8')
print('UI approvata integrata. IndexedDB, turni e dati di alimentazione invariati.')
