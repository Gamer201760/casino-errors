### Ошибка 1 – Нельзя создавать экземпляр интерфейса
Место: `main.py`, метод `main`

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
