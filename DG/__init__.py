from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'DG'
    players_per_group = 2
    num_rounds = 1
    ENDOWMENT = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=Constants.ENDOWMENT,
        label="I will keep",
    )


class Player(BasePlayer):
    Gender = models.StringField(label='Please enter your gender')
    Age = models.StringField(label='Please enter your age')


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = Constants.ENDOWMENT - group.kept


# PAGES
class Introduction(Page):
    pass


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=Constants.ENDOWMENT - group.kept)

class Survey(Page):
    form_model = 'player'
    form_fields = ['Gender', 'Age']

page_sequence = [Introduction, Offer, ResultsWaitPage, Results, Survey]