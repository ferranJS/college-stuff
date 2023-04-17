
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Conjunto linealmente separable %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load ../data/mini/tr.dat
load ../data/mini/trlabels.dat

res = svmtrain(xl, X, '-t 0 -c 1000');
theta = res.sv_coef' * res.SVs
%Usando X1
theta0 = sign(res.sv_coef(1)) - theta * res.SVs(1,:)'
margen = 2 / norm(theta)
tolerancia = 1 - (sign(res.sv_coef)'.*(theta*X(res.sv_indices,:)' + theta0));
tolerancia = round(100*tolerancia)/100;

x1  = [0:7];
x2  = - theta(1)/theta(2)*x1 - theta0/theta(2);
x21 = - theta(1)/theta(2)*x1 - (theta0 - 1 )/theta(2);
x22 = - theta(1)/theta(2)*x1 - (theta0 + 1) /theta(2);

plot(X(xl==1,1), X(xl==1,2), "sr", X(xl==2,1), X(xl==2,2), "ob", res.SVs(:,1), res.SVs(:,2), "xk", x1, x2, -"k");
hold on
plot(x1, x21, -"k");
hold on
plot(x1, x22, -"k");

aux = X(res.sv_indices,:);
text(aux(1,1) + 0.1,aux(1,2), mat2str(tolerancia(1)));
text(aux(2,1) + 0.1,aux(2,2), mat2str(tolerancia(2)));
text(aux(3,1) + 0.1,aux(3,2), mat2str(tolerancia(3)));
text(aux(4,1) + 0.1,aux(4,2), mat2str(tolerancia(4)));
text(aux(5,1) + 0.1,aux(5,2), mat2str(tolerancia(5)));
text(X(2,1) + 0.1 ,X(2,2), "0");
text(X(3,1) + 0.1 ,X(3,2), "0");
text(X(6,1) + 0.1 ,X(6,2), "0");
text(X(7,1) + 0.1 ,X(7,2), "0");
text(X(8,1) + 0.1 ,X(8,2), "0");
axis([0 7 0 7]);

disp ("-------------------------------------\nPulsa cualquier tecla para terminar la ejecución")
b = waitforbuttonpress ()
