function [P_aux] = filter_data (P)
[lt,~,nj]=size(P);
 P_aux = P;
 for n=1:nj
        for time=3:lt-1
            dist = sqrt((P_aux(time-1,1,n)-P_aux(time,1,n))^2+(P_aux(time-1,2,n)-P_aux(time,2,n))^2);  
            if dist > 15
                P_aux(time,1,n) = P_aux(time-1,1,n);
                P_aux(time,2,n) = P_aux(time-1,2,n);
        end
    end
end
