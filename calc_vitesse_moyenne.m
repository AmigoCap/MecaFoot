function [vitesse]=calc_vitesse_moyenne(P)

[lt,~,nj]=size(P);
vitesse=zeros([1 lt]);
conteur=1;
for t=1:lt
	conteur=0;
	v=0;
	for n=1:nj
		vitesse(t)=vitesse(t)+P(t,3,n);
		conteur=conteur+1;
	end
	vitesse(t)=vitesse(t)/conteur;
end
end