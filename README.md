### Ошибка 5 – Изменение коллекции во время итерации
Место: [`engine.py`](domain/engine.py#L19), метод `tick`

Симптом:
Приложение падает с `RuntimeError: dictionary changed size during iteration` при удаление истёкших эффектов

Как воспроизвести:
Запустить симуляцию `make run`, с конфигом:
```yaml
seed: 1
event_weights:
  bet: 0             # Ставка
  goose_attack: 100  # Атака гуся
  flock_create: 0    # Создание стаи
  flock_disband: 0   # Распад стаи
  panic: 0           # Паника
```
Этот конфиг гарантирует одинаковое поведение: каждый шаг = событие атаки 

Отладка: 
- Установлен breakpoint на 20 строке
- В стэктрейсе видно: `RuntimeError: dictionary changed size during iteration`

Причина:
При итерации по словарю без копии ключей, удаление элемента внутри цикла изменяет размер словаря во время обхода
```python
for key, bucket in self._effects.items():
...
```

Исправление:
Создать копию ключей с помощью `list` перед итерацией
```python
for key, bucket in list(self._effects.items()):
...
```

Проверка:
Симуляция проходит без `RuntimeError`, истёкшие эффекты корректно удаляются из словаря

Доказательства:
- [Breakpoints](artefacts/error5-breakpoints.png)
- [Stacktrace](artefacts/error5-stacktrace.png)
- [Locals](artefacts/error5-locals.png)
