# notes.md

To dziennik roboczy zespołu: notatki ze spotkań, ustalenia, szybkie decyzje, blokery i “co robimy dalej”. Warto dopisywać tam daty i linki do Issue/PR, żeby łatwo było wrócić do kontekstu. Nie zastępuje dokumentacji architektury, tylko przechowuje bieżące ustalenia.

Struktura projektu: `tree /F /A`

---

## Podstawowe komendy GIT (ściąga)

### Sprawdzenie stanu repo
- `git status` — pokazuje zmienione pliki, staged/unstaged, aktualny branch.
- `git log --oneline --decorate --graph --all` — historia commitów w skrócie.

### Pobieranie informacji o zmianach na GitHubie (bez zmiany plików lokalnie)
- `git fetch origin` — pobiera informacje o nowych commitach na zdalnym repo.
- `git status` — po `fetch` pokaże czy jesteś ahead/behind względem `origin/<branch>`.

### Aktualizacja lokalnego `main`
- `git checkout main`
- `git pull origin main` — pobiera i scala zmiany z `origin/main` do lokalnego `main`.

### Tworzenie brancha do pracy
- `git checkout main && git pull origin main`
- `git checkout -b feature/nazwa-tematu` — tworzy branch i przełącza na niego.

### Dodawanie zmian i commit
- `git add .` — dodaje wszystkie zmiany do stage.
- `git add <plik>` — dodaje konkretny plik.
- `git commit -m "Add: opis zmiany"` — zapisuje commit.

### Push na GitHuba
- `git push -u origin feature/nazwa-tematu` — pierwszy push brancha (ustawia upstream).
- `git push` — kolejne pushe na ten sam branch.

### Pull Request (PR)
- PR tworzymy na GitHubie: `feature/...` → `main`.
- W opisie PR zawsze:
  - co zostało zrobione,
  - jak to przetestować,
  - ewentualne uwagi/ryzyka.

### Aktualizacja swojego brancha o zmiany z `main`
Opcja A (merge):
- `git checkout main && git pull origin main`
- `git checkout feature/nazwa-tematu`
- `git merge main`

Opcja B (rebase) — używać tylko jeśli zespół się na to umawia:
- `git checkout main && git pull origin main`
- `git checkout feature/nazwa-tematu`
- `git rebase main`

### Rozwiązywanie konfliktów
- Po konflikcie edytujesz pliki konfliktowe, usuwasz markery `<<<<<<`, `======`, `>>>>>>`.
- Następnie:
  - `git add .`
  - `git commit` (przy merge) lub `git rebase --continue` (przy rebase)

### Cofanie zmian (ostrożnie)
- `git restore <plik>` — cofa niezacommitowane zmiany w pliku.
- `git restore --staged <plik>` — usuwa plik ze stage.
- `git reset --soft HEAD~1` — cofa commit, zostawia zmiany w stage.
- `git reset --hard HEAD~1` — cofa commit i usuwa zmiany (ryzykowne).

### Usuwanie brancha po merge
- `git checkout main`
- `git pull origin main`
- `git branch -d feature/nazwa-tematu` — usuwa lokalnie (jeśli zmerge’owany).
- `git branch -D feature/nazwa-tematu` — wymusza usunięcie lokalnie (ostrożnie).
- `git push origin --delete feature/nazwa-tematu` — usuwa branch na GitHubie.

### Podejrzenie różnic
- `git diff` — różnice w niezastage’owanych plikach.
- `git diff --staged` — różnice w staged.
- `git diff main..origin/main` — różnice lokalnego main vs zdalnego.

---

## Zasady pracy zespołowej (krótko i konkretnie)

1. Nie robimy commitów bezpośrednio na `main` (tylko PR).
2. Każda funkcjonalność / zmiana = osobny branch (`feature/...`, `fix/...`, `docs/...`).
3. Commity małe i logiczne (żeby dało się je reviewować).
4. Przed rozpoczęciem pracy: `git fetch origin` + `git status` i ewentualnie `git pull`.
5. Przed PR:
   - uaktualnij branch o `main` (merge/rebase),
   - uruchom szybkie testy/odpalenie GUI,
   - dopisz w PR “jak testować”.
6. Nie commitujemy:
   - `__pycache__/`, `.venv/`, plików wynikowych (`data/output/...`), plików IDE.
7. Każdy PR ma opis i instrukcję testowania; brak “wrzucam bo działa u mnie”.

---

## Notatki / ustalenia (uzupełniać na bieżąco)

### [YYYY-MM-DD]
- Ustalenia:
  - ...
- Co robimy dalej:
  - ...
- Blokery:
  - ...
- Linki:
  - PR: ...
  - Issue: ...