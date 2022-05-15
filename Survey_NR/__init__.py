from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Survey_NR'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Q1_buyer = models.IntegerField(label="1.请问您能接受的商品最高价格是多少？若您的购买决策与卖家出价无关，则填200。（填空题：请填写[0,200]区间内的数值）",
                                  min=0,
                                  max=200)  # 填数字直接放
    Q2_buyer = models.StringField(label="")

    Q1_seller = models.IntegerField(label="1.请问您认为买家能够接受的最高出价是？若您认为购买决策与价格无关，则填200。（填空题：请填写[0,200]区间内的数值）",
                                    min=0,
                                    max=200)
    Q2_seller = models.StringField(label="",choices=["A","B","C","D"])
    Q3_seller = models.StringField(label="",choices=["A","B"])
    Q4_seller = models.StringField(label="")
    pass


# PAGES
class BuyerSurveyone(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "buyer"
    form_model = "player"
    form_fields = ["Q1_buyer"]
    pass

class BuyerSurveytwo(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "buyer"
    form_model = "player"
    form_fields = ["Q2_buyer"]
    pass


class SellerSurveyone(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q1_seller"]
    pass

class SellerSurveytwo(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q2_seller"]
    pass


class SellerSurveythree(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q3_seller"]
    pass

class SellerSurveyfour(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q4_seller"]
    pass


class Thank(Page):
    pass


page_sequence = [BuyerSurveyone, BuyerSurveytwo,SellerSurveyone,SellerSurveytwo,SellerSurveythree,SellerSurveyfour,Thank]
