# Casino Errors

Репозиторий содержит набор ошибок в проекте [`Casino Simulation`](https://github.com/gamer201760/casino.git)\
Каждая ошибка оформлена в отдельной ветке `error-{n}` и сопровождается собственным `README.md` с описанием

## Навигация
- [`error-1`](https://github.com/gamer201760/casino-errors/tree/error-1) – Нельзя создавать экземпляр интерфейса
- [`error-2`](https://github.com/gamer201760/casino-errors/tree/error-2) – Обработка события panic без проверки игрока
- [`error-3`](https://github.com/gamer201760/casino-errors/tree/error-3) – Бесконечное оглушение
- [`error-4`](https://github.com/gamer201760/casino-errors/tree/error-4) – ...
- [`error-5`](https://github.com/gamer201760/casino-errors/tree/error-5) – ...

## Как запускать примеры
1. Клонировать репозиторий
```bash
git clone https://github.com/gamer201760/casino-errors.git
cd casino-errors
```

2. Переключиться на ветку с интересующей ошибкой, например:
```bash
git checkout error-1
```

3. Установить зависимости
```bash
make install
```

4. Запустить симуляцию
```bash
make run
```

5. Следовать шагам из `README.md` соответствующей ветки:
- при необходимости изменить `config.yaml` (seed, количество игроков и т.п.)

Логи симуляции пишутся в `casino.log`, их можно использовать как дополнительный источник информации при отладке
