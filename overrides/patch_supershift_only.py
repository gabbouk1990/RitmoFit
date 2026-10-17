"""Supershift 2026 only: exact source, dashboard correction and responsive cards."""
from pathlib import Path
app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
anchor='async function importHealth('
assert s.count(anchor)==1,'Punto inserimento turno non univoco'
assert "secure-supershift-2026-"+'' in s,'Secure Supershift functionality missing'
assert 'function renderShifts(){' in s
assert 'function renderWorkoutCardsPro()' in s
assert 'function secure2026ImportDialog()' in s
addition=Path('overrides/supershift-only-ui.js.txt').read_text(encoding='utf-8')
assert 'renderShifts=renderSupershift2026;' in addition
assert 'shiftFor=function(d){return sup2026Source(d);};' in addition
s=s.replace(anchor,addition+'\n'+anchor,1)
app.write_text(s,encoding='utf-8')

css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/supershift-only-ui.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')

sw=Path('_site/sw.js')
service=sw.read_text(encoding='utf-8')
assert service.count('ritmo-fit-static-v16')==1,'Versione cache inattesa'
sw.write_text(service.replace('ritmo-fit-static-v16','ritmo-fit-static-v17'),encoding='utf-8')

assert 'function sup2026Source(d)' in s
assert "id==='secure-supershift-2026-'+d" in s
assert 'function renderSupershift2026()' in s
assert 'sup2026OriginalRecommended' in s
print('Turnistica: fonte unica Supershift verificata. Schede riordinate.')
