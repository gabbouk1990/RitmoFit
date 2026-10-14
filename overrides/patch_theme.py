from pathlib import Path
import json

app=Path('_site/app.js')
src=app.read_text(encoding='utf-8')
anchor="function render(){renderNav();"
assert src.count(anchor)==1, "Punto di navigazione inatteso"
src=src.replace(anchor,"function render(){document.body.dataset.tab=state.tab;renderNav();",1)
app.write_text(src,encoding='utf-8')

css=Path('_site/style.css')
theme=Path('overrides/theme-dark.css').read_text(encoding='utf-8')
assert 'body[data-tab="allenamenti"]' in theme and 'body[data-tab="alimentazione"]' in theme
css.write_text(css.read_text(encoding='utf-8')+'\n'+theme+'\n',encoding='utf-8')

html=Path('_site/index.html')
htmltext=html.read_text(encoding='utf-8')
assert '<meta name="theme-color" content="#0b1523"' in htmltext
html.write_text(htmltext.replace('<meta name="theme-color" content="#0b1523"','<meta name="theme-color" content="#07111a"',1),encoding='utf-8')

manifest=Path('_site/manifest.webmanifest')
data=json.loads(manifest.read_text(encoding='utf-8'))
data['background_color']='#07111a'
data['theme_color']='#07111a'
manifest.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')

sw=Path('_site/sw.js')
service=sw.read_text(encoding='utf-8')
assert service.count('ritmo-fit-static-v6')==1,'Versione cache inattesa'
sw.write_text(service.replace('ritmo-fit-static-v6','ritmo-fit-static-v7'),encoding='utf-8')
print('Tema scuro, sfondi dedicati, manifest e cache aggiornati.')
