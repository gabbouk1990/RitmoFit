from pathlib import Path

app=Path('_site/app.js')
s=app.read_text(encoding='utf-8')
data=Path('overrides/food-latest-20261017.js.txt').read_text(encoding='utf-8')
anchor='const FOOD_CATALOG=FOOD_CATALOG_ROWS.map'
assert s.count(anchor)==1,'Catalogo alimentare non individuato in modo univoco'
assert 'FOOD_CATALOG_ROWS.push(' in s,'Patch alimenti precedenti assente'
s=s.replace(anchor,data+'\n'+anchor,1)

a=s.index('function foodCatalogView(){')
b=s.index('function foodDiaryView(',a)
view=s[a:b]
def replace_once(old,new,label):
 global view
 n=view.count(old)
 assert n==1,f'{label}: trovate {n} occorrenze (attesa 1)'
 view=view.replace(old,new,1)

replace_once(
 "const active=FOOD_CATEGORIES.some(c=>c.id===state.foodCategory)?state.foodCategory:'proteine';",
 "const active=state.foodCategory==='recenti'||FOOD_CATEGORIES.some(c=>c.id===state.foodCategory)?state.foodCategory:'proteine';",
 'Filtro recenti')
replace_once(
 "const category=FOOD_CATEGORIES.find(c=>c.id===active);",
 "const category=active==='recenti'?{id:'recenti',icon:'✨',name:'Ultime aggiunte',hint:'Alimenti scelti nei pasti recenti'}:FOOD_CATEGORIES.find(c=>c.id===active);",
 'Titolo categoria recente')
replace_once(
 "const items=FOOD_CATALOG.filter(x=>x.category===active);",
 "const items=active==='recenti'?FOOD_CATALOG.filter(x=>RF_FOOD_LATEST_IDS.includes(x.id)):FOOD_CATALOG.filter(x=>x.category===active);",
 'Filtro alimenti recenti')
replace_once(
 '<div class="nutrition-category-filter" aria-label="Categorie di alimenti">${FOOD_CATEGORIES.map(c=>',
 '''<div class="nutrition-category-filter" aria-label="Categorie di alimenti"><button type="button" class="nutrition-category-button nutrition-recent-tab ${active==='recenti'?'active':''}" data-act="foodCategory" data-to="recenti" aria-pressed="${active==='recenti'}">✨ Ultime aggiunte</button>${FOOD_CATEGORIES.map(c=>''',
 'Pulsante ultime aggiunte')
replace_once(
 '<div class="nutrition-catalog-list">${items.length?',
 '''${active==='recenti'?'<p class="nutrition-recent-note">I valori dei prodotti di marca sono quelli discussi o stime provvisorie: fai riferimento alla confezione. Nessun pasto già registrato viene modificato.</p>':''}
 <div class="nutrition-catalog-list">${items.length?''',
 'Avvertenza prodotti')
replace_once(
 '<div><strong>${safe(item.name)}</strong><small>${safe(item.detail)}</small></div>',
 '''<div><strong>${safe(item.name)}</strong>${RF_FOOD_LATEST_IDS.includes(item.id)?'<span class="nutrition-new-badge">Nuovo · 17/10</span>':''}<small>${safe(item.detail)}</small></div>''',
 'Segnalazione alimenti nuovi')

s=s[:a]+view+s[b:]
app.write_text(s,encoding='utf-8')
css=Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8')+'\n'+Path('overrides/food-latest-20261017.css').read_text(encoding='utf-8')+'\n',encoding='utf-8')
sw=Path('_site/sw.js')
cache=sw.read_text(encoding='utf-8')
assert cache.count('ritmo-fit-static-v13')==1,'Versione cache inattesa'
sw.write_text(cache.replace('ritmo-fit-static-v13','ritmo-fit-static-v14'),encoding='utf-8')
print('Catalogo alimenti aggiornato con 12 prodotti, filtro Ultime aggiunte, senza toccare il diario.')
