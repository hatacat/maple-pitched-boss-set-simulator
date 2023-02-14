import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
# set effect
class State:
    def __init__(self):
        self.all_state=0
        self.boss_damage=0
        self.attack=0
        self.ignore_defense=0
        self.critical_damage=0
        
    def set_state(self, set_dict):
        # set_dict = {'all_state': , 'boss_damage': , 'attack': , 'ignore_defense':, 'critical_damage':}  
        self.all_state=set_dict['all_state']
        self.boss_damage=set_dict['boss_damage']
        self.attack=set_dict['attack']
        self.ignore_defense=set_dict['ignore_defense']/100.
        self.critical_damage=set_dict['critical_damage']
        
    def add_state(self, set_dict):
        # set_dict = {'all_state': , 'boss_damage': , 'attack': , 'ignore_defense':, 'critical_damage':}  
        self.all_state+=set_dict['all_state']
        self.boss_damage+=set_dict['boss_damage']
        self.attack+=set_dict['attack']
        self.ignore_defense=1-(1-self.ignore_defense)*(1-set_dict['ignore_defense']/100.)
        self.critical_damage+=set_dict['critical_damage']
        
    def sub_state(self, set_dict):
        # set_dict = {'all_state': , 'boss_damage': , 'attack': , 'ignore_defense':, 'critical_damage':}  
        self.all_state-=set_dict['all_state']
        self.boss_damage-=set_dict['boss_damage']
        self.attack-=set_dict['attack']
        self.ignore_defense=1-(1-self.ignore_defense)/(1-set_dict['ignore_defense']/100.)
        self.critical_damage-=set_dict['critical_damage']
    
    def add(self, other):
        self.all_state+=other.all_state
        self.boss_damage+=other.boss_damage
        self.attack+=other.attack
        self.ignore_defense=1-(1-self.ignore_defense)*(1-other.ignore_defense)
        self.critical_damage+=other.critical_damage

    def sub(self, other):
        self.all_state-=other.all_state
        self.boss_damage-=other.boss_damage
        self.attack-=other.attack
        self.ignore_defense=1-(1-self.ignore_defense)/(1-other.ignore_defense)
        self.critical_damage-=other.critical_damage

    def calculate_total(self, exchange_rate_dict,state_to_final):
        # exchange_rate_dict = {'all_state': , 'boss_damage': , 'attack': , 'ignore_defense':, 'critical_damage':}  
        # convert to main state & sum all
        state_to_final=state_to_final/100
        total=1
        total*=(1+self.all_state*exchange_rate_dict['all_state']*state_to_final)
        total*=(1+self.boss_damage*exchange_rate_dict['boss_damage']*state_to_final)
        total*=(1+self.attack*exchange_rate_dict['attack']*state_to_final)
        total*=(1+self.ignore_defense*exchange_rate_dict['ignore_defense']*100*state_to_final)
        total*=(1+self.critical_damage*exchange_rate_dict['critical_damage']*state_to_final)

        return (total-1)*100
    
    def show(self):
        print("all_state : ",self.all_state)
        print("boss_damage : ",self.boss_damage)
        print("attack : ",self.attack)
        print("ignore_defense : %.2f"%self.ignore_defense)
        print("critical_damage : ",self.critical_damage)



def calulate_star(level,star,isweapon=False): # output : State
    # isweapon = True 인 경우 미구현
    result=State()
    set_dict = {'all_state':0 , 'boss_damage':0 , 'attack':0 , 'ignore_defense':0, 'critical_damage':0}
    for i in range(15):
        if (i+1)>star:
            break
        if (i+1)<6:
            set_dict['all_state']+=2
        elif (i+1)<16:
            set_dict['all_state']+=3
        
    if level==130:
        state=[7,7,7,7,7,0,0,0,0,0]
        attack=[7,8,9,10,11,0,0,0,0]        
            
    elif level==140 or level==145:
        state=[9,9,9,9,9,9,9,0,0,0]
        attack=[8,9,10,11,12,13,15,17,19,21]
        
    elif level==150:
        state=[11,11,11,11,11,11,11,0,0,0]
        attack=[9,10,11,12,13,14,16,18,20,22]
        
    elif level==160:
        state=[13,13,13,13,13,13,13,0,0,0]
        attack=[10,11,12,13,14,15,17,19,21,23]
        
    elif level==200:
        state=[15,15,15,15,15,15,15,0,0,0]
        attack=[12,13,14,15,16,17,19,21,23,25]
        
    elif level==250:
        state=[17,17,17,17,17,17,17,0,0,0]
        attack=[14,15,16,17,18,19,21,23,25,27]
    
    else:
        print("error!")
        return None

    for ind,i in enumerate(range(16,26)):
        if i>star:
            break
        set_dict['all_state']+=state[ind]
        set_dict['attack']+=attack[ind]
         
    result.add_state(set_dict)
    return result


def equip_gen(name,star,addtional_option): # output : State
    '''
    루컨(160) : 10/10 <-> 트왈(140) : 5/5
    마깃(160) : 3/15 <-> 파풀(145) : 1/8
    몽벨(200) : 6/50 <-> 분자벨(150) : 1/18
    고근(160) : 3/10  <-> 도미(140) : 3/20
    커포(200) : 5/7  <-> 에스텔라(160) : 2/7
    거공(추옵x)(200) : 4/5 <-> 이벤링(추옵x, 강화x) : 25/40
    마도서(강화x)(160) : 10/20 <-> 성배(강화x)(140) : 5/5
    '''
    base={'루컨':[10,10,160], '트왈':[5,5,140], '마깃':[3,15,160], '파풀':[1,8,145], '몽벨':[6,50,200], '분자벨':[1,18,150],
           '고근':[3,10,160], '도미':[3,20,140], '커포':[5,7,200], '에스텔라':[2,7,160], '거공':[4,5,200], '이벤링':[25,40,120],
           '마도서':[10,20,160], '성배':[5,5,140]}

    result=State()
    level=base[name][2]
    # base option
    result.all_state=base[name][1]
    result.attack=base[name][0]
    
    # additional_option
    if name!="거공" and name!="이벤링":
        result.all_state=result.all_state+addtional_option[level]
    
    # starforce
    if name!="마도서" and name!="이벤링" and name!="성배":
        star_enhance=calulate_star(level,star)
        result.add(star_enhance)
    
    return result   

# 여명, 칠흑 세트옵션 구현
def dawn_set_gen(num): # output : State
    result=State()
    
    if num>=2:
        set_option = {'all_state': 10 , 'boss_damage': 10 , 'attack': 10, 'ignore_defense': 0, 'critical_damage': 0}
        result.add_state(set_option)
    if num>=3:
        set_option = {'all_state': 10 , 'boss_damage': 0 , 'attack': 10, 'ignore_defense': 0, 'critical_damage': 0}
        result.add_state(set_option)
    if num>=4:
        set_option = {'all_state': 10 , 'boss_damage': 0 , 'attack': 10, 'ignore_defense': 10, 'critical_damage': 0}
        result.add_state(set_option)
    return result

def pitched_set_gen(num): # output : State
    result=State()    
    if num>=2:
        set_option = {'all_state': 10 , 'boss_damage': 10 , 'attack': 10, 'ignore_defense': 0, 'critical_damage': 0}
        result.add_state(set_option)
    if num>=3:
        set_option = {'all_state': 10 , 'boss_damage': 0 , 'attack': 10, 'ignore_defense': 10, 'critical_damage': 0}
        result.add_state(set_option)
    if num>=4:
        set_option = {'all_state': 15 , 'boss_damage': 0 , 'attack': 15, 'ignore_defense': 0, 'critical_damage': 5}
        result.add_state(set_option)
    if num>=5:
        set_option = {'all_state': 15 , 'boss_damage': 10 , 'attack': 15, 'ignore_defense': 0, 'critical_damage': 0}
        result.add_state(set_option)
    if num>=6:
        set_option = {'all_state': 15 , 'boss_damage': 0 , 'attack': 15, 'ignore_defense': 10, 'critical_damage': 0}
        result.add_state(set_option)
    if num>=7:
        set_option = {'all_state': 15 , 'boss_damage': 0 , 'attack': 15, 'ignore_defense': 0, 'critical_damage': 5}
        result.add_state(set_option)
    if num>=8:
        set_option = {'all_state': 15 , 'boss_damage': 10 , 'attack': 15, 'ignore_defense': 0, 'critical_damage': 0}
        result.add_state(set_option)
    if num>=9:
        set_option = {'all_state': 15 , 'boss_damage': 0 , 'attack': 15, 'ignore_defense': 0, 'critical_damage': 5}
        result.add_state(set_option)
    return result

# [트왈,파풀,분자벨,도미,에스텔라,이벤링,성배] > [루컨,마깃,몽벨,고근,커포,거공,마도서]
# 여명 4셋에서, [-1,0,0,0,-1,0,0] set num 감소

# 칠흑 부위별 변화량
def get_pitched_set_change(is_pitched, star, additional_option, exchange_rate_dict, state_to_final, pitched_num_init=0, is_print=False): # output : total state
    before_name=['트왈','파풀','분자벨','도미','에스텔라','이벤링','성배']
    after_name=['루컨','마깃','몽벨','고근','커포','거공','마도서']
        
    dawn_num=4
    pitched_num=pitched_num_init
    if is_print:
        print("변경전 칠흑 ",pitched_num,"셋, 여명 ",dawn_num,"셋 \n")
    
    dawn_num=dawn_num+np.sum(is_pitched*np.array([-1,0,0,0,-1,0,0]))
    pitched_num+=np.sum(is_pitched)
    if is_print:
        print("변경이후 칠흑 ",pitched_num,"셋, 여명 ",dawn_num,"셋 \n")
    # set initial item
    change_item=[]
    for i in range(7):
        after=equip_gen(after_name[i],star[i],additional_option)
        before=equip_gen(before_name[i],22,additional_option)
        after.sub(before)
        change_item.append(after)
           
    # apply change
    result=State()
    for ind, i in enumerate(is_pitched):
        if i:
            result.add(change_item[ind])
    
    # apply set effect
    result.add(pitched_set_gen(pitched_num))
    result.add(dawn_set_gen(dawn_num))
    result.sub(dawn_set_gen(4))
    result.sub(pitched_set_gen(pitched_num_init))
    
    if is_print:
        print("변경 스탯들")
        result.show()
        print("\n")
    return result.calculate_total(exchange_rate_dict,state_to_final)
    

def cashing_final_damage(star,additional_option,exchange_rate_dict,state_to_final,pitched_num_init=0):
    # cashing is_pitched > final_damage array
    cashed_data=[]
    for i in range(128):
        is_pitched=np.unpackbits(np.array([i*2],dtype=np.uint8), count=-1)!=0
        temp=get_pitched_set_change(is_pitched, star, additional_option, exchange_rate_dict,state_to_final, pitched_num_init)
        cashed_data.append(temp)
    cashed_data=np.array(cashed_data)
    return np.array(cashed_data)


        