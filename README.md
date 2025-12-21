### Ошибка 4 – Бесконечные деньги
Место: [`casino.py`](usecase/casino.py#L141), метод `_event_bet`

Симптом:
При ставке деньги не списываются

Как воспроизвести:
Запустить симуляцию `make run` с конфигом:
```yaml
seed: 1
bet_win_base: 0
event_weights:
  bet: 100           # Ставка
  goose_attack: 0    # Атака гуся
  flock_create: 0    # Создание стаи
  flock_disband: 0   # Распад стаи
  panic: 0           # Паника
```
Этот конфиг гарантирует одинаковое поведение: 
каждый шаг = событие bet, каждая ставка = проигрыш

Отладка: 
- Установлен breakpoint на 141 строке
- В отладчике до списания денег видно, что у player баланс 16, а ставка 11
- После списания денег, у player стало 27, а должно 5

Причина:
Когда у игрока резервируют деньги для ставки их начисляют, а не снимают
```python
...
player.change_balance(chip.value)
self.balance += chip.value
...
```

Исправление:
Поменять знак
```python
...
player.change_balance(-chip.value)
self.balance += chip.value
...
```

Проверка:
При постановке ставки баланс игрока уменьшается на величину ставки.\
В итоговой статистике большинство игроков имеют отрицательную дельу баланса, а банк казино положительную

Доказательства:
- [Breakpoints](artefacts/error{n}-breakpoints.png)
- [Stacktrace](artefacts/error{n}-stacktrace.png)
- [Locals](artefacts/error{n}-locals.png)
