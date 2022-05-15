from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Q1_buyer = models.IntegerField(label="1.请问您一般在卖家标准化均分大于等于多少时才会选择购买？若您的购买决策与卖家评分无关，则填0。（填空题：请填写[0,100]区间内的数值）",
                                 min=0,
                                 max=100) #填写数字，直接放
    Q2_buyer = models.IntegerField(label="2.请问您能接受的商品最高价格是多少？若您的购买决策与卖家出价无关，则填200。（填空题：请填写[0,200]区间内的数值）",
                                  min=0,
                                  max=200)  # 填数字直接放
    Q3_buyer = models.StringField(label="")
    # 单独放
    Q4_buyer = models.StringField(label="")
    # 单独放
    Q5_buyer = models.StringField(label="5.请问当卖家盈余与买家盈余相等时，您会愿意给出一百分满分的评分吗?",
                                  choices=[["A","愿意"],["B","不愿意"]] )
    # 直接放
    Q1_seller = models.IntegerField(label="1.请问您觉得至少将标准化均分维持在多少，买家才可能选择购买您的商品？若您认为购买决策与评分无关，则填0。（填空题：请填写[0,100]区间内数值）",
                                    min=0,
                                    max=100)
    # 直接放
    Q2_seller = models.IntegerField(label="2.请问您认为买家能够接受的最高出价是？若您认为购买决策与价格无关，则填200。（填空题：请填写[0,200]区间内的数值）",
                                    min=0,
                                    max=200)
    # 直接放
    Q3_seller = models.StringField(label="",choices=["A","B","C","D"])
    Q4_seller = models.StringField(label="",choices=["A","B"])
    Q5_seller = models.StringField(label="")
    Q6_seller = models.StringField(label="")
    pass


# PAGES
class BuyerSurveyone(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "buyer"
    form_model = "player"
    form_fields = ["Q1_buyer", "Q2_buyer"]
    pass


class BuyerSurveytwo(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "buyer"
    form_model = "player"
    form_fields = ["Q3_buyer"]
    pass


class BuyerSurveythree(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "buyer"
    form_model = "player"
    form_fields = ["Q4_buyer","Q5_buyer"]
    pass

#---------------------------------------------------------------------
class SellerSurveyone(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q1_seller","Q2_seller"]
    pass

class SellerSurveytwo(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q3_seller"]
    pass


class SellerSurveythree(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q4_seller"]
    pass

class SellerSurveyfour(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q5_seller"]
    pass


class SellerSurveyfive(Page):
    def is_displayed(player):
        return player.participant.vars['role'] == "seller"
    form_model = "player"
    form_fields = ["Q6_seller"]
    pass


class Thank(Page):
    pass


page_sequence = [BuyerSurveyone,BuyerSurveytwo,BuyerSurveythree, SellerSurveyone,SellerSurveytwo,SellerSurveythree,SellerSurveyfour,SellerSurveyfive,Thank]
