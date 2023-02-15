import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from core import *

class Simulate:
    def __init__(self,p,n,week,target,star,exchange_rate_dict,state_to_final,cashed_data):
        self.p = p # 칠흑 드랍율
        self.n = n # 시뮬레이션 횟수
        self.week = week # 칠흑 파밍 주
        self.success_p={0:1,17:1, 18:0.9388, 19:0.7727, 20:0.5587, 21:0.4576, 22:0.2920} # 올파방 목표 성공률
        self.target = target # 칠흑 완성 목표
        self.star = star # [루컨,마깃,몽벨,거공,커포,고근,마도서]
        self.exchange_rate_dict =exchange_rate_dict # 환산값(타스탯>스탯)
        self.state_to_final =state_to_final # 환산값(스택>최종뎀)
        self.cashed_data = cashed_data # 최종뎀 캐싱
        self.result=[]
        self.total_change=[]
        self.debug=[]

    def simulating(self):
        self.result=[]
        self.total_change=[]
        sep=5000
        for i in tqdm(range(int(self.n/sep))):
            is_drop=np.random.rand(sep,self.week,7)<self.p # [루컨,마깃,몽벨,거공,커포,고근,마도서]
            drop_count=is_drop.sum(axis=1) # shape : (iter, 7)
            max_drop=drop_count.max()

            is_completed=np.zeros((max_drop,sep,7),dtype=bool) # determine target success
            for ind,_ in enumerate(is_completed):
                is_completed[ind]=drop_count>=ind+1

            target_success=np.random.rand(max_drop,sep,7)<dict2arr(self.success_p,self.star)# target 달성 판별용 random 값
            target_success[:,:,6]=True # 마도서는 항상 성공

            is_completed=is_completed*target_success
            final=np.sum(is_completed,axis=0,dtype=bool) # final : batch * final result(boolean)
            index=np.sum(final*np.array([64,32,16,8,4,2,1]),axis=-1)
            self.total_change.append(index)
            self.result.append(np.sum(final,axis=1))

        self.result=np.array(self.result).flatten()
        self.total_change=np.array(self.total_change).flatten()
        self.debug=self.total_change
        self.total_change=self.cashed_data[self.total_change]
        self.total_change[self.total_change<0]=0

    def plot(self):
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['figure.figsize'] = [10, 4]
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)


        ax1.set_title("%d주 동안 %d성 칠흑셋 완성 확률"%(self.week,self.target))
        ax1.hist(self.result,bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5],density=True, cumulative=-1, label='누적 확률', color='skyblue',rwidth=0.85)

        ax1.hist(self.result,bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5],density=True, cumulative=False, label='확률', color='orange',rwidth=0.85)

        ax1.set_xlabel("완성된 %d성 칠흑개수"%self.target)
        ax1.set_ylabel("확률")
        ax1.legend(loc='upper right')

        print("%d주 동안 %d성 칠흑셋 완성 확률"%(self.week,self.target))
        for i in range(8):
            print("%d 개 확률 : %5.2f %%"%(7-i, np.sum(self.result==(7-i))/self.result.shape[0]*100))

        print("")

        ax2.set_title("%d주 동안 %d성 칠흑셋 목표시 최종뎀 증가 분포"%(self.week,self.target))

        ax2.hist(self.total_change ,density=True, cumulative=False, label='확률', color='skyblue',rwidth=0.85)

        ax2.set_xlabel("최종뎀 증가량(%)")
        ax2.set_ylabel("확률")

        print("%d주 동안 %d성 칠흑셋 최종뎀 증가량"%(self.week,self.target))
        print("평균 : %5.2f %%"%np.average(self.total_change))
        print("표준편차 : %5.2f %%"%np.std(self.total_change),"\n")
        print("상위 1%% : %5.2f %%"%np.quantile(self.total_change,0.99))
        print("상위 10%% : %5.2f %%"%np.quantile(self.total_change,0.9))
        print("상위 25%% : %5.2f %%"%np.quantile(self.total_change,0.75))
        print("중간값 : %5.2f %%"%np.quantile(self.total_change,0.5))
        print("하위 25%% : %5.2f %%"%np.quantile(self.total_change,0.25))
        print("하위 10%% : %5.2f %%"%np.quantile(self.total_change,0.10))
        print("하위 1%% : %5.2f %%"%np.quantile(self.total_change,0.01))
        
class Simulate_spare:
    def __init__(self,p,n,week,target,star,star_next, exchange_rate_dict,state_to_final,cashed_data):
        self.p = p # 칠흑 드랍율
        self.n = n # 시뮬레이션 횟수
        self.week = week # 칠흑 파밍 주
        self.success_p={0:1, 17:1, 18:0.9388, 19:0.7727, 20:0.5587, 21:0.4576, 22:0.2920} # 올파방 목표 성공률
        self.target = target # 칠흑 완성 목표
        self.star = star # [루컨,마깃,몽벨,거공,커포,고근,마도서]
        self.star_next = star_next # [루컨,마깃,몽벨,거공,커포,고근,마도서]
        self.exchange_rate_dict =exchange_rate_dict # 환산값(타스탯>스탯)
        self.state_to_final =state_to_final # 환산값(스택>최종뎀)
        self.cashed_data = cashed_data # 최종뎀 캐싱
        self.result_target=[]
        self.result_spare=[]
        self.total_change=[]
        self.debug=[]

    def simulating(self):
        self.result_target=[]
        self.result_spare=[]
        self.total_change=[]
        sep=5000
        for i in tqdm(range(int(self.n/sep))):
            is_drop=np.random.rand(sep,self.week,7)<self.p # [루컨,마깃,몽벨,거공,커포,고근,마도서]
            drop_count=is_drop.sum(axis=1) # shape : (iter, 7)
            max_drop=drop_count.max()

            is_completed=np.zeros((max_drop,sep,7),dtype=bool) # determine target success
            for ind,_ in enumerate(is_completed):
                is_completed[ind]=drop_count>=ind+1
            
            # target star 강화용 확률값
            target_success=np.random.rand(max_drop,sep,7)<dict2arr(self.success_p,self.star)# target 달성 판별용 random 값
            target_success[:,:,6]=True # 마도서는 항상 성공

            is_completed=is_completed*target_success # star 강화 성공값

            # 스페어 22 강화용 확률값
            target_next_success=np.random.rand(max_drop,sep,7)<dict2arr(self.success_p,self.star_next)/dict2arr(self.success_p,self.star) # target_next 달성 판별용 random 값

            target_next_success[:,:,6]=True # 마도서는 항상 성공

            # 스페어 강화 성공 확인
            spare_count=np.sum(is_completed,axis=0) # 스페어 개수
            spare_count=spare_count-1 # star_target 에 성공한거는 강화 안함
            spare_count[spare_count==-1]=0 # star_target 실패한거 스페어 개수 0개로 바꿈

            is_spare_completed=np.zeros((max_drop,sep,7),dtype=bool) # determine star_next success
            for ind,_ in enumerate(is_spare_completed):
                is_spare_completed[ind]=spare_count>=ind+1

            is_spare_completed=is_spare_completed*target_next_success # spare star_next 강화 성공값

            final=np.sum(is_completed,axis=0,dtype=bool) # final : batch * final result(boolean) : target 성공 여부
            final_spare=np.sum(is_spare_completed,axis=0,dtype=bool) # final_spare : batch * final result : spare 성공 여부
            index=np.sum((final*1+final_spare*1)*np.array([729,243,81,27,9,3,1]),axis=-1)
            self.total_change.append(index)
            self.result_target.append(np.sum(final,axis=1))
            self.result_spare.append(np.sum(final_spare,axis=1))

        self.result_target=np.array(self.result_target).flatten()
        self.result_spare=np.array(self.result_spare).flatten()
        self.total_change=np.array(self.total_change).flatten()
        self.debug=self.total_change
        self.total_change=self.cashed_data[self.total_change]        
        self.total_change[self.total_change<0]=0
        
    def plot(self):
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['figure.figsize'] = [10, 4]
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)


        ax1.set_title("%d주 동안 %d성 칠흑셋 완성 확률"%(self.week,self.target))
        ax1.hist(self.result_target,bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5],density=True, cumulative=-1, label='누적 확률', color='skyblue',rwidth=0.85)

        ax1.hist(self.result_target,bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5],density=True, cumulative=False, label='확률', color='orange',rwidth=0.85)

        ax1.set_xlabel("완성된 %d성 칠흑개수"%self.target)
        ax1.set_ylabel("확률")
        ax1.legend(loc='upper right')

        print("%d주 동안 %d성 칠흑셋 완성 확률"%(self.week,self.target))
        for i in range(8):
            print("%d 개 확률 : %5.2f %%"%(7-i, np.sum(self.result_target==(7-i))/self.result_target.shape[0]*100))

        print("")
        
        print("%d주 동안 22성 칠흑 완성 확률(스페어 강화)"%(self.week))
        for i in range(8):
            print("%d 개 확률 : %5.2f %%"%(7-i, np.sum(self.result_spare==(7-i))/self.result_spare.shape[0]*100))

        print("")
        
        ax2.set_title("%d주 동안 %d성 칠흑셋 목표시 최종뎀 증가 분포"%(self.week,self.target))

        ax2.hist(self.total_change ,density=True, cumulative=False, label='확률', color='skyblue',rwidth=0.85)

        ax2.set_xlabel("최종뎀 증가량(%)")
        ax2.set_ylabel("확률")

        print("%d주 동안 %d성 칠흑셋 최종뎀 증가량"%(self.week,self.target))
        print("평균 : %5.2f %%"%np.average(self.total_change))
        print("표준편차 : %5.2f %%"%np.std(self.total_change),"\n")
        print("상위 1%% : %5.2f %%"%np.quantile(self.total_change,0.99))
        print("상위 10%% : %5.2f %%"%np.quantile(self.total_change,0.9))
        print("상위 25%% : %5.2f %%"%np.quantile(self.total_change,0.75))
        print("중간값 : %5.2f %%"%np.quantile(self.total_change,0.5))
        print("하위 25%% : %5.2f %%"%np.quantile(self.total_change,0.25))
        print("하위 10%% : %5.2f %%"%np.quantile(self.total_change,0.10))
        print("하위 1%% : %5.2f %%"%np.quantile(self.total_change,0.01))