# Comandos básicos de Git

## Inicio y estado
- `git init` — inicializa un repositorio Git en la carpeta actual
- `git status` — muestra el estado de los archivos (modificados, staged, sin seguimiento)
- `git log` — muestra el historial de commits
- `git diff` — muestra diferencias entre cambios no staged y el último commit
- `git clone <url>` — descarga/copia un repositorio remoto completo

## Remotos
- `git remote add origin <url>` — conecta tu repo local a uno remoto (alias "origin")
- `git remote -v` — muestra las URLs de fetch y push del remoto
- `git remote remove origin` — elimina la conexión con el remoto

## Ramas
- `git branch -M main` — renombra la rama actual a "main" (forzado)
- `git checkout -b nombre-rama` — crea y cambia a una nueva rama

## Subir/bajar cambios
- `git push origin nombre-rama` — sube commits locales a la rama del remoto
- `git pull origin nombre-rama` — descarga y combina cambios del remoto (fetch + merge)

## Archivos
- `git add archivo` — agrega cambios al staging
- `git commit -m "mensaje"` — guarda los cambios
- `git rm archivo` — elimina archivo del repo y del disco
- `git rm --cached archivo` — elimina solo del repo (queda en disco)

## Pull Request (flujo en GitHub)
1. `git checkout -b nombre-rama`
2. Hacer cambios, `git add`, `git commit`
3. `git push origin nombre-rama`
4. En GitHub: clic en "Compare & pull request" → completar descripción → "Create pull request"
5. El merge a la rama principal lo hace alguien manualmente con "Merge pull request"

## Notas clave
- Push a repos públicos requiere permisos de escritura; pull/clone no.
- No hay restricción de Git para hacer push entre ramas principales o secundarias; las protecciones se configuran en GitHub ("branch protection rules").
</file_text>