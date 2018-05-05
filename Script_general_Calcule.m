%% load
clc
clear all
load('Match_1_Traite');
P_m=transformation_en_metres(P);

%% Filtrages des données

%P_m_filtered=filter_data(P_m);

[P_Time_1,P_Time_2,P_Time_3,P_Time_4] = filter_time_stamp(P_m);
[P_Zone_1,P_Zone_2,P_Zone_3,P_Zone_4] = filter_pitch_zone(P_m);
save('Match_1_Traite');

%% Création vecteurs de Tau sans filtrage
% Général
disp("General");
[Tau,Phi]=calc_angle_tau(P_m,t);
% Filtrage Temporel
disp("Temp1");
[Tau_Time_1,Phi_Time_1]=calc_angle_tau(P_Time_1,t);
disp("Temp2");
[Tau_Time_2,Phi_Time_2]=calc_angle_tau(P_Time_2,t);
disp("Temp3");
[Tau_Time_3,Phi_Time_3]=calc_angle_tau(P_Time_3,t);
disp("Temp4");
[Tau_Time_4,Phi_Time_4]=calc_angle_tau(P_Time_4,t);
disp("Temps fini");
save('Match_1_Traite');
disp("Temps fini saved");
% Filtrage Spatial
disp("Zone1");
[Tau_Zone_1,Phi_Zone_1]=calc_angle_tau(P_Zone_1,t);
disp("Zone2");
[Tau_Zone_2,Phi_Zone_2]=calc_angle_tau(P_Zone_2,t);
disp("Zone3");
[Tau_Zone_3,Phi_Zone_3]=calc_angle_tau(P_Zone_3,t);
disp("Zone4");
[Tau_Zone_4,Phi_Zone_4]=calc_angle_tau(P_Zone_4,t);
disp("Zone fini");
save('Match_1_Traite');
disp("Zone fini saved");

%% Création vecteurs de Voronoi sans filtrage
% Général
disp("General Voronoi");
[Pdf,Area,PDF_sim,AREA_sim]=voronoi_own(P_m);
% Filtrage Temporel
disp("Time1");
[Pdf_Time_1,Area_Time_1,~,~]=voronoi_own(P_Time_1);
disp("Time2");
[Pdf_Time_2,Area_Time_2,~,~]=voronoi_own(P_Time_2);
disp("Time3");
[Pdf_Time_3,Area_Time_3,~,~]=voronoi_own(P_Time_3);
disp("Time4");
[Pdf_Time_4,Area_Time_4,~,~]=voronoi_own(P_Time_4);
disp("Time fini");
save('Match_1_Traite');
disp("Time fini saved");
% Filtrage Spatial
disp("Zone1");
[Pdf_Zone_1,Area_Zone_1,~,~]=voronoi_own(P_Zone_1);
disp("Zone2");
[Pdf_Zone_2,Area_Zone_2,~,~]=voronoi_own(P_Zone_2);
disp("Zone3");
[Pdf_Zone_3,Area_Zone_3,~,~]=voronoi_own(P_Zone_3);
disp("Zone4");
[Pdf_Zone_4,Area_Zone_4,~,~]=voronoi_own(P_Zone_4);
disp("Zone fini");
save('Match_1_Traite');
disp("Zone fini saved");
%% Création vecteurs de Cascade Energetique sans filtrage
% Général
disp("General Cascade");
[Freq,Ener]=energy_cascade(P_m);
disp("Cascade fini");
save('Match_1_Traite');
disp("Cascade fini saved");

%% Création vecteurs de Probabilité sans filtrage
% Général
disp("General Probabilite");
[Angle,Prob]=calc_angle_proba(P_m);
disp("Proba fini");
save('Match_1_Traite');
disp("Proba fini saved");

%% Création vecteurs de Probabilité avec filtrage
Angle_filter = transpose(Angle_filter);
disp("General Probabilite Filter");
Angle_filter(:,1) = smooth(Angle(1,:),'rlowess');
Angle_filter(:,2) = smooth(Angle(2,:),'rlowess');
Angle_filter(:,3) = smooth(Angle(3,:),'rlowess');
Angle_filter(:,4) = smooth(Angle(4,:),'rlowess');
Angle_filter(:,5) = smooth(Angle(5,:),'rlowess');
Angle_filter = transpose(Angle_filter);
%% Création vecteurs Voronoi Normalisé

% Général
disp("General Voronoi inverse");
Lamda_general = poissfit(Area,Pdf);
Pdf_norm = Pdf./Lamda_general;

% Filtrage Temporel
Lamda_Time_1 = poissfit(Area,Pdf_Time_1);
Pdf_norm_Time_1 = Pdf_Time_1./Lamda_Time_1;
Lamda_Time_2 = poissfit(Area,Pdf_Time_2);
Pdf_norm_Time_2 = Pdf_Time_2./Lamda_Time_2;
Lamda_Time_3 = poissfit(Area,Pdf_Time_3);
Pdf_norm_Time_3 = Pdf_Time_3./Lamda_Time_3;
Lamda_Time_4 = poissfit(Area,Pdf_Time_4);
Pdf_norm_Time_4 = Lamda_Time_1./Lamda_Time_4; 

% Filtrage Spatial
Lamda_Zone_1 = poissfit(Area,Pdf_Zone_1);
Pdf_norm_Zone_1 = Pdf_Zone_1./Lamda_Zone_1;
Lamda_Zone_2 = poissfit(Area,Pdf_Zone_2);
Pdf_norm_Zone_2 = Pdf_Zone_2./Lamda_Zone_2;
Lamda_Zone_3 = poissfit(Area,Pdf_Zone_3);
Pdf_norm_Zone_3 = Pdf_Zone_3./Lamda_Zone_3;
Lamda_Zone_4 = poissfit(Area,Pdf_Zone_4);
Pdf_norm_Zone_4 = Lamda_Zone_1./Lamda_Zone_4; 

%% Création vecteur Voronoi filtré 
%Général
Pdf_filter = smooth(Pdf,'moving');
% Filtrage Temporel
Pdf_filter_Time_1 = smooth(Pdf_Time_1,'moving');
Pdf_filter_Time_2 = smooth(Pdf_Time_2,'moving');
Pdf_filter_Time_3 = smooth(Pdf_Time_3,'moving');
Pdf_filter_Time_4 = smooth(Pdf_Time_4,'moving');
% Filtrage Spatial
Pdf_filter_Zone_1 = smooth(Pdf_Zone_1,'moving');
Pdf_filter_Zone_2 = smooth(Pdf_Zone_2,'moving');
Pdf_filter_Zone_3 = smooth(Pdf_Zone_3,'moving');
Pdf_filter_Zone_4 = smooth(Pdf_Zone_4,'moving');
save('Match_1_Traite');

%% Calcule Variance de Voronoi des données

% Général 
Pdf_Mean = mean(Pdf.*Area);
Pdf_Sigma = var(Pdf,Area);

% Filtrage Temporel
Pdf_Mean_Time(1,1) = mean(Pdf_Time_1.*Area);
Pdf_Mean_Time(2,1) = mean(Pdf_Time_2.*Area);
Pdf_Mean_Time(3,1) = mean(Pdf_Time_3.*Area);
Pdf_Mean_Time(4,1) = mean(Pdf_Time_4.*Area);

Pdf_Sigma_Time(1,1) = var(Pdf_Time_1,Area);
Pdf_Sigma_Time(2,1) = var(Pdf_Time_2,Area);
Pdf_Sigma_Time(3,1) = var(Pdf_Time_3,Area);
Pdf_Sigma_Time(4,1) = var(Pdf_Time_4,Area);

% Filtrage Spatial
Pdf_Mean_Zone(1,1) = mean(Pdf_Zone_1.*Area);
Pdf_Mean_Zone(2,1) = mean(Pdf_Zone_2.*Area);
Pdf_Mean_Zone(3,1) = mean(Pdf_Zone_3.*Area);
Pdf_Mean_Zone(4,1) = mean(Pdf_Zone_4.*Area);

Pdf_Sigma_Zone(1,1) = var(Pdf_Zone_1,Area);
Pdf_Sigma_Zone(2,1) = var(Pdf_Zone_2,Area);
Pdf_Sigma_Zone(3,1) = var(Pdf_Zone_3,Area);
Pdf_Sigma_Zone(4,1) = var(Pdf_Zone_4,Area);

%% Calcule Variance de Voronoi des fonctions d'approx

%Général
[a,b,~,~]=find_shape(Area,Pdf);
Pdf_Mean_approx=a/b;
Pdf_Sigma_approx=a/(b^2);

% Filtrage Temporel
[a,b,~,~] = find_shape(Area,Pdf_Time_1);
Pdf_Mean_Time(1,2) = a/b;
Pdf_Sigma_Time(1,2)= a/(b^2);

[a,b,~,~] = find_shape(Area,Pdf_Time_2);
Pdf_Mean_Time(2,2) = a/b;
Pdf_Sigma_Time(2,2)= a/(b^2);

[a,b,~,~] = find_shape(Area,Pdf_Time_3);
Pdf_Mean_Time(3,2) = a/b;
Pdf_Sigma_Time(3,2)= a/(b^2);

[a,b,~,~] = find_shape(Area,Pdf_Time_4);
Pdf_Mean_Time(4,2) = a/b;
Pdf_Sigma_Time(4,2)= a/(b^2);


% Filtrage Spatial
[a,b,~,~] = find_shape(Area,Pdf_Zone_1);
Pdf_Mean_Zone(1,2) = a/b;
Pdf_Sigma_Zone(1,2)= a/(b^2);

[a,b,~,~] = find_shape(Area,Pdf_Zone_2);
Pdf_Mean_Zone(2,2) = a/b;
Pdf_Sigma_Zone(2,2)= a/(b^2);

[a,b,~,~] = find_shape(Area,Pdf_Zone_3);
Pdf_Mean_Zone(3,2) = a/b;
Pdf_Sigma_Zone(3,2)= a/(b^2);

[a,b,~,~] = find_shape(Area,Pdf_Zone_4);
Pdf_Mean_Zone(4,2) = a/b;
Pdf_Sigma_Zone(4,2)= a/(b^2);
