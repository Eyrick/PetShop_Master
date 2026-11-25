## [0.1.0] - 2026-11-25 (Sprint 0 — Resgate e Estabilização)

### Corrigido
- Ambiente isolado com `.venv` e `requirements.txt` (Django 5.2.19, Pillow, `django-crispy-forms`, `crispy-bootstrap4`).
- Compatibilidade de `settings.py` com Django 5.2 (`CRISPY_ALLOWED_TEMPLATE_PACKS`, `DEFAULT_AUTO_FIELD`, remoção de `USE_L10N`).
- Erro `405 Method Not Allowed` na exclusão de pets (migração de links `GET` para formulários `POST` com `{% csrf_token %}` e confirmação).
- Erro `404` na rota raiz `/` e erros `500` em IDs inexistentes (substituição por `get_object_or_404`).
- Indentação YAML e escopo de análise do workflow `.github/workflows/build.yml`.

### Melhorado
- Consulta de pets disponíveis movida da memória Python para o banco (`Pet.objects.filter(available=True)`).
- Templates refatorados para HTML válido, responsividade (`viewport`), acessibilidade (`alt`), estado vazio e feedback visual via `messages`.
- Segurança do repositório reforçada com `.gitignore` adequado e `.env.example`.