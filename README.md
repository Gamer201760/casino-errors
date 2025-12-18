### Ошибка 1 – Нельзя создавать экземпляр интерфейса
Место: [`main.py`](error-1/main.py), метод `main`

Симптом:
Приложение падает при создании `players = PlayerCollection()`, с ошибкой `TypeError: Protocols cannot be instantiated`

Как воспроизвести:
Запустить симуляцию `make run`

Отладка: 
- Установлен breakpoint на 44 строке
- В отладчике видна ошибка и стэк вызывов

Причина:
Интерпретатор не позволяет создавать экземпляры классов, помеченных как `Protocol`. Протоколы описывают контракт и не предназначены для непосредственной инициализации
```python
players = PlayerCollection()
...
casino = Casino(players, goose, balance, stat=stats, config=cfg)
```

Исправление:
Использовать конкретную реализацию коллекции 
```python
players = InMemoryPlayerCollection()
...
casino = Casino(players, goose, balance, stat=stats, config=cfg)
```

Проверка:
Симуляция запускается 

Доказательства:
- [Breakpoints](artefacts/error1-breakpoints.png)
- [Stacktrace](artefacts/error1-stacktrace.png)
- [Locals](artefacts/error1-locals.png)

### Ошибка 2 – Обработка события panic без проверки игрока
Место: [`usecase/casino.py`](casino-errors/blob/error-2/usecase/casino.py), метод `_event_panic`

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
