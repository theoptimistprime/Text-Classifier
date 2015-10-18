# -*- coding: utf-8 -*-

import numpy as np
from learner import Learner

class Gaussian(Learner):
    
    def __init__(self, train_X, train_Y, c_ratio):
        super(Gaussian, self).__init__(train_X, train_Y, c_ratio)
        
        self.class_label = np.unique(np.array(self.y))
        self.classes     = np.arange(len(self.class_label))
        self.n_class     = len(self.classes)
        
        self.mu      = []
        self.sigma   = []
        
        self.class_prob = []
        
    def calc_log_likelihood(self, x):
        log_likelihood = []
        for class_i in range(np.size(self.classes)):
            prob = -0.5 * np.sum((np.array((x-self.mu[class_i])) ** 2) / 
                                         (self.sigma[class_i]), 1) #cofirm this gaussian definition
            prob -= 0.5 * np.sum(np.log(2 * np.pi * self.sigma[class_i]))
            
            prob += np.log(self.class_prob[class_i])
            
            log_likelihood.append(prob)
        
        log_likelihood = np.array(log_likelihood).T
        return log_likelihood
        
    def learn(self, x, y, c_valid = False):
        if(c_valid == False):
            print('Actual learning (not cross validation.',
                  'Using self.x and self.y')
            x = self.x
            y = self.y
        
        n = x.shape[0]
        m = x.shape[1]
        
        self.class_label = np.unique(np.array(y))
        self.classes     = np.arange(len(self.class_label))
        self.n_class     = len(self.classes)
        
        self.mu         = np.zeros((self.n_class, m))
        self.sigma      = np.ones((self.n_class, m))

        self.class_prob = np.zeros(self.n_class)
        
        for class_i in self.classes:
            x_feat = self.get_subset(x, y, class_i)
            
            self.mu[class_i, :] = np.mean(x_feat, axis = 0)
            self.sigma[class_i, :] = np.std(x_feat, axis = 0)
            
            self.class_prob[class_i] = x_feat.shape[0]/n
            
        self.sigma[:, :] += (10**(-5)) * np.var(x, axis = 0).max()
        
    def predict(self, x):
        temp = x        
        x = np.ones([x.shape[0], x.shape[1]+1])
        x[:, 1:] = temp
        prob = self.calc_log_likelihood(x)
        return self.class_label[self.classes[np.argmax(prob, axis = 1)]]
     
    def get_subset(self, x, y, class_i):
        res = []
        x = np.array(x)
        y = np.array(y)
        
        for i in range(y.shape[0]):
            if y[i, 0] == self.class_label[class_i]:
                res.append(x[i, :])
        return np.matrix(res)
        
    def tester(self):
        x = np.matrix([[1, 2], [3, 4], [1, 2], [3, 4]])
        n = np.matrix([1, 0, 1, 0]).T
        
        self.learn(x, n)
        print(self.predict(x))
        
if __name__=='__main__':
    x = np.matrix([[1, 2], [3, 4], [1, 2], [3, 4]])
    n = np.array(['asdas', 'sds', 'asdas', 'sds']).T
    
    print(x.shape)
    print(n.shape)
    
    
    lr = Gaussian(x, n, 0.25)
    lr.tester()
#    lr.learn(x, n)
#    print('predict')
#    print(lr.predict(x))
    
