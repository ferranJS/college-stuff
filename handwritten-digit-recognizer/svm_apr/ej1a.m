
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

x1 = [0:7];
x2 = - theta(1)/theta(2)*x1 - theta0/theta(2);
x21= - theta(1)/theta(2)*x1 - (theta0 - 1 )/theta(2);
x22= - theta(1)/theta(2)*x1 - (theta0 + 1) /theta(2);

plot(X(xl==1,1), X(xl==1,2), "sr", X(xl==2,1), X(xl==2,2), "ob", res.SVs(:,1), res.SVs(:,2), "xk", x1, x2, -"k");
hold on
plot(x1, x21, -"k");
hold on
plot(x1, x22, -"k");

axis([0 7 0 7]);

disp ("-------------------------------------\nPulsa cualquier tecla para terminar la ejecución")
b = waitforbuttonpress ()
