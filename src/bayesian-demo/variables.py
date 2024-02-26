import numpy as np

class Prior_of_p:
   def __init__(self, a, b):
       self.a = a
       self.b = b
  
   def click(self,):
       self.a += 1

   def no_click(self,):
       self.b += 1
  
   def draw_p(self,):
       return np.random.beta(a=self.a, b=self.b)

class Prior_of_lambda:
   def __init__(self, a, b):
       self.a = a
       self.b = b
  
   def update_lambda(self, t):
       self.a += 1
       self.b += t
  
   def draw_lambda(self,):
       return np.random.gamma(shape=self.a, scale=1/self.b)

class Arm:
   def __init__(self, id, p_a=1, p_b=1, lambda_a=1, lambda_b=1):
       self.id = id
       self.prior_of_p = Prior_of_p(a=p_a, b=p_b)
       self.prior_of_lambda = Prior_of_lambda(a=lambda_a, b=lambda_b)
  
   def p_a(self,):
       return self.prior_of_p.a
  
   def p_b(self,):
       return self.prior_of_p.b
  
   def lambda_a(self,):
       return self.prior_of_lambda.a
  
   def lambda_b(self,):
       return self.prior_of_lambda.b
  
   def click(self,):
       self.prior_of_p.click()
  
   def no_click(self,):
       self.prior_of_p.no_click()
  
   def draw_p(self,):
       return self.prior_of_p.draw_p()
  
   def update_lambda(self, t):
       self.prior_of_lambda.update_lambda(t)
  
   def draw_lambda(self,):
       return self.prior_of_lambda.draw_lambda()
  
   def predict_reward(self,):
       p = self.draw_p()
       lambda_ = self.draw_lambda()
       return p / lambda_