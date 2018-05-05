function [acceleration]=calc_acceleration_moyenne(P)

[lt,~,nj]=size(P);
acceleration=zeros([1 lt]);
conteur=1;
for t=1:lt
	conteur=0;
	v=0;
	for n=1:nj
		acceleration(t)=acceleration(t)+P(t,4,n);
		conteur=conteur+1;
	end
	acceleration(t)=acceleration(t)/conteur;
end
end