function [x,y] = plot_joueur(P,num_joueur)

n=num_joueur;
[lt,~,~]=size(P);
t_1=0;
conteur_1=1;
conteur_2=1;

while t_1<lt
    
    for t_2=t_1:lt
        
        if sum(isnan(P(t_2,1:2,n)))==0
            x(conteur_1,conteur_2)=P(t_2,1,n);
            y(conteur_1,conteur_2)=P(t_2,2,n);
            conteur_2=conteur_2+1;
        else
            conteur_1=conteur_1+1;
            t_1=t_2+1;
            break
        end
        
    end
    
end

end

