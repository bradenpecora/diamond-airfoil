% For a diamond airfoil

function[Cl,Cd] = aeroCoef(M,theta,alpha,g)
    arguments
        M
        theta
        alpha
        g = 1.4
    end

    [~,~,~,~,P1,~,~,~,M1] = obliqueShock(M,theta-alpha);
    [~,~,~,~,P4,~,~,~,M4] = obliqueShock(M,theta+alpha);
    M2 = prandtl(M1,2*theta);
    M3 = prandtl(M4,2*theta);

    [~,P01r,~] = isentropic(M1);
    [~,P02r,~] = isentropic(M2);
    [~,P03r,~] = isentropic(M3);
    [~,P04r,~] = isentropic(M4);

    P2 = P1*P01r/P02r;
    P3 = P4*P04r/P03r;

    Cl = ((P4-P2)*cosd(theta+alpha) + (P3-P1)*cosd(theta-alpha))/(cosd(theta)*M^2*g);
    Cd = ((P4-P2)*sind(theta+alpha) - (P3-P1)*sind(theta-alpha))/(cosd(theta)*M^2*g);

end