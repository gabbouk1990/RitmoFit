from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
def change(old,new,label):
 global s
 found=s.count(old)
 assert found==1,f'{label}: corrispondenze trovate {found}, attesa 1'
 s=s.replace(old,new,1)

library=Path('overrides/exercise-image-map.js.txt').read_text(encoding='utf-8')
change('function proTemplateCard(t,i){',library+'\nfunction proTemplateCard(t,i){','Inserimento libreria esercizi')
change('exercises.slice(0,5).map((x,j)=>{','exercises.map((x,j)=>{','Mostra tutti gli esercizi in scheda')
change('''<span class="pro-exercise-symbol">'+fx.icon+'</span><span class="pro-exercise-copy">''',
       '''<span class="pro-exercise-symbol pro-illustration-slot">'+proExerciseIllustration(x)+'</span><span class="pro-exercise-copy">''',
       'Immagine miniature lista')
change("+(exercises.length>5?'<p class=\"caption\">+'+(exercises.length-5)+' esercizi nella scheda completa</p>':'')",
       "",
       'Rimuovi contatore oltre prime cinque')
change('''<div class="pro-current-icon">'+proInfo(x.name).icon+'</div><div><h2>''',
       '''<div class="pro-current-icon pro-active-art">'+proExerciseIllustration(x,1,'pro-current-image')+'</div><div><h2>''',
       'Immagine esercizio attivo')
change('''<span class="pro-jump-index">'+(i+1)+'</span><span><strong>''',
       '''<span class="pro-jump-index">'+(i+1)+'</span><span class="pro-jump-art">'+proExerciseIllustration(e,1,'pro-jump-image')+'</span><span><strong>''',
       'Immagine elenco esercizi sessione')
change('''<div class="pro-detail-icon">'+meta.icon+'</div><div class="eyebrow">''',
       '''<div class="pro-detail-art">'+proExerciseIllustration(x,1,'pro-detail-image')+proExerciseIllustration(x,2,'pro-detail-image')+'</div><div class="eyebrow">''',
       'Immagini posizioni nella scheda tecnica')
change("'<p class=\"caption\">Indicazioni generali: non sostituiscono la supervisione di un allenatore o di un professionista sanitario.</p></div>'",
       "'<p class=\"caption\">Indicazioni generali: non sostituiscono la supervisione di un allenatore o di un professionista sanitario.</p>'+PRO_EXERCISE_IMAGE_CREDITS+'</div>'",
       'Attribuzione dettagli')
change("+'</div><div class=\"pro-bottom-actions\"><button class=\"btn btn-outline\" data-act=\"newTemplate\">+ Crea scheda</button><button class=\"btn btn-outline\" data-act=\"restoreProgram\">↺ Schede consigliate</button></div>';",
       "+'</div><div class=\"pro-bottom-actions\"><button class=\"btn btn-outline\" data-act=\"newTemplate\">+ Crea scheda</button><button class=\"btn btn-outline\" data-act=\"restoreProgram\">↺ Schede consigliate</button></div>'+PRO_EXERCISE_IMAGE_CREDITS;",
       'Attribuzione schede')
app.write_text(s,encoding='utf-8')

css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/exercise-image-styles.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')

sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v9')==1,'Versione cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v9','ritmo-fit-static-v10'),encoding='utf-8')

assert 'function proImageSlug(name)' in s
assert 'proExerciseIllustration(x,2' in s
assert 'exercises.map((x,j)' in s
assert 'PRO_EXERCISE_IMAGE_CREDITS' in s
print('Immagini esercizi integrate in schede, sessione e dettagli.')
