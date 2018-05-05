function [P] = transformation_en_metres(P)

[lt,~,nj]=size(P);
bl=[43.4820806 -1.5371083333333333];

for n=1:nj
    for m=1:lt
        P(m,1:2,n)=abs((P(m,1:2,n)-bl)*pi*6378000/180);
    end
end

end

