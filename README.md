### Ошибка 3 – Бесконечное оглушение
Место: [`effect.py`](domain/effect.py#L29), метод `on_tick`

Симптом:
Игроки перестают делать ставки, как только на игрока накладывается эффект оглушения, он становится бесконечным, поэтому `Casino` всегда считает игрока оглушённым и больше не выбирает его для события `bet`

Как воспроизвести:
Запустить симуляцию `make run` с конфигом:
```yaml
seed: 1
generate_player_count: 10
```
При достаточно длинной симуляции в логах перестают появляться записи вида `ставка игрок ...`, хотя симуляция продолжает идти

Отладка: 
- Установлен breakpoint на 50 строке в [`main.py`](main.py#L50) после симуляции
- В `locals` в `Casino._effects` если посмотреть на эффекты любого игрока, то можно увидеть неистёкшие станы
- Видно, что `duration` у `StunEffect` остаётся положительным и не уменьшается между шагами, хотя `EffectEngine.tick()` вызывается на каждом шаге

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
После правки при остановке на breakpoint в `main.py` видно, что `duration` у `StunEffect` уменьшается на каждом шаге и эффекты исчезают после достижения нуля\
В логах после некоторого времени снова появляются события `bet` от игроков, которые ранее были оглушены

Доказательства:
- [Breakpoints](artefacts/error3-breakpoints.png)
- [Locals](artefacts/error3-locals.png)
