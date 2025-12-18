### Ошибка {n} – ...
Место: [`main.py`](main.py#L44), метод `main`

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
- [Breakpoints](artefacts/error{n}-breakpoints.png)
- [Stacktrace](artefacts/error{n}-stacktrace.png)
- [Locals](artefacts/error{n}-locals.png)
