function [a_fin,b_fin,c_fin,err] = find_shape(Area,Dist_Area)
pas=1;
n_max=100;
a_min=-5;
a_max=5;
b_min=-5;
b_max=5;
c_min=-5;
c_max=5;
error_exponent=2;

crit1=sum(abs(Dist_Area).^error_exponent);

for n=1:n_max
    clc
    disp([int2str(n/n_max*100) '%'])
for a=a_min:pas:a_max
   for b=b_min:pas:b_max
       for c=c_min:pas:c_max
               test=c*(b^(a/c))/gamma(a/c).*Area.^(a-1).*exp(-b*Area.^c);
               plot(Area,test,'r',Area,Dist_Area,'b')
               axis([0 3 0 2.5])
               pause(0.000000000000001)
               crit2=sum(abs(Dist_Area-test).^error_exponent);
               if crit1>crit2
                   crit1=crit2;
                   a_fin=a;
                   b_fin=b;
                   c_fin=c;
               end
       end
   end

end
a_min=a_fin-pas;
a_max=a_fin+pas;
b_min=b_fin-pas;
b_max=b_fin+pas;
c_min=c_fin-pas;
c_max=c_fin+pas;
pas=pas/2;
end
   test=c*(b_fin^(a_fin/c_fin))/gamma(a_fin/c_fin).*Area.^(a_fin-1).*exp(-b_fin*Area.^c_fin);
   test=test/trapz(Area,test);
   plot(Area,test,'r',Area,Dist_Area,'b')
   axis([0 3 0 2.5])
   err=mean(abs(Dist_Area-test));
end

