import numpy as np
import pandas as pd

class ItemManager:
   def __init__(self, file_path):
       self.file_path = file_path
       self.items = self._create_items()
  
   def _create_items(self):
       df = pd.read_csv(self.file_path, sep='\t')
       df['p_a'] = 1
       df['p_b'] = 1
       df['lambda_a'] = 1
       df['lambda_b'] = 1

       items = {}
       for _, row in df.iterrows():
           items[row['video_id']] = row.to_dict()
       return items

   def update_score(self):
       for value in self.items.values():
           p_a = value['p_a']
           p_b = value['p_b']
           lambda_a = value['lambda_a']
           lambda_b = value['lambda_b']


           p = np.random.beta(p_a, p_b)
           lambda_ = np.random.gamma(shape=lambda_a, scale=1/lambda_b)
           predicted_time_spent = p/lambda_
           value['score'] = predicted_time_spent
  
   def get_sorted_items(self):
       return sorted(self.items.values(), key=lambda x: x["score"], reverse=True)
  
   def update_lambda(self, video_id, time_spent):
       item = self.items[video_id]
       item['lambda_a'] += 1
       item['lambda_b'] += min(time_spent, 10_000)
       return item['lambda_a'], item['lambda_b']
  
   def update_p_parameters(self, impressed_video_ids, video_id):
       for impressed_video_id in impressed_video_ids:
           if impressed_video_id == video_id:
               self.items[impressed_video_id]['p_a'] += 1
           else:
               self.items[impressed_video_id]['p_b'] += 1
  
   def show_current_state(self, video_id=None):
       if video_id is not None:
           return self.items.get(video_id, {})
       else:
           return self.items