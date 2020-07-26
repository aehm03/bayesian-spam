import glob
import random
from math import log, exp
from collections import Counter
from itertools import chain

def main():
  random.seed(44)

  spam_train, spam_test = read_and_split('data/raw/enron1/spam/*')
  ham_train, ham_test = read_and_split('data/raw/enron1/ham/*')
  print(f'ham {len(ham_train)}, {len(ham_test)}. spam {len(spam_train)}, {len(spam_test)}')
  

  all_words = create_features(spam_train, ham_train)
  pi_ham, pi_spam, theta_ham, theta_spam = train(spam_train, ham_train)
  predict(spam_test[0], all_words, pi_ham, pi_spam, theta_ham, theta_spam)

def read_and_split(path):
  train = []
  test = []
  for file in glob.glob(path):
          with open(file, 'r', errors='ignore') as f:
            mail = list(set(f.read().split()))
            if random.random() < .2:
              test.append(mail)
            else:
              train.append(mail)
  return train, test


def create_features(spam_train, ham_train):
  features_ham = set(chain(*ham_train)) 
  features_spam = set(chain(*spam_train))

  final_features = []
  for word in set.union(features_spam, features_ham):
    if (word in features_ham) and (word in features_spam) and (word.isalpha()):
      final_features.append(word)
  return final_features
    


def train(spam, ham):
  n_ham = len(ham)
  n_spam = len(spam)
  
  pi_ham = n_ham / (n_spam + n_ham)
  pi_spam = n_spam / (n_spam + n_ham)
  
  ham_count = count_words(ham)
  spam_count = count_words(spam)
  
  theta_ham = compute_theta(ham_count, spam_count)
  theta_spam  = compute_theta(spam_count, ham_count)

  return pi_ham, pi_spam, theta_ham, theta_spam

def count_words(mails):
  counts = Counter()
  for mail in mails:
    for word in mail:
      counts[word] += 1
  return counts


def compute_theta(words, other):
  theta = Counter()
  for word,count in words.items():
    theta[word] = count / (count + other[word])
  return theta


def predict(mail, all_words, pi_ham, pi_spam, theta_ham, theta_spam):
  pi = {'ham': pi_ham, 'spam': pi_spam}
  theta = {'ham': theta_ham, 'spam': theta_spam}
  p = {}
  li ={}
  for c in ['ham', 'spam']:
    li[c] = log(pi[c])
    for word in all_words:
      if word in mail:
        li[c] += log(theta[c][word])
      else:
        li[c] += log(1 - theta[c][word])
  print(li)  
  print(exp(li['ham'])) 
  for c in ['ham', 'spam']: 
    p[c] = exp(li[c] - log(exp(li['ham']) + exp(li['spam'])) )
  
  print(f'Mail:\n{mail}\n {p}')


if __name__ == '__main__':
  main()