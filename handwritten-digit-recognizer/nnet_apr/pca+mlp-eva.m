
#!/usr/bin/octave -qf

if (nargin!=4)
printf("Usage: pca+mlp-eva.m <trdata> <trlabels> <trdataY> <trlabelsY>\n")
exit(1);
end;

arg_list=argv();
trdata=arg_list{1};
trlabs=arg_list{2};
nHiddens=30;
k=20;
trdatay=arg_list{3};
trlabelsy=arg_list{4};

load(trdata);
load(trlabs);
load(trdatay);
load(trlabelsy);

%N=rows(X);
%seed=23; rand("seed",seed); permutation=randperm(N);
%X=X(permutation,:); xl=xl(permutation,:);

%Ntr=round(trper/100*N);
%Ndv=round(dvper/100*N);
%Xtr=X(1:Ntr,:); xltr=xl(1:Ntr);
%Xdv=X(N-Ndv+1:N,:); xldv=xl(N-Ndv+1:N);

% octave pca+mlp-eva.m ../train-images-idx3-ubyte.mat.gz ../train-labels-idx1-ubyte.mat.gz ../t10k-images-idx3-ubyte.mat.gz ../t10k-labels-idx1-ubyte.mat.gz

printf("\n  alpha dv-err");
printf("\n------- ------\n");
show=10;
seed=300;
epochs=300;
[m,W]=pca(X);
Xtrp=(X-m)*W(:,1:k);
Xdvp=(Y-m)*W(:,1:k);
edv = mlp(Xtrp,xl,Xdvp,yl,Y,yl,nHiddens,epochs,show,seed);
printf("%3d %6.3f\n",nHiddens,edv);
