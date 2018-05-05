function [] = ShowTrace(P,n)
[lt,~,nj]=size(P);
hold on
%
BR=[43.4821194 -1.5383444444444443];
BL_init=[43.4820806 -1.5371083333333333];
TR=[43.4814889 -1.5383499999999999];
TL=[43.4814694 -1.537122222222222];
BL=[0 0];
BR=(BL_init-BR)*pi*6378000/180;
TR=(BL_init-TR)*pi*6378000/180;
TL=(BL_init-TL)*pi*6378000/180;

X=[BL(1),BR(1),TR(1),TL(1),BL(1)];
Y=[BL(2),BR(2),TR(2),TL(2),BL(2)];

plot(X,Y,'black')
plot(P(:,1,n),P(:,2,n))
end
