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

class Player(BasePlayer):

    #Name = models.StringField(label='Please enter your Name')
    Gender = models.StringField(label='Please enter your gender')
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

def feedback_proposer (group: Group):

    p1 = group.get_player_by_id(1)
    p1.fair = 0

    if group.split_amount > 20:     #We will enter the amount here from the baseline survey
        p1.fair = 1
    else:
        p1.fair = 0

    #p1.totalfair_proposer = p1.in_round(1).fair + p1.in_round(2).fair + p1.in_round(3).fair + p1.in_round(4).fair + p1.in_round(5).fair

def feedback_receiver(group: Group):

    p2 = group.get_player_by_id(1)
    p2.fair = 0
    if group.split_amount > 20 & group.receiver_response == 0:
        p2.fair = p2.fair + 10
    else:
        p2.fair = p2.fair + 0

    #p2.totalfair_receiver = p2.in_round(1).fair + p2.in_round(2).fair + p2.in_round(3).fair + p2.in_round(
        #4).fair + p2.in_round(5).fair

# PAGES

class Proposer(Page):
    form_model = 'group'
    form_fields = ['split_amount']

    def is_displayed(player):
        return player.id_in_group == 1

class Receiver(Page) :
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

class ResultsWaitPage3(WaitPage) :
    after_all_players_arrive = 'feedback_receiver'

class Results(Page) :
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

class Feedback_Proposer(Page) :
    @staticmethod
    def is_displayed(player):
        return player.round_number == 5

    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)

        return dict(
            totalfair_p=p1.totalfair_proposer,
            totalfair_r=p2.totalfair_receiver
        )

class Survey(Page):
    form_model = 'player'
    form_fields =['Name', 'Gender']

page_sequence = [Proposer, WaitForP1, Receiver, ResultsWaitPage, ResultsWaitPage2, ResultsWaitPage3, Results, Feedback_Proposer]