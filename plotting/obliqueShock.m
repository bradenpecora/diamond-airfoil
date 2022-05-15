function[Mn1,Mn2,beta,dr,pr,tr,ds,spr,M2] = obliqueShock(M1,theta)
    g = 1.4;
    cp = 1005;
    R = 287;

    beta = thetabetam(theta,M1,g,1);


    Mn1 = M1 * sind(beta);
    Mn2 = sqrt((1+(g-1)/2 * Mn1^2)/(g*Mn1^2 - (g-1)/2));
    M2 = Mn2/sind(beta-theta);
    dr = ((g+1) * Mn1^2)/(2+(g-1)*Mn1^2);
    pr = 1+2*g/(g+1)*(Mn1^2-1);
    tr = pr / dr;
    ds = cp*log(tr) - R * log(pr);
    spr = exp(-ds / R);

    function B = thetabetam(theta,M,g,delta)
        a = M^2 - 1;
        T = 1 + (g-1)/2*M^2;
        b = 1 + (g+1)/2*M^2;
        tn = tand(theta);
        lamda = sqrt(a^2- 3*T*b*tn^2);
        chi = (a^3 - 9*T*(T+(g+1)/4*M^4)*tn^2)/lamda^3;
        B = atand((a+2*lamda*cos((4*pi*delta + acos(chi))/3))/(3*T*tn));
    end
end
