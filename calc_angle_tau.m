function [tau,angle] = calc_angle_tau(P,t)
[lt,~,nj]=size(P);
points=200;
list=logspace(0,log10((lt-1)/2),points);
angle=zeros([points,1]);
tau=zeros([points,1]);
dt=t(2)-t(1);
        
for m=1:points
           
    dp=round(list(m));
    angle_interim_1=0;
    conteur_1=0;
    if m==1 || dp~=round(list(m-1))       
    for n=1:nj
               
        angle_interim_2=0;
        conteur_2=0;
        conteur_1=conteur_1+1;
               
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
                        
               angle_interim_2=angle_interim_2+abs(acos(dot(dpos1,dpos2)/(norm(dpos1)*norm(dpos2))))/pi;
               conteur_2=conteur_2+1;
            end
            end
        end
               
        angle_interim_1=angle_interim_1+angle_interim_2/conteur_2;

    end        
    angle(m)=angle_interim_1/conteur_1;
    tau(m)=dt*dp;
    disp(m)
    end   

end


