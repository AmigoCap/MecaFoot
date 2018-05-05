%% load
clc
load('Match_1_Traite');

%% Visualisation des zones du terrain 
figure;
hold on 
%ShowTrace(P_Zone_1,1)
%ShowTrace(P_Zone_2,1)
%ShowTrace(P_Zone_3,1)
%ShowTrace(P_Zone_4,1)

%% Visualisation des temps de jeux
figure;
hold on 
ShowTrace(P_Time_1,1)
%ShowTrace(P_Time_2,1)
%ShowTrace(P_Time_3,1)
%ShowTrace(P_Time_4,1)

%% distribution de probabilité d'angles sans filtre
Fig_Proba = figure;

plot(Prob,Angle);
xlabel('^{\theta}/_{\pi}')
ylabel('Probabilité')
title('Distribution de probabilité des angles \theta')
savefig('Distribution_Proba.fig');
saveas(Fig_Proba,'Distribution_Proba.png');

%% distribution de probabilité d'angles avec filtre
Fig_Proba_filt = figure;

plot(Prob,Angle_filter);
xlabel('^{\theta}/_{\pi}')
ylabel('Probabilité')
title('Distribution de probabilité des angles \theta filtré')
savefig('Distribution_Proba_filter.fig');
saveas(Fig_Proba_filt,'Distribution_Proba_Filter.png');

%% Création Courbe Tau Géneral
Fig_Tau = figure;
[Limite_X,Limite_Y,Pente_Tau_X_1,Pente_Tau_Y_1,Pente_Tau_X_2,Pente_Tau_Y_2,Pente_Tau_X_3,Pente_Tau_Y_3] = calc_angle_tau_pente(Tau);

loglog(Tau,Phi,'b', Limite_X, Limite_Y,'k',Pente_Tau_X_2,Pente_Tau_Y_2,'r',Pente_Tau_X_1,Pente_Tau_Y_1,'g',Pente_Tau_X_3,Pente_Tau_Y_3,'y') 
xlabel('\tau _(_e_n_ _s_)');
ylabel('^{\theta}/_{\pi}');
xlim([10^0 10^3.7])
ylim([0.2 0.8])
title('Direction du mouvement \theta en fonction du temps seuil \tau');
legend('Joueurs de Rugby','^2/_3','Tau^0^.^5', 'Tau^0^.^3', 'Tau^0^.^1^5','Location','southeast')
savefig('Angle_Tau_General.fig');
saveas(Fig_Tau,'Angle_Tau_General.png');

%% Création Courbe Tau Filtrage Spatial
Fig_Tau_Zone = figure;
[Limite_X,Limite_Y,Pente_Tau_X_1,Pente_Tau_Y_1,Pente_Tau_X_2,Pente_Tau_Y_2,Pente_Tau_X_3,Pente_Tau_Y_3] = calc_angle_tau_pente(Tau);

loglog(Tau_Zone_1,Phi_Zone_1,'b',Tau_Zone_2,Phi_Zone_2,'g',Tau_Zone_3,Phi_Zone_3,'r',Tau_Zone_4,Phi_Zone_4,'k') 
xlabel('\tau _(_e_n_ _s_)');
ylabel('^{\theta}/_{\pi}');
xlim([10^0 10^2.8])
ylim([0.2 0.8])
title('Direction du mouvement \theta en fonction du temps seuil \tau (Filtrage par Zones Spatiales)');
legend('Zone 1','Zone 2','Zone 3','Zone 4','Location','southeast');
savefig('Angle_Tau_Zone.fig');
saveas(Fig_Tau_Zone,'Angle_Tau_Zone.png');

%% Création Courbe Tau Filtrage Temporel
Fig_Tau_Time = figure;
[Limite_X,Limite_Y,Pente_Tau_X,Pente_Tau_Y,Pente_Tau_X_2,Pente_Tau_Y_2] = calc_angle_tau_pente(Tau);

loglog(Tau_Time_1,Phi_Time_1,'b',Tau_Time_2,Phi_Time_2,'g',Tau_Time_3,Phi_Time_3,'r',Tau_Time_4,Phi_Time_4,'c',Limite_X,Limite_Y,'--') 
xlabel('\tau _(_e_n_ _s_)');
ylabel('^{\theta}/_{\pi}');
xlim([10^0 10^3.1])
ylim([0.2 0.9])
title('Direction du mouvement \theta en fonction du temps seuil \tau (Filtrage par Zones Temporelles)');
legend('Temps 1','Temps 2','Temps 3','Temps 4','Location','southeast');
savefig('Angle_Tau_Time.fig');
saveas(Fig_Tau_Time,'Angle_Tau_Time.png');

%% Création Courbe Voronoi Géneral
Fig_Voronoi = figure;

semilogx(Area,Pdf,'b',AREA_sim,PDF_sim,'r')
xlabel('^{Area}/_{Area_m_e_a_n}')
ylabel('PDF')
title('Espaces de Voronoi');
legend('Joueurs de rugby','Théorique');
savefig('Voronoi_General.fig');
saveas(Fig_Voronoi,'Voronoi_General.png');

%% Création Courbe Voronoi Filtrage Spatial
Fig_Voronoi_Zone = figure ;

semilogx(Area_Zone_1,Pdf_Zone_1,'b',Area_Zone_2,Pdf_Zone_2,'g',Area_Zone_3,Pdf_Zone_3,'r',Area_Zone_4,Pdf_Zone_4,'k')
xlabel('^{Area}/_{Area_m_e_a_n}')
ylabel('PDF')
title('Espaces de Voronoi (Filtrage par Zones Spatiales)');
legend('Zone 1', 'Zone 2', 'Zone 3', 'Zone 4');
savefig('Voronoi_Zone.fig');
saveas(Fig_Voronoi_Zone,'Voronoi_Zone.png');

%% Création Courbe Voronoi Filtrage Temporel
Fig_Voronoi_Time = figure;

semilogx(Area_Time_1,Pdf_Time_1,'b',Area_Time_2,Pdf_Time_2,'g',Area_Time_3,Pdf_Time_3,'r',Area_Time_4,Pdf_Time_4,'k')
xlabel('^{Area}/_{Area_m_e_a_n}')
ylabel('PDF')
title('Espaces de Voronoi (Filtrage par Zones Temporelles)');
legend('Temps 1','Temps 2','Temps 3','Temps 4');
savefig('Voronoi_Time.fig');
saveas(Fig_Voronoi_Time,'Voronoi_Time.png');

%% Création courbe Voronoi General  Filtré
Fig_Voronoi_filt = figure;

semilogx(Area,Pdf,'b',AREA_sim,PDF_sim,'r',Area,Pdf_filter,'y');
xlabel('^{Area}/_{Area_m_e_a_n}');
ylabel('PDF');
title('Espaces de Voronoi');
legend('Joueurs de rugby','Théorique','Filtrage');
savefig('Voronoi_General_Filter.fig');
saveas(Fig_Voronoi_filt,'Voronoi_General_Filter.png');

%% Création courbe Voronoi Filtrage Spatial Filtré
Fig_Voronoi_filt_Zone = figure;

semilogx(Area_Zone_1,Pdf_filter_Zone_1,'b',Area_Zone_2,Pdf_filter_Zone_2,'g',Area_Zone_3,Pdf_filter_Zone_3,'r',Area_Zone_4,Pdf_filter_Zone_4,'k')
xlabel('^{Area}/_{Area_m_e_a_n}')
ylabel('PDF')
xlim([10^-3 10^0])
title('Espaces de Voronoi filter (Filtrage par Zones Spatiales)');
legend('Zone 1', 'Zone 2', 'Zone 3', 'Zone 4');
savefig('Voronoi_Zone_Filter.fig');
saveas(Fig_Voronoi_filt_Zone,'Voronoi_Zone_Filter.png');

%% Création courbe Voronoi Filtrage Temporel Filtré
Fig_Voronoi_filt_Time = figure;

semilogx(Area_Time_1,Pdf_filter_Time_1,'b',Area_Time_2,Pdf_filter_Time_2,'g',Area_Time_3,Pdf_filter_Time_3,'r',Area_Time_4,Pdf_filter_Time_4,'k')
xlabel('^{Area}/_{Area_m_e_a_n}')
ylabel('PDF')
xlim([10^-3 10^0.6])
title('Espaces de Voronoi filter (Filtrage par Zones Temporelles)');
legend('Temps 1', 'Temps 2', 'Temps 3', 'Temps 4');
savefig('Voronoi_Time_Filter.fig');
saveas(Fig_Voronoi_filt_Time,'Voronoi_Time_Filter.png');

%% Création courbe Voronoi Sigma et Mean 
Fig_Voronoi_Sigma_Mean = figure;

subplot(2,2,1);
plot(Pdf_Sigma_Time(:,1));
xlabel('Temps')
ylabel('Sigma')
subplot(2,2,2);
plot(Pdf_Sigma_Time(:,1));
xlabel('Zone')
ylabel('Sigma')
subplot(2,2,3);
plot(Pdf_Mean_Time(:,1));
xlabel('Temps')
ylabel('Mean')
subplot(2,2,4);
plot(Pdf_Mean_Time(:,1));
xlabel('Zone')
ylabel('Mean')

savefig('Fig_Voronoi_Sigma_Mean.fig');
saveas(Fig_Voronoi_Sigma_Mean,'Fig_Voronoi_Sigma_Mean.png');

%% Création courbe Voronoi Sigma et Mean pour les fonctions d'approximation

figure
subplot(2,2,1);
plot(Pdf_Sigma_Time(:,2));
xlabel('Temps')
ylabel('Sigma')
subplot(2,2,2);
plot(Pdf_Sigma_Time(:,2));
xlabel('Zone')
ylabel('Sigma')
subplot(2,2,3);
plot(Pdf_Mean_Time(:,2));
xlabel('Temps')
ylabel('Mean')
subplot(2,2,4);
plot(Pdf_Mean_Time(:,2));
xlabel('Zone')
ylabel('Mean')
savefig('Fig_Voronoi_Sigma_Mean_approx.fig');
saveas(Fig_Voronoi_Sigma_Mean,'Fig_Voronoi_Sigma_Mean_approx.png');

%% Création courbe Voronoi Sigma et Mean 
Fig_Voronoi_Sigma_Mean = figure;

subplot(2,2,1);
plot(Pdf_Sigma_Time);
xlabel('Temps')
ylabel('Sigma')
subplot(2,2,2);
plot(Pdf_Sigma_Time);
xlabel('Zone')
ylabel('Sigma')
subplot(2,2,3);
plot(Pdf_Mean_Time);
xlabel('Temps')
ylabel('Mean')
subplot(2,2,4);
plot(Pdf_Mean_Time);
xlabel('Zone')
ylabel('Mean')

savefig('Fig_Voronoi_Sigma_Mean.fig');
saveas(Fig_Voronoi_Sigma_Mean,'Fig_Voronoi_Sigma_Mean.png');

%% Création courbe Voronoi General Normalisé 
Fig_Voronoi_Norm = figure;

semilogx(Area,Pdf_norm,'b',Area,Pdf,'y',AREA_sim,PDF_sim,'k')
xlabel('Area / Area_m_e_a_n')
ylabel('PDF')
title('Espaces de Voronoi normalisé');
legend('Normaliser','Normal','Sim');
% savefig('Voronoi_Time.fig');
% saveas(Fig_Voronoi_Time,'Voronoi_Time.png');