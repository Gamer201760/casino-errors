### Ошибка 2 – Обработка события panic без проверки игрока
Место: [`usecase/casino.py`](usecase/casino.py#L242), метод `_event_panic`

Симптом:
Приложение падает с ошибкой `AttributeError: 'NoneType' object has no attribute 'lucky'`, если в казино не осталось игроков с положительным балансом, при событии паника

Как воспроизвести:
Запустить симуляцию `make run`\
В конфиге выставить
```yaml
seed: 1
generate_player_count: 1
```

Отладка: 
- Установлен breakpoint на 246 строке
- В locals видно, что `player = None`

Причина:
При получение игрока забыли проверить на None
`_pick_player() -> Player | None`
```python
player = self._pick_player(require_balance=True, require_not_stunned=False)

p = self._panic_probability(player)
...
```

Исправление:
Проверить на None
```python
player = self._pick_player(require_balance=True, require_not_stunned=False)

if player is None:
	logger.info('паника пропуск: нет игрока')
	return []

p = self._panic_probability(player)
...
```

Проверка:
Теперь симуляция не падает, если нет игрока с положительным балансом, а `casino.log` появиться запись `паника пропуск: нет игрока`

Доказательства:
- [Breakpoints](artefacts/error2-breakpoints.png)
- [Stacktrace](artefacts/error2-stacktrace.png)
- [Locals](artefacts/error2-locals.png)
