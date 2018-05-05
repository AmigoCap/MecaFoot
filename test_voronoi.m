[lt,~,nj]=size(P_m);
BL1=[43.4820806 -1.5371083333333333];
BL= abs(([43.4820806 -1.5371083333333333]-BL1)*pi*6378000/180);
BR= abs(([43.4821194 -1.5383444444444443]-BL1)*pi*6378000/180);
TR= abs(([43.4814889 -1.5383499999999999]-BL1)*pi*6378000/180);
TL= abs(([43.4814694 -1.537122222222222]-BL1)*pi*6378000/180);
Liste_surfaces=zeros([1 2]);
conteur=1;
for t=1:lt
    X=zeros([nj 2]);
    for n=1:nj        
        X(n,1)=P_m(t,1,n);
        X(n,2)=P_m(t,2,n);        
    end
    
    [V,C]=voronoin(X);
    [num_cells,~]=size(C);
    for n=1:num_cells
        num_points=length(C{n});
        points=zeros([num_points,2]);
        for m1=1:num_points
            m2=C{n}(m1);
            points(m1,:)=V(m2,:);
        end
        if sum(sum(points))<Inf
            points=convhull(points);
            area=polyarea(points);
            if isnan(area)
               Liste_surfaces(1,conteur)=area;
               conteur=conteur+1;
            end
            clear points
        end
    end
end