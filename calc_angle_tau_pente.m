function [Limite_X,Limite_Y,Pente_Tau_X_1,Pente_Tau_Y_1,Pente_Tau_X_2,Pente_Tau_Y_2,Pente_Tau_X_3,Pente_Tau_Y_3] = calc_angle_tau_pente (Tau)

Limite_X = Tau;
Limite_Y = 2/3+Limite_X*0;

Pente_Tau_X_1 = Tau(10:85);
Pente_Tau_Y_1 = (Pente_Tau_X_1.^0.33)/pi*0.7;

Pente_Tau_X_2 = Tau(10:85);
Pente_Tau_Y_2 = (Pente_Tau_X_2.^0.5)/pi*0.7;

Pente_Tau_X_3 = Tau(85:145);
Pente_Tau_Y_3 = (Pente_Tau_X_3.^0.15)/pi;
end