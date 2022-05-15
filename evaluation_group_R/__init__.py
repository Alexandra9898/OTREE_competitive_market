from otree.api import *
import random
from numpy import *
import pandas as pd
from itertools import chain
c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'evaluation_group_R'
    players_per_group = 6  # 6 相当于一组交易组
    num_rounds = 20
    sellerA_role = 'sellerA'
    sellerB_role = 'sellerB'
    sellerC_role = 'sellerC'
    buyerA_role = 'buyerA'
    buyerB_role = 'buyerB'
    buyerC_role = 'buyerC'
    beta = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quality = models.CurrencyField()  # 先随机生成成本
    price = models.CurrencyField(min=0,
                                 max=200,
                                 label="您的出价是：")  # seller定价
    value_to_buyer = models.CurrencyField()  # buyer效用
    buyer_choice = models.StringField(choices=[
        ["A","A"],
        ["B","B"],
        ["C","C"],
        ["no", "不购买"]],
        label="请问您的购买选择是？")
    buyer_decision = models.StringField()
    purchase_time = models.IntegerField(initial=0)
    score = models.IntegerField(min=0,
                                max=100,
                                label="请您为该卖家打分：")
    score_R = models.FloatField()  # 因为要调用历史信息，都在上一期，所以每期buyer只要一评好分就直接生成简单均值
    seller_score = models.StringField()
    pass


def creating_session(subsession):
    # 生成随机choice_list列表
    choice_list=["A", "B", "C"]
    total_list=[]
    for i in range(20):
        random.shuffle(choice_list)  # 如生成[C,B,A]
        total_list += choice_list

    n = 0
    for player in subsession.get_players():
        if player.role in ("sellerA", "sellerB", "sellerC"):
            player.quality=random.randint(1, 100)  # 随机生成quality
            player.buyer_choice = total_list[n]
            n+=1


to_int=lambda X: int(eval(str(X).replace("元","")))

# PAGES


class MyWaitPage1(WaitPage):  # 比如12个人到了以后变成两个组别，66分组，每一轮的结构都是一样的
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class IdentityPage(Page):
    def is_displayed(self):  # 如果是第一轮，则显示这一页
        return self.round_number == 1

    def vars_for_template(self):
        if self.role in ("sellerA", "sellerB", "sellerC"):
            role = "卖家"
            self.participant.vars['role'] = "seller"
        else:
            role = "买家"
            self.participant.vars['role'] = "buyer"
        return {
            "role": role
        }
    pass


class SellerPage(Page):  # 卖家定价页面+生成卖家均分+卖家历史记录
    def is_displayed(player):  # 仅仅在角色是sellerA，sellerB，sellerC才返回该页面）
        return player.role in (Constants.sellerA_role,Constants.sellerB_role,Constants.sellerC_role)

    def vars_for_template(player):
        buyerA = player.group.get_player_by_role("buyerA")
        buyerB = player.group.get_player_by_role("buyerB")
        buyerC = player.group.get_player_by_role("buyerC")
        if player.round_number == 1:
            score_R = None  # 如果是第一轮，那么score_R=None
        else:
            # 生成过去所有轮数的卖家分数的简单平均分score_R，提供给买家进行决策
            previous_score=[]
            for i in (buyerA,buyerB,buyerC):
                for j in i.in_previous_rounds():
                    if j.field_maybe_none('buyer_decision') == str(player.role):
                        previous_score.append(j.score)  # 如果buyer_decision==当前玩家的role的话，那么在列表里面加上score
            print("SellerPage生成该卖家所有历史分数",previous_score)
            score_R = None if len(previous_score)==0 else mean(previous_score)
        player.score_R = score_R
        player.value_to_buyer = player.quality * Constants.beta
        # python制作html表格--------------------------------------------------
        previous_player = player.in_previous_rounds()
        previous_quality = [to_int(i.quality) for i in previous_player]
        previous_price = [to_int(i.price) for i in previous_player]
        previous_score_R = []
        for i in previous_player:  # 获取每轮买家的决策依据（平均分）
            try:
                previous_score_R.append(str(round(i.score_R,2))+"分")
            except:
                previous_score_R.append("无")
        previous_purchase_time= [i.purchase_time for i in previous_player]
        previous_score_list = list(map(lambda x: "无" if x=="" else x,[i.seller_score for i in previous_player]))
        data = {"历史均分": previous_score_R, "成本": previous_quality, "定价": previous_price,"卖出件数":previous_purchase_time,
                "卖家评分": previous_score_list}
        htmltable_df = pd.DataFrame(data, index=["第" + str(i) + "轮" for i in range(1, player.round_number)]).T
        htmltable = htmltable_df.to_html()
        # -----------------------------------------------------------------------------
        return {
            "quality": player.quality,
            "value_to_buyer": player.value_to_buyer,
            "score_R": None if score_R == None else round(score_R,2),
            "convertTohtml": htmltable
        }
    form_model = "player"
    form_fields = ["price"]


def extend_list(table_dic,buyer,new_content,previous_record):
    new_record=["", "", ""]
    new_record[table_dic[buyer.buyer_decision]] = new_content
    previous_record.extend(new_record)


def get_table(sellerA, sellerB, sellerC, player):
    # 生成html表格-----------------------------------------------------------
    sellerA_score = [i.field_maybe_none('score_R') for i in sellerA.in_previous_rounds()]
    sellerB_score = [i.field_maybe_none('score_R') for i in sellerB.in_previous_rounds()]
    sellerC_score = [i.field_maybe_none('score_R') for i in sellerC.in_previous_rounds()]
    previous_average_score_R = ["无" if j == None else round(j,2) for j in list(chain.from_iterable(zip(sellerA_score,sellerB_score,sellerC_score)))]
    print(previous_average_score_R)
    sellerA_price = [to_int(i.field_maybe_none('price')) for i in sellerA.in_previous_rounds()]
    sellerB_price = [to_int(i.field_maybe_none('price')) for i in sellerB.in_previous_rounds()]
    sellerC_price = [to_int(i.field_maybe_none('price')) for i in sellerC.in_previous_rounds()]
    previous_price = list(chain.from_iterable(zip(sellerA_price,sellerB_price,sellerC_price)))
    print(previous_price)
    table_dic={"sellerA":0,"sellerB":1,"sellerC":2}
    previous_buyer_decision,previous_score,previous_quality=[],[],[]
    for buyer in player.in_previous_rounds():
        if buyer.field_maybe_none('buyer_decision')!=None:
            extend_list(table_dic, buyer, "是", previous_buyer_decision)
            extend_list(table_dic, buyer, buyer.score, previous_score)
            extend_list(table_dic, buyer, to_int(buyer.quality), previous_quality)
        else:
            for previous_record in previous_buyer_decision, previous_score, previous_quality:
                previous_record.extend(["","",""])
    print(previous_buyer_decision,len(previous_quality),len(previous_score))
    seller_list=["卖家A","卖家B","卖家C"]*(player.round_number-1)
    index=[]
    for i in range(1,player.round_number):
        index.extend(["","第" + str(i) + "轮",""])
    data = {"":seller_list,
            "卖家均分": previous_average_score_R,
            "商品价格": previous_price,
            "是否购买": previous_buyer_decision,
            "商品成本": previous_quality,
            "评分": previous_score}
    htmltable_df = pd.DataFrame(data,index=index).T
    return htmltable_df.to_html()
    # -----------------------------------------------------------------------


class BuyerPage(Page):  # 买家评分要参考：价格、评分
    def is_displayed(player):
        return player.role in (Constants.buyerA_role, Constants.buyerB_role, Constants.buyerC_role)

    def vars_for_template(player):
        # 生成选项和实际卖家的dict
        sellerA = player.group.get_player_by_role("sellerA")
        sellerB = player.group.get_player_by_role("sellerB")
        sellerC = player.group.get_player_by_role("sellerC")
        seller_list=[sellerA, sellerB, sellerC]
        seller_=["sellerA","sellerB","sellerC"]
        choice_list=[i.buyer_choice for i in seller_list]
        choice_seller=dict(zip(choice_list,seller_))

        scoreR_A = player.group.get_player_by_role(choice_seller["A"]).field_maybe_none('score_R')
        scoreR_B = player.group.get_player_by_role(choice_seller["B"]).field_maybe_none('score_R') # sellerA的price
        scoreR_C = player.group.get_player_by_role(choice_seller["C"]).field_maybe_none('score_R')
        htmltable = get_table(sellerA, sellerB, sellerC, player)
        return{
            "priceA": player.group.get_player_by_role(choice_seller["A"]).price,  # 生成sellerC的price
            "priceB": player.group.get_player_by_role(choice_seller["B"]).price,  # 生成sellerA的price
            "priceC": player.group.get_player_by_role(choice_seller["C"]).price,  # 生成sellerB的price
            "scoreR_A": "暂无" if scoreR_A == None else scoreR_A,
            "scoreR_B": "暂无" if scoreR_B == None else scoreR_B,
            "scoreR_C": "暂无" if scoreR_C == None else scoreR_C,
            "convertTohtml": htmltable
        }
    form_model = "player"
    form_fields = ["buyer_choice"]


def seller_score(buyerA, buyerB, buyerC, role):
    seller_score_list=[]
    for the_buyer in (buyerA, buyerB, buyerC):
        if the_buyer.field_maybe_none('buyer_decision') == role:
            seller_score_list.append(str(the_buyer.score))
    return ",".join(seller_score_list)

class MyWaitPage(WaitPage):  # 计算seller的被购买次数，收益，和获得的score
    @staticmethod
    def after_all_players_arrive(group: Group):  # 当一个group同时到达，则开始计算seller的数据
        sellerA = group.get_player_by_role("sellerA")
        sellerB = group.get_player_by_role("sellerB")
        sellerC = group.get_player_by_role("sellerC")
        buyerA = group.get_player_by_role("buyerA")
        buyerB = group.get_player_by_role("buyerB")
        buyerC = group.get_player_by_role("buyerC")

        buyer_record = [buyerA.field_maybe_none('buyer_decision'), buyerB.field_maybe_none('buyer_decision'),
                        buyerC.field_maybe_none('buyer_decision')]

        sellerA.purchase_time = buyer_record.count("sellerA")  # 生成卖家被购买的次数
        sellerB.purchase_time = buyer_record.count("sellerB")
        sellerC.purchase_time = buyer_record.count("sellerC")

        sellerA.payoff = sellerA.purchase_time*(sellerA.price-sellerA.quality)
        sellerB.payoff = sellerB.purchase_time*(sellerB.price-sellerB.quality)
        sellerC.payoff = sellerC.purchase_time*(sellerC.price - sellerC.quality)

        for the_seller in (sellerA,sellerB,sellerC):
            the_seller.seller_score = seller_score(buyerA, buyerB, buyerC,str(the_seller.role))

class ResultsWaitPage(WaitPage):#等待界面
    pass


class BuyerResults(Page):
    def is_displayed(player):  # 只有买家看得到这个页面
        return player.role in (Constants.buyerA_role, Constants.buyerB_role, Constants.buyerC_role)

    def vars_for_template(player):
        buyer_decision = player.field_maybe_none('buyer_decision')  # 购买决定：如sellerA，或者0
        if buyer_decision != None:  # 如果交易发生了
            buyer_result = "购买了"
        else:
            buyer_result="未购买任何"
            player.payoff=0
        return {
            "buyer_result":buyer_result,
        }
    pass


class SellerResults(Page):
    def is_displayed(player):  # 只有买家看得到这个页面
        return player.role in (Constants.sellerA_role, Constants.sellerB_role, Constants.sellerC_role)

    def vars_for_template(player):
        if player.purchase_time!=0:
            seller_result="被{}位买家购买".format(player.purchase_time)
        else:
            seller_result="未被购买"
        return{
            "seller_result":seller_result,
            "seller_score":player.seller_score
        }
    pass


class BuyerScorePage(Page):
    def is_displayed(player):  # 购买了商品的买家进入BuyerScorePage，其他人在MyWaitPage等待
        return str(player.role) in ("buyerA", "buyerB", "buyerC") and player.buyer_choice != "no"

    def vars_for_template(player):
        sellerA = player.group.get_player_by_role("sellerA")
        sellerB = player.group.get_player_by_role("sellerB")
        sellerC = player.group.get_player_by_role("sellerC")
        seller_ = ["sellerA", "sellerB", "sellerC"]
        choice_list = [i.buyer_choice for i in [sellerA, sellerB, sellerC]]
        choice_seller = dict(zip(choice_list, seller_))

        player.buyer_decision = choice_seller[player.buyer_choice]  # 生成choice背后真正的seller
        target_seller = player.group.get_player_by_role(player.buyer_decision)  # 获取target_seller
        player.price = target_seller.price  # 把target_seller的数据传递过来，传递price、quality和value_to_buyer
        player.quality = target_seller.quality
        player.value_to_buyer = target_seller.value_to_buyer
        player.payoff = player.value_to_buyer - player.price
        seller_payoff = player.price-player.quality
        player.score_R = target_seller.field_maybe_none("score_R")  # 获取buyer做决策用的score_R
        htmltable = get_table(sellerA, sellerB, sellerC, player)
        return{
            "quality":player.quality,
            "price":player.price,
            "value_to_buyer":player.value_to_buyer,
            "buyer_payoff":player.payoff,
            "seller_payoff":seller_payoff,
            "convertTohtml": htmltable
        }

    form_model = "player"
    form_fields = ["score"]
    pass


class CombinedResults(Page):
    def is_displayed(self): #如果是最后一轮，那么在此之后返回combinedResults这一页
        return self.round_number==Constants.num_rounds
    def vars_for_template(player): #这个用来生成累加过后的payoff
        all_players = player.in_all_rounds() #返回该角色（同id/role）玩家
        combined_payoff=0
        for player in all_players:
            combined_payoff += player.payoff
        return{
            "combined_payoff":combined_payoff
        }


page_sequence = [IdentityPage, SellerPage, ResultsWaitPage, BuyerPage, BuyerScorePage, MyWaitPage, BuyerResults, SellerResults,CombinedResults]
