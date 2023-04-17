#!/usr/bin/octave -qf

if (nargin!=9)
printf("Usage: svm-exp.m <trdata> <trlabels> <C> <T> <D> <G> <Dim> <%%trper> <%%dvper>\n")
exit(1);
end;

arg_list=argv();
trdata=arg_list{1};
trlabs=arg_list{2};
C=str2num(arg_list{3});
T=str2num(arg_list{4});
D=str2num(arg_list{5});
G=str2num(arg_list{6});
Dim=str2num(arg_list{7});
trper=str2num(arg_list{8});
dvper=str2num(arg_list{9});

load(trdata);
load(trlabs);

N=rows(X);
seed=23; rand("seed",seed); permutation=randperm(N);
X=X(permutation,:); xl=xl(permutation,:);

Ntr=round(trper/100*N);
Ndv=round(dvper/100*N);
Xtr=X(1:Ntr,:); xltr=xl(1:Ntr);
Xdv=X(N-Ndv+1:N,:); xldv=xl(N-Ndv+1:N);

Xtr = Xtr/255;
Xdv = Xdv/255;

% octave pca+svm-exp.m ../train-images-idx3-ubyte.mat.gz ../train-labels-idx1-ubyte.mat.gz "[1 10 100]" "[0 1 2 3]" "[1 2 3 4 5]" "[1e-1 1e-2 1e-3 1e-4 1e-5]" "[50 100 200]" 9 1
% si t==1 -> -d 1,2,3,4,5,... |  si t==2,3 -> -g 1e-1, 1e-2, 1e-3, 1e-4, 1e-5,...
% PCA 50 100 200
% En el caso de SVM, es imprescindible normalizar los datos dividiendo por su valor maximo.

[m,W]=pca(Xtr);
for j=Dim
    Xtrp=(Xtr-m)*W(:,1:j);
    Xdvp=(Xdv-m)*W(:,1:j);
    for c=C
        for t=T
            if ( t==1 )
                printf("\n dim   c    t     d    dv-err");
                printf("\n----  ---  ---   ---  -------\n");
                for d=D
                    ar = ['-t ',num2str(t), ' -c ',num2str(c), ' -d ',num2str(d),' -q'];
                    svm = svmtrain(xltr,Xtrp,ar);
                    cl = svmpredict(xldv,Xdvp,svm,'-q');
                    edv = 1-mean(cl == xldv);
                    printf(" %d     %d   %d   %d   %6.3f\n",j,c,t,d,edv);
                endfor
            else 
                if ( t==3 || t==2 )
                    printf("\n dim   c    t     g    dv-err");
                    printf("\n----  ---  ---   ---  -------\n");
                    for g=G
                        ar = ['-t ',num2str(t), ' -c ',num2str(c), ' -g ',num2str(g),' -q'];
                        svm = svmtrain(xltr,Xtrp,ar);
                        cl = svmpredict(xldv,Xdvp,svm,'-q');
                        edv = 1-mean(cl == xldv);
                        printf(" %d     %d   %d   %d   %6.3f\n",j,c,t,g,edv);
                    endfor
                else
                    printf("\n dim   c    t    dv-err");
                    printf("\n----  ---  ---  -------\n");
                    ar = ['-t ',num2str(t), ' -c ',num2str(c),' -q'];
                    svm = svmtrain(xltr,Xtrp,ar);
                    cl = svmpredict(xldv,Xdvp,svm,'-q');
                    edv = 1-mean(cl == xldv);
                    printf(" %d     %d   %d   %6.3f\n",j,c,t,edv);
                endif
            endif
        endfor
    endfor
endfor
