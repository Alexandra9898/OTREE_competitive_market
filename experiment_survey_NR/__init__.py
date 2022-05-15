from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'experiment_survey_NR'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Q1 = models.StringField(
        label="1.请问您所在的组别为？",
        choices=["无评分组", "有评分组"]
    )
    Q2 = models.StringField(
        label="2.请问您现在是否知道您的实验身份？",
        choices=["我是卖家","我是买家","目前不知道"]
    )
    Q3 = models.StringField(
        label="3.请问卖家定价时知晓若交易发生，买卖双方的交易盈余分别是多少吗？",
        choices=["知道","不知道"]
    )
    Q4 = models.StringField(
        label="4.请问买家选择是否购买时知晓此商品对自己的真实价值吗？",
        choices=["知道","不知道"]
    )
    Q5 = models.StringField(
        label="5.请问上一轮的卖家A一定是这一轮的卖家A吗？",
        choices=["一定","不一定"]
    )
    Q6=models.StringField(
        label="6.请问买家可以选择不购买吗？",
        choices=["可以", "不可以"]
    )
    Q7=models.StringField(
        label="7.请问卖家一轮中最多可以卖出多少商品？",
        choices=["0","1","2","3","4"]
    )
    Q8=models.StringField(
        label="8.请问交易中买家的盈余可能为负吗？",
        choices=["可能","不可能"]
    )
    Q9 = models.StringField(
        label="9.请问交易中卖家的盈余可能为负吗？",
        choices=["可能", "不可能"]
    )
    Q10=models.StringField(
        label="10.请问同一卖家每次交易的产品质量相同吗？",
        choices=["相同","每次交易的产品质量为电脑随机数"]
    )
    Q11=models.StringField(
        label="11.请问买家交易盈余的计算方法为？",
        choices=["就是产品的质量","就是产品对买家的真实价值","产品对买家的真实价值-产品的价格"]
    )
    Q12=models.StringField(
        label="12.请问卖家交易盈余的计算方法为？",
        choices=["就是产品的质量","就是产品的价格","产品的价格-产品的质量"]
    )
    Q13=models.StringField(
        label="13.请问最终按比例折合为实验报酬的数值是？",
        choices=["买卖双方各自的交易盈余","产品对买家的真实价值","产品的卖方成本"]
    )
    pass


# PAGES
class PageOne(Page):
    form_model = "player"
    form_fields = ["Q"+str(i) for i in range(1,7)]
    pass

class PageTwo(Page):
    form_model = "player"
    form_fields = ["Q"+str(i) for i in range(7,14)]
    pass


page_sequence = [PageOne,PageTwo]
