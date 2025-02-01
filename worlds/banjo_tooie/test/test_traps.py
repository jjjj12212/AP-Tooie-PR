from worlds.banjo_tooie.Items import BanjoTooieItem, all_item_table
from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from collections import defaultdict

class TrapTestBase(BanjoTooieTestBase):
    class Pool:
        trap_distribution = defaultdict(int)
        filler_distribution = defaultdict(int)


    def pool(self) -> Pool:
        pool = self.Pool()
        for item in self.world.multiworld.itempool:
            if item.trap:
                pool.trap_distribution[item.name] += 1
            if item.filler:
                pool.filler_distribution[item.name] += 1

        return pool

class TestTrapsDisabled(TrapTestBase):
    options = {
        'randomize_bk_moves': 2,
        'traps': 'false',
        'nestsanity': 'false',
        'extra_trebleclefs_count': 0,
        'bassclef_amount': 0,
        # to add 10 filler items
        'cheato_rewards': 'false',
        'honeyb_rewards': 'false',
    }
    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 10
        assert sum(pool.trap_distribution.values()) == 0

class TestTrapsEnabled(TrapTestBase):
    options = {
        'randomize_bk_moves': 2,
        'traps': 'true',
        'nestsanity': 'false',
        'extra_trebleclefs_count': 0,
        'bassclef_amount': 0,
        # to add 10 filler items
        'cheato_rewards': 'false',
        'honeyb_rewards': 'false',
    }
    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0
        assert sum(pool.trap_distribution.values()) == 10


class TestTrapsEnabledExtraClefs(TrapTestBase):
    options = {
        'randomize_bk_moves': 2,
        'traps': 'true',
        'randomize_notes': 'true',
        'extra_trebleclefs_count': 21,
        'bass_clef_amount': 30
    }
    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0
        assert sum(pool.trap_distribution.values()) == 30 + 21*3


class TestTrapsEnabledNestsanity(TrapTestBase):
    options = {
        'randomize_bk_moves': 2,
        'traps': 'true',
        'nestsanity': 'true',
        'traps_nests_ratio': 50,
    }
    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0
        assert sum(pool.trap_distribution.values()) == int(0.5 * (315 + 135)) + 23
        assert pool.filler_distribution[itemName.ENEST] == 158
        assert pool.filler_distribution[itemName.FNEST] == 67


class TestTrapsEnabledRespectDistribution(TrapTestBase):
    options = {
        'randomize_bk_moves': 2,
        'traps': 'true',
        'nestsanity': 'true',
        'traps_nests_ratio': 100,

        'randomize_notes': 'true',
        'extra_trebleclefs_count': 21,
        'bassclef_amount': 30,

        'golden_eggs_weight': 10,
        'trip_trap_weight': 25,
        'slip_trap_weight': 40,
        'transform_trap_weight': 55,
        'squish_trap_weight': 70,
        'tip_trap_weight': 85,
    }
    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0

        expected_traps = 315 + 135 + 23 + 30 + 3*21 ##566
        assert sum(pool.trap_distribution.values()) == expected_traps
        assert pool.trap_distribution[itemName.GEGGS] < pool.trap_distribution[itemName.TTRAP]
        assert pool.trap_distribution[itemName.TTRAP] < pool.trap_distribution[itemName.STRAP]
        assert pool.trap_distribution[itemName.STRAP] < pool.trap_distribution[itemName.TRTRAP]
        assert pool.trap_distribution[itemName.TRTRAP] < pool.trap_distribution[itemName.SQTRAP]
        assert pool.trap_distribution[itemName.SQTRAP] < pool.trap_distribution[itemName.TITRAP]

# class TestTrapsEnabledDisableTraps(TrapTestBase):
#     options = {
#         'traps': 'true',
#         'nestsanity': 'true',
#         'extra_trebleclefs_count': 21,
#         'bassclef_amount': 30,
#         'traps_nests_ratio': 100,

#         'golden_eggs_weight': 0,
#         'trip_trap_weight': 50,
#         'slip_trap_weight': 50,
#         'transform_trap_weight': 50,
#         'squish_trap_weight': 0,
#     }
#     weights = []
#     def test_item_pool(self) -> None:
#         super()._item_pool()



# golden_eggs_weight: 40
#   trip_trap_weight: 40        # 0 - 100; weight of trip traps in the trap pool. Requires traps.
#   slip_trap_weight: 40        # 0 - 100; weight of slip traps in the trap pool. Requires traps.
#   transform_trap_weight: 40   # 0 - 100; weight of transform traps in the trap pool. Requires traps.
#   squish_trap_weight: 20      # 0 - 100; weight of squish traps in the trap pool. Requires traps.
