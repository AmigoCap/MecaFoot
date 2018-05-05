function [] = ShowGame(P)
[lt,~,nj]=size(P);
BR=[43.48209284184595 -1.538339432868406];
BL_init=[43.48211003528411 -1.537103401773021];
TR=[43.48185372025666 -1.53800087855859];
TL=[43.48185372025666 -1.53800087855859];
BL=[0 0];
BR=(BR-BL_init)*pi*6378000/180;
TR=(TR-BL_init)*pi*6378000/180;
TL=(TL-BL_init)*pi*6378000/180;

X=[BL(1),BR(1),TR(1),TL(1),BL(1)];
Y=[BL(2),BR(2),TR(2),TL(2),BL(2)];

    for time=1:lt 
            hold on
        	plot(X,Y,'black')
            plot(reshape(P(time,1,:),[nj 1]),reshape(P(time,2,:),[nj 1]),'.');
            axis([0 70 0 200])
            pause(0.01)
    end
end
