function [pdf_real,area_real,pdf_sim,area_sim]=voronoi_own(P_m)
[lt,~,nj]=size(P_m);
BL=[43.4820806 -1.5371083333333333];
TR= abs(([43.4814889 -1.5383499999999999]-BL)*pi*6378000/180);

tot_area=abs((BL(1)-TR(1))*(BL(2)-TR(2)));
area=ones([1 1]);
max_x=TR(1);
max_y=TR(2);
dt=1;
conteur=1;
areas=1:3;
for time=1:dt:lt
    
    clc
    disp(time/lt*50)
    
    x=zeros([nj,2]);
    
    for n=1:nj
       
        x(n,:)=P_m(time,1:2,n);
        
    end
    try
    [V,C]=voronoin(x);
    
    for cell=1:length(C)
        
        valable=1;
        points=zeros([length(C{cell}),2]);
        
        for point=1:length(C{cell})
            
            if V(C{cell}(point))<Inf
                points(point,:)=V(C{cell}(point),:);
            else
                valable=0;
                break
            end
            
        end
        
        if valable==1
            try
            [~,area_interim]=convhull(points);
            if area_interim~=0
                area(conteur)=area_interim/tot_area;
                conteur=conteur+1;
            end
            end
        end
        
    end
	end
    
end

mean_area=tot_area/nj;
max_affich=median(area)*5;
[a,b]=histcounts(area,'BinWidth',max_affich/1000,'BinLimits',[0 max_affich]);
[c,d]=random_players(lt/dt,nj,max_x,max_y);
a=a/sum(a);
f=abs(trapz(a,b(2:length(b))*tot_area/mean_area));

plot(b(2:length(b))*tot_area/mean_area,a/f,'blue',c,d,'red')
xlabel('area / area_m_e_a_n')
ylabel('PDF')

area_real=b(2:length(b))*tot_area/mean_area;
pdf_real=a/f;
area_sim=c;
pdf_sim=d;

end