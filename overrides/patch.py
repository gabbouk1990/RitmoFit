from pathlib import Path
p=Path('_site/app.js')
s=p.read_text(encoding='utf-8')
start=s.index('function renderShifts(){')
end=s.index('function renderSettings(){',start)
new=Path('overrides/renderShifts.js.txt').read_text(encoding='utf-8')
s=s[:start]+new+'\n'+s[end:]
old="case 'monthStep':{const [y,m]=state.month.split('-').map(Number);const x=new Date(y,m-1+Number(t.dataset.n),1);state.month=`${x.getFullYear()}-${String(x.getMonth()+1).padStart(2,'0')}`;render();break;}"
updated="case 'monthStep':{const [y,m]=state.month.split('-').map(Number);const x=new Date(y,m-1+Number(t.dataset.n),1);state.month=`${x.getFullYear()}-${String(x.getMonth()+1).padStart(2,'0')}`;state.date=`${state.month}-${String(Math.min(Number(state.date.slice(8)),new Date(x.getFullYear(),x.getMonth()+1,0).getDate())).padStart(2,'0')}`;render();break;}"
if old not in s:raise RuntimeError('monthStep non trovato: impossibile eseguire patch in sicurezza')
s=s.replace(old,updated,1)
p.write_text(s,encoding='utf-8')
css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/turni.css').read_text(encoding='utf-8'),encoding='utf-8')
sw=Path('_site/sw.js')
a=sw.read_text(encoding='utf-8')
if 'ritmo-fit-static-v1' not in a:raise RuntimeError('Versione cache inattesa')
sw.write_text(a.replace('ritmo-fit-static-v1','ritmo-fit-static-v2'),encoding='utf-8')
