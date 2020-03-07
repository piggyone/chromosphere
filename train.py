#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/3/7 13:37
# @Author: Jtyoui@qq.com
"""训练数据"""
from pyunit_log import Log
import doublechromosphere
import torch
import logging

Log().log_config()

print('爬取双色球数据')
data_all = doublechromosphere.double_data_chart()
print('爬取完毕')
length = len(data_all)
data = torch.tensor(data=[data[1:] for data in data_all[1:]], dtype=torch.float32)
normalization = data / 33  # 归一化


class Net(torch.nn.Module):
    def __init__(self, input_size, hidden_size, out_features):
        super(Net, self).__init__()
        self.rnn = torch.nn.LSTM(input_size=input_size, hidden_size=hidden_size)
        self.fc = torch.nn.Linear(in_features=hidden_size, out_features=out_features)

    def forward(self, x):
        x = x.unsqueeze(dim=-1)
        x, _ = self.rnn(x)
        x = self.fc(x)
        x = x.squeeze()
        return x


net = Net(input_size=1, hidden_size=5, out_features=1)
train_len, test_len = round(length * 0.9), round(length * 0.1)
print(f'总数据：{length},训练数据：{train_len},测试数据：{test_len}')
inputs = torch.clone(normalization[:-1])
labels = torch.clone(normalization[1:])
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(params=net.parameters())
for step in range(5001):
    pred = net(inputs)
    train_pred = pred[:train_len]
    train_label = labels[:train_len]
    train_loss = criterion(train_pred, train_label)
    optimizer.zero_grad()
    train_loss.backward()
    optimizer.step()

    test_pred = pred[-test_len:]
    test_label = labels[-test_len:]
    test_loss = criterion(test_pred, test_label)

    logging.info(f'训练步骤：{step},训练损失值：{train_loss},测试损失值:{test_loss}')
    logging.info(train_pred * 33)
    logging.info(test_pred * 33)
