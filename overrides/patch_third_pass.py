from pathlib import Path

app=Path('_site/app.js')
src=app.read_text(encoding='utf-8')
insertion='async function importHealth('
assert src.count(insertion)==1, 'Punto aggiunta JS non univoco'
assert 'function renderTrainingTimerPro()' in src
assert 'function proMuscleDetails(ex)' in src
assert 'function proSetDetails()' in src
assert "function proCompleteSet()" in src
third=Path('overrides/workout-third-pass.js.txt').read_text(encoding='utf-8')
assert 'const thirdOriginalCards=' in third
assert 'const thirdOriginalCompleteSet=' in third
assert 'function thirdVolumeBySession(' in third
assert 'data-act="proCompleteSet"' in third
src=src.replace(insertion,third+'\n'+insertion,1)
app.write_text(src,encoding='utf-8')

css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/workout-third-pass.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')

sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v11')==1, 'Cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v11','ritmo-fit-static-v12'),encoding='utf-8')
print('Terza passata Allenamenti installata senza alterare schede e storico.')
