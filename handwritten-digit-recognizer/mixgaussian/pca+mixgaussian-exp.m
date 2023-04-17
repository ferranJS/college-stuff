#!/usr/bin/octave -qf

if (nargin!=7)
printf("Usage: pca+mixgaussian-exp.m <trdata> <trlabels> <alphas> <Dim> <ks> <%%trper> <%%dvper>\n")
exit(1);
end;

arg_list=argv();
trdata=arg_list{1};
trlabs=arg_list{2};
alphas=str2num(arg_list{3});
Dim=str2num(arg_list{4});
ks=str2num(arg_list{5});
trper=str2num(arg_list{6});
dvper=str2num(arg_list{7});

load(trdata);
load(trlabs);

N=rows(X);
seed=23; rand("seed",seed); permutation=randperm(N);
X=X(permutation,:); xl=xl(permutation,:);

Ntr=round(trper/100*N);
Ndv=round(dvper/100*N);
Xtr=X(1:Ntr,:); xltr=xl(1:Ntr);
Xdv=X(N-Ndv+1:N,:); xldv=xl(N-Ndv+1:N);

printf("\ndim   ks  dv-err");
printf("\n---  --- -------\n");

%octave pca+mixgaussian-exp.m ../train-images-idx3-ubyte.mat.gz ../train-labels-idx1-ubyte.mat.gz "[1e-4]" "[1 2 5 10 20 50 100]" "[1 2 5 10 20 50 100]" 90 10

[m,W]=pca(Xtr);
for j=Dim    % dimensiones de pca
  Xtrp=(Xtr-m)*W(:,1:j);
  Xdvp=(Xdv-m)*W(:,1:j);
  for i=1:length(alphas)   % solo usamos un valor elegido por conveniencia
  	for k=1:length(ks)    % ks
      [edv] = mixgaussian(Xtrp,xltr,Xdvp,xldv,ks(k),alphas(i)); 
      printf(" %d   %d    %6.3f\n",j,ks(k),edv(i));
    end
  end
end
