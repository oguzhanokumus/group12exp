from otree.api import *
from numpy import random
c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'FehrSchmidt'
    players_per_group = 2
    num_rounds = 1
    amount = c(100)
    ENDOWMENT = c(100)
    participation_fee = c(50)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    split_amount = models.CurrencyField(min=0, max=Constants.amount,
                                        label='How much do you want to split to the other player?')

    receiver_response = models.IntegerField(choices=[[0, "Yes"],[1, "No"]],
                                            widget=widgets.RadioSelectHorizontal,
        label='Do you accept the proposed split amount?'
                                            )
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=Constants.ENDOWMENT,
        label="I will keep",
    )


class Player(BasePlayer):

    Gender = models.StringField(label='Please enter your gender')
    Age = models.StringField(label='Please enter your age')

    fair = models.IntegerField(initial=0)
    totalfair_proposer = models.IntegerField(initial=0)
    totalfair_receiver = models.IntegerField(initial=0)

#FUNCTIONS

#def creating_session(subsession):
#    for player in subsession.get_players():
#        player.treatment = next(treated)
#        player.participant.quiztype = next(quiz)


def set_payoffs(group: Group):

    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    if group.receiver_response == 0:
        p2.payoff = group.split_amount
        p1.payoff = Constants.amount - group.split_amount

    else:
        p1.payoff = 0
        p2.payoff = 0

def set_payoffs2(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = Constants.ENDOWMENT - group.kept


def feedback_proposer (group: Group):

    p1 = group.get_player_by_id(1)
    p1.fair = 0

    if group.split_amount > 20:     #We will enter the amount here from the baseline survey
        p1.fair = 1
    else:
        p1.fair = 0

    #p1.totalfair_proposer = p1.in_round(1).fair + p1.in_round(2).fair + p1.in_round(3).fair + p1.in_round(4).fair + p1.in_round(5).fair

# PAGES

class a_Introduction(Page):
    pass

class ba_Player1(Page):
    form_model = 'group'
    form_fields = ['split_amount']

    def is_displayed(player):
        return player.id_in_group == 1

class bb_Player2(Page) :
    form_model = 'group'
    form_fields = ['receiver_response']

    def is_displayed(player) :
        return player.id_in_group == 2


class WaitForP1(WaitPage) :
    def is_displayed(player) :
        return player.id_in_group >> 1


class ResultsWaitPage(WaitPage) :
    after_all_players_arrive = 'set_payoffs'

class ResultsWaitPage2(WaitPage) :
    after_all_players_arrive = 'feedback_proposer'


class ca_Results(Page) :
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)

        return dict(
                    payoff1 = p1.payoff,
                    payoff2= p2.payoff,
                    totalfair_p = p1.totalfair_proposer,
                    totalfair_r = p2.totalfair_receiver
                    )

class cb_Feedback_Proposer(Page) :
    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)

        return dict(
            totalfair_p=p1.totalfair_proposer,
            totalfair_r=p2.totalfair_receiver
        )

class d_Introduction(Page):
    pass


class e_Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class ResultsWaitPage3(WaitPage):
    after_all_players_arrive = 'set_payoffs2'


class f_Results2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=Constants.ENDOWMENT - group.kept)

class g_Survey(Page):
    form_model = 'player'
    form_fields = ['Gender', 'Age']


page_sequence = [a_Introduction, ba_Player1, WaitForP1, bb_Player2, ResultsWaitPage, ResultsWaitPage2, ca_Results, cb_Feedback_Proposer,
                 d_Introduction, e_Offer, ResultsWaitPage3, f_Results2, g_Survey]