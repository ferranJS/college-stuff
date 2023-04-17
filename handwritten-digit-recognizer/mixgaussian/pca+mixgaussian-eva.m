#!/usr/bin/octave -qf

if (nargin!=4)
printf("Usage: pca+mixgaussi-eva.m <trdata> <trlabels> <tedata> <telabels>\n")
exit(1);
end;

arg_list=argv();
trdata=arg_list{1};
trlabs=arg_list{2};
tedata=arg_list{3};
telabs=arg_list{4};

alphas=[1e-4];
Dim=100;
k=50;

load(trdata);
load(trlabs);
load(tedata);
load(telabs);

%N=rows(X);
%seed=23; rand("seed",seed); permutation=randperm(N);
%X=X(permutation,:); xl=xl(permutation,:);

%Ntr=round(trper/100*N);
%Ndv=round(dvper/100*N);
%Xtr=X(1:Ntr,:); xltr=xl(1:Ntr);
%Xdv=X(N-Ndv+1:N,:); xldv=xl(N-Ndv+1:N);

printf("\ndim   k  dv-err");
printf("\n---  --- -------\n");

%octave pca+mixgaussian-eva.m ../train-images-idx3-ubyte.mat.gz ../train-labels-idx1-ubyte.mat.gz ../t10k-images-idx3-ubyte.mat.gz ../t10k-labels-idx1-ubyte.mat.gz

[m,W]=pca(X);
Xtrp=(X-m)*W(:,1:Dim);
Xdvp=(Y-m)*W(:,1:Dim);
[edv] = mixgaussian(Xtrp,xl,Xdvp,yl,k,alphas(1));
printf("%d  %d  %6.3f\n",Dim,k,edv(1));