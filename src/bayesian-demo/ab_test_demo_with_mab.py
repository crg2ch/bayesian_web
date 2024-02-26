import numpy as np

from variables import Arm

def thompson_sampling(arms):
   sample = [arm.predict_reward() for arm in arms]
   idx = np.argmax(sample)
   return idx

def monte_carlo_simulation(arms, draw=100):
   k = len(arms)
   p_as = [arm.p_a() for arm in arms]
   p_bs = [arm.p_b() for arm in arms]

   lambda_as = np.array([arm.lambda_a() for arm in arms])
   lambda_bs = np.array([arm.lambda_b() for arm in arms])

   mc_p = np.random.beta(p_as, p_bs, size=(draw, k))
   mc_lambda = np.random.gamma(lambda_as, 1/lambda_bs, size=(draw, k))
   mc = mc_p / mc_lambda

   counts = [0 for _ in range(k)]
   winner_idx = mc.argmax(axis=1)
   for idx in winner_idx:
       counts[idx] += 1
  
   p_winner = [count / draw for count in counts]
   return mc, p_winner

def should_terminate(p_winner, mc, alpha=0.05):
   champion = np.argmax(p_winner)
   values_remaing = (mc.max(axis=1) - mc[:, champion]) / mc[:, champion]
   pctile = np.percentile(values_remaing, q=100 * (1 - alpha))
   return pctile < 0.01

def k_arm_bandit(ctrs, lambdas, alpha=0.05, burn_in=1000, max_iter=100_000, draw=100, silent=False):
   n_arms = len(ctrs)
   arms = [Arm(id=i) for i in range(n_arms)]
   history_p = [[] for _ in range(n_arms)]

   for i in range(max_iter):
       idx = thompson_sampling(arms)
       arm, ctr, lambda_ = arms[idx], ctrs[idx], lambdas[idx]

       if np.random.random() < ctr:
           arm.click()
           t = np.random.exponential(scale=1/lambda_)
           arm.update_lambda(t)
       else:
           arm.no_click()
      
       mc, p_winner = monte_carlo_simulation(arms, draw)
       for j, p in enumerate(p_winner):
           history_p[j].append(p)
      
       predicted_rewards = [arm.predict_reward() for arm in arms]

       if i >= burn_in and should_terminate(p_winner, mc, alpha):
           if not silent:
               print("Terminated at iteration %i"%(i+1))
           break

   traffic = [arm.p_a() + arm.p_b() - 2 for arm in arms]
   return predicted_rewards, history_p, traffic, arms

if __name__=='__main__':
   np.random.seed(1)
   ctrs = [0.3, 0.38, 0.41]
   lambdas = [1/20, 1/20, 1/18]
   predicted_rewards, history_p, traffic, arms = k_arm_bandit(ctrs, lambdas, burn_in=10000, max_iter=1_000_000, alpha=0.0001)

   print('ctrs:', ctrs)
   print('lambdas:', lambdas)
   print('time spent:', np.array(ctrs) / np.array(lambdas))

   for arm in arms:
       p_a, p_b = arm.p_a(), arm.p_b()
       lambda_a, lambda_b = arm.lambda_a(), arm.lambda_b()
       print()
       print('arm id:', arm.id)
       print('p_a:', p_a)
       print('p_b:', p_b)
       print('lambda_a:', lambda_a)
       print('lambda_b:', lambda_b)
       print('expected p:', p_a/(p_a+p_b))
       print('expected lamdba:', lambda_a/lambda_b)
       print('expected time spent:', p_a/(p_a+p_b) * 1/(lambda_a/lambda_b))
  
   import matplotlib.pyplot as plt
   plt.plot(history_p[0], label='AD 0', alpha=0.8)
   plt.plot(history_p[1], label='AD 1', alpha=0.8)
   plt.plot(history_p[2], label='AD 2', alpha=0.8)
   plt.legend()
   plt.title('3-armed bandit experiment')
   plt.ylabel('p_winner')
   plt.xlabel('iteration')
   plt.show()