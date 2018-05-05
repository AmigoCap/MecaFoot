function [P_aux1,P_aux2,P_aux3,P_aux4] = filter_time_stamp(P)
[lt,~,nj]=size(P);
P_aux1=zeros(size(P));
P_aux2=zeros(size(P));
P_aux3=zeros(size(P));
P_aux4=zeros(size(P));

disp("Début Filtrage par Temps");
    for n=1:nj
        for time=1:lt 
            if (time < lt/4)
                P_aux1(time,:,n) = P(time,:,n);   
            else
                P_aux1(time,:,n) = nan;
            end
            if (time > lt/4) && (time < lt/2)
                P_aux2(time,:,n) = P(time,:,n); 
            else
                P_aux2(time,:,n) = nan;
            end
            if (time > lt/2) && (time < 3*lt/4)
                P_aux3(time,:,n) = P(time,:,n);
            else
                P_aux3(time,:,n) = nan;
            end
            if (time > 3*lt/4)
                P_aux4(time,:,n) = P(time,:,n);
            else
                P_aux4(time,:,n) = nan;
            end
        end
        disp(n/nj*100);
    end
    disp("Filtrage réalisé correctement");
end
