from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
entry='async function importHealth('
assert s.count(entry)==1, 'Punto di inserimento della quarta passata imprevisto'
assert 'function renderTrainingTimerPro()' in s
assert 'function renderWorkoutStatsPro()' in s
assert 'function thirdExerciseHistory(ex)' in s
assert 'function proMuscleDetails(ex)' in s
assert 'function proExerciseIllustration(ex' in s
assert 'function workoutSessionAction(s)' in s
overlay=Path('overrides/workout-fourth-pass.js.txt').read_text(encoding='utf-8')
assert 'rf4ExerciseScreen()' in overlay
assert 'rf4ActivityScreen()' in overlay
assert 'renderWorkoutCardsPro=function()' in overlay
assert 'renderTrainingTimerPro=function()' in overlay
assert 'handleWorkoutProAction=async function' in overlay
s=s.replace(entry,overlay+'\n'+entry,1)
app.write_text(s,encoding='utf-8')

css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/workout-fourth-pass.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')

sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v12')==1,'Versione cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v12','ritmo-fit-static-v13'),encoding='utf-8')
print('Quarta passata UX applicata. Schede, salvataggi e funzioni esistenti conservati.')
