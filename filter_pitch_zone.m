function [P_aux1,P_aux2,P_aux3,P_aux4] = filter_pitch_zone(P)
[lt,~,nj]=size(P);
P_aux1=zeros(size(P));
P_aux2=zeros(size(P));
P_aux3=zeros(size(P));
P_aux4=zeros(size(P));
P_aux5=zeros(size(P));
disp("Début Filtrage par Zone");
    for n=1:nj
        for time=1:lt 
            if ((P(time,1,n) < 15) || (P(time,1,n) > 55))
                P_aux1(time,:,n) = P(time,:,n);   
            else
                P_aux1(time,:,n) = nan;
            end
            if ((P(time,1,n) < 40) && (P(time,1,n) > 20))
                P_aux2(time,:,n) = P(time,:,n); 
            else
                P_aux2(time,:,n) = nan;
            end
            if ((P(time,2,n) < 40) || (P(time,2,n) > 100))
                P_aux3(time,:,n) = P(time,:,n);
            else
                P_aux3(time,:,n) = nan;
            end
            if ((P(time,2,n) < 90) && (P(time,2,n) > 50))
                P_aux4(time,:,n) = P(time,:,n);
            else
                P_aux4(time,:,n) = nan;
            end  
            if (((P(time,2,n)<40) && (P(time,1,n)<15 || P(time,1,n)>55) )|| (((P(time,2,n)>100) && ((P(time,1,n)<15) || P(time,1,n)>55))))
                P_aux5(time,:,n) = P(time,:,n);
            else
                P_aux5(time,:,n) = nan;
            end  
        end
        disp(floor(n/nj*100));
    end
    disp ("Filtrage réalisé correctement");
end
