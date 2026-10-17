"""Enable encrypted 2026 shift import in the local PWA without publishing shift data."""
from pathlib import Path
import json, shutil

app=Path('_site/app.js')
source=app.read_text(encoding='utf-8')
def replace_exact(old,new,description):
 global source
 assert source.count(old)==1, f'{description}: found {source.count(old)}'
 source=source.replace(old,new,1)
replace_exact(
 "case 'icsImport':$('#icsFile').click();break;",
 "case 'secure2026Import':secure2026ImportDialog();break;case 'icsImport':$('#icsFile').click();break;",
 'Secure shift import dispatcher'
)
replace_exact(
 "async function importHealth(",
 Path('overrides/secure-import-2026.js.txt').read_text(encoding='utf-8')+'\nasync function importHealth(',
 'One-time key dialog and decryption'
)
replace_exact(
 "if(s?.type==='Ferie')return {name:'Allenamento facoltativo',why:'Ferie: giornata libera. Puoi scegliere una sessione di forza o nuoto, oppure recuperare; non è un obbligo.',key:'forza-a',icon:'🌴'};",
 """if(s?.type==='Ferie')return {name:'Allenamento facoltativo',why:'Ferie: giornata libera. Puoi scegliere una sessione di forza o nuoto, oppure recuperare; non è un obbligo.',key:'forza-a',icon:'🌴'};
 if(s?.type==='Malattia')return {name:'Recupero e riposo',why:'Giornata di malattia: niente allenamenti programmati automaticamente.',key:null,icon:'🛌'};
 if(['Congedo','Formazione','RPre'].includes(s?.type))return {name:'Programma da valutare',why:'Giornata speciale riportata da Supershift: nessun allenamento programmato automaticamente.',key:null,icon:'📆'};""",
 'No automatic workout on illness or special days'
)
replace_exact(
 "if(s&&s.type!=='Riposo'&&s.type!=='Smonto'&&s.type!=='Ferie')return s;",
 "if(s&&!['Riposo','Smonto','Ferie','Malattia','Congedo','RPre'].includes(s.type))return s;",
 'Next service excludes time off/illness'
)
app.write_text(source,encoding='utf-8')

secure=Path('overrides/supershift-2026-encrypted.json')
data=json.loads(secure.read_text(encoding='utf-8'))
assert data['alg']=='AES-256-GCM' and data['version']==1 and len(data['data'])>1700
dest=Path('_site/assets/secure/supershift-2026.enc.json')
dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile(secure,dest)

css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/secure-import-2026.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')

sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v15')==1,'Versione cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v15','ritmo-fit-static-v16'),encoding='utf-8')
print('Calendario cifrato caricato nella build: codice privato non incluso nel sito.')
