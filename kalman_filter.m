function [P] = kalman_filter(P,t)

[lt,~,nj]=size(P);

for n=1:nj
   
    pos_x=P(:,1,n);
    pos_y=P(:,2,n);
    vel_x=zeros(size(pos_x));
    vel_y=zeros(size(pos_y));
    acc_x=zeros(size(pos_x));
    acc_y=zeros(size(pos_y));
    
    dt=t(2)-t(1);
    vel_x(1)=(pos_x(2)-pos_x(1))/dt;
    vel_y(1)=(pos_y(2)-pos_y(1))/dt;
    for time=2:lt-1
        vel_x(time)=(pos_x(time+1)-pos_x(time-1))/(2*dt);
        vel_y(time)=(pos_y(time+1)-pos_y(time-1))/(2*dt);
    end
    vel_x(lt)=(pos_x(lt)-pos_x(lt-1))/dt;
    vel_y(lt)=(pos_y(lt)-pos_y(lt-1))/dt;
    
    
    acc_x(1)=(vel_x(2)-vel_x(1))/dt;
    acc_y(1)=(vel_y(2)-vel_y(1))/dt;
    for time=2:lt-1
        acc_x(time)=(vel_x(time+1)-vel_x(time-1))/(2*dt);
        acc_y(time)=(vel_y(time+1)-vel_y(time-1))/(2*dt);
    end
    acc_x(lt)=(vel_x(lt)-vel_x(lt-1))/dt;
    acc_y(lt)=(vel_y(lt)-vel_y(lt-1))/dt;
    
    A=0;
   
    B1=dt;
    B2=(dt^2)/2;
   
    C=1;
  
    Plant=ss(A,[B1 B2 1],C,0,-1,'inputname',{'v','a','bruit'},'outputname','y');
  
    Q=1;
    R=1;
    
    [kalmf,~,~,~]=kalman(Plant,Q,R);
  
    kalmf = kalmf(1,:);
    
    U_x=[vel_x';acc_x';pos_x']';
    U_y=[vel_y';acc_y';pos_y']';
    T=0:lt-1;
    
    [out_x,~] = lsim(kalmf,U_x,T);
    [out_y,~] = lsim(kalmf,U_y,T);
    
    P(:,1,n)=out_x;
    P(:,2,n)=out_y;

end 
    
end
