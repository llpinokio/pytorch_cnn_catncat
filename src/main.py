#!/usr/bin/env python3
from args import get_args
import os
from utils import download_and_extract_zip,get_dataset
import torch
import torch.nn as nn


args=get_args()

if args.gpu and (not torch.cuda.is_available()):
	raise RuntimeError("Cuda is not supported")

if args.dataset==None:
	args.dataset="dataset"
	if not os.path.isdir("dataset"):
		url="https://llpinokio-ia.herokuapp.com/cats.zip"
		print("downloading dataset...")
		download_and_extract_zip(url,args.dataset)

train_imgs,train_labels=get_dataset(args.dataset,"train",shuffle=True)
eval_imgs,eval_labels=get_dataset(args.dataset,"evaluation")

# print(train_imgs[0])
# print(train_imgs.size())
# exit()

model=args.model
no_eval=float(eval_labels.size(0))

if args.gpu:
	model.cuda()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=args.lr)
for epoch in range(args.no_epochs):
	optimizer.zero_grad()
	outputs = model(train_imgs)
	loss = criterion(outputs, train_labels)
	loss.backward()
	optimizer.step()

	outputs = model(eval_imgs)
	_, predicted = torch.max(outputs.data, 1)
	accr=((predicted == eval_labels).sum())/no_eval

	print(f"{epoch} loss:{loss} accr:{accr*100:.2f}%")