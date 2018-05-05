function [frequ, Energy] = energy_cascade(P)

[lt,~,nj]=size(P);
dt=0.1;
for n=1:nj
    for t=1:(lt-1)
        x1=P(t,1:2,n);
        x2=P(t+1,1:2,n);
        v(n,t)=norm(x2-x1)/dt;
    end
end

T=0.1;
Fs=1/T;
L=lt;
t = (0:L-1)*T;
Energy=zeros([1 lt-1]);
E=zeros([nj lt-1]);
for i=1:nj
    v_w(i,:)=fft(v(i,:));
    E(i,:)=0.5*abs(v_w(i,:).*conj(v_w(i,:)));
    Energy=Energy+E(i,:);
end

Energy = abs(Energy/L);
Energy = Energy(1:L/2+1);
Energy(2:end-1) = 2*Energy(2:end-1);

frequ = Fs*(0:(L/2))/L;


end

