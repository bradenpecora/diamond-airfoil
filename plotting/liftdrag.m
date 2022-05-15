addpath ./plotting
M = 3;
theta = atand(.3/3);

alphaT = -5:1:5;

Cl = zeros(1,length(alphaT));
Cd = zeros(1,length(alphaT));

for i = 1:length(alphaT)
    [l,d] = aeroCoef(M,theta,alphaT(i));
    Cl(i) = l;
    Cd(i) = d;
end

clear theta M i l d

%%
theta = atand(.3/3);
c = 3;
M = 5;
g = 1.4;
fS = "./simulations/lift-drag/mach5/alpha";
fE = "/postProcessing/singleGraph/10/surface";

surf = ["1_p.csv","2_p.csv","3_p.csv","4_p.csv"];
alpha = [0,-1,-2,-3,-4,-5];

F = zeros(1,length(alpha));
CF = zeros(1,length(alpha));


for k = 1:length(alpha)

    % Lift and drag as a complex number
    % Re{F} = L, Im{F} = D
    F(k) = 0 + i*0;

    % Computes the lift/drag coefficients
    for j = 1:4
        a = readmatrix(append(fS, num2str(abs(alpha(k))), fE, surf(j)));
        b = [-1 -1 1 1];
        d = [-1 1 -1 1];
        for i = 1:(length(a(:,1))-1)
            p = (a(i,4)+a(i+1,4))/2;
            dx = norm([(a(i,1)-a(i+1,1)),(a(i,2)-a(i+1,2))],2);
            F(k) = F(k) + b(j)*dx*p*exp(d(j)*1i*pi/180*(theta + d(j)*alpha(k)));    
        end
    
    end

    % Complex force coefficient
    CF(k) = F(k)/(g*M^2*c);
end


clear b a d g i fS 
clear theta c fE F j M p dx surf

%% Plot coefficients of lift/drag
hold on
plot(alphaT(6:end),Cl(6:end),"LineWidth",1.3)
plot(alphaT(6:end),Cd(6:end),"LineWidth",1.3)
scatter(-alpha,-real(CF),'filled')
scatter(-alpha,imag(CF),'filled')
title("Coefficients of Lift and Drag for Mach 5")
xlabel("\alpha (degrees)")
ylabel("Coefficient of Lift/Drag")
legend("Analytical Lift Solution","Analytical Drag Solution",...
        "Numerical Lift Solution","Numerical Drag Solution")




%% Convergence
theta = atand(.3/3);
c = 3;
M = 3;
g = 1.4;
fS = "./simulations/lift-drag/";
fE = "/postProcessing/singleGraph/10/surface";

runs = ["converge/N1","converge/N2","converge/N3","converge/N4",'mach3/alpha0'];

surf = ["1_p.csv","2_p.csv","3_p.csv","4_p.csv"];

F = zeros(1,length(runs));
CF = zeros(1,length(runs));


for k = 1:length(runs)

    % Lift and drag as a complex number
    % Re{F} = L, Im{F} = D
    F(k) = 0 + i*0;

    % Computes the lift/drag coefficients
    for j = 1:4
        a = readmatrix(append(fS, runs(k), fE, surf(j)));
        b = [-1 -1 1 1];
        d = [-1 1 -1 1];
        for i = 1:(length(a(:,1))-1)
            p = (a(i,4)+a(i+1,4))/2;
            dx = norm([(a(i,1)-a(i+1,1)),(a(i,2)-a(i+1,2))],2);
            F(k) = F(k) + b(j)*dx*p*exp(d(j)*1i*pi/180*theta);    
        end
    
    end
    % Complex force coefficient
    CF(k) = F(k)/(g*M^2*c);
end
CF = imag(CF);


N = [3600, 14400, 32400, 57600, 90000];
err = abs(CF-Cd(6))/Cd(6);
pF = polyfit(log(N),log(err),1);
Nvec = linspace(3000,100000,100);
errvec = exp(pF(1)*log(Nvec)+pF(2));


loglog(N,err,'.',"MarkerSize",16)
hold on;
loglog(Nvec,errvec,"--","LineWidth",1.3)
legend("","Curve of Best Fit")
ylabel("Error")
xlabel("Number of Cells")
title("Error vs Spatial Resolution")
axis([3000,100000,0,.03])


clear b a d g i fS 
clear theta c fE F j M p dx surf

%% Pressure distribution
fS = "./simulations/lift-drag/";
fE = "/postProcessing/singleGraph/10/surface";
runs = ["converge/N1","converge/N2","converge/N3","converge/N4",'mach3/alpha0'];
surf = ["1_p.csv","2_p.csv"];

N = [3600, 14400, 32400, 57600, 90000];
p = [1.52986713,0.6293];

j = 2;

hold on;
for k = 1:length(runs)
    a = readmatrix(append(fS, runs(k), fE, surf(j)));
    x = sqrt((a(:,1)-a(1,1)).^2 + (a(:,2)-a(1,2)).^2);
    plot(x/x(end),a(:,4),'LineWidth',1.1)
end
plot(x/x(end),p(j)*ones(1,length(x)),'--k','LineWidth',1.1)
legend(num2str(N(1)),num2str(N(2)),num2str(N(3)),num2str(N(4)),num2str(N(5)),"Analytical Solution")
xlabel("Normalized Surface Location")
ylabel("Normalized Pressure")
title(append("Pressure Distribution on Surface ", num2str(j), " for Varying Spatial Resolutions"))

