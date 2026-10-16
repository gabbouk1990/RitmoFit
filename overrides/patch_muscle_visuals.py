from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
def change(old,new,label):
 global s
 n=s.count(old)
 assert n==1,f'{label}: {n} corrispondenze invece di 1'
 s=s.replace(old,new,1)

js=Path('overrides/muscle-visuals.js.txt').read_text(encoding='utf-8')
change('function proTemplateCard(t,i){',js+'\nfunction proTemplateCard(t,i){','Iniezione mapping anatomico')

change(
 '''<span class="pro-exercise-symbol pro-illustration-slot">'+proExerciseIllustration(x)+'</span><span class="pro-exercise-copy">''',
 '''<span class="pro-exercise-symbol pro-illustration-slot">'+proExerciseIllustration(x)+'</span><span class="pro-muscle-mini">'+proMuscleThumb(x)+'</span><span class="pro-exercise-copy">''',
 'Miniatura muscoli nelle schede')
change(
 '''<div class="pro-current-icon pro-active-art">'+proExerciseIllustration(x,1,'pro-current-image')+'</div><div><h2>''',
 '''<div class="pro-current-icon pro-active-art">'+proExerciseIllustration(x,1,'pro-current-image')+'</div><div class="pro-active-muscles">'+proMuscleThumb(x,'pro-active-muscle-img')+'</div><div><h2>''',
 'Muscoli durante esercizio attivo')
change(
 '''<div class="pro-detail-prescription"><strong>Programmazione</strong>''',
 '''<div class="pro-detail-prescription"><strong>Programmazione</strong>''',
 'Verifica dettaglio tecnico')
# Inserisci il pannello anatomico prima della tecnica, mantenendo il movimento prima del pannello.
change(
 '''</div><h3>Tecnica e attenzione</h3><p>''',
 '''</div>'+proMuscleDetails(x)+'<h3>Tecnica e attenzione</h3><p>''',
 'Panel anatomico dettagli')
app.write_text(s,encoding='utf-8')

css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/muscle-visuals.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')

sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v10')==1,'Versione cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v10','ritmo-fit-static-v11'),encoding='utf-8')

assert "function proMuscleKey(ex)" in s
assert "function proMuscleDetails(ex)" in s
assert "proMuscleThumb(x)" in s
assert "proMuscleDetails(x)" in s
print('Mappe anatomiche inserite nelle schede, esercizio corrente e dettagli.')
