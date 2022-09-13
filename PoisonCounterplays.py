from CommonContent import *
from Consumables import *

import sys

curr_module = sys.modules[__name__]

def fix_description(item):
    if isinstance(item.spell, PotionSpell):

        if item.spell.buff == StoneShield:
            item.description = "Gain immunity to [physical], [fire], [ice], and [poison] damage for 30 turns. Cures [poison]."
    
    if isinstance(item.spell, HealPotSpell):
        item.description =  "Drinking this potion restores the drinker to full health.\nIf the user is [poisoned], remove [poison] but does not heal."

    item.spell.description = item.description

def modify_class(cls):

    if cls is Poison:

        def on_advance(self):
            if self.owner.resists[Tags.Poison] >= 100:
                self.owner.remove_buff(self)
            else:
                self.owner.deal_damage(self.damage, Tags.Poison, self)

    if cls is StoneShield:

        def on_init(self):
            self.name = "Stone Shield"
            self.color = Tags.Physical.color
            self.resists[Tags.Physical] = 100
            self.resists[Tags.Fire] = 100
            self.resists[Tags.Ice] = 100
            self.resists[Tags.Poison] = 100

    if cls is Item:

        def set_spell(self, spell):
            spell.range = 0
            spell.on_init()
            if spell.range == 0:
                spell.self_cast = True
            self.spell = spell
            spell.item = self
            spell.name = self.name

            if not spell.description:
                spell.description = self.description
            fix_description(self)

    if cls is HealPotSpell:

        def cast_instant(self, x, y):
            poison = self.caster.get_buff(Poison)
            if poison:
                self.caster.remove_buff(poison)
            else:
                self.caster.deal_damage(-self.caster.max_hp, Tags.Heal, self)

        def can_cast(self, x, y):
            return Spell.can_cast(self, x, y)

    for func_name, func in [(key, value) for key, value in locals().items() if callable(value)]:
        if hasattr(cls, func_name):
            setattr(cls, func_name, func)

for cls in [Poison, StoneShield, Item, HealPotSpell]:
    curr_module.modify_class(cls)