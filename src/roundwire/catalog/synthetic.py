"""Synthetic but realistic match dump builder for demos and tests."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.damage import DamageEvent
from roundwire.models.edition import GameEdition
from roundwire.models.inventory import InventorySnapshot
from roundwire.models.kill import Kill
from roundwire.models.match import Match
from roundwire.models.player import Player
from roundwire.models.round import Round
from roundwire.models.team import TeamSide
from roundwire.models.utility_event import UtilityEvent, UtilityKind
from roundwire.models.weapon import Weapon
from roundwire.types import MatchId, Milliseconds, PlayerId, RoundNumber


@dataclass
class SyntheticConfig:
    match_id: str
    map_name: str
    edition: GameEdition
    team_ct: str = "Aurora"
    team_t: str = "Nimbus"
    target_ct_rounds: int = 13
    total_rounds: int = 22
    ct_rifle: str = "m4a1"
    t_rifle: str = "ak47"
    ct_pistol: str = "usp_silencer"
    t_pistol: str = "glock"
    seed_offset: int = 0


CT_NICKS = ("lux", "pine", "arq", "milo", "zen")
T_NICKS = ("kaze", "riot", "nolo", "byte", "haze")


def _pids(prefix: str) -> list[PlayerId]:
    return [PlayerId(f"{prefix}{i}") for i in range(1, 6)]


def _players(cfg: SyntheticConfig) -> list[Player]:
    players: list[Player] = []
    for i, pid in enumerate(_pids(f"{cfg.match_id}_ct"), start=1):
        players.append(Player(player_id=pid, name=CT_NICKS[i - 1], team=TeamSide.CT))
    for i, pid in enumerate(_pids(f"{cfg.match_id}_t"), start=1):
        players.append(Player(player_id=pid, name=T_NICKS[i - 1], team=TeamSide.T))
    return players


def _inventory(
    pid: PlayerId,
    *,
    cash: int,
    eq: int,
    primary: str | None,
    secondary: str,
    armor: bool,
    grenades: list[str] | None = None,
) -> InventorySnapshot:
    return InventorySnapshot(
        player_id=pid,
        cash=cash,
        equipment_value=eq,
        primary=Weapon(primary) if primary else None,
        secondary=Weapon(secondary),
        armor=armor,
        helmet=armor,
        defuse_kit=False,
        grenades=list(grenades or []),
    )


def _script_round(
    cfg: SyntheticConfig,
    number: int,
    winner: TeamSide,
    ct_ids: list[PlayerId],
    t_ids: list[PlayerId],
) -> Round:
    half = 15 if cfg.edition is GameEdition.CSGO else 12
    pistol = number in {1, half + 1}
    if pistol:
        eq_ct, eq_t, prim_ct, prim_t = 850, 850, None, None
    elif number % 5 == 0:
        eq_ct, eq_t, prim_ct, prim_t = 1900, 4500, None, cfg.t_rifle
    elif number % 4 == 0:
        eq_ct, eq_t, prim_ct, prim_t = 4700, 2100, cfg.ct_rifle, None
    else:
        eq_ct, eq_t, prim_ct, prim_t = 5000, 4800, cfg.ct_rifle, cfg.t_rifle

    invs = [
        _inventory(
            pid,
            cash=900 if pistol else 1600,
            eq=eq_ct,
            primary=prim_ct,
            secondary=cfg.ct_pistol,
            armor=not pistol,
            grenades=["flashbang", "smokegrenade"] if not pistol else [],
        )
        for pid in ct_ids
    ] + [
        _inventory(
            pid,
            cash=900 if pistol else 1400,
            eq=eq_t,
            primary=prim_t,
            secondary=cfg.t_pistol,
            armor=not pistol,
            grenades=["flashbang", "molotov"] if not pistol else [],
        )
        for pid in t_ids
    ]

    w_ct = prim_ct or cfg.ct_pistol
    w_t = prim_t or cfg.t_pistol
    base = 4000 + cfg.seed_offset + number * 17

    if winner is TeamSide.CT:
        kills = [
            Kill(ct_ids[0], t_ids[0], Weapon(w_ct), Milliseconds(base), headshot=True),
            Kill(t_ids[1], ct_ids[1], Weapon(w_t), Milliseconds(base + 900)),
            Kill(ct_ids[2], t_ids[1], Weapon(w_ct), Milliseconds(base + 1500)),
            Kill(ct_ids[0], t_ids[2], Weapon(w_ct), Milliseconds(base + 2800), headshot=True),
            Kill(ct_ids[3], t_ids[3], Weapon(w_ct), Milliseconds(base + 4200)),
            Kill(ct_ids[4], t_ids[4], Weapon(w_ct), Milliseconds(base + 5600)),
        ]
        survivors = list(ct_ids)
        damage = [
            DamageEvent(ct_ids[i % 5], t_ids[i % 5], Weapon(w_ct), 55 + i * 7, Milliseconds(base + i * 80))
            for i in range(8)
        ]
    else:
        kills = [
            Kill(t_ids[0], ct_ids[0], Weapon(w_t), Milliseconds(base), headshot=True),
            Kill(ct_ids[1], t_ids[0], Weapon(w_ct), Milliseconds(base + 1100)),
            Kill(t_ids[2], ct_ids[1], Weapon(w_t), Milliseconds(base + 2000)),
            Kill(t_ids[2], ct_ids[2], Weapon(w_t), Milliseconds(base + 3300), headshot=True),
            Kill(t_ids[3], ct_ids[3], Weapon(w_t), Milliseconds(base + 4700)),
            Kill(t_ids[4], ct_ids[4], Weapon(w_t), Milliseconds(base + 6100)),
        ]
        survivors = list(t_ids)
        damage = [
            DamageEvent(t_ids[i % 5], ct_ids[i % 5], Weapon(w_t), 60 + i * 6, Milliseconds(base + i * 90))
            for i in range(8)
        ]

    utility = [
        UtilityEvent(ct_ids[1], UtilityKind.FLASH, Milliseconds(base - 1000), enemies_flashed=2),
        UtilityEvent(t_ids[1], UtilityKind.SMOKE, Milliseconds(base - 800)),
        UtilityEvent(ct_ids[2], UtilityKind.HE, Milliseconds(base - 500), damage_dealt=35),
        UtilityEvent(
            t_ids[3],
            UtilityKind.MOLOTOV if cfg.edition is GameEdition.CS2 else UtilityKind.INCENDIARY,
            Milliseconds(base - 300),
            damage_dealt=22,
        ),
    ]

    return Round(
        number=RoundNumber(number),
        winner=winner,
        win_reason="elimination",
        bomb_planted=winner is TeamSide.T and number % 3 == 0,
        inventories=invs,
        kills=kills,
        damage=damage,
        utility=utility,
        survivors=survivors,
        duration_ms=85000 + number * 120,
    )


def build_synthetic_match(cfg: SyntheticConfig) -> Match:
    if cfg.total_rounds < 1:
        raise ValueError("total_rounds must be positive")
    if cfg.target_ct_rounds > cfg.total_rounds:
        raise ValueError("target_ct_rounds exceeds total_rounds")
    ct_ids = _pids(f"{cfg.match_id}_ct")
    t_ids = _pids(f"{cfg.match_id}_t")
    rounds: list[Round] = []
    ct_wins = 0
    t_wins = 0
    for n in range(1, cfg.total_rounds + 1):
        remaining = cfg.total_rounds - n + 1
        need_ct = cfg.target_ct_rounds - ct_wins
        if need_ct >= remaining:
            winner = TeamSide.CT
        elif ct_wins >= cfg.target_ct_rounds:
            winner = TeamSide.T
        elif ct_wins <= t_wins:
            winner = TeamSide.CT
        else:
            winner = TeamSide.T
        if winner is TeamSide.CT:
            ct_wins += 1
        else:
            t_wins += 1
        rounds.append(_script_round(cfg, n, winner, ct_ids, t_ids))
    return Match(
        match_id=MatchId(cfg.match_id),
        map_name=cfg.map_name,
        edition=cfg.edition,
        team_ct_name=cfg.team_ct,
        team_t_name=cfg.team_t,
        players=_players(cfg),
        rounds=rounds,
        event_name="Synthetic Series",
    )


def default_cs2_match(match_id: str = "syn_cs2") -> Match:
    return build_synthetic_match(
        SyntheticConfig(
            match_id=match_id,
            map_name="de_mirage",
            edition=GameEdition.CS2,
            target_ct_rounds=13,
            total_rounds=22,
        )
    )


def default_csgo_match(match_id: str = "syn_csgo") -> Match:
    return build_synthetic_match(
        SyntheticConfig(
            match_id=match_id,
            map_name="de_dust2",
            edition=GameEdition.CSGO,
            target_ct_rounds=16,
            total_rounds=26,
            ct_rifle="weapon_m4a1",
            t_rifle="weapon_ak47",
            ct_pistol="weapon_usp_silencer",
            t_pistol="weapon_glock",
        )
    )
