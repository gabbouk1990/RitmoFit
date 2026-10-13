from pathlib import Path

app = Path('_site/app.js')
s = app.read_text(encoding='utf-8')
original_start = s.index('const TEMPLATES=[')
original_end = s.index('const MEALS=[', original_start)
legacy = s[original_start:original_end].replace('const TEMPLATES=', 'const LEGACY_TEMPLATES=', 1)
program = Path('overrides/training-program.js.txt').read_text(encoding='utf-8')
s = s[:original_start] + legacy + '\n' + program + '\n' + s[original_end:]

# Upgrade only stock templates. Custom exercises and historical sessions are untouched.
initial = "state.settings={...{proteinGoal:150,kcalGoal:0,carbsGoal:0,fatsGoal:0,shiftAnchor:'',patternEnabled:false,weekendsOff:true},...state.settings};render();}"
assert initial in s, "Punto inizializzazione sconosciuto"
s = s.replace(initial, initial.replace(';render();}', ';await migrateTrainingProgram();render();}'), 1)

# Preserve historical-session rendering while updating only template cards.
start = s.index(" if(state.workoutPane==='schede')content=", s.index("function renderWorkouts(){"))
end = s.index("\n else content=", start)
s = s[:start] + ' ' + Path('overrides/workouts-render.js.txt').read_text(encoding='utf-8').strip() + s[end:]

# Update editor and read-only template detail without altering the session logging.
start = s.index('function editTemplate(')
end = s.index('function logWorkout(', start)
s = s[:start] + Path('overrides/workouts-editor.js.txt').read_text(encoding='utf-8') + '\n' + s[end:]

event_anchor = "case 'newTemplate':editTemplate(null);break;"
assert event_anchor in s, "Dispatcher schede non trovato"
s = s.replace(event_anchor, "case 'restoreProgram':await restoreTrainingProgram();break;" + event_anchor, 1)
s = s.replace('Forza A/B, piscina e Hybrid modificabili.', 'Forza A, Hybrid B e due piscine, con Forza B alternativa.', 1)
app.write_text(s, encoding='utf-8')

css = Path('_site/style.css')
css.write_text(css.read_text(encoding='utf-8') + '\n' +
               Path('overrides/workouts.css').read_text(encoding='utf-8'), encoding='utf-8')

sw = Path('_site/sw.js')
cache = sw.read_text(encoding='utf-8')
assert 'ritmo-fit-static-v2' in cache, "Versione cache imprevista"
sw.write_text(cache.replace('ritmo-fit-static-v2','ritmo-fit-static-v3'), encoding='utf-8')
