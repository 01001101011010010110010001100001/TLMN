from ..base.player import Player
import random
from colorama import Fore, Style
import json
 
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
        self.pairs = []
 
    def action(self, dict_input):
        list_action = self.get_list_index_action(dict_input['State'], dict_input['List_all_action_code'], dict_input['Close_game'])
        random.shuffle(list_action)
        # print(list_action)
        action = random.choice(list_action)
        # print(action)
        # print(dict_input['State'][:52], 'Đã đánh')
        # print(dict_input['State'][52:104], 'Cần chặn')
        # print(dict_input['State'][104:156], 'Trên tay')
        # print(dict_input['State'][156], 'ID')
        # print(dict_input['State'][157:161], 'Số lá còn lại')
        # print(dict_input['State'][161:165], 'Tình trạng bỏ vòng')
        # print(dict_input['State'][165], 'ID chủ nhân bài hiện tại')
        # print(dict_input['Close_game'])
        if dict_input['Close_game'] == -1:
            self.pairs.append([dict_input["State"],action])
        if dict_input['Close_game'] != -1:
            # if dict_input['Close_game'] == 0:
            #     print(Fore.LIGHTYELLOW_EX + self.name + ' thua')
            if dict_input['Close_game'] == 1:
                # print(Fore.LIGHTYELLOW_EX + self.name + ' thắng')
                with open('/content/TLMN/gym_TLMN/envs/agents/model.json', 'r') as openfile:
                    model = json.load(openfile)
                # print("mô hình",model)
                for id_pair in range(len(self.pairs)):
                    pair = self.pairs[id_pair]
                    state = pair[0]
                    act = pair[1]
                    if id_pair == len(self.pairs) -1:
                        next_state = dict_input["State"]
                    else:
                        next_state = self.pairs[id_pair + 1][0]
                    for id_state in range(len(state)):
                        name_state = str(id_state) + "_" + str(state[id_state])
                        new_state = next_state[id_state]
                        if name_state not in model.keys():
                            model[name_state] = [{} for _ in range(403)]
                        if new_state not in model[name_state][act].keys():
                            model[name_state][act][new_state] = 1
                        else:
                            model[name_state][act][new_state] += 1
                # print("mô hình",model)
                y = json.dumps(model)
                with open("/content/TLMN/gym_TLMN/envs/agents/model.json", "w") as outfile:
                    outfile.write(y)
 
            # print('Dòng lệnh trên và dòng lệnh này được in ra từ agent')
            # print(Style.RESET_ALL)
        return action
 
    
 
 
 
 
 
 
 

