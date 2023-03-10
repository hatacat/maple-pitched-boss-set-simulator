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
    # isweapon = True ??? ?????? ?????????
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
    ??????(160) : 10/10 <-> ??????(140) : 5/5
    ??????(160) : 3/15 <-> ??????(145) : 1/8
    ??????(200) : 6/50 <-> ?????????(150) : 1/18
    ??????(160) : 3/10  <-> ??????(140) : 3/20
    ??????(200) : 5/7  <-> ????????????(160) : 2/7
    ??????(??????x)(200) : 4/5 <-> ?????????(??????x, ??????x) : 25/40
    ?????????(??????x)(160) : 10/20 <-> ??????(??????x)(140) : 5/5
    '''
    base={'??????':[10,10,160], '??????':[5,5,140], '??????':[3,15,160], '??????':[1,8,145], '??????':[6,50,200], '?????????':[1,18,150],
           '??????':[3,10,160], '??????':[3,20,140], '??????':[5,7,200], '????????????':[2,7,160], '??????':[4,5,200], '?????????':[25,40,120],
           '?????????':[10,20,160], '??????':[5,5,140]}

    result=State()
    level=base[name][2]
    # base option
    result.all_state=base[name][1]
    result.attack=base[name][0]
    
    # additional_option
    if name!="??????" and name!="?????????":
        result.all_state=result.all_state+addtional_option[level]
    
    # starforce
    if name!="?????????" and name!="?????????" and name!="??????":
        star_enhance=calulate_star(level,star)
        result.add(star_enhance)
    
    return result   

# ??????, ?????? ???????????? ??????
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

# [??????,??????,?????????,??????,????????????,?????????,??????] > [??????,??????,??????,??????,??????,??????,?????????]
# ?????? 4?????????, [-1,0,0,0,-1,0,0] set num ??????

# ?????? ????????? ?????????
def get_pitched_set_change(is_pitched, star, additional_option, exchange_rate_dict, state_to_final, pitched_num_init=0, is_print=False): # output : total state
    before_name=['??????','??????','?????????','?????????','????????????','??????','??????']
    after_name=['??????','??????','??????','??????','??????','??????','?????????']
    dawn_num=4
    pitched_num=pitched_num_init
    if is_print:
        print("????????? ?????? ",pitched_num,"???, ?????? ",dawn_num,"??? \n")
    
    dawn_num=dawn_num+np.sum(is_pitched*np.array([-1,0,0,0,-1,0,0]))
    pitched_num+=np.sum(is_pitched)
    if is_print:
        print("???????????? ?????? ",pitched_num,"???, ?????? ",dawn_num,"??? \n")
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
        print("?????? ?????????")
        result.show()
        print("\n")
    return result.calculate_total(exchange_rate_dict,state_to_final)
    
# ????????? ?????? ?????? (is_pitched3 : 3?????? (0: ??????, 1: target_star ??????, 2: ????????? next_target_star ??????)
def get_pitched_set_change_spare(is_pitched, star, star_next, additional_option, exchange_rate_dict, state_to_final, pitched_num_init=0, is_print=False): # output : total state
    before_name=['??????','??????','?????????','?????????','????????????','??????','??????']
    after_name=['??????','??????','??????','??????','??????','??????','?????????']
        
    dawn_num=4
    pitched_num=pitched_num_init
    if is_print:
        print("????????? ?????? ",pitched_num,"???, ?????? ",dawn_num,"??? \n")
    
    dawn_num=dawn_num+np.sum((is_pitched!=0)*np.array([-1,0,0,0,-1,0,0]))
    pitched_num+=np.sum(is_pitched!=0)
    if is_print:
        print("???????????? ?????? ",pitched_num,"???, ?????? ",dawn_num,"??? \n")
    # set initial item
    change_item=[]
    change_item_next=[]
    for i in range(7):
        after=equip_gen(after_name[i],star[i],additional_option)
        before=equip_gen(before_name[i],22,additional_option)
        after.sub(before)
        change_item.append(after)

    for i in range(7):
        after=equip_gen(after_name[i],star_next[i],additional_option)
        before=equip_gen(before_name[i],22,additional_option)
        after.sub(before)
        change_item_next.append(after)

    # apply change
    result=State()
    for ind, i in enumerate(is_pitched==1):
        if i:
            result.add(change_item[ind])

    for ind, i in enumerate(is_pitched==2):
        if i:
            result.add(change_item_next[ind])
            
    # apply set effect
    result.add(pitched_set_gen(pitched_num))
    result.add(dawn_set_gen(dawn_num))
    result.sub(dawn_set_gen(4))
    result.sub(pitched_set_gen(pitched_num_init))
    
    if is_print:
        print("?????? ?????????")
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

def unzip(index,base,n):
    result=np.zeros(n,dtype=int)
    temp=index    
    for i in range(n):
        result[i]=temp//(base**(n-i-1))
        temp=temp%(base**(n-i-1))    
    # check
    for i in result:
        if i>=base:
            print("error in length! : ",result)
            break    
    return result

def cashing_final_damage_spare(star,star_next,additional_option,exchange_rate_dict,state_to_final,pitched_num_init=0):
    # cashing is_pitched(base 3) > final_damage array
    cashed_data=[]
    for i in range(3**7):
        is_pitched=unzip(i,3,7)
        temp=get_pitched_set_change_spare(is_pitched, star, star_next, additional_option, exchange_rate_dict,state_to_final, pitched_num_init)
        cashed_data.append(temp)
        #print(is_pitched,temp)
    cashed_data=np.array(cashed_data)
    return np.array(cashed_data)

def dict2arr(dictionary, ind_list):
    result=np.zeros_like(ind_list,dtype=float)
    for ind,i in enumerate(ind_list):
        result[ind]=dictionary[i]
    return result

