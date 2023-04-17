#!/usr/bin/octave -qf

if (nargin!=6)
printf("Usage: pca+mlp-exp.m <trdata> <trlabels> <nHiddens> <ks> <%%trper> <%%dvper>\n")
exit(1);
end;

arg_list=argv();
trdata=arg_list{1};
trlabs=arg_list{2};
nHiddens=str2num(arg_list{3});
ks=str2num(arg_list{4});
trper=str2num(arg_list{5});
dvper=str2num(arg_list{6});

load(trdata);
load(trlabs);

N=rows(X);
seed=23; rand("seed",seed); permutation=randperm(N);
X=X(permutation,:); xl=xl(permutation,:);

Ntr=round(trper/100*N);
Ndv=round(dvper/100*N);
Xtr=X(1:Ntr,:); xltr=xl(1:Ntr);
Xdv=X(N-Ndv+1:N,:); xldv=xl(N-Ndv+1:N);

% octave pca+mlp-exp.m ../train-images-idx3-ubyte.mat.gz ../train-labels-idx1-ubyte.mat.gz "[1 2 5 10 20 30 40 50]" "[1 2 5 10 20 30]" 40 10

printf("\n alpha   dv-err");
printf("\n------  -------\n");
show=10;
seed=300;
epochs=300;
yl=xldv;
[m,W]=pca(Xtr);
for j=ks
    Xtrp=(Xtr-m)*W(:,1:j);
    Xdvp=(Xdv-m)*W(:,1:j);
	Y=Xdvp;
	for i=1:length(nHiddens)
		edv = mlp(Xtrp,xltr,Xdvp,xldv,Y, yl,nHiddens(i),epochs,show,seed);
		printf("%3d %6.3f\n",nHiddens(i),edv);
	end
end
