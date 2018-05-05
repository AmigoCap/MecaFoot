function [phi,angles_disp] = calc_angle_proba(P)
[lt,~,nj]=size(P);
courbes=5;
list=logspace(0,log10((lt-1)/1000),courbes);
phi=zeros([courbes 315]);
        
for m=1:courbes
    angle=0;
    conteur=1;      
    dp=round(list(m));
    if m==1 || dp~=round(list(m-1))       
    for n=1:nj    
        for time=1:(lt-2*dp)
            a=0;
            for p=time:time+2*dp
                if isnan(P(p,1,n))
                    a=1;
                    break
                end
            end
            if a==0
            pos1=P(time,1:2,n);
            pos2=P(time+dp,1:2,n);
            pos3=P(time+2*dp,1:2,n);
                   
            dpos1=pos2-pos1;
            dpos2=pos3-pos2;
                   
                if (sum(pos1~=pos2)~=0)&&(sum(pos2~=pos3)~=0)&&(sum(pos1~=pos3)~=0)
                        
                    angle(conteur)=abs(acos(dot(dpos1,dpos2)/(norm(dpos1)*norm(dpos2))));
                    conteur=conteur+1;
                end
            end
        end
    end
   
    [a,b]=histcounts(angle,'BinWidth',0.01,'BinLimits',[0 pi]);
    f=abs(trapz(a,b(2:316)/pi));
    phi(m,:)=a/f;
    clc
    disp(m)
    end  
    angles_disp=b(2:316)/pi;
end
