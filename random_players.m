function [area,proba] = random_players(lt,nj,max_x,max_y)

conteur2=1;

for t=1:lt
    clc
    disp(t/lt*50+50)
   
Test_rand=rand([nj 2]);
Test_rand(:,1)=Test_rand(:,1)*max_x;
Test_rand(:,2)=Test_rand(:,2)*max_y;
tot_area=max_x*max_y;

[V_rand,C_rand]=voronoin(Test_rand);


for cell=1:length(C_rand)
        
        valable=1;
        points=zeros([length(C_rand{cell}),2]);
        
        for point=1:length(C_rand{cell})
            
            if V_rand(C_rand{cell}(point))<Inf
                points(point,:)=V_rand(C_rand{cell}(point),:);
            else
                valable=0;
                break
            end
            
        end
        
        if valable==1
            try
            [~,area_interim]=convhull(points);
            if area_interim~=0
                area_rand(conteur2)=area_interim/tot_area;
                conteur2=conteur2+1;
            end
            end
        end
        
end

    
end

max_affich=median(area_rand)*5;
mean_area=tot_area/nj;   
[c,d]=histcounts(area_rand,'BinWidth',max_affich/1000,'BinLimits',[0 max_affich]);

area=d(2:length(d))*tot_area/mean_area;
proba=c/sum(c);

f=abs(trapz(proba,area));

proba=proba/f;
end

