# Lean Agent Skills

Два скилла для Codex и Claude Code: предотвращают лишнюю сложность при обсуждении плана
и находят её в готовом коде. Особенно проверяют обращения к сервисам и БД,
самовольное расширение задачи и защиту от гипотетических рисков.

## Установка

### Codex

Нужны актуальный Codex CLI с командами `codex plugin` и Git.
Выполните одну строку в терминале:

```sh
codex plugin marketplace add rubinho-m/lean-agent-skills && codex plugin add lean-agent-skills@rubinho-m
```

Начните новый сеанс Codex. Через `/hooks` проверьте и подтвердите доверие
к `SessionStart` плагина. Codex не запускает новый хук до подтверждения;
команда установки не меняет настройки доверия. После установки плагин также
доступен в настольном приложении при использовании той же локальной конфигурации.

### Claude Code

Нужны актуальный Claude Code с поддержкой плагинов и Git.
Выполните одну строку в терминале:

```sh
claude plugin install lean-agent-skills --marketplace https://github.com/rubinho-m/lean-agent-skills.git
```

Начните новый сеанс Claude Code или выполните `/reload-plugins` в текущем.
Оба скилла и общий `SessionStart`-хук загружаются из того же пакета.
Проверить установку можно командой `claude plugin list`.

Дополнительные Python, Node.js, MCP-серверы, API-ключи и сервисы не требуются.
Сам хук выполняет только встроенную команду `echo`.

## Использование

В Codex для обсуждения идеи или плана:

```text
$lean-agent-skills:lean-grilling Хочу спроектировать ...
```

В Codex для проверки одного или нескольких MR/PR:

```text
$lean-agent-skills:overengineering-review <ссылки на MR> Согласованный план: <источник>
```

В Claude Code используйте `/` вместо `$`:

```text
/lean-agent-skills:lean-grilling Хочу спроектировать ...
/lean-agent-skills:overengineering-review <ссылки на MR> Согласованный план: <источник>
```

`lean-grilling` работает без отдельно установленного `grilling`. Он фильтрует
вопросы до раунда, проверяет простой достаточный вариант, показывает существенную
цену решений и перед итоговым подтверждением проводит один независимый разбор
плана. Если субагенты недоступны, скилл сообщает об этом и выполняет собственную
проверку, не выдавая её за независимую.

Если у вас уже есть внешний `grilling`, хук добавляет агенту инструкцию применять
компаньон вместе с ним. Распознавание смысла вопросов выполняет модель;
хук не является автоматическим доказательством отсутствия оверинжиниринга.

`overengineering-review` проверяет весь diff относительно целевой ветки,
прослеживает запросы через несколько MR и сопоставляет поведение с решениями
пользователя. Скилл выдаёт отчёт; сам не исправляет код и не создаёт задачи.
Нужные проверки безопасности, прав и сохранности данных остаются частью решения.

## Обновление и удаление

Codex:

```sh
codex plugin marketplace upgrade rubinho-m && codex plugin add lean-agent-skills@rubinho-m
```

После обновления начните новый сеанс. Если Codex запросит повторную проверку
изменившегося хука, подтвердите её в `/hooks`.

```sh
codex plugin remove lean-agent-skills@rubinho-m
```

Claude Code:

```sh
claude plugin marketplace update rubinho-m && claude plugin update lean-agent-skills@rubinho-m
```

```sh
claude plugin uninstall lean-agent-skills@rubinho-m
```

Удаление плагина не удаляет другие плагины каталога `rubinho-m`.
Личные копии скиллов и хуков, установленные вручную, пакет не перезаписывает.
Если такие копии уже есть, проверьте дублирование перед использованием плагина.

## Авторство

Основа раундового обсуждения —
[`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
от [Matt Pocock](https://github.com/mattpocock), лицензия MIT.
Автор указан также в `metadata.credits` скилла `lean-grilling`.
Фильтрация лишней сложности, учёт цены решений и ревью изменений — дополнения
этого пакета. Лицензия пакета — [MIT](LICENSE).

## Проверка пакета

Для разработки и запуска тестов нужен Python 3:

```sh
python3 -m unittest discover -s tests -v
```

Перед выпуском обновления синхронно измените `version` в `plugin.json`
и `.claude-plugin/plugin.json`, затем выполните проверки. Манифесты используют
общие `skills/` и `hooks/hooks.json`; повторно объявлять хук в манифесте не нужно.
Для проверки формата Claude Code выполните `claude plugin validate . --strict`.

Описание формата плагинов и установки:
[пакеты Codex](https://developers.openai.com/plugins/build/plugins),
[команды CLI](https://learn.chatgpt.com/docs/cli/reference),
[хуки и доверие Codex](https://learn.chatgpt.com/docs/hooks),
[плагины Claude Code](https://code.claude.com/docs/en/plugins-reference),
[команды плагинов Claude Code](https://code.claude.com/docs/en/plugins/cli-reference).

Этот репозиторий — Git-каталог для установки плагина; публикация в официальный
каталог плагинов OpenAI не выполняется.
