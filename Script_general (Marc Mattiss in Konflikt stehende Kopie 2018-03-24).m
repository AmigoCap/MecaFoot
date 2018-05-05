%% load
clear all
clc
load('Match_1');
P_m=transformation_en_metres(P);
P_m_filtered=filter_data(P_m);

%% distribution de probabilité d'angles

figure
[a,b]=calc_angle_proba(P_m_filtered);
semilogy(b,a)
xlabel('angle/pi')
ylabel('probabilité')
title('Distribution de probabilité des angles')
legend1=['tau = ';'tau = ';'tau = ';'tau = ';'tau = '];
legend2=num2str(round(logspace(0,log10((length(t)-1)/1000),5)'*(t(2)-t(1)),2));
legend3=['s';'s';'s';'s';'s'];
legend_tot=[legend1 legend2 legend3];
legend(legend_tot);

%% Angle tau

figure
[tau,phi]=calc_angle_tau(P_m,t);
loglog(tau,phi,'.')
xlabel('tau')
ylabel('angle/pi')
title('Angles en fonction de dt')


%% Cascade énergétique

figure
[frequ, ener]=energy_cascade(P_m);
loglog(frequ,ener)
xlabel('w / [1/s]')
ylabel('Energy_e_q_u / [m^2/s^2]')
title('Energy cascade')

%% Comparaison Voronoi

[pdf_real_tot,area_real_tot,pdf_sim_tot,area_sim_tot]=voronoi_own(P_m);

semilogx(b_part,a_part,d_part_sim,c_part_sim,area_real_tot,pdf_real_tot,area_sim_tot,pdf_sim_tot)


%% Shape Voronoi

figure

lambda=poissfit(pdf_real_tot);
poisson_pdf=poisspdf(area_real_tot,lambda);
semilogx(area_real_tot,pdf_real_tot,area_real_tot,f(area_real_tot));

figure

normalized_pdf=-log(pdf_real_tot/(factorial(round(area_real_tot))/lambda.^area_real_tot))/lambda-1;
plot(area_real_tot,normalized_pdf)

%% Calcul espaces de Voronoi selon la zone

[P_aux1,P_aux2,P_aux3,P_aux4,P_aux5] = filter_pitch_zone(P_m);
clc;
disp("Calcule Zone 1");
[pdf_real1,area_real1,pdf_sim,area_sim]=voronoi_own(P_aux1)
clc;
disp("Calcule Zone 2");
[pdf_real2,area_real2,~,~]=voronoi_own(P_aux2)
clc;
disp("Calcule Zone 3");
[pdf_real3,area_real3,~,~]=voronoi_own(P_aux3)
clc;
disp("Calcule Zone 4");
[pdf_real4,area_real4,~,~]=voronoi_own(P_aux4)
figure
f=figure;
semilogx(area_real1,pdf_real1,'.','b',area_real2,pdf_real2,'.','r',area_real3,pdf_real3,'.','g',area_real4,pdf_real4,'.','b',area_sim,pdf_sim,'y')
xlabel('area / area_m_e_a_n')
ylabel('PDF')
title('Espaces de Voronoi (Filtrage par Zone)');
legend('Zone 1','Zone 2','Zone 3','Zone 4','Théorique');
savefig('voronoi_match_1_zone.fig');
saveas(f,'voronoi_match_1_zone_bis.png');

%% Calcul espaces de Voronoi selon le temps de jeu

[P_aux1,P_aux2,P_aux3,P_aux4] = filter_time_stamp(P_m);
clc
disp("Calcule Temps 1");
[pdf_real1,area_real1,pdf_sim,area_sim]=voronoi_own(P_aux1)
clc;
disp("Calcule Temps 2");
[pdf_real2,area_real2,~,~]=voronoi_own(P_aux2)
clc;
disp("Calcule Temps 3");
[pdf_real3,area_real3,~,~]=voronoi_own(P_aux3)
clc;
disp("Calcule Temps 4");
[pdf_real4,area_real4,~,~]=voronoi_own(P_aux4)
f=figure
semilogx(area_real1,pdf_real1,area_real2,pdf_real2,area_real3,pdf_real3,area_real4,pdf_real4,area_sim,pdf_sim)
xlabel('area / area_m_e_a_n')
ylabel('PDF')
title('Espaces de Voronoi (Filtrage par Temps)');
legend('Temps 1','Temps 2','Temps 3','Temps 4','Théorique');
savefig('voronoi_match_1_time.fig');
saveas(f,'voronoi_match_1_time_bis.png');

%% Angle_tau selon la zone du terrain

[P_aux1,P_aux2,P_aux3,P_aux4] = filter_pitch_zone(P_m_filtered);
[Limite_X,Limite_Y,Pente_Tau_X,Pente_Tau_Y,Pente_Tau_X_2,Pente_Tau_Y_2] = calc_angle_tau_pente();
[tau1,phi1]=calc_angle_tau(P_aux1,t);
[tau2,phi2]=calc_angle_tau(P_aux2,t);
[tau3,phi3]=calc_angle_tau(P_aux3,t);
[tau4,phi4]=calc_angle_tau(P_aux4,t);

f=figure;
loglog(tau1,phi1,'b',tau2,phi2,'g',tau3,phi3,'r',tau4,phi4,'k',Limite_X,Limite_Y,'c',Pente_Tau_X,Pente_Tau_Y,'c',Pente_Tau_X_2,Pente_Tau_Y_2,'c')
xlabel('Tau (en s)');
ylabel('Angle/Pi');
title('Angles en fonction de dt (Filtrage par Zones Spatiales)');
legend('Zone 1','Zone 2','Zone 3','Zone 4','Location','southeast');
savefig('angle_tau_match_1_zone.fig');
saveas(f,'angle_tau_match_1_zone_bis.png');


%% Angle_tau selon le temps de jeu

[P_aux1,P_aux2,P_aux3,P_aux4] = filter_time_stamp(P_m);
clc;
disp("Calcule Temps 1");
[tau,phi1]=calc_angle_tau(P_aux1,t);
clc;
disp("Calcule Temps 2");
[tau,phi2]=calc_angle_tau(P_aux2,t);
clc;
disp("Calcule Temps 3");
clc;
disp("Calcule Temps 4");
[tau,phi4]=calc_angle_tau(P_aux4,t);
f=figure
loglog(tau1,phi1,'b',tau2,phi2,'g',tau3,phi3,'r',tau4,phi4,'k');
xlabel('Tau');
ylabel('Angle/Pi');
title('Angles en fonction de dt (Filtrage par Temps)');
legend('Zone 1','Zone 2','Zone 3','Zone 4','Location','southeast');
savefig('angle_tau_match_1_time.fig');
saveas(f,'angle_tau_match_1_time_bis.png');

%% Affichage Vitesse Acceleration et Distance

vitesse = calc_vitesse_moyenne(P_m);
acceleration = calc_acceleration_moyenne(P_m);
figure
yyaxis left
plot(t,vitesse,'b')
ylabel('Vitesse (en m/s)');
yyaxis right
plot(t,acceleration,'r')
ylabel('Acceleration en m/s^2');
xlabel('Temps de match (en s)');

%% Filtrage Zone Affichage
[P_aux1,P_aux2,P_aux3,P_aux4] = filter_pitch_zone(P_m_filtered);
ShowTrace(P_aux1)





