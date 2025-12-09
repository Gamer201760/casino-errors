from dataclasses import dataclass
from typing import Protocol

from domain.effect import Effect, OnceStealBalance, StunEffect
from domain.entity import Entity
from domain.player import Player


class Goose(Entity, Protocol):
    name: str
    lucky: int

    def act_player(self, player: Player) -> list[Effect]: ...
    def act_self(self) -> list[Effect]: ...

    def __add__(self, other: 'Goose') -> 'Goose': ...


@dataclass
class WarGoose(Goose):
    name: str
    strength: int
    lucky: int = 0
    balance: int = 0

    def change_balance(self, delta: int) -> None:
        self.balance += delta

    def act_player(self, player: Player) -> list[Effect]:
        """
        Атакует игрока с некоторым шансем,
        на него влияет удача гуся - удача игрока
        Может атаковать сам себя, тогда его баланс переходит игроку
        """
        steal = min(self.strength, player.balance)

        return [
            # Игрок теряет деньги
            OnceStealBalance(source=self, target=player, delta=-steal),
            # Гусь получает доход
            OnceStealBalance(source=self, target=self, delta=steal),
        ]

    def act_self(self) -> list[Effect]:
        lost = min(self.strength, self.balance)
        if lost <= 0:
            return []
        return [
            OnceStealBalance(source=self, target=self, delta=-lost),
        ]

    def __add__(self, other: Goose) -> Goose:
        if isinstance(other, FlockGoose):
            return other + self
        return FlockGoose(self.name, [self, other])


@dataclass
class HonkGoose(Goose):
    name: str
    honk_volume: int
    lucky: int = 0
    balance: int = 0

    def _stun_turns(self) -> int:
        return max(1, self.honk_volume // 10)

    def act_player(self, player: Player) -> list[Effect]:
        """
        Есть шанс оглушение игрока на (громкость / 10) шагов,
        на него влияет удача гуся - удача игрока,
        иначе оглушает самого себя
        """
        return [
            StunEffect(source=self, target=player, duration=self._stun_turns()),
        ]

    def act_self(self) -> list[Effect]:
        return [
            StunEffect(source=self, target=self, duration=self._stun_turns()),
        ]

    def __add__(self, other: Goose) -> Goose:
        if isinstance(other, FlockGoose):
            return other + self
        return FlockGoose(self.name, [self, other])


class FlockGoose(Goose):
    def __init__(self, name: str, geese: list[Goose]) -> None:
        self.name = name

        self.geese: list[Goose] = []
        self.war: list[WarGoose] = []
        self.honk: list[HonkGoose] = []

        self._count: int = 0
        self._honk_count: int = 0

        self._lucky_sum: int = 0
        self._strength: int = 0
        self._honk_sum: int = 0

        self.lucky: int = 0
        self._honk_volume: int = 0

        for g in geese:
            self._add_goose_incremental(g)

    @property
    def strength(self) -> int:
        return self._strength

    @property
    def honk_volume(self) -> int:
        return self._honk_volume

    @property
    def count(self) -> int:
        return self._count

    def _add_goose_incremental(self, g: Goose) -> None:
        self.geese.append(g)
        self._count += 1
        self._lucky_sum += g.lucky

        if isinstance(g, WarGoose):
            self.war.append(g)
            self._strength += g.strength

        if isinstance(g, HonkGoose):
            self.honk.append(g)
            self._honk_count += 1
            self._honk_sum += g.honk_volume

        self._update_aggregates()

    def _extend_from_flock(self, other: 'FlockGoose') -> None:
        self.geese.extend(other.geese)
        self.war.extend(other.war)
        self.honk.extend(other.honk)

        self._count += other._count
        self._honk_count += other._honk_count

        self._lucky_sum += other._lucky_sum
        self._strength += other._strength
        self._honk_sum += other._honk_sum

        self._update_aggregates()

    def _update_aggregates(self) -> None:
        if self._count > 0:
            self.lucky = int(self._lucky_sum / self._count)
        else:
            self.lucky = 0

        if self._honk_count > 0:
            self._honk_volume = int(self._honk_sum / self._honk_count)
        else:
            self._honk_volume = 0

    def act_player(self, player: Player) -> list[Effect]:
        effects: list[Effect] = []

        # 1. стан игрока на среднюю громкость всех HonkGoose
        if self._honk_volume > 0:
            stun_turns = max(1, self._honk_volume // 10)
            effects.append(
                StunEffect(source=self, target=player, duration=stun_turns),
            )

        # 2. украсть min(_strength, player.balance)
        steal = min(self._strength, player.balance)
        if steal > 0:
            effects.append(
                OnceStealBalance(source=self, target=player, delta=-steal),
            )

            share, rem = divmod(steal, len(self.war)) if self.war else (0, 0)
            for i, w in enumerate(self.war):
                delta = share + (1 if i < rem else 0)
                effects.append(
                    OnceStealBalance(source=self, target=w, delta=delta),
                )

        return effects

    def act_self(self) -> list[Effect]:
        effects: list[Effect] = []

        # 1. стан каждого гуся на среднюю громкость HonkGoose
        if self._honk_volume > 0:
            stun_turns = max(1, self._honk_volume // 10)
            for g in self.geese:
                effects.append(
                    StunEffect(source=self, target=g, duration=stun_turns),
                )

        # 2. у каждого WarGoose забираем min(balance, _strength)
        if self._strength > 0:
            for w in self.war:
                lost = min(w.balance, self._strength)
                if lost > 0:
                    effects.append(
                        OnceStealBalance(source=self, target=w, delta=-lost),
                    )

        return effects

    def __add__(self, other: Goose) -> Goose:
        if isinstance(other, FlockGoose):
            self._extend_from_flock(other)
            return self

        self._add_goose_incremental(other)
        return self
