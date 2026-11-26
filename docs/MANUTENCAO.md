# Manutenção solicitada

## Executar (PowerShell, ambiente local)
Use o ambiente virtual e o .env já existentes. Se necessário, copie .env.example para .env e configure SECRET_KEY. Antes de migrar, pare o servidor e faça uma cópia de db.sqlite3, se existir. Não use seed_petshop --reset em um banco existente.

```
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver
```

Para um banco novo, opcionalmente `python manage.py seed_petshop`.
O ZIP original não contém banco SQLite. A migration 0007 é aditiva: cria Category, Breed, AdoptionRequest e ChatMessage e adiciona breed a Pet. Registros antigos conhecidos do seed são classificados; outros ficam sem classificação até edição. Categoria é derivada da raça, evitando pares inconsistentes no banco. O catálogo inicial é limitado e pode ser ampliado no admin.

## Uso
- Detalhe do pet > Fila de adoção: nome e e-mail de contato, sem conta. A posição é por data e ID. No admin existente, Adoption requests: selecione a primeira solicitação pendente e execute a ação de falha ou conclusão. Falha libera o próximo; conclusão torna o pet indisponível e encerra os demais pedidos. Não reabra um pet já adotado para uma nova fila.
- Cadastro/edição: categoria e raça obrigatórias; opções filtradas no navegador e validadas no servidor. O admin também valida o par. Pets legados sem classificação continuam visíveis.
- Detalhe > Chat: envie mensagem e use Atualizar mensagens para ler respostas. No admin existente, Chat messages: abra uma mensagem e preencha Responder ao cliente, depois salve. A sessão separa os visitantes; apagar cookies perde o acesso ao histórico. Não é chat em tempo real. Não há novo login ou cadastro. A equipe usa a autenticação administrativa que já existia. Se não houver administrador no banco local, o comando Django createsuperuser é a configuração administrativa padrão, não uma conta de cliente.

## Limitações
O CRUD público original foi mantido, inclusive edição/exclusão sem autenticação; não é indicado para publicação na internet sem revisão de segurança. Excluir pet exclui fila e mensagens associadas. Não foram alteradas dependências nem configurações de segurança. A execução Django não pôde ser testada no ambiente de entrega: dependências ausentes e instalação sem rede. Execute os comandos acima e o SonarQube localmente antes de integrar.
