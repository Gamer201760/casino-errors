### Ошибка 3 – Бесконечное оглушение
Место: [`main.py`](main.py#L44), метод `main`

Симптом:
Игроки перестают делать ставки \
Если на игрока наложает эффект оглушение он будет бесконечным и игрок не сможет делать ставки

Как воспроизвести:
Запустить симуляцию `make run` с конфигом:
```yaml
seed: 1
generate_player_count: 1
```

Отладка: 
- Установлен breakpoint на 44 строке
- В отладчике видна ошибка и стэк вызывов

Причина:
`duration` не уменьшается при тике симуляции
```python
@dataclass
class StunEffect:
    source: Entity
    target: Entity
    duration: int

    def on_tick(self) -> None:
        pass
```

Исправление:
Уменьшать `duration` на 1 при тике 
```python
@dataclass
class StunEffect:
    source: Entity
    target: Entity
    duration: int

    def on_tick(self) -> None:
        # Просто тикает таймер
        # Casino проверяет наличие StunEffect, чтобы запретить действия
        self.duration -= 1
```

Проверка:
Симуляция запускается 

Доказательства:
- [Breakpoints](artefacts/error3-breakpoints.png)
- [Stacktrace](artefacts/error3-stacktrace.png)
- [Locals](artefacts/error3-locals.png)
