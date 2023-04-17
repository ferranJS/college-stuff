#!/usr/bin/octave -qf

if (nargin!=4)
printf("Usage: pca+svm-eva.m <trdata> <trlabels> <tedata> <telabels>\n")
exit(1);
end;

arg_list=argv();
trdata=arg_list{1};
trlabs=arg_list{2};
tedata=arg_list{3};
telabs=arg_list{4};

c = 100;
t = 2;
g = 0.01;
Dim = 100;

load(trdata);
load(trlabs);
load(tedata);
load(telabs);

Xtr = X/255;
Xdv = Y/255;

% octave pca+svm-eva.m ../train-images-idx3-ubyte.mat.gz ../train-labels-idx1-ubyte.mat.gz ../t10k-images-idx3-ubyte.mat.gz ../t10k-labels-idx1-ubyte.mat.gz

[m,W]=pca(Xtr);
Xtrp=(Xtr-m)*W(:,1:Dim);
Xdvp=(Xdv-m)*W(:,1:Dim);
ar = ['-t ',num2str(t), ' -c ',num2str(c), ' -g ',num2str(g),' -q'];
svm = svmtrain(xl,Xtrp,ar);
cl = svmpredict(yl,Xdvp,svm,'-q');
edv = 1-mean(cl == yl);
printf("Error: %6.5f\n",edv);
